# utils/responder.py (Versão Simplificada)

import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Carrega as variáveis de ambiente (como a sua API key) do arquivo .env
load_dotenv()


class Chatbot:
    def __init__(self):
        """
        O construtor da classe agora faz tudo: configura a API, carrega os dados,
        cria o contexto e inicia a sessão de chat com o Gemini.
        """
        print("🤖 Inicializando o Chatbot com Gemini...")

        # 1. Configura a chave da API
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "API Key do Gemini não encontrada! Verifique seu arquivo .env"
            )
        genai.configure(api_key=api_key)

        # 2. Carrega os dados de contexto do seu JSON
        try:
            with open("dados.json", "r", encoding="utf-8") as f:
                self.dados = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(
                "Arquivo 'dados.json' não encontrado! Execute o scraper.py primeiro."
            )

        # 3. Cria o prompt de contexto inicial para o Gemini
        self.contexto_inicial = self._criar_contexto()

        # 4. Inicia o modelo e a sessão de chat
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.chat_session = self.model.start_chat(history=[])

        # 5. "Ensina" o Gemini enviando o contexto inicial
        self.chat_session.send_message(self.contexto_inicial)
        print("✅ Chatbot pronto e online!")

    def _criar_contexto(self):
        """
        Esta função é a mais importante. Ela monta as instruções para o Gemini.
        """
        # Formata a seção de dúvidas
        duvidas_texto = "".join(
            [
                f"• {pergunta}: {resposta}\n"
                for pergunta, resposta in self.dados.get("duvidas", {}).items()
            ]
        )

        # Formata a seção de notícias (NOVO)
        noticias_formatadas = self.dados.get("noticias", [])
        if isinstance(noticias_formatadas, list) and noticias_formatadas:
            noticias_texto = "".join(
                [
                    f"• Título: {n.get('titulo', '')}\n  Resumo: {n.get('resumo', '')}\n  Link: {n.get('link', '')}\n\n"
                    for n in noticias_formatadas
                ]
            )
            
              # Formata a seção 'Como ser Professor' (NOVO)
        prof_info = self.dados.get("ser_professor", {})
        prof_texto = "Informação sobre como se tornar professor não foi encontrada."
        if prof_info and prof_info.get('vagas_abertas'):
            vagas = prof_info.get('vagas_abertas', {})
            interesse = prof_info.get('registrar_interesse', {})
            prof_texto = (
                f"Existem duas maneiras de se candidatar:\n"
                f"1. Para Vagas Abertas: {vagas.get('texto', '')} O link do portal é: {vagas.get('link', '')}\n"
                f"2. Para Registrar Interesse: {interesse.get('texto', '')} A página para isso é: {interesse.get('link_pagina', '')}"
            )
            
            
        else:
            noticias_texto = "Nenhuma notícia recente disponível."

        contexto = f"""
        Você é um assistente virtual especialista no programa Jovem Programador.
        Sua personalidade é amigável, prestativa e você usa emojis para ser mais acolhedor 😊.
        Sua única e exclusiva função é responder perguntas sobre este programa.

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

        --- REGRAS DE COMPORTAMENTO ---
        1. Se a pergunta do usuário não tiver relação com o programa Jovem Programador, recuse educadamente. Diga algo como: "Minha especialidade é apenas o programa Jovem Programador. Posso ajudar com algo sobre isso? 😉"
        2. Mantenha as respostas claras e diretas.
        3. Seja sempre simpático e profissional.
        """
        return contexto

    def gerar_resposta(self, user_message):
        """
        Este é agora o único método público. Ele recebe a mensagem do usuário
        e retorna a resposta do Gemini.
        """
        if not user_message.strip():
            return "Por favor, digite sua pergunta! Estou aqui para ajudar. 😄"

        try:
            # Simplesmente envia a mensagem do usuário para a sessão de chat ativa.
            # O Gemini já sabe como se comportar por causa do contexto inicial.
            response = self.chat_session.send_message(user_message)
            return response.text
        except Exception as e:
            print(f"❌ Erro ao se comunicar com a API do Gemini: {e}")
            return "Ops, parece que estou com um probleminha de conexão... 😅 Poderia tentar de novo em um instante?"
