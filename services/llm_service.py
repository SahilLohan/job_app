from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
from dotenv import load_dotenv
load_dotenv()

import json

with open("config.json", "r") as file:
    config = json.load(file)

def get_llm():
    print("Getting LLM")
    MODEL = config["model"]
    MODEL_PROVIDER = config["model_provider"]

    # ============================================================
    # LLM
    # ============================================================
    if MODEL_PROVIDER == "groq":
        llm = ChatGroq(
                model=MODEL,
                temperature=0,
            )
        print("Groq model selected...")
    elif MODEL_PROVIDER == "ollama":

        llm = ChatOllama(
            model="qwen3:14b",
            temperature=0,
        )
        print("ollama model selected...")
    else:
        llm = ChatGroq(
                        model="openai/gpt-oss-20b",
                        temperature=0,
                    )
        print("Fallback model selected...")
    return llm