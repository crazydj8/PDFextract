import os
import json
import requests
import time
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_mistralai import ChatMistralAI, MistralAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore

class LLM():
    def __init__(self, data, api_key):
        self.prompt_template = ChatPromptTemplate(
            [
                (
                    "system",
                    "You are here to answer the questions asked to you."
                    "you have to answer the question using the information provided in the context text"
                    "You can use external and prior knowledge only when it is related to the text in question" 
                    "Be precise and directly reference the context text"
                    "If the answer cannot be found in the text, respond with 'The answer is not available in the given text.'",
                ),
                ("system", "{context}"),
                ("human", "{question}"),
            ]
        )
        if not api_key:
            raise ValueError("API key is required")
        os.environ["MISTRAL_API_KEY"] = api_key
            
        self.model = ChatMistralAI(model="mistral-large-2411")
        self.generate_embeddings(data)

    def generate_embeddings(self, data):
        embeddings = MistralAIEmbeddings(model="mistral-embed")
        textdata = " ".join(value for value in data["text"].values())
        try:
            self.vectorstore = InMemoryVectorStore.from_texts(
                [textdata],
                embedding=embeddings,
            )
        except Exception as e:
            # More comprehensive error handling
            if hasattr(e, 'response') and e.response.status_code == 401:
                raise ValueError("Invalid or unauthorized API key")
            else:
                raise ValueError(f"Embedding generation error: {str(e)}")
        
    def answer(self, inp):
        context_docs = self.vectorstore.as_retriever().invoke(inp)
        context = " ".join([doc.page_content for doc in context_docs])
        prompt = self.prompt_template.invoke({"context": context, "question": inp})
        
        try:
            resp = self.model.invoke(prompt)
            resp_json = json.loads(resp.model_dump_json())
            print(resp)
            return resp_json
        except Exception as e:
            if hasattr(e, 'response') and e.response.status_code == 429:
                raise ValueError("Rate limit exceeded, please try again in a few seconds")
            else:
                raise e