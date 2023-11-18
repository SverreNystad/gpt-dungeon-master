from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings

import os
from dotenv import load_dotenv

load_dotenv()

class EmbeddingConfig:
    API_KEY = os.getenv('OPENAI_DALL_E_API_KEY')

# 1. Vectorise the sales repsonse csv data
loader = CSVLoader(file_path="characters_facts.csv")
documents = loader.load()

print(f"documents: {documents[0]}")
print(f"documents length: {len(documents)}")

embeddings = OpenAIEmbeddings(api_key=EmbeddingConfig.API_KEY)
db = FAISS.from_documents(documents, embeddings)

# 2. Function for similarity search
def retrieve_info(query) -> list:
    """
    Retrieve information from the database based on the query
    Will allways return something if the db is not empty. 
    Meaning that if the query is not in the database, it will return the most similar document.
    Example:
        ans = retrieve_info("Who is CHARACTER DOES NOT EXIST sister?")
        # ans Gave Andreas. Even though there are no sister in the database and CHARACTER DOES NOT EXIST does not exist.
    
    We might need to add a threshold for the similarity search. When using it for world facts or characters.
    """
    similar_documents = db.similarity_search(query, k=1)
    print(f"similar_documents: {similar_documents}")

    page_content = [doc.page_content for doc in similar_documents]

    return page_content

ans = retrieve_info("Who is CHARACTER DOES NOT EXIST sister?")
print(ans)
# 3. Setup LLMChain & prompts

# 4. 