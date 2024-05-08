from src.llmtuner.webui.interface import run_web_demo, run_web_ui
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

if __name__ == "__main__":
    run_web_ui()