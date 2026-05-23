import os
from dotenv import load_dotenv

load_dotenv()


def read_prompt():
    try:
        path = os.getenv("prompt_path")
        if not path:
            print("check the file path in env")
            return
        with open(file=path, mode="r") as f:
            prompt = f.read().strip()
            if not prompt or prompt == "":
                print("prompt file is empty")
                return
            return prompt
    except FileNotFoundError or TypeError:
        print("prompt not found")