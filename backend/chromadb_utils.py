import chromadb
from chromadb.utils import embedding_functions
import json
import os
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=openai_api_key,
    model_name="text-embedding-3-large"    
)

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="threat_embeddings",
    embedding_function=openai_ef
)

# def store_analysis_vector(document_id, analysis_json):
#     collection.add(
#         documents=[analysis_json["summary_impact"]],
#         metadatas=[analysis_json],
#         ids=[document_id]
#     )



def store_analysis_vector(document_id, analysis_result, source_name, source_url):
    """
    Store analysis results in ChromaDB with metadata including source information.

    :param document_id: Unique ID for the document.
    :param analysis_result: Dictionary with analysis information.
    :param source_name: Name of the source (e.g., "The Hacker News").
    :param source_url: URL to the original article.
    """
    flat_metadata = {
        "source_name": source_name,
        "source_url": source_url
    }

    for key, value in analysis_result.items():
        if isinstance(value, (list, dict)):
            flat_metadata[key] = json.dumps(value)  # Serialize complex types
        else:
            flat_metadata[key] = value

    collection.add(
        documents=[analysis_result["summary_impact"]],
        metadatas=[flat_metadata],
        ids=[document_id]
    )


def query_similar_threats(query_text, top_k=5):
    return collection.query(query_texts=[query_text], n_results=top_k)
