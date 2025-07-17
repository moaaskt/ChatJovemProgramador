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

        # A formatação de todas as suas seções existentes
        duvidas_texto = "".join(
            [
                f"• {pergunta}: {resposta}\n"
                for pergunta, resposta in self.dados.get("duvidas", {}).items()
            ]
        )

        # Formata a seção 'notícias'
        todas_as_noticias = self.dados.get("noticias", [])
        noticias_para_contexto = todas_as_noticias[:5]

        noticias_texto = "Nenhuma notícia recente disponível."
        if isinstance(noticias_para_contexto, list) and noticias_para_contexto:
            noticias_texto = "".join(
                [
                    f"• Título: {n.get('titulo', '')}\n  Texto Completo: {n.get('texto_completo', '')}\n  Link: {n.get('link', '')}\n\n"
                    for n in noticias_para_contexto
                ]
            )

        # Formata a seção 'Como ser professor'
        prof_info = self.dados.get("ser_professor", {})
        prof_texto = "Informação sobre como se tornar professor não foi encontrada."
        if prof_info and prof_info.get("vagas_abertas"):
            vagas = prof_info.get("vagas_abertas", {})
            interesse = prof_info.get("registrar_interesse", {})
            prof_texto = (
                f"Existem duas maneiras de se candidatar:\n"
                f"1. Para Vagas Abertas: {vagas.get('texto', '')} O link do portal é: {vagas.get('link', '')}\n"
                f"2. Para Registrar Interesse: {interesse.get('texto', '')} A página para isso é: {interesse.get('link_pagina', '')}"
            )

        # Formata a seção 'Hackathon'
        hackathon_info = self.dados.get("hackathon", {})
        hackathon_texto = "Informação sobre o Hackathon não foi encontrada."
        if hackathon_info:
            partes_texto = []
            descricao = hackathon_info.get("descricao", "")
            video = hackathon_info.get("link_video", "")
            noticias_hackathon = hackathon_info.get("noticias", [])
            if descricao:
                partes_texto.append(descricao)
            if video:
                partes_texto.append(
                    f"Para saber mais, assista ao vídeo principal: {video}"
                )
            if noticias_hackathon:
                partes_texto.append("\nÚLTIMAS NOTÍCIAS SOBRE O HACKATHON:")
                noticias_formatadas = "".join(
                    [
                        f"- Título: {n.get('titulo')}\n  Resumo: {n.get('resumo')}\n  Leia mais em: {n.get('link')}\n"
                        for n in noticias_hackathon
                    ]
                )
                partes_texto.append(noticias_formatadas)
            if partes_texto:
                hackathon_texto = "\n\n".join(partes_texto)

        # Formata a seção 'Redes Sociais'
        redes_info = self.dados.get("redes_sociais", {})
        redes_texto = (
            "Não encontrei informações sobre as redes sociais oficiais do programa."
        )
        if redes_info:
            # Cria uma lista formatada: "- Facebook: https://..."
            lista_redes = [f"- {nome}: {url}" for nome, url in redes_info.items()]
            redes_texto = (
                "Você pode encontrar e seguir o Jovem Programador nas seguintes redes sociais:\n"
                + "\n".join(lista_redes)
            )

        # Formata a seção 'Apoiadores'
        apoiadores_info = self.dados.get("apoiadores", [])
        apoiadores_texto = "Não encontrei a lista de empresas apoiadoras."
        if apoiadores_info:
            # Pega apenas o nome de cada apoiador e junta com vírgulas
            lista_nomes = [apoiador.get("nome", "") for apoiador in apoiadores_info]
            apoiadores_texto = (
                "O programa conta com o apoio de diversas empresas importantes, como: "
                + ", ".join(lista_nomes)
                + "."
            )

        # Formata a seção 'Patrocinadores'
        patrocinadores_info = self.dados.get("patrocinadores", [])
        patrocinadores_texto = "Não encontrei a lista de empresas patrocinadoras."
        if patrocinadores_info:
            lista_nomes = [p.get("nome", "") for p in patrocinadores_info]
            patrocinadores_texto = (
                "O programa é patrocinado por grandes empresas de tecnologia, como: "
                + ", ".join(lista_nomes)
                + "."
            )

        # Formata a seção 'Parceiros'
        parceiros_info = self.dados.get("parceiros", [])
        parceiros_texto = "Não encontrei a lista de parceiros do programa."
        if parceiros_info:
            lista_nomes = [p.get("nome", "") for p in parceiros_info]
            parceiros_texto = (
                "Os parceiros do programa são: " + ", ".join(lista_nomes) + "."
            )

            # Formata a seção 'Links de Acesso' (NOVO)
        acesso_info = self.dados.get("links_acesso", {})
        acesso_texto = "Não encontrei os links para as áreas de acesso."
        if acesso_info:
            link_aluno = acesso_info.get("aluno", "Link não disponível")
            link_empresa = acesso_info.get("empresa", "Link não disponível")
            acesso_texto = f"Existem portais de acesso específicos. O link para a Área do Aluno é: {link_aluno}. O link para a Área da Empresa é: {link_empresa}."

        # A montagem do contexto final
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
        
        ÚLTIMAS NOTÍCIAS:
        {noticias_texto}

        SOBRE O BLOG:
        A seção 'Blog' e a seção 'ÚLTIMAS NOTÍCIAS' do site Jovem Programador são a mesma coisa e apresentam o mesmo conteúdo. Se um usuário perguntar sobre o blog, use as informações disponíveis em 'ÚLTIMAS NOTÍCIAS' para formular a resposta.

        COMO SER PROFESSOR:
        {prof_texto}
        
        SOBRE O HACKATHON:
        {hackathon_texto}
        
        REDES SOCIAIS:
        {redes_texto}
        
        APOIADORES:
        {apoiadores_texto}
        
        PATROCINADORES:
        {patrocinadores_texto}
        
        PARCEIROS:
        {parceiros_texto}
        
        PORTAIS DE ACESSO:
        {acesso_texto}

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
