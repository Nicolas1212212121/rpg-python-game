from __future__ import annotations
from dataclasses import dataclass, field
import uuid
from Dados.dados_jogo import RESET_COR

def gerar_id_curto() -> str:
    return str(uuid.uuid4())[:8]

@dataclass
class Habilidade:
    nome: str
    custo_mana: int
    tipo_magia: str  # Armazena se é "Ataque", "Efeito", "Passiva", etc.
    potencia: int
    efeito: str      # Ex: "Veneno", "Cura", "Paralisia", "Nenhum"
    descricao: str
    id: str = field(default_factory=gerar_id_curto)

    @property
    def nome_colorido(self) -> str:
        return f"\033[35m[Habilidade] {self.nome}{RESET_COR}"