# Inisialisasi model (sama dengan GPT-4o di phi)
from langchain_groq import ChatGroq
import os

llm = ChatGroq(model_name="qwen/qwen3-32b", api_key=os.getenv("GROQ_API_KEY"))