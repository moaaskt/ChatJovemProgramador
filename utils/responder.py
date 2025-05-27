import json
import re
from difflib import get_close_matches

class Responder:
    def __init__(self):
        with open('dados.json', 'r', encoding='utf-8') as f:
            self.dados = json.load(f)
    
    def buscar_resposta(self, pergunta):
        pergunta = pergunta.lower().strip()
        
        # 1. Verificar saudações
        resposta_saudacao = self.processar_saudacao(pergunta)
        if resposta_saudacao:
            return resposta_saudacao
            
        # 2. Comandos especiais
        if pergunta.startswith('/'):
            return self.processar_comando(pergunta)
            
        # 3. Busca por intenções específicas
        resposta = self.buscar_intencao(pergunta)
        if resposta:
            return resposta
            
        # 4. Busca nas dúvidas frequentes
        resposta = self.buscar_em_duvidas(pergunta)
        if resposta:
            return resposta
            
        # 5. Busca no texto "sobre"
        resposta = self.buscar_no_sobre(pergunta)
        if resposta:
            return resposta
            
        # 6. Fallback inteligente
        return self.fallback_inteligente(pergunta)

    def buscar_cidades(self):
        if "cidades" in self.dados:
            cidades = self.dados["cidades"]
            if isinstance(cidades, str):
                # Verifica se já está no formato completo
                if "Araranguá" in cidades:
                    return "📍 CIDADES PARTICIPANTES:\n" + cidades
                # Se for uma string incompleta, tenta formatar
                return "📍 CIDADES PARTICIPANTES:\n" + ", ".join([c.strip() for c in cidades.split(',')])
            elif isinstance(cidades, list):
                return "📍 CIDADES PARTICIPANTES:\n" + ", ".join(cidades)
        return "Não foi possível encontrar a lista de cidades participantes."

    def processar_saudacao(self, mensagem):
        saudacoes = {
            r'oi|olá|ola|eae|iai|saudações|hey|hello': "Olá! 🤖 Sou o assistente do Jovem Programador. Em que posso te ajudar hoje?",
            r'bom dia': "Bom dia! 🌞 Como posso te ajudar com o programa Jovem Programador?",
            r'boa tarde': "Boa tarde! ☀️ No que posso te auxiliar sobre o Jovem Programador?",
            r'boa noite': "Boa noite! 🌙 Em que posso ajudar com o programa Jovem Programador?"
        }
        
        for regex, resposta in saudacoes.items():
            if re.search(regex, mensagem, re.IGNORECASE):
                return resposta + "\n\n" + self.mostrar_sugestoes()
        return None

    def mostrar_sugestoes(self):
        sugestoes = [
            "Como faço para me inscrever?",
            "Quais cidades participam do programa?",
            "O curso é gratuito?",
            "Quem pode participar?",
            "Quando começam as aulas?"
        ]
        return "Você pode perguntar sobre:\n" + "\n".join([f"• {s}" for s in sugestoes]) + "\n\nOu digite /menu para ver todas opções."

    def processar_comando(self, comando):
        comandos = {
            '/sobre': self.formatar_sobre,
            '/cidades': self.formatar_cidades,
            '/ajuda': self.mostrar_ajuda
        }
        return comandos.get(comando, lambda: "Comando desconhecido. Digite /ajuda.")()

    def buscar_intencao(self, pergunta):
        intencoes = {
            r'sobre o programa|sobre|informações|programa': 'sobre',
            r'inscri|participar|matric|como entro|quero participar': 'Como faço para conseguir uma vaga?',
            r'cidades participantes|cidades|municípios|quais cidades|onde tem|locais': 'cidades',
            r'horas|duraç|meses|quanto tempo|semestres': 'Quantas horas têm o programa?',
            r'gratui|preço|pagamento|custo|valor|pagar': 'O programa tem algum custo?',
            r'online|remoto|distância|virtual|presencial': 'O curso será a distância?',
            r'idade|anos|velho|15|16|17': 'Quem pode participar?',
            r'começ|início|iniciar|quando começa': 'Quando começam as aulas?',
            r'experiência|conhecimento|saber|já programo': 'Não possuo experiência na área. Posso me inscrever?',
            r'estudando|escola|ensino médio|estudo': 'Preciso estar estudando para me inscrever?',
            r'vagas|limite|quantas pessoas|lotado': 'As vagas são limitadas?',
            r'turno|período|manhã|tarde|noite|horário': 'Em que período ocorrerão as aulas?'
        }
        
        for regex, pergunta_chave in intencoes.items():
            if re.search(regex, pergunta, re.IGNORECASE):
                if pergunta_chave == 'cidades':
                    return self.buscar_cidades()
                elif pergunta_chave == 'sobre':
                    return self.formatar_sobre()
                return self.dados["duvidas"].get(pergunta_chave, "Resposta não encontrada.")
        return None

    def buscar_em_duvidas(self, pergunta):
        pergunta = pergunta.lower()
        for perg_chave, resposta in self.dados["duvidas"].items():
            if pergunta in perg_chave.lower():
                return resposta
        
        palavras_chave = {
            'inscri': 'Como faço para conseguir uma vaga?',
            'gratui': 'O programa tem algum custo?',
            'cidade': 'Em que local acontecerá o curso?',
            'idade': 'Quem pode participar?',
            'começ': 'Quando começam as aulas?'
        }
        
        for palavra, pergunta_chave in palavras_chave.items():
            if palavra in pergunta:
                return self.dados["duvidas"].get(pergunta_chave, "Resposta não encontrada.")
        
        return None

    def buscar_no_sobre(self, pergunta):
        sobre = self.dados.get("sobre", "").lower()
        termos = {
            'senac': 'O curso é realizado em parceria com o Senac SC.',
            'empregabilidade': 'O foco do programa é a empregabilidade na área de TI.',
            'equipamento': 'Os alunos precisam ter acesso a equipamentos para as atividades práticas.',
            'hibrido': 'As aulas são no formato híbrido (presencial e virtual).',
            'seprosc': 'O programa é uma iniciativa do SEPROSC em parceria com o SENAC.'
        }
        
        for termo, resposta in termos.items():
            if termo in pergunta and termo in sobre:
                return resposta
        
        return None

    def fallback_inteligente(self, pergunta):
        sugestoes = [
            "Como faço para me inscrever?",
            "O programa é gratuito?",
            "Quais são as cidades participantes?"
        ]
        
        return ("Não entendi sua pergunta. Você pode:\n"
                "• Reformular sua pergunta\n"
                "• Digitar /menu para opções\n"
                "• Perguntar sobre:\n" + 
                "\n".join([f"  - {s}" for s in sugestoes]))

    def formatar_sobre(self):
        if "sobre" in self.dados:
            sobre = self.dados["sobre"]
            if isinstance(sobre, str):
                # Pega os primeiros 3 parágrafos não vazios
                paras = [p for p in sobre.split('\n\n') if p.strip()][:3]
                return "ℹ️ SOBRE O PROGRAMA:\n" + '\n\n'.join(paras)
        return "ℹ️ Informações sobre o programa não disponíveis."

    def formatar_cidades(self):
        return self.buscar_cidades()

    def mostrar_ajuda(self):
        return ("Comandos disponíveis:\n"
                "/sobre - Informações sobre o programa\n"
                "/cidades - Lista de cidades participantes\n"
                "/menu - Mostrar menu principal\n"
                "/sair - Encerrar o chat")