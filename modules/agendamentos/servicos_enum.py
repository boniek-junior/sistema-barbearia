import enum


class TipoServico(str, enum.Enum):
    CORTE = "corte"
    BARBA = "barba"
    CORTE_E_BARBA = "corte_e_barba"
    SOBRANCELHA = "sobrancelha"
    PINTURA = "pintura"
    PEZINHO = "pezinho"

    @property
    def duracao_minutos(self) -> int:
        return _DURACOES[self]

_DURACOES = {
    TipoServico.CORTE: 30,
    TipoServico.BARBA: 30,
    TipoServico.CORTE_E_BARBA: 70,
    TipoServico.SOBRANCELHA: 20,
    TipoServico.PINTURA: 60,
    TipoServico.PEZINHO: 15,
}