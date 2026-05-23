from chromadb.errors import ChromaError

RETRY_ON = (ChromaError, OSError)
