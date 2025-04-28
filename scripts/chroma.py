import os
import chromadb

from sentence_transformers import SentenceTransformer


def collection_add(collection, model_name):
    model = SentenceTransformer(model_name)
    embedding_dim = model.get_sentence_embedding_dimension()

    if collection.metadata and "embedding_dim" in collection.metadata:
        if collection.metadata["embedding_dim"] != embedding_dim:
            print(f"Dimension incompatible for {model_name}!")
            exit()
    else:
        collection.metadata = {"embedding_dim": embedding_dim}

    resumes_path = "./resumes/filtered/"
    files_name = os.listdir(resumes_path)

    ids = []
    metadatas = []
    documents = []

    for txt in files_name:
        if not txt.endswith(".txt"):
            continue

        lab = txt.replace(".txt", ".lab")

        with open(os.path.join(resumes_path, txt), "r", encoding="utf-8") as file:
            content = file.read().replace("\n", ",")

        with open(os.path.join(resumes_path, lab), "r", encoding="utf-8") as file:
            label = file.read().replace("\n", ",")

        ids.append(lab)
        metadatas.append({"txt": txt, "label": label})
        documents.append(content)

    embeddings = model.encode(documents).tolist()

    assert len(embeddings[0]) == embedding_dim, "Dimension incompatible."

    collection.upsert(
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas,
        ids=ids,
    )


def main():
    model_names = [
        "all-mpnet-base-v2",
        "multi-qa-mpnet-base-dot-v1",
        "all-distilroberta-v1",
        "all-MiniLM-L12-v2",
        "multi-qa-distilbert-cos-v1",
        "all-MiniLM-L6-v2",
        "multi-qa-MiniLM-L6-cos-v1",
        "paraphrase-multilingual-mpnet-base-v2",
        "paraphrase-albert-small-v2",
        "paraphrase-multilingual-MiniLM-L12-v2",
        "paraphrase-MiniLM-L3-v2",
        "distiluse-base-multilingual-cased-v1",
        "distiluse-base-multilingual-cased-v2",
    ]

    for model_name in model_names:
        client = chromadb.PersistentClient(path="./chroma/")

        collection_name = f"collection_{model_name}"

        model = SentenceTransformer(model_name)
        embedding_dim = model.get_sentence_embedding_dimension()

        collection = client.get_or_create_collection(
            name=collection_name, metadata={"embedding_dim": embedding_dim}
        )

        collection_add(collection, model_name)
        print(f"Collection added in {model_name}")


if __name__ == "__main__":
    main()
