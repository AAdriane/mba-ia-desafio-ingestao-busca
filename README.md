# Desafio MBA Engenharia de Software com IA - Full Cycle

---

## Ingestão e Busca Semântica com LangChain e Postgres
Tecnologias utilizadas:
- ![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
- ![LangChain](https://img.shields.io/badge/LangChain-Integration-green)
- ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-pgVector-blue)
- ![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)

LLM utilizado:
- gemini-2.5-flash-lite

### Como executar o projeto?
Assumo que já tenha Python 3 e Docker Desktop instalados, serão necessários.

- 1. Clonar o repositório.
- 2. Na raiz do projeto execute os comandos abaixo para criar o ambiente virtual:


        `python3 -m venv venv` 
       
        `source venv/bin/activate`


- 3. Após ativar o ambiente virtual, instale as dependências com o seguinte comando:

        `pip install -r requirements.txt`

- 4. Crie o seu arquivo `.env` e faça uma cópia do conteúdo do `.env.exemple` substituindo o valor das variáveis de configuração.
- 5. Com o docker desktop rodando, buildar o container:

        `docker compose up -d`

- 6. Fazer a ingestão do PDF no banco de dados:

        `python src/ingest.py `

- 7. Execute o chat:

        `python src/chat.py`
        
- 8. Exemplo de chat:
        ```json
            Escolha a opção e digite o número:
            1. Fazer uma pergunta
            2. Sair
            1
            --------------------------------------------------------
            Digite sua pergunta: Sua pergunta?
            Resposta: Resposta LLM
            --------------------------------------------------------
        ```