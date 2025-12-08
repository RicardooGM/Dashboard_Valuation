from dotenv import load_dotenv
import os

load_dotenv()

chave = os.getenv("FRED_API_KEY")

print("Chave carregada:", chave)

