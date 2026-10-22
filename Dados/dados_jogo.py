
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

# ==========================================
# LOCALIZAÇÃO: Dados/dados_jogo.py
# ==========================================
BANCO_HABILIDADES = {
    # Comum ---
    "Bola de Fogo": {
        "custo_mana": 12, "tipo": "Ataque", "potencia": 15, "efeito": "Nenhum",
        "raridade": "Comum", "duracao_base": 3,
        "descricao": "Dispara uma bola de fogo ardente contra o inimigo."
    },
    "Ondas Ultrassônicas": {
        "custo_mana": 10, "tipo": "Ataque", "potencia": 10, "efeito": "Atordoamento",
        "raridade": "Comum", "duracao_base": 1,
        "descricao": "Emite ondas sonoras de alta frequência que perturbam o inimigo."
    },
    "Teias Pegajosas": {
        "custo_mana": 10, "tipo": "Efeito", "potencia": 0, "efeito": "Lentidão",
        "raridade": "Comum", "duracao_base": 3,
        "descricao": "Dispara teias viscosas que reduzem a velocidade de ação inimiga."
    },
    "Percepção de Calor": {
        "custo_mana": 0, "tipo": "Passiva", "potencia": 0, "efeito": "Rastrear",
        "raridade": "Comum", "duracao_base": 99,
        "descricao": "Permite enxergar assinaturas térmicas, anulando camuflagens."
    },

    # --- INCOMUNS (Intermediárias) ---
    "Cura Divina": {
        "custo_mana": 15, "tipo": "Efeito", "potencia": 12, "efeito": "Cura",
        "raridade": "Incomum", "duracao_base": 1,
        "descricao": "Evoca luz sagrada para restaurar os pontos de vida."
    },
    "Voar/Planar": {
        "custo_mana": 5, "tipo": "Passiva", "potencia": 8, "efeito": "Esquiva",
        "raridade": "Incomum", "duracao_base": 3,
        "descricao": "Permite pairar no ar, tornando os ataques inimigos difíceis de acertar."
    },

    # --- RARAS (Difíceis) ---
    "Passo Sombrio": {
        "custo_mana": 8, "tipo": "Passiva", "potencia": 5, "efeito": "Esquiva",
        "raridade": "Raro", "duracao_base": 3,
        "descricao": "Move-se pelas sombras, aumentando a agilidade temporariamente."
    },
    "Fios Resistentes": {
        "custo_mana": 12, "tipo": "Efeito", "potencia": 6, "efeito": "Prender",
        "raridade": "Raro", "duracao_base": 2,
        "descricao": "Cria linhas de aço quase invisíveis para restringir o alvo."
    },
    "Sopro Venenoso": {
        "custo_mana": 18, "tipo": "Ataque", "potencia": 14, "efeito": "Veneno",
        "raridade": "Raro", "duracao_base": 3,
        "descricao": "Dispara um jato corrosivo que drena a vida a cada turno."
    },

    # --- ÉPICAS (Muito Difíceis) ---
    "Fúria do Deserto": {
        "custo_mana": 20, "tipo": "Ataque", "potencia": 22, "efeito": "Nenhum",
        "raridade": "Épico", "duracao_base": 3,
        "descricao": "Invoca uma tempestade de areia cortante."
    },
    "Armadura Corporal": {
        "custo_mana": 0, "tipo": "Passiva", "potencia": 10, "efeito": "Defesa",
        "raridade": "Épico", "duracao_base": 99,
        "descricao": "Endurece a pele como escamas de dragão, aumentando a resistência física."
    },

    # --- LENDÁRIAS (Extremamente Raras) ---
    "Sopro de Paralisia": {
        "custo_mana": 15, "tipo": "Efeito", "potencia": 5, "efeito": "Paralisia",
        "raridade": "Lendário", "duracao_base": 2,
        "descricao": "Expele uma névoa roxa com alta chance de paralisar o oponente."
    }
}

