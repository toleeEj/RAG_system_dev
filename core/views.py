from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import Document
from .serializers import QuerySerializer, AnswerSerializer


from django.http import StreamingHttpResponse
import json




# LangChain imports (2026 compatible)
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


class QueryAPIView(APIView):
    def post(self, request):
        serializer = QuerySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_query = serializer.validated_data["query"]

        # Step 1: Load all documents from DB
        docs = Document.objects.all()
        if not docs.exists():
            return Response(
                {"answer": "No knowledge base documents found. Please add some via the admin panel."},
                status=status.HTTP_200_OK,
            )

        texts = [doc.content for doc in docs]
        metadatas = [{"title": doc.title, "id": doc.id} for doc in docs]  # optional but useful

        # Step 2: Embeddings model (use the one that worked in your test)
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",  # stable & widely supported in 2026
            # Alternative (if you tested it successfully): "models/gemini-embedding-001"
            google_api_key=settings.GOOGLE_API_KEY,
        )

        # Step 3: Build FAISS vector store (in-memory, recreated per request → ok for MVP)
        vectorstore = FAISS.from_texts(
            texts=texts,
            embedding=embeddings,
            metadatas=metadatas,
        )

        # Step 4: LLM (use a current model)
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",           # fast & good quality in 2026
            # Alternatives: "gemini-2.5-flash-lite", "gemini-3-flash-preview" (if available)
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0.3,                     # low = more factual & consistent
            max_output_tokens=600,
        )

        # Step 5: Prompt template (banking-specific)
        prompt_template = """You are a polite and accurate banking customer service assistant.
        Answer based only on the provided context. Be concise, helpful, and professional.
        If the information is not in the context, say: "I'm sorry, I don't have that information right now."

        Context:
        {context}

        Question: {question}

        Answer:"""

        prompt = PromptTemplate.from_template(prompt_template)

        # Step 6: Helper to format retrieved documents into context string
        def format_docs(docs):
            return "\n\n".join(
                f"From document '{doc.metadata.get('title', 'Unknown')}':\n{doc.page_content}"
                for doc in docs
            )

        # Step 7: LCEL RAG chain (modern & recommended way in 2026)
        rag_chain = (
            # Input: question → retrieve docs → format them → pass to prompt + question
            {
                "context": vectorstore.as_retriever(search_kwargs={"k": 4}) | format_docs,
                "question": RunnablePassthrough(),
            }
            | prompt
            | llm
            | StrOutputParser()
        )

        # Step 8: Run the chain
        try:
            answer = rag_chain.invoke(user_query)
        except Exception as e:
            return Response(
                {"answer": f"Error processing query: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Return clean JSON
        response_serializer = AnswerSerializer({"answer": answer.strip()})
        return Response(response_serializer.data, status=status.HTTP_200_OK)