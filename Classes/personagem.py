from __future__ import annotations
import random
from Classes.item import Item
from Classes.habilidade import Habilidade

class Jogador:
    def __init__(self, nome: str):
        self.nome: str = nome
        
        # Atributos Base (Sorteados no início)
        self.forca_base: int = random.randint(5, 12)
        self.inteligencia_base: int = random.randint(6, 15)
        self.resistencia_base: int = random.randint(4, 10)
        self.velocidade_base: int = random.randint(90, 110)
        
        # Atributos de Recursos
        self.vida_maxima: int = 80
        self.vida_atual: int = self.vida_maxima
        self.mana_maxima: int = 40
        self.mana_actual: int = self.mana_maxima
        self.sorte: int = random.randint(1, 10)
        
        # Controle de Estado e Equipamentos
        self.inventario: dict[str, Item | Habilidade] = {}
        self.equipados: dict[str, any] = {
            "arma": None,
            "armadura": None,
            "item": None,
            "habilidade_1": None,
            "habilidade_2": None,
            "habilidade_3": None
        }
        
        # Efeitos de Status Ativos no Combate
        self.status: dict[str, int] = {"veneno": 0, "paralisia": 0}

    def calcular_atributos(self) -> tuple[int, int, int, int, int, int]:
        """Calcula os status totais somando os equipamentos atuais."""
        f_total = self.forca_base
        r_total = self.resistencia_base
        i_total = self.inteligencia_base
        v_total = self.velocidade_base
        roubo_v = 0
        crit_c = 0
        
        if self.equipados["arma"]:
            f_total += self.equipados["arma"].bonus_forca
            roubo_v += self.equipados["arma"].roubo_vida
            crit_c += self.equipados["arma"].taxa_critica
        if self.equipados["armadura"]:
            r_total += self.equipados["armadura"].bonus_resistencia
        if self.equipados["item"]:
            i_total += self.equipados["item"].bonus_inteligencia
            
        return f_total, r_total, i_total, roubo_v, crit_c, v_total

    def obter_itens_filtrados_e_ordenados(self, tipo_filtro: str) -> list[tuple[str, any]]:
        """
        Filtra o inventário por tipo e ordena do mais raro para o mais comum.
        Retorna uma lista de tuplas contendo (id_unico, objeto_do_item).
        """
        ordem_prioridade = {
            "Tesouro Nacional": 6,
            "Lendário": 5,
            "Épico": 4,
            "Raro": 3,
            "Incomum": 2,
            "Comum": 1
        }
        
        itens_filtrados = []
        for idx, item in self.inventario.items():
            # Verifica se o item pertence à categoria buscada
            if tipo_filtro == "habilidade" and isinstance(item, Habilidade):
                itens_filtrados.append((idx, item))
            elif isinstance(item, Item) and item.tipo == tipo_filtro:
                itens_filtrados.append((idx, item))
                
        # Ordenação decrescente baseada no peso da raridade atribuída
        itens_filtrados.sort(
            key=lambda x: ordem_prioridade.get(x[1].raridade if hasattr(x[1], "raridade") else "Comum", 0), 
            reverse=True
        )
        return itens_filtrados


class Inimigo:
    def __init__(self, nome: str, dados_base: dict, nivel_mundo: int):
        self.nome: str = nome
        self.tipo: str = dados_base["tipo"]  # "normal" ou "boss"
        self.descricao: str = dados_base["descricao"]
        
        # Escalonamento dinâmico baseado no Nível do Mundo do jogo
        multiplicador = 1.0 + (nivel_mundo - 1) * 0.25
        
        self.vida_maxima: int = int(dados_base["vida"] * multiplicador)
        self.vida_atual: int = self.vida_maxima
        self.forca: int = int(dados_base["forca"] * multiplicador)
        self.resistencia: int = int(dados_base["resistencia"] * multiplicador)
        self.velocidade: int = dados_base.get("velocidade", 95)
        
        # Efeitos de Status Ativos no Combate
        self.status: dict[str, int] = {"veneno": 0, "paralisia": 0}