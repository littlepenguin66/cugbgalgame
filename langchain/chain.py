import torch
from transformers import AutoTokenizer, AutoModel
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
import codecs

class LangChain:
    def __init__(self, model_path, embedding_model_path):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        self.model = AutoModel.from_pretrained(model_path, trust_remote_code=True).half().cuda()
        self.model = self.model.eval()
        self.embedding_model_path = embedding_model_path
        self.history = []

    def torch_gc(self):
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()
        elif torch.backends.mps.is_available():
            try:
                from torch.mps import empty_cache
                empty_cache()
            except Exception as e:
                print(e)
                print("如果您使用的是 macOS 建议将 pytorch 版本升级至 2.0.0 或更高版本，以支持及时清理 torch 产生的内存占用。")

    def load_documents(self, file_path):
        raw_documents = TextLoader(file_path,encoding='utf-8').load()
        text_splitter = CharacterTextSplitter(chunk_size=250, chunk_overlap=0)
        documents = text_splitter.split_documents(raw_documents)
        embedding_device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
        embeddings = HuggingFaceEmbeddings(model_name=self.embedding_model_path, model_kwargs={'device': embedding_device})
        db = Chroma.from_documents(documents, embeddings)
        return db, embeddings

    def chunked_input(self, input_ids, max_length):
        return [input_ids[i:i+max_length] for i in range(0, len(input_ids), max_length)]

    def chat(self, db, embeddings):
        while True:
            query = input("question: ")
            if query == "exit":
                break
            embedding_vector = embeddings.embed_query(query)
            docs = db.similarity_search_by_vector(embedding_vector)
            test_text = "用10个字回答" + query +":" + docs[0].page_content
            input_ids = self.tokenizer.encode(test_text, return_tensors='pt')[0]
            chunked_ids = self.chunked_input(input_ids, max_length=8192)
            responses = []
            for ids in chunked_ids:
                text = self.tokenizer.decode(ids)
                response, self.history = self.model.chat(self.tokenizer, text, history=self.history)
                responses.append(response)
            print("AI: " + ' '.join(responses))
            self.torch_gc()

    def convert_to_utf8(file_path):
        # 读取文件内容
        with codecs.open(file_path, 'r', encoding='gbk', errors='ignore') as f:
            content = f.read()
        # 将内容转换为utf-8编码
        content_utf8 = content.encode('utf-8')
        # 将转换后的内容写回文件
        with codecs.open(file_path, 'w', encoding='utf-8') as f:
            f.write(content_utf8.decode('utf-8'))

if __name__ == "__main__":
    model_path = "../try_model/models/ZhipuAI/chatglm3-6b"
    embedding_model_path = "shibing624/text2vec-base-chinese"
    LangChain.convert_to_utf8('./tlbb.txt')
    lang_chain = LangChain(model_path, embedding_model_path)
    db, embeddings = lang_chain.load_documents('./tlbb.txt')
    lang_chain.chat(db, embeddings)