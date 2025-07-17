import requests
from bs4 import BeautifulSoup
import json
import re


#  raspagem do sobre
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


# raspagem de dúvidas frequentes

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



# raspasgem de cidades

def raspar_cidades():
    try:
        url = "https://www.jovemprogramador.com.br/sobre.php"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        for p in soup.find_all("p"):
            if p.get_text(strip=True).startswith("Para a edição de"):

                cidades_paragraph = p.find_next_sibling("p")
                if cidades_paragraph:

                    cidades = cidades_paragraph.find("strong").get_text(strip=True)
                    return {"cidades": cidades}

        return {"cidades": "Lista de cidades não encontrada na página."}

    except Exception as e:
        print(f"Erro ao raspar cidades: {e}")
        return {"cidades": "Erro ao carregar lista de cidades."}




# raspagem de notícias

def raspar_noticias():
    """
    Raspa a lista de notícias e, em seguida, visita cada link para
    extrair TODO o texto de cada artigo.
    """
    print(
        "📰 Iniciando raspagem profunda de TODAS as notícias (isso pode levar alguns minutos)..."
    )
    try:
        url_lista = "https://www.jovemprogramador.com.br/noticias.php"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response_lista = requests.get(url_lista, headers=headers)

        if response_lista.status_code != 200:
            print(
                f"❌ ERRO: Falha ao acessar a lista de notícias. Código: {response_lista.status_code}"
            )
            return {"noticias": []}

        soup_lista = BeautifulSoup(response_lista.text, "html.parser")
        noticias_completas = []

        cards_containers = soup_lista.find_all("div", class_="col-md-4")
        total_noticias = len(cards_containers)
        print(f"Encontrados {total_noticias} artigos para extrair.")

        for i, container in enumerate(cards_containers):
            titulo_tag = container.find("h3", class_="title")
            link_tag = container.find("a")

            if titulo_tag and link_tag and "href" in link_tag.attrs:
                titulo = titulo_tag.get_text(strip=True)
                link_absoluto = (
                    f"https://www.jovemprogramador.com.br/{link_tag['href']}"
                )

                print(
                    f"    -> Raspando conteúdo do artigo {i+1}/{total_noticias}: {titulo}"
                )
                try:
                    response_artigo = requests.get(link_absoluto, headers=headers)
                    if response_artigo.status_code == 200:
                        soup_artigo = BeautifulSoup(response_artigo.text, "html.parser")
                        secao_artigo = soup_artigo.find("div", id="fh5co-blog-section")

                        texto_completo = ""
                        if secao_artigo:
                            texto_completo = secao_artigo.get_text(
                                separator="\n", strip=True
                            )
                        else:
                            texto_completo = (
                                "Não foi possível extrair o texto completo do artigo."
                            )

                        noticias_completas.append(
                            {
                                "titulo": titulo,
                                "link": link_absoluto,
                                "texto_completo": texto_completo,
                            }
                        )
                except Exception as e_artigo:
                    print(
                        f"      - ERRO ao processar o artigo {link_absoluto}: {e_artigo}"
                    )

        print(
            f"✅ SUCESSO! Conteúdo completo de {len(noticias_completas)} notícias extraído."
        )
        return {"noticias": noticias_completas}

    except Exception as e:
        print(f"❌ ERRO INESPERADO na função raspar_noticias: {e}")
        return {"noticias": []}




# raspagem de ser professor

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




# raspagem de hackathon

def raspar_hackathon():
    """Raspa a descrição, vídeo e notícias relacionadas da página do Hackathon."""
    print("🏆 Raspando informações completas sobre o Hackathon...")
    try:
        url = "https://www.jovemprogramador.com.br/hackathon/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(
                f"❌ ERRO ao acessar a página do Hackathon. Código: {response.status_code}"
            )
            return {"hackathon": {}}

        soup = BeautifulSoup(response.text, "html.parser")

        # ---  Extrair a descrição geral ---
        descricao = ""
        container_desc = soup.find("div", id="fh5co-about")
        if container_desc:
            paragrafos = container_desc.find_all("p")
            descricao = "\n".join([p.get_text(strip=True) for p in paragrafos])

        # --- Extrair o link do vídeo ---
        link_video = ""
        if container_desc:
            iframe = container_desc.find("iframe")
            if iframe and "src" in iframe.attrs:
                link_video = iframe["src"]

        # ---  Extrair as notícias do Hackathon  ---
        print("    - Procurando notícias relacionadas ao Hackathon...")
        noticias_relacionadas = []
        # O seletor 'a' com a classe 'item-grid' parece ser o ideal
        cards_noticias = soup.find_all("a", class_="item-grid")

        for card in cards_noticias:
            titulo_tag = card.find("h3", class_="title")
            resumo_tag = card.find("p")

            if titulo_tag and "href" in card.attrs:
                titulo = titulo_tag.get_text(strip=True)
                link_relativo = card["href"]
                link = f"https://www.jovemprogramador.com.br/{link_relativo}"
                resumo = resumo_tag.get_text(strip=True) if resumo_tag else ""
                noticias_relacionadas.append(
                    {"titulo": titulo, "resumo": resumo, "link": link}
                )

        print(f"    - Encontradas {len(noticias_relacionadas)} notícias do Hackathon.")

        # ---  Montar o dicionário final ---
        dados_hackathon = {
            "descricao": descricao,
            "link_video": link_video,
            "noticias": noticias_relacionadas,  # Adicionando a lista de notícias
        }

        print("✅ Informações do Hackathon extraídas com sucesso.")
        return {"hackathon": dados_hackathon}

    except Exception as e:
        print(f"❌ ERRO INESPERADO ao raspar a página do Hackathon: {e}")
        return {"hackathon": {}}




# raspagem de redes sociais

def raspar_redes_sociais():
    """Raspa os links das redes sociais do cabeçalho do site."""
    print("📱 Raspando links das redes sociais...")
    try:

        url = "https://www.jovemprogramador.com.br/sobre.php"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        redes = {}
        # Encontramos o elemento <nav> que contém os links
        nav_container = soup.find("nav", attrs={"role": "navigation"})

        if nav_container:
            links = nav_container.find_all("a")  # Pega todos os links dentro do <nav>
            for link in links:
                href = link.get("href", "")
                # Verificamos se o link pertence a uma rede social conhecida
                if "facebook.com" in href:
                    redes["Facebook"] = href
                elif "instagram.com" in href:
                    redes["Instagram"] = href
                elif "linkedin.com" in href:
                    redes["LinkedIn"] = href
                elif "tiktok.com" in href:
                    redes["TikTok"] = href

        if redes:
            print(f"✅ Encontradas {len(redes)} redes sociais.")
        else:
            print("⚠️ Nenhuma rede social encontrada.")

        return {"redes_sociais": redes}

    except Exception as e:
        print(f"❌ ERRO ao raspar redes sociais: {e}")
        return {"redes_sociais": {}}




# raspagem dos apoiadores

def raspar_apoiadores():
    """Raspa a lista de empresas apoiadoras do programa."""
    print("🤝 Raspando lista de Apoiadores...")
    try:
        url = "https://www.jovemprogramador.com.br/apoiadores.php"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        apoiadores = []
        # O seletor 'a' com a classe 'item-grid' parece ser o ideal para cada apoiador
        cards_apoiadores = soup.find_all("a", class_="item-grid")

        for card in cards_apoiadores:
            link = card.get("href", "")
            img_tag = card.find("img")

            # O nome da empresa está no atributo 'alt' da imagem
            nome = (
                img_tag.get("alt", "Nome não encontrado")
                if img_tag
                else "Nome não encontrado"
            )

            # Adicionamos apenas se tivermos um nome e um link
            if nome != "Nome não encontrado" and link:
                apoiadores.append({"nome": nome, "link": link})

        if apoiadores:
            print(f"✅ Encontrados {len(apoiadores)} apoiadores.")
        else:
            print("⚠️ Nenhum apoiador encontrado.")

        return {"apoiadores": apoiadores}

    except Exception as e:
        print(f"❌ ERRO ao raspar Apoiadores: {e}")
        return {"apoiadores": []}





# raspagem dos patriconadores 

def raspar_patrocinadores():
    """Raspa a lista de empresas patrocinadoras do programa."""
    print("💰 Raspando lista de Patrocinadores...")
    try:
        url = "https://www.jovemprogramador.com.br/patrocinadores.php"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        
        patrocinadores = []
        # A estrutura e classes são as mesmas, o que é ótimo!
        cards_patrocinadores = soup.find_all('a', class_='item-grid')

        for card in cards_patrocinadores:
            link = card.get('href', '')
            img_tag = card.find('img')
            
            nome = img_tag.get('alt', 'Nome não encontrado') if img_tag else 'Nome não encontrado'
            
            if nome != 'Nome não encontrado' and link:
                patrocinadores.append({"nome": nome, "link": link})
        
        if patrocinadores:
            print(f"✅ Encontrados {len(patrocinadores)} patrocinadores.")
        else:
            print("⚠️ Nenhum patrocinador encontrado.")
            
        return {"patrocinadores": patrocinadores}

    except Exception as e:
        print(f"❌ ERRO ao raspar Patrocinadores: {e}")
        return {"patrocinadores": []}






# dito isso, salvar tudo

def salvar_dados():
    print("\n🚀 Iniciando raspagem completa do site...")
    dados = {
        "sobre": raspar_sobre()["sobre"],
        "duvidas": raspar_duvidas()["duvidas"],
        "cidades": raspar_cidades()["cidades"],
        "noticias": raspar_noticias()["noticias"],
        "ser_professor": raspar_ser_professor()["ser_professor"],
        "hackathon": raspar_hackathon()["hackathon"],
        "redes_sociais": raspar_redes_sociais()["redes_sociais"],
        "apoiadores": raspar_apoiadores()["apoiadores"],
         "patrocinadores": raspar_patrocinadores()["patrocinadores"]  
    }

    with open("dados.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    print("\n✅ Dados atualizados e salvos com sucesso em 'dados.json'")


if __name__ == "__main__":
    salvar_dados()
