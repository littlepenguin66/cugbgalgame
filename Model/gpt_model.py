# coding: utf-8

import math
import torch
from torch import nn
from torch.nn import functional as F
from torchinfo import summary


class GPTConfig:
    vocab_size: int = 4118
    seq_len: int = 128
    d_model: int = 128  # d_model
    n_layer: int = 4
    n_head: int = 4
    bias: bool = True
    dropout: float = 0.0


class SinusoidPE(nn.Module):
    """ 正弦/余弦位置编码 """

    def __init__(self, config):
        super().__init__()
        d_model, seq_len = config.d_model, config.seq_len
        pe = torch.zeros(seq_len, d_model)
        position = torch.arange(0, seq_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0)
        self.register_buffer('sinusoid_pe', pe)

    def forward(self, x):
        return self.sinusoid_pe[:, :x.shape[1], :]


class SelfAttention(nn.Module):
    """ 多头注意力 """

    def __init__(self, config):
        super().__init__()
        assert config.d_model % config.n_head == 0
        # 所有头的键、查询、值投影，但在一个批次中
        self.attn = nn.Linear(config.d_model, 3 * config.d_model, bias=config.bias)
        # 输出投影
        self.proj = nn.Linear(config.d_model, config.d_model, bias=config.bias)
        # 正则化
        self.attn_dropout = nn.Dropout(config.dropout)
        # 自注意力掩码，确保注意力仅应用于输入序列的左侧
        self.register_buffer("mask", torch.tril(torch.ones(config.seq_len, config.seq_len))
                                          .view(1, 1, config.seq_len, config.seq_len))

    def forward(self, x):
        B, C, E = x.size()

        q, k, v = self.attn(x).split(self.d_model, dim=2)
        q = q.view(B, C, self.n_head, E // self.n_head).transpose(1, 2)  # (B, nh, C, hs)
        k = k.view(B, C, self.n_head, E // self.n_head).transpose(1, 2)  # (B, nh, C, hs)
        v = v.view(B, C, self.n_head, E // self.n_head).transpose(1, 2)  # (B, nh, C, hs)

        # 自注意力: (B, nh, C, hs) x (B, nh, hs, C) -> (B, nh, C, C)
        att = (q @ k.transpose(-2, -1)) * (1.0 / math.sqrt(k.size(-1)))
        att = att.masked_fill(self.mask[:, :, :C, :C] == 0, float('-inf'))
        att = F.softmax(att, dim=-1)
        att = self.attn_dropout(att)
        y = att @ v  # (B, nh, C, C) x (B, nh, C, hs) -> (B, nh, C, hs)
        y = y.transpose(1, 2).contiguous().view(B, C, E)

        return self.proj(y)


class FeedFoward(nn.Module):
    """ 两层mlp """

    def __init__(self, config):
        super().__init__()
        d_model = config.d_model
        self.net = nn.Sequential(
            nn.Linear(d_model, 4 * d_model),
            nn.GELU(),
            nn.Linear(4 * d_model, d_model),
            nn.Dropout(config.dropout),
        )

    def forward(self, x):
        return self.net(x)


class Block(nn.Module):
    """ 解码器块 """

    def __init__(self, config):
        # n_embd: 嵌入维度，n_head: 我们想要的头数
        super().__init__()
        self.ln1 = nn.LayerNorm(config.d_model, bias=config.bias)
        self.attn = SelfAttention(config)
        self.ln2 = nn.LayerNorm(config.d_model, bias=config.bias)
        self.ffn = FeedFoward(config)

    def forward(self, x):
        x = x + self.attn(self.ln1(x))
        x = x + self.ffn(self.ln2(x))
        return x


class GPTModel(nn.Module):

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.tok_embed_table = nn.Embedding(config.vocab_size, config.d_model)
        self.pos_embed_table = SinusoidPE(config)
        self.decoder_blocks = nn.Sequential(*[Block(config) for _ in range(config.n_layer)])
        self.layer_norm = nn.LayerNorm(config.d_model, bias=config.bias)
        self.final_linear = nn.Linear(config.d_model, config.vocab_size, bias=False)

        # 初始化所有权重
        self.apply(self._init_weights)
        for pn, p in self.named_parameters():
            if pn.endswith('proj.weight'):
                torch.nn.init.normal_(p, mean=0.0, std=0.02 / math.sqrt(2 * config.n_layer))

    def _init_weights(self, module):
        if isinstance(module, nn.Linear):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)
            if module.bias is not None:
                torch.nn.init.zeros_(module.bias)
        elif isinstance(module, nn.Embedding):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)

    def forward(self, features, targets=None):
        tok_emb = self.tok_embed_table(features)  # (B,C,E)
        pos_emb = self.pos_embed_table(tok_emb)
        x = tok_emb + pos_emb  # (B,C,E)
        x = self.decoder_blocks(x)

        x = self.layer_norm(x)
        if targets is not None:
            logits = self.final_linear(x)  # (B,C,V)
            loss = F.cross_entropy(logits.view(-1, logits.size(-1)), targets.view(-1), ignore_index=-1)
        else:
            logits = self.final_linear(x[:, [-1], :])
            loss = None
        return logits, loss

    @torch.no_grad()
    def generate(self, seq, max_new_tokens):
        for _ in range(max_new_tokens):
            seq = seq[:, -self.config.seq_len:]
            logits, _ = self(seq)
            # 仅关注最后一个时间步长
            logits = logits[:, -1, :]  # 变为 (B, V)
            # 应用 softmax 得到概率
            probs = F.softmax(logits, dim=-1)  # (B, V)
            # 从分布中抽样
            seq_next = torch.multinomial(probs, num_samples=1)  # (B, 1)
            seq = torch.cat((seq, seq_next), dim=1)
        return seq


def main():
    config = GPTConfig()
    model = GPTModel(config)
    summary(model, input_size=[(100, config.seq_len), (100, config.seq_len)],
            dtypes=[torch.long, torch.long])


if __name__ == '__main__':
    main()
