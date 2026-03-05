import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",  # updated to a supported model
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

vector = embeddings.embed_query("What is the capital of Ethiopia?")
print(f"Embedding length: {len(vector)}")
print(f"First 5 values: {vector[:5]}")