import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Carrega as variáveis de ambiente (como a sua API key) do arquivo .env
load_dotenv()


class Chatbot:
    def __init__(self):
        print("🤖 Inicializando o Chatbot com Gemini...")

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "API Key do Gemini não encontrada! Verifique seu arquivo .env"
            )
        genai.configure(api_key=api_key)

        try:
            with open("dados.json", "r", encoding="utf-8") as f:
                self.dados = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(
                "Arquivo 'dados.json' não encontrado! Execute o scraper.py primeiro."
            )

        self.contexto_inicial = self._criar_contexto()
        self.model = genai.GenerativeModel("gemini-2.5-flash")
        self.chat_session = self.model.start_chat(history=[])
        self.chat_session.send_message(self.contexto_inicial)
        print("✅ Chatbot pronto e online!")

    def _criar_contexto(self):
        duvidas_texto = "".join(
            [
                f"• {pergunta}: {resposta}\n"
                for pergunta, resposta in self.dados.get("duvidas", {}).items()
            ]
        )

        todas_as_noticias = self.dados.get("noticias", [])
        noticias_para_contexto = todas_as_noticias[:5]

        if isinstance(noticias_para_contexto, list) and noticias_para_contexto:
            noticias_texto = "".join(
                [
                    f"• Título: {n.get('titulo', '')}\n  Texto Completo: {n.get('texto_completo', '')}\n  Link: {n.get('link', '')}\n\n"
                    for n in noticias_para_contexto
                ]
            )
        else:
            noticias_texto = "Nenhuma notícia recente disponível."

        prof_info = self.dados.get("ser_professor", {})
        if prof_info and prof_info.get("vagas_abertas"):
            vagas = prof_info.get("vagas_abertas", {})
            interesse = prof_info.get("registrar_interesse", {})
            prof_texto = (
                f"Existem duas maneiras de se candidatar:\n"
                f"1. Para Vagas Abertas: {vagas.get('texto', '')} O link do portal é: {vagas.get('link', '')}\n"
                f"2. Para Registrar Interesse: {interesse.get('texto', '')} A página para isso é: {interesse.get('link_pagina', '')}"
            )
        else:
            prof_texto = "Informação sobre como se tornar professor não foi encontrada."

        hackathon_info = self.dados.get("hackathon", {})
        hackathon_texto = ""

        desc = hackathon_info.get("descricao", "")
        video = hackathon_info.get("link_video", "")
        noticias_hackathon = hackathon_info.get("noticias", [])

        if desc:
            hackathon_texto += f"{desc}\n"
        if video:
            hackathon_texto += f"Para saber mais, assista ao vídeo principal: {video}\n"

        if noticias_hackathon:
            hackathon_texto += "\nÚLTIMAS NOTÍCIAS SOBRE O HACKATHON:\n"
            noticias_formatadas = "".join(
                [
                    f"- Título: {n.get('titulo')}\n  Resumo: {n.get('resumo')}\n  Leia mais em: {n.get('link')}\n\n"
                    for n in noticias_hackathon
                ]
            )
        hackathon_texto += noticias_formatadas

        if not hackathon_texto.strip():
            hackathon_texto = "Informação sobre o Hackathon não foi encontrada."

        contexto = f"""
        Você é um assistente virtual chamado "leo" ou "leozin" especialista no programa Jovem Programador.
        Sua única e exclusiva função é responder perguntas sobre este programa.
        Sua personalidade é amigável, prestativa e você usa emojis de forma leve e ocasional 😊. 
        Evite repetir saudações como "Olá" ou "Oi" em todas as respostas. Use saudações apenas no início da conversa.


        Use APENAS as informações oficiais fornecidas abaixo para basear 100% de suas respostas.
        NÃO invente informações e NÃO use conhecimento externo.

        --- INFORMAÇÕES OFICIAIS ---
        
        SOBRE O PROGRAMA:
        {self.dados.get("sobre", "Informação não disponível.")}

        DÚVIDAS FREQUENTES:
        {duvidas_texto}

        CIDADES PARTICIPANTES:
        {self.dados.get("cidades", "Lista de cidades não disponível.")}

        ÚLTIMAS NOTÍCIAS:
        {noticias_texto}
        
        COMO SER PROFESSOR:
        {prof_texto}
        
        SOBRE O HACKATHON:
        {hackathon_texto}

        --- REGRAS DE COMPORTAMENTO ---
        1. Se a pergunta do usuário não tiver relação com o programa Jovem Programador, recuse educadamente. Diga algo como: "Minha especialidade é apenas o programa Jovem Programador. Posso ajudar com algo sobre isso? 😉"
        2. Mantenha as respostas claras e diretas.
        3. Seja sempre simpático e profissional.
        """
        return contexto

    def gerar_resposta(self, user_message):
        if not user_message.strip():
            return "Por favor, digite sua pergunta! Estou aqui para ajudar. 😄"

        try:
            response = self.chat_session.send_message(user_message)
            return response.text
        except Exception as e:
            print(f"❌ Erro ao se comunicar com a API do Gemini: {e}")
            return "Ops, parece que estou com um probleminha de conexão... 😅 Poderia tentar de novo em um instante?"
