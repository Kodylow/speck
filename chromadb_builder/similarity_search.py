import os

import langchain
import openai
from chromadb.utils import embedding_functions
from langchain.chains import VectorDBQAWithSourcesChain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma

openai.api_key = os.getenv("OPENAI_API_KEY")

# openai_ef = embedding_functions.OpenAIEmbeddingFunction(
#     api_key=openai.api_key,
#     model_name="text-embedding-ada-002"
# )
openai_ef = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))


vectorstore = Chroma(collection_name="bitcoin2",
                     embedding_function=openai_ef,
                     persist_directory="/Users/kodylow/Documents/github/deep-learning/ln-spec-bot/chromadb_builder/dbs")

docs = vectorstore.similarity_search("who is satoshi", k=1)
print(docs)


# /Users/kodylow/Documents/github/deep-learning/ln-spec-bot/
