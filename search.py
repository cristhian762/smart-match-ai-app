import chromadb

from sentence_transformers import SentenceTransformer


def sumarized(value="full"):
    data = {
        "full": "./chroma",
        "llm": "./chroma_llm",
        "pegasus": "./chroma_pegasus",
    }

    return data[value]


def models():
    return {
        "all-mpnet-base-v2": "All Mpnet Base V2",
        "multi-qa-mpnet-base-dot-v1": "Multi Qa Mpnet Base Dot V1",
        "all-distilroberta-v1": "All Distilroberta V1",
        "all-MiniLM-L12-v2": "All Minilm L12 V2",
        "multi-qa-distilbert-cos-v1": "Multi Qa Distilbert Cos V1",
        "all-MiniLM-L6-v2": "All Minilm L6 V2",
        "multi-qa-MiniLM-L6-cos-v1": "Multi Qa Minilm L6 Cos V1",
        "paraphrase-multilingual-mpnet-base-v2": "Paraphrase Multilingual Mpnet Base V2",
        "paraphrase-albert-small-v2": "Paraphrase Albert Small V2",
        "paraphrase-multilingual-MiniLM-L12-v2": "Paraphrase Multilingual Minilm L12 V2",
        "paraphrase-MiniLM-L3-v2": "Paraphrase Minilm L3 V2",
        "distiluse-base-multilingual-cased-v1": "Distiluse Base Multilingual Cased V1",
        "distiluse-base-multilingual-cased-v2": "Distiluse Base Multilingual Cased V2",
    }


def matches(model_name, n_results, message, suma="full"):
    collection_name = f"collection_{model_name}"
    client = chromadb.PersistentClient(path=sumarized(suma))
    collection = client.get_collection(name=collection_name)

    model = SentenceTransformer(model_name)

    query_embedding = model.encode([
        "Considering the following resume, find the one that best matches it. Curriculum: "
        + message
    ]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results,
    )

    if not results["metadatas"]:
        return []

    dic = {}
    docs = results["documents"]

    for index, value in enumerate(results["ids"][0]):
        key = value.replace(".lab", "")
        labels = str(results["metadatas"][0][index]["label"])

        if not docs or not docs[0] or not docs[0][index]:
            continue

        dic[key] = {
            "labels": labels.replace("_", " ").split(","),
            "desc": docs[0][index],
        }

    return dic
