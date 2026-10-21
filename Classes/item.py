from __future__ import annotations
from dataclasses import dataclass, field
import uuid
from Dados.dados_jogo import RARIDADES, RESET_COR

@dataclass
class Item:
    nome: str
    tipo: str  # "arma", "armadura", "item" (consumível)
    raridade: str
    bonus_forca: int = 0
    bonus_resistencia: int = 0
    bonus_inteligencia: int = 0
    roubo_vida: int = 0
    taxa_critica: int = 0
    durabilidade_maxima: int = 5
    durabilidade_atual: int = 5
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])

    @property
    def nome_colorido(self) -> str:
        # Puxa dinamicamente a cor configurada na sua pasta Dados
        cor = RARIDADES.get(self.raridade, {"cor": "\033[0m"})["cor"]
        return f"{cor}[{self.raridade}] {self.nome}{RESET_COR}"