import time
import os
from Classes.personagem import Jogador
from Classes.item import Item
from Classes.habilidade import Habilidade
from Motores.combate import iniciar_combate
from Motores.roleta import abrir_bau_roleta

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

# Inicialização do Jogo
limpar_tela()
print("=== BEM-VINDO AO ADVENTURE CHRONICLES ===")
nome_player = input('Nome do seu personagem: ')

# Instancia o jogador (Atributos base são gerados via construtor da classe)
jogador = Jogador(nome_player)

# Dicionário de contexto global para evitar variáveis globais soltas
contexto_jogo = {
    "nivel_do_mundo": 1,
    "jogo_rodando": True
}

# Concede uma magia inicial garantida direto no inventário do jogador
magia_inicial = Habilidade(
    nome="Bola de Fogo", 
    custo_mana=12, 
    tipo_magia="Ataque", 
    potencia_base=15,
    efeito="Nenhum", 
    descricao="Dispara uma bola de fogo ardente em direção ao inimigo."
)
jogador.inventario[magia_inicial.id] = magia_inicial

print("\n1 - Iniciar Aventura\n2 - Sair do Jogo")
if input("Opção: ").strip() == "2":
    exit()

# Loop Principal do Jogo
while contexto_jogo["jogo_rodando"] and jogador.vida_atual > 0:

    # Calcula os atributos dinâmicos baseados no que está equipado
    f_t, r_t, i_t, roubo_t, crit_t, vel_t = jogador.calcular_atributos()
    
    limpar_tela()
    print(f"=== CAPÍTULO {contexto_jogo['nivel_do_mundo']:02d}: CAVERNAS E MASMORRAS ===")
    print(f"👤 Herói: {jogador.nome} | Nv. Mundo: {contexto_jogo['nivel_do_mundo']}")
    print(f"💪 Força: {f_t} | 🧠 Magia: {i_t} | 🛡️ Defesa: {r_t} | 跑 Vel: {vel_t}")
    print(f"❤️ Vida: {jogador.vida_atual}/{jogador.vida_maxima} | 🧪 Mana: {jogador.mana_actual}/{jogador.mana_maxima} | 🍀 Sorte: {jogador.sorte}%")
    print("=========================================================")
    print("1 - Abrir Mochila e Equipamentos")
    print("2 - Descansar no Acampamento (Restaurar HP/MP)")
    print("3 - Explorar Região (Procurar Batalha)")
    print("4 - Abrir um Baú Místico Grátis")
    print("5 - Salvar e Sair do Jogo")
    
    escolha = input("Sua opção: ").strip()
    
    # Abrir Mochila e Equipamentos
    if escolha == "1":
        mochila_ativa = True
        while mochila_ativa:
            limpar_tela()
            print("🎒 ======= MOCHILA DO AVENTUREIRO =======")
            print("Escolha uma categoria para filtrar:")
            print("1 - Ver Armas")
            print("2 - Ver Armaduras")
            print("3 - Ver Habilidades")
            print("4 - Ver Itens (Consumíveis)")
            print("5 - Voltar ao Menu Principal")
            print("=========================================")
            
            opcao_filtro = input("Sua opção: ").strip()
            tipo_filtrado = ""
            
            # Define o tipo de filtro baseado na escolha do jogador
            if opcao_filtro == "1":
                tipo_filtrado = "arma"
            elif opcao_filtro == "2":
                tipo_filtrado = "armadura"
            elif opcao_filtro == "3":
                tipo_filtrado = "habilidade"
            elif opcao_filtro == "4":
                tipo_filtrado = "item"
            elif opcao_filtro == "5":
                mochila_ativa = False
                continue
            else:
                print("\n❌ Opção inválida.")
                time.sleep(1)
                continue
                
            # Busca os itens já filtrados e ordenados por raridade
            itens_exibição = jogador.obter_itens_filtrados_e_ordenados(tipo_filtrado)
            
            filtrando = True
            while filtrando:
                limpar_tela()
                print(f"🎒 ======= FILTRO: {tipo_filtrado.upper()}S =======")
                
                if not itens_exibição:
                    print(f" Você não carrega nenhuma {tipo_filtrado} na mochila.")
                    print("-----------------------------------------")
                    input("\nPressione Enter para voltar às categorias...")
                    filtrando = False
                    continue
                    
                # Lista os itens usando SLOTS numéricos sequenciais (1, 2, 3)
                for slot_num, (idx_real, item) in enumerate(itens_exibição, start=1):
                    status_uso = ""
                    if tipo_filtrado in jogador.equipados and jogador.equipados[tipo_filtrado] == item:
                        status_uso = " [EM USO]"
                    print(f"Slot [{slot_num}] | {item.nome_colorido}{status_uso}")
                    if hasattr(item, "descricao") and item.descricao:
                        print(f"   ↳ {item.descricao}")
                print("-----------------------------------------")
                print("1 - Selecionar um item (Equipar)")
                print("2 - Voltar para as categorias")
                
                acao_filtro = input("Opção: ").strip()

                if acao_filtro == "1":
                    escolha_slot = input("Digite o número do SLOT do item: ").strip()
                    if escolha_slot.isdigit():
                        idx_slot = int(escolha_slot) - 1
                        if 0 <= idx_slot < len(itens_exibição):

                            # Resgata o ID único real do item selecionado pelo número do slot
                            id_real, item_selecionado = itens_exibição[idx_slot]
                            
                            if tipo_filtrado == "habilidade":
                                slots_hab = ["habilidade_1", "habilidade_2", "habilidade_3"]
                                
                                # Verifica se a habilidade já está equipada em algum slot
                                já_equipada = False
                                for s in slots_hab:
                                    if jogador.equipados[s] == item_selecionado:
                                        já_equipada = True
                                        break
                                
                                if já_equipada:
                                    print(f"\n❌ A habilidade {item_selecionado.nome} já está equipada!")
                                    time.sleep(1.5)
                                else:
                                    # Procura o primeiro slot de habilidade vazio disponível
                                    slot_vazio = None
                                    for s in slots_hab:
                                        if jogador.equipados[s] is None:
                                            slot_vazio = s
                                            break
                                    
                                    if slot_vazio:
                                        jogador.equipados[slot_vazio] = item_selecionado
                                        print(f"\n✅ {item_selecionado.nome} foi equipada no {slot_vazio.replace('_', ' ').capitalize()}!")
                                        time.sleep(1.5)
                                        filtrando = False  # Fecha o menu de slots e volta para as categorias
                                    else:
                                        # Força a substituição se todos os 3 slots de magia estiverem cheios
                                        print("\n⚠️ Seus slots de habilidade estão CHEIOS (3/3)!")
                                        print("Escolha qual habilidade deseja substituir:")
                                        print(f"1 - {jogador.equipados['habilidade_1'].nome}")
                                        print(f"2 - {jogador.equipados['habilidade_2'].nome}")
                                        print(f"3 - {jogador.equipados['habilidade_3'].nome}")
                                        print("0 - Cancelar")
                                        
                                        sub_op = input("Sua opção: ").strip()
                                        if sub_op in ["1", "2", "3"]:
                                            slot_alvo = f"habilidade_{sub_op}"
                                            antiga = jogador.equipados[slot_alvo].nome
                                            jogador.equipados[slot_alvo] = item_selecionado
                                            print(f"\n🔄 {antiga} foi substituída por {item_selecionado.nome}!")
                                            time.sleep(1.5)
                                            filtrando = False
                                        else:
                                            print("\nSubstituição cancelada.")
                                            time.sleep(1)
                                            
                            # --- FLUXO PARA EQUIPAMENTOS PADRÃO (ARMA, ARMADURA, ITEM) ---
                            else:
                                jogador.equipados[tipo_filtrado] = item_selecionado
                                print(f"\n✅ {item_selecionado.nome} foi equipado com sucesso!")
                                time.sleep(1.2)
                                filtrando = False
                        else:
                            print("\n❌ SLOT inválido.")
                            time.sleep(1)
                    else:
                        print("\n❌ Por favor, digite um número.")
                        time.sleep(1)
                elif acao_filtro == "2":
                    filtrando = False

    # --- DESCANSAR NO ACAMPAMENTO (RESTAURAÇÃO DE VIDA E MANA) ---
    elif escolha == "2":
        jogador.vida_atual = jogador.vida_maxima
        jogador.mana_actual = jogador.mana_maxima
        print("\n💤 Você montou acampamento. Vida e Mana totalmente restauradas!"); 
        time.sleep(1.2)
    # Iniciar combate
    elif escolha == "3":
        iniciar_combate(jogador, contexto_jogo)
    # abrir um baú místico grátis (Para teste)
    elif escolha == "4":
        item_sorteado = abrir_bau_roleta("Comum", jogador, contexto_jogo["nivel_do_mundo"])
        jogador.inventario[item_sorteado.id] = item_sorteado
        input("\nPressione Enter para continuar...")
    # Fim do Loop Principal
    elif escolha == "5":
        contexto_jogo["jogo_rodando"] = False
        print("\n👋 Obrigado por jogar! Até a próxima aventura.")