from utils.responder import Responder
from utils.menu import Menu
import json
import os

def main():
    # Verifica se o JSON existe
    if not os.path.exists('dados.json'):
        print("❌ Erro: Arquivo 'dados.json' não encontrado. Execute scraper.py primeiro!")
        return

    responder = Responder()
    
    try:
        with open('dados.json', 'r', encoding='utf-8') as f:
            dados = json.load(f)
    except Exception as e:
        print(f"❌ Erro ao ler dados: {e}")
        return

    print("🤖 Bem-vindo ao Chatbot do Jovem Programador!")
    print("Digite uma mensagem como 'Oi' ou 'Bom dia' para começar, /menu para opções ou faça uma pergunta livre.")

    while True:
        try:
            entrada = input("\nVocê: ").strip()
            
            if not entrada:
                print("🤖: Por favor, digite sua pergunta ou /menu para opções.")
                continue
                
            if entrada.lower() == "/menu":
                while True:
                    opcao = Menu.mostrar()
                    
                    if opcao == "1":
                        print("\n📌 SOBRE O PROGRAMA:")
                        print(responder.buscar_resposta("sobre o programa"))
                    
                    elif opcao == "2":
                        Menu.exibir_duvidas(dados)
                    
                    elif opcao == "3":
                        print("\n📍 CIDADES PARTICIPANTES:")
                        print(responder.buscar_resposta("cidades participantes"))
                    
                    elif opcao == "4":
                        print("Modo chat livre ativado. Digite sua pergunta ou /menu para voltar.")
                        break
                    
                    elif opcao == "5":
                        print("Até logo! 👋")
                        return
                    
                    else:
                        print("Opção inválida. Tente novamente.")
            
            elif entrada.lower() == "/sair":
                print("Até logo! 👋")
                break
            
            else:
                print("🤖:", responder.buscar_resposta(entrada))
                
        except KeyboardInterrupt:
            print("\nAté logo! 👋")
            break
        except Exception as e:
            print(f"🤖: Ocorreu um erro. Por favor, tente novamente. ({e})")

if __name__ == "__main__":
    main()