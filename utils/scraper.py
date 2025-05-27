import requests
from bs4 import BeautifulSoup
import json
import re

def raspar_sobre():
    try:
        url = "https://www.jovemprogramador.com.br/sobre.php"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        secao_sobre = soup.find('div', class_='fh5co-heading')  
        
        if not secao_sobre:
            return {"sobre": "Informações não disponíveis."}

        textos = []
        for p in secao_sobre.find_all('p'):
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
        soup = BeautifulSoup(response.text, 'html.parser')
        duvidas = {}
        
        accordion = soup.find('div', class_='accordion')
        if not accordion:
            return {"duvidas": {}}
            
        itens_duvida = accordion.find_all('div', recursive=False)
        
        for item in itens_duvida:
            pergunta = item.find('h4').get_text(strip=True) if item.find('h4') else ""
            resposta_div = item.find('div', class_='collapse')
            resposta = resposta_div.find('p').get_text(strip=True) if resposta_div and resposta_div.find('p') else ""
            
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
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Encontra o parágrafo que começa com "Para a edição de"
        for p in soup.find_all('p'):
            if p.get_text(strip=True).startswith("Para a edição de"):
                # O próximo elemento <p> contém as cidades
                cidades_paragraph = p.find_next_sibling('p')
                if cidades_paragraph:
                    # Extrai o texto dentro da tag <strong>
                    cidades = cidades_paragraph.find('strong').get_text(strip=True)
                    return {"cidades": cidades}
        
        return {"cidades": "Lista de cidades não encontrada na página."}
    
    except Exception as e:
        print(f"Erro ao raspar cidades: {e}")
        return {"cidades": "Erro ao carregar lista de cidades."}

def salvar_dados():
    dados = {
        "sobre": raspar_sobre()["sobre"],
        "duvidas": raspar_duvidas()["duvidas"],
        "cidades": raspar_cidades()["cidades"]
    }
    
    with open('dados.json', 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    print("✅ Dados salvos em 'dados.json'")

if __name__ == "__main__":
    salvar_dados()