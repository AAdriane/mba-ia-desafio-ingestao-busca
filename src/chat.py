import os
from search import search_prompt
from dotenv import load_dotenv

load_dotenv();

def main():

    print("Olá, escolha a opção e digite o número:");
    print("1. Fazer uma pergunta sobre o contexto");
    print("2. Sair");

    choice = input();

    while True:
        match choice:
            case "1":
                print("-"*100);
                question = input("Digite sua pergunta: ");

                if not question:
                    print("Você não digitou uma pergunta.");
                    continue;

                response = search_prompt(question);
                
                print(f"\nResposta: {response}");
            
                print("-"*100);
            case "2":
                print("Saindo do chat. Até mais!");
                break;
            case _:
                print("Opção inválida. Por favor, escolha novamente.");

        print("\nEscolha a opção e digite o número:");
        print("1. Fazer uma pergunta");
        print("2. Sair");
        choice = input();

if __name__ == "__main__":
    main()