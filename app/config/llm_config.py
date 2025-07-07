# Inisialisasi model (sama dengan GPT-4o di phi)
from langchain.chat_models import init_chat_model


llm = init_chat_model("gemini-2.0-flash", model_provider="google_genai")