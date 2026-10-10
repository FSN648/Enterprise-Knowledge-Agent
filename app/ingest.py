from .rag import ingest_documents

if __name__ == "__main__":
    docs, chunks = ingest_documents()
    print(f"Ingested {docs} documents into {chunks} chunks.")
