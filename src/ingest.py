import os;
from dotenv import load_dotenv;
from pathlib import Path;
from langchain_community.document_loaders import PyPDFLoader;
from langchain_text_splitters import RecursiveCharacterTextSplitter;
from langchain_core.documents import Document;
from langchain_postgres import PGVector;
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

for k in ("GOOGLE_API_KEY",  "DATABASE_URL", "PG_VECTOR_COLLECTION_NAME", "PDF_PATH", "GOOGLE_EMBEDDING_MODEL"):
    if not os.getenv(k):
        raise ValueError(f"Missing environment variable: {k}")

# buscar documento
current_dir = Path(__file__).parent;
pdf_path = current_dir / os.getenv("PDF_PATH");

# fazer chunck
docs = PyPDFLoader(str(pdf_path)).load();

splits = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=150,
    add_start_index=False
    ).split_documents(docs);
if not splits:
    raise SystemExit(0);

# enriquecer documentos
enriched = [
    Document(
        page_content=d.page_content,
        metadata={k: v for k, v in d.metadata.items() if v not in ("", None )}
    )
    for d in splits
]

ids = [f"doc-{i}" for i in range(len(enriched))];

# criar embeddings
embeddings = GoogleGenerativeAIEmbeddings(
    model=os.getenv("GOOGLE_EMBEDDING_MODEL")
);

# criar vetor
store = PGVector(
    embeddings=embeddings,
    collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
    connection=os.getenv("DATABASE_URL"),
    use_jsonb=True
);

# adicionar documentos
store.add_documents(documents=enriched, ids=ids);