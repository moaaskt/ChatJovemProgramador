# app.py (Versão Final com Modo Terminal e Web)

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from utils.responder import Chatbot  # Importamos nossa nova classe simplificada

# --- Configuração do Servidor Web (Flask) ---
app = Flask(__name__)
CORS(app)

# Tenta inicializar o chatbot uma única vez.
# Esta instância será usada pela aplicação web.
try:
    chatbot_web = Chatbot()
except Exception as e:
    print(f"CRÍTICO: Não foi possível inicializar o chatbot para a web. Erro: {e}")
    chatbot_web = None


# Rota para a página principal
@app.route("/")
def index():
    return render_template("index.html")


# Rota para a API do chat
@app.route("/api/chat", methods=["POST"])
def chat():
    if not chatbot_web:
        return (
            jsonify(
                {
                    "response": "Desculpe, o chatbot está temporariamente fora de serviço."
                }
            ),
            500,
        )

    user_message = request.json.get("message", "")
    bot_response = chatbot_web.gerar_resposta(user_message)
    return jsonify({"response": bot_response})


# --- Função para Teste no Terminal ---


def main_terminal():
    """Função para rodar uma sessão de chat interativa no terminal."""
    print("\n--- MODO DE TESTE NO TERMINAL ---")
    print("O chatbot será inicializado exclusivamente para esta sessão de teste.")

    try:
        # Cria uma instância separada do chatbot para o terminal
        chatbot_terminal = Chatbot()
    except Exception as e:
        print(f"CRÍTICO: Falha ao iniciar o chatbot para o terminal. Erro: {e}")
        return  # Encerra se não conseguir iniciar

    print("\n✅ Chatbot de teste pronto. Digite sua mensagem ou '/sair' para encerrar.")

    while True:
        try:
            user_message = input("\nVocê: ").strip()

            # Comando para sair do loop de teste
            if user_message.lower() in ["/sair", "exit", "quit"]:
                print("🤖 Encerrando sessão de teste. Até logo!")
                break

            if not user_message:
                continue

            # Gera e imprime a resposta do bot
            bot_response = chatbot_terminal.gerar_resposta(user_message)
            print(f"🤖 Léo: {bot_response}")

        except KeyboardInterrupt:  # Permite sair com Ctrl+C
            print("\n🤖 Encerrando sessão de teste. Até logo!")
            break
        except Exception as e:
            print(f"🤖 Ocorreu um erro inesperado: {e}")


# --- Ponto de Entrada do Script ---

if __name__ == "__main__":
    # Para rodar o chat de TESTE no TERMINAL, deixe esta linha descomentada:
    main_terminal()

    # Para rodar o SERVIDOR WEB, comente a linha acima e descomente a linha abaixo:
    # app.run(debug=True, port=5000)
