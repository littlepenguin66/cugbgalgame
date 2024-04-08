# 从 gpt_model 模块中导入 GPTConfig 和 GPTModel 类
from gpt_model import GPTConfig, GPTModel

import numpy as np
import sentencepiece as spm
import sys
import torch

# 确定设备类型为 'cuda'（如果可用）或 'cpu'
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# 学习率为 1e-3
learning_rate = 1e-3
# 最大迭代次数为 12000
max_iters = 12000

# 从 'train.dat' 和 'test.dat' 中调用数据
train_data = np.memmap('train.dat', dtype=np.int32, mode='r')
test_data = np.memmap('test.dat', dtype=np.int32, mode='r')


# 定义 get_batch 函数，根据 split 参数返回训练集或测试集的批次数据
def get_batch(split, config):
    data = train_data if split == 'train' else test_data
    ix = torch.randint(len(data) - config.seq_len, (config.batch_size,))
    x = torch.stack([torch.from_numpy((data[i:i + config.seq_len]).astype(np.int32)) for i in ix])
    y = torch.stack([torch.from_numpy((data[i + 1:i + 1 + config.seq_len]).astype(np.int64)) for i in ix])
    if device == 'cuda':
        x, y = x.pin_memory().to(device, non_blocking=True), y.pin_memory().to(device, non_blocking=True)
    else:
        x, y = x.to(device), y.to(device)
    return x, y


# 定义 train 函数，用于训练模型
def train(config, model):
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)

    # 迭代训练模型
    for iter_num in range(max_iters):
        optimizer.zero_grad()

        xb, yb = get_batch('train', config)

        # 前向传播和损失计算
        _, loss = model(xb, yb)
        if (iter_num + 1) % 100 == 0:
            print(f"[train_info] iter:{iter_num + 1:5d}, loss:{loss.item():5.3f}")

        # 反向传播和梯度下降
        loss.backward()

        # 更新权重
        optimizer.step()

    print(f"final loss: {loss.item()}")


# 定义主函数 main
def main():
    config = GPTConfig()
    config.batch_size = 32
    config.dropout = 0.1

    model = GPTModel(config).to(device)

    # 调用 train 函数训练模型
    train(config, model)

    # 加载分词器
    from data_set import load_tokenizer
    model_file = "bird_shooter.model"
    flag, sp = load_tokenizer(model_file)
    if not flag:
        print(f"load tokenizer model from: {model_file} failed")
        sys.exit(1)

    # 使用模型生成文本
    user_inputs = ["郭靖一掌挥出", "黄蓉突然想到", "周伯通好奇心大起", "洪七公哈哈大笑"]
    for user_input in user_inputs:
        context = torch.tensor([sp.encode(user_input)], dtype=torch.int32, device=device)
        gpt_output = model.generate(context, max_new_tokens=50)[0].tolist()
        print(f"gpt({user_input}) => {sp.decode(gpt_output)}")


# 如果当前脚本为主程序，则执行主函数 main
if __name__ == '__main__':
    main()
