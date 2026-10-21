import random
import time
import os
from Classes.item import Item
from Classes.habilidade import Habilidade
from Classes.personagem import Jogador
from Dados.dados_jogo import (
    RARIDADES, ARMAS, ARMADURAS, CONSUMIVEIS, 
    BANCO_HABILIDADES, ITENS_UNICOS
)

def criar_item_por_raridade(raridade: str, nivel_mundo: int) -> Item | Habilidade:
    """Gera um item ou habilidade aleatória balanceada pelo nível do mundo."""
    # 30% de chance de vir um item ÚNICO predefinido se a raridade bater
    if raridade in ["Lendário", "Tesouro Nacional"] and random.randint(1, 100) <= 30:
        possiveis_unicos = [n for n, d in ITENS_UNICOS.items() if d["raridade"] == raridade]
        if possiveis_unicos:
            nome_unico = random.choice(possiveis_unicos)
            dados = ITENS_UNICOS[nome_unico]
            
            if dados["tipo"] == "habilidade":
                dados_hab = BANCO_HABILIDADES.get(nome_unico, {
                    "custo_mana": 10, "tipo": "Ataque", "potencia": 15, "efeito": "Nenhum", "descricao": ""
                })
                return Habilidade(
                    nome=f"⭐ {nome_unico} ⭐", custo_mana=dados_hab["custo_mana"], 
                    tipo_magia=dados_hab["tipo"], potencia=dados_hab["potencia"], 
                    efeito=dados_hab["efeito"], descricao=dados_hab["descricao"]
                )
            
            return Item(
                nome=f"⭐ {nome_unico} ⭐", tipo=dados["tipo"], raridade=dados["raridade"],
                bonus_forca=dados.get("bonus_forca", 0), bonus_resistencia=dados.get("bonus_resistencia", 0),
                bonus_inteligencia=dados.get("bonus_inteligencia", 0), roubo_vida=dados.get("roubo_vida", 0),
                taxa_critica=dados.get("taxa_critica", 0)
            )

    # Caso não seja um item único, sorteia uma categoria padrão
    tipo = random.choice(["arma", "armadura", "item", "habilidade"])
    
    if tipo == "arma":
        nome = random.choice(ARMAS)
    elif tipo == "armadura":
        nome = random.choice(ARMADURAS)
    elif tipo == "habilidade":
        nome = random.choice(list(BANCO_HABILIDADES.keys()))
        dados = BANCO_HABILIDADES[nome]
        return Habilidade(
            nome=nome, custo_mana=dados["custo_mana"], tipo_magia=dados["tipo"], 
            potencia=dados["potencia"], efeito=dados["efeito"], descricao=dados["descricao"]
        )
    else:
        nome = random.choice(CONSUMIVEIS)

    item = Item(nome=nome, tipo=tipo, raridade=raridade)
    b_raridade = RARIDADES.get(raridade, {"bonus": 0})["bonus"]
    
    # Adiciona escalonamento baseado no nível do mundo
    modificador_mundo = 1 + (nivel_mundo * 0.1)

    if tipo == "arma":
        item.bonus_forca = int((random.randint(3, 8) + b_raridade) * modificador_mundo)
        item.taxa_critica = int((random.randint(2, 6) + (b_raridade // 2)) * modificador_mundo)
        if b_raridade > 10: 
            item.roubo_vida = random.randint(3, 8)
    elif tipo == "armadura":
        item.bonus_resistencia = int((random.randint(4, 10) + b_raridade) * modificador_mundo)
    elif tipo == "item":
        item.bonus_inteligencia = int((random.randint(2, 6) + (b_raridade // 2)) * modificador_mundo)
        
    return item

def sortear_raridade(tipo_bau: str, jogador: Jogador, nivel_mundo: int) -> str:
    """Calcula a raridade final do baú baseado na sorte e nível do mundo."""
    sorteio = random.randint(1, 100) + nivel_mundo + jogador.sorte
    if tipo_bau == "Aventureiro":
        if sorteio <= 30: return "Raro"
        if sorteio <= 60: return "Épico"
        if sorteio <= 90: return "Lendário"
        return "Tesouro Nacional"
    else:
        if sorteio <= 45: return "Comum"
        if sorteio <= 75: return "Incomum"
        if sorteio <= 93: return "Raro"
        return "Épico"

def abrir_bau_roleta(tipo_bau: str, jogador: Jogador, nivel_mundo: int) -> Item | Habilidade:
    """Executa a animação gráfica da roleta no terminal e entrega a recompensa."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("==================================================")
    print(f" 🔑 ABRINDO: BAÚ DO {tipo_bau.upper()}... ")
    print("==================================================")
    time.sleep(0.4)
    
    raridade_final = sortear_raridade(tipo_bau, jogador, nivel_mundo)
    item_ganho = criar_item_por_raridade(raridade_final, nivel_mundo)
    
    # Animação simulada de roleta girando
    lista_animacao = list(RARIDADES.keys())
    for _ in range(8):
        os.system('cls' if os.name == 'nt' else 'clear')
        r_falsa = random.choice(lista_animacao)
        print("==================================================")
        print(f" 🎰 ROLETA [{tipo_bau.upper()}] 🎰 ")
        print(f"  GIRANDO: >>>> [{r_falsa}] <<<<")
        print("==================================================")
        time.sleep(0.08)
        
    os.system('cls' if os.name == 'nt' else 'clear')
    print("==================================================")
    print(" 🎉 RECOMPENSA CONQUISTADA! 🎉 ")
    print("==================================================")
    print(f"\n✨ Você obteve: {item_ganho.nome_colorido} !! ✨")
    
    if isinstance(item_ganho, Item):
        print(f"📦 Tipo: {item_ganho.tipo.capitalize()}")
    else:
        print(f"📦 Tipo: Habilidade ({item_ganho.tipo_magia})")
    print(f"🆔 ID Único: {item_ganho.id}")
    
    return item_ganho