import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",          # current stable fast model
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7,
)

response = llm.invoke("Hello! Tell me a short fun fact about Ethiopia.")
print(response.content)