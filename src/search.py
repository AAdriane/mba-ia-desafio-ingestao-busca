import os;
from dotenv import load_dotenv;
from langchain_google_genai import GoogleGenerativeAIEmbeddings;
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI;
from langchain_postgres import PGVector;
from langchain.prompts import PromptTemplate;
from langchain_core.output_parsers import StrOutputParser;

load_dotenv();

for k in ("GOOGLE_API_KEY", "DATABASE_URL","PG_VECTOR_COLLECTION_NAME", "PDF_PATH", "GOOGLE_EMBEDDING_MODEL", "GOOGLE_LLM_MODEL"):
    if not os.getenv(k):
        raise RuntimeError(f"Variável de ambiente {k} não está definida");
    

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
""";

def search_prompt(question=None):
  if not question:
      return ();

  embeddings = GoogleGenerativeAIEmbeddings(model=os.getenv("GOOGLE_EMBEDDING_MODEL"));

  store = PGVector(
      embeddings=embeddings,
      collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
      connection=os.getenv("DATABASE_URL"),
      use_jsonb=True
  );

  result = store.similarity_search_with_score(question, k=10);

  # concatenar o contexto
  contexto = "\n".join([f"\n{doc.page_content}" for doc, _ in result]);

  template = PromptTemplate(
      template=PROMPT_TEMPLATE,
      input_variables=["contexto", "pergunta"]
  );

  llm = ChatGoogleGenerativeAI(
      model=os.getenv("GOOGLE_LLM_MODEL"),
      temperature=0.5
  );

  chain = template | llm | StrOutputParser();

  return chain.invoke({
      "contexto": contexto,
      "pergunta": question
  });