# ==================================================
# ARQUIVO DE BANCO DE DADOS DO RPG (dados_jogo.py)
# ==================================================

RARIDADES = {
    "Comum": {"cor": "\033[0m", "bonus": 0},            
    "Incomum": {"cor": "\033[32m", "bonus": 3},         
    "Raro": {"cor": "\033[34m", "bonus": 7},            
    "Épico": {"cor": "\033[35m", "bonus": 12},          
    "Lendário": {"cor": "\033[33m", "bonus": 20},       
    "Tesouro Nacional": {"cor": "\033[31;1;4m", "bonus": 35} 
}
RESET_COR = "\033[0m"

ARMAS = ["Espada Espacial", "Machado Rúnico", "Adaga Sombria", "Arco Élfico", "Cajado de Dragão"]
ARMADURAS = ["Escudo Relíquia", "Manto Arcano", "Cota de Mithril", "Elmo do Dragão", "Armadura de Placas"]
HABILIDADES_NOMES = ["Bola de Fogo", "Cura Divina", "Passo Sombrio", "Fúria do Deserto"]
CONSUMIVEIS = ["Poção de Vida", "Elixir de Mana", "Pergaminho Antigo", "Pedra de Amolar"]

ITENS_UNICOS = {
    "Excalibur": {
        "tipo": "arma",
        "raridade": "Tesouro Nacional",
        "bonus_forca": 25,
        "bonus_inteligencia": 0,
        "roubo_vida": 15,
        "taxa_critica": 20
    },
    "Escudo de Aegis": {
        "tipo": "armadura",
        "raridade": "Lendário",
        "bonus_resistencia": 30,
        "taxa_critica": 0,
        "bonus_forca": 0
    },
    "Olho de Odin": {
        "tipo": "habilidade",
        "raridade": "Tesouro Nacional",
        "bonus_inteligencia": 40,
        "taxa_critica": 0
    }
}

BANCO_INIMIGOS = {
    "Cobra Gigante (Black Snake)": {
        "vida": 25, "forca": 6, "resistencia": 4, "tipo": "normal",
        "descricao": "Criatura perigosa da caverna."
    },
    "Morcego Gigante (Evil Bat)": {
        "vida": 18, "forca": 4, "resistencia": 2, "tipo": "normal",
        "descricao": "Monstro local ótimo para testar suas habilidades."
    },
    "Centopeia Maldita (Evil Centipede)": {
        "vida": 22, "forca": 5, "resistencia": 5, "tipo": "normal",
        "descricao": "Inseto gigante da masmorra."
    },
    "Lobo Gigante Líder (Direwolf Boss)": {
        "vida": 50, "forca": 12, "resistencia": 8, "tipo": "boss",
        "descricao": "O primeiro grande rival da Floresta de Jura!"
    }
}
