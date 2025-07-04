from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from utils.responder import Responder
from utils.menu import Menu
import json
import os

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas
responder = Responder()

# Suas rotas existentes permanecem aqui
@app.route('/')
def index():
    return render_template('index.html')

# Rota para o chatbot
@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    bot_response = responder.buscar_resposta(user_message)
    return jsonify({
        'response': bot_response,
        'is_command': user_message.startswith('/')  # Pode ser útil para o frontend
    })

# Rota para obter dados
@app.route('/api/data')
def get_data():
    with open('dados.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return jsonify({
        'sobre': data.get('sobre', ''),
        'duvidas': data.get('duvidas', {}),
        'cidades': data.get('cidades', '')
    })

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
                        print(responder.alternar_modo_livre())
                        print("Digite sua pergunta ou /menu para voltar.")
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
        
        
# if __name__ == '__main__':
#     app.run(debug=True)
    
    