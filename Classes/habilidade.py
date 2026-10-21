from __future__ import annotations
from dataclasses import dataclass, field
import uuid
from Dados.dados_jogo import RESET_COR

@dataclass
class Habilidade:
    # 1. Primeiro colocamos tudo que NÃO TEM valor padrão (obrigatórios)
    nome: str
    custo_mana: int
    tipo_magia: str  
    potencia_base: int  
    efeito: str      
    descricao: str
    
    # 2. Depois colocamos tudo que TEM valor padrão (opcionais)
    raridade: str = "Comum" 
    duracao: int = 3  
    nivel: int = 1         
    xp_atual: int = 0      
    xp_necessaria: int = 5 
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])

    @property
    def potencia(self) -> int:
        """A potência aumenta dinamicamente conforme o nível da habilidade sobe."""
        return self.potencia_base + (self.nivel - 1) * 3

    @property
    def barra_aprendizado(self) -> str:
        """Retorna o texto da barra de progresso (Ex: 40% [★★☆☆☆])."""
        porcentagem = int((self.xp_atual / self.xp_necessaria) * 100)
        estrelas = "★" * self.nivel + "☆" * (5 - self.nivel)
        return f"{porcentagem}% [Nível {self.nivel} {estrelas}]"

    def ganhar_xp(self) -> bool:
        """Adiciona 1 ponto de aprendizado. Retorna True se subir de nível."""
        self.xp_atual += 1
        if self.xp_atual >= self.xp_necessaria:
            self.xp_atual = 0
            self.nivel += 1
            self.xp_necessaria = int(self.xp_necessaria * 1.5)
            return True
        return False

    @property
    def nome_colorido(self) -> str:
        return f"\033[35m[Hab. Nv.{self.nivel}] {self.nome}{RESET_COR}"