import requests
from bs4 import BeautifulSoup
import json
import re


def raspar_sobre():
    try:
        url = "https://www.jovemprogramador.com.br/sobre.php"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        secao_sobre = soup.find("div", class_="fh5co-heading")

        if not secao_sobre:
            return {"sobre": "Informações não disponíveis."}

        textos = []
        for p in secao_sobre.find_all("p"):
            texto = p.get_text(strip=True)
            if texto and len(texto) > 20:
                textos.append(texto)

        textos_unicos = []
        visto = set()
        for texto in textos:
            if texto not in visto:
                visto.add(texto)
                textos_unicos.append(texto)

        return {"sobre": "\n\n".join(textos_unicos[:5])}

    except Exception as e:
        print(f"Erro ao raspar 'sobre': {e}")
        return {"sobre": "Erro ao carregar dados."}


def raspar_duvidas():
    try:
        url = "https://www.jovemprogramador.com.br/duvidas.php"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        duvidas = {}

        accordion = soup.find("div", class_="accordion")
        if not accordion:
            return {"duvidas": {}}

        itens_duvida = accordion.find_all("div", recursive=False)

        for item in itens_duvida:
            pergunta = item.find("h4").get_text(strip=True) if item.find("h4") else ""
            resposta_div = item.find("div", class_="collapse")
            resposta = (
                resposta_div.find("p").get_text(strip=True)
                if resposta_div and resposta_div.find("p")
                else ""
            )

            if pergunta and resposta:
                duvidas[pergunta.strip()] = resposta.strip()

        return {"duvidas": duvidas}
    except Exception as e:
        print(f"Erro ao raspar 'duvidas': {e}")
        return {"duvidas": {}}


def raspar_cidades():
    try:
        url = "https://www.jovemprogramador.com.br/sobre.php"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Encontra o parágrafo que começa com "Para a edição de"
        for p in soup.find_all("p"):
            if p.get_text(strip=True).startswith("Para a edição de"):
                # O próximo elemento <p> contém as cidades
                cidades_paragraph = p.find_next_sibling("p")
                if cidades_paragraph:
                    # Extrai o texto dentro da tag <strong>
                    cidades = cidades_paragraph.find("strong").get_text(strip=True)
                    return {"cidades": cidades}

        return {"cidades": "Lista de cidades não encontrada na página."}

    except Exception as e:
        print(f"Erro ao raspar cidades: {e}")
        return {"cidades": "Erro ao carregar lista de cidades."}


def raspar_noticias():
    """Raspa TODAS as notícias da página usando a estrutura HTML correta."""
    print("📰 Raspando TODAS as notícias com o novo seletor...")
    try:
        url = "https://www.jovemprogramador.com.br/noticias.php"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"❌ ERRO: Falha ao acessar a página. Código: {response.status_code}")
            return {"noticias": "Erro de conexão com o site."}

        soup = BeautifulSoup(response.text, "html.parser")
        noticias = []

        # NOVA ESTRATÉGIA: Encontrar os contêineres das colunas, que são mais confiáveis.
        # A classe 'col-md-4' parece ser o contêiner de cada notícia.
        cards_containers = soup.find_all("div", class_="col-md-4")
        print(f"Encontrados {len(cards_containers)} possíveis contêineres de notícia.")

        for container in cards_containers:
            # Dentro de cada contêiner, procuramos os elementos específicos da notícia
            titulo_tag = container.find("h3", class_="title")
            resumo_tag = container.find("p")
            link_tag = container.find(
                "a"
            )  # O link geralmente envolve a imagem ou o card todo

            # Só consideramos um card válido se ele tiver um título e um link
            if titulo_tag and link_tag and "href" in link_tag.attrs:
                titulo = titulo_tag.get_text(strip=True)
                link_relativo = link_tag["href"]
                link = f"https://www.jovemprogramador.com.br/{link_relativo}"

                # Pega o resumo, se existir, senão define um padrão.
                resumo = (
                    resumo_tag.get_text(strip=True)
                    if resumo_tag
                    else "Resumo não disponível."
                )

                noticias.append({"titulo": titulo, "link": link, "resumo": resumo})

        if noticias:
            print(f"✅ SUCESSO! Total de {len(noticias)} notícias extraídas.")
        else:
            print(
                "⚠️ AVISO: Nenhuma notícia foi extraída. A estrutura pode ter mudado novamente."
            )

        return {"noticias": noticias}

    except Exception as e:
        print(f"❌ ERRO INESPERADO: {e}")
        return {"noticias": "Erro durante a execução do scraper."}


def raspar_ser_professor():
    """Raspa as informações da página 'Quero Ser Professor'."""
    print("🧑‍🏫 Raspando informações sobre 'Quero Ser Professor'...")
    try:
        url = "https://www.jovemprogramador.com.br/queroserprofessor/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(
                f"❌ ERRO ao acessar a página 'Quero Ser Professor'. Código: {response.status_code}"
            )
            return {"ser_professor": {}}

        soup = BeautifulSoup(response.text, "html.parser")

        # Encontrar a informação sobre vagas abertas
        h3_vagas = soup.find("h3", string=re.compile(r"Acesse o portal do Senac SC"))
        link_vagas_abertas = ""
        if h3_vagas:
            link_tag = h3_vagas.find_next("a", class_="btn-primary")
            if link_tag and "href" in link_tag.attrs:
                link_vagas_abertas = link_tag["href"]

        # Encontrar a informação sobre registrar interesse
        h3_interesse = soup.find("h3", string=re.compile(r"Não tem vaga disponível"))

        # Montar o dicionário de dados se as informações foram encontradas
        if h3_vagas and h3_interesse and link_vagas_abertas:
            dados_professor = {
                "titulo": "Como se tornar um professor do Jovem Programador",
                "vagas_abertas": {
                    "texto": "Para conferir as vagas de professor que estão abertas, o candidato deve acessar o portal de talentos do Senac SC.",
                    "link": link_vagas_abertas,
                },
                "registrar_interesse": {
                    "texto": "Caso não encontre uma vaga para a sua cidade no portal do Senac, o candidato pode registrar seu interesse preenchendo o formulário na página 'Quero Ser Professor' no site do Jovem Programador.",
                    "link_pagina": url,
                },
            }
            print("✅ Informações de 'Quero Ser Professor' extraídas com sucesso.")
            return {"ser_professor": dados_professor}
        else:
            print(
                "⚠️ AVISO: Não foi possível extrair as informações da página 'Quero Ser Professor'."
            )
            return {"ser_professor": {}}

    except Exception as e:
        print(f"❌ ERRO INESPERADO ao raspar 'Quero Ser Professor': {e}")
        return {"ser_professor": {}}


def salvar_dados():
    print("\n🚀 Iniciando raspagem completa do site...")
    dados = {
        "sobre": raspar_sobre()["sobre"],
        "duvidas": raspar_duvidas()["duvidas"],
        "cidades": raspar_cidades()["cidades"],
        "noticias": raspar_noticias()["noticias"],
        "ser_professor": raspar_ser_professor()["ser_professor"],  # <-- NOVA LINHA
    }

    with open("dados.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    print("\n✅ Dados atualizados e salvos com sucesso em 'dados.json'")


if __name__ == "__main__":
    salvar_dados()
