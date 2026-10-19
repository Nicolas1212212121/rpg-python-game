from __future__ import annotations  

from dataclasses import dataclass, field
import os
import random
import time 
import uuid

from Dados.dados_jogo import RARIDADES, RESET_COR, ARMAS, ARMADURAS, HABILIDADES_NOMES, CONSUMIVEIS, BANCO_INIMIGOS, ITENS_UNICOS #lembrar de sempre ter os importes no arquivo principal, caso contrario da erro de importação




def criar_item_por_raridade(raridade: str) -> Item:
    if raridade in ["Lendário", "Tesouro Nacional"] and random.randint(1, 100) <= 30:
        possiveis_unicos = [nome for nome, dados in ITENS_UNICOS.items() if dados["raridade"] == raridade]
        if possiveis_unicos:
            nome_unico = random.choice(possiveis_unicos)
            dados = ITENS_UNICOS[nome_unico]
            return Item(
                nome=f"⭐ {nome_unico} ⭐",
                tipo=dados["tipo"],
                raridade=dados["raridade"],
                bonus_forca=dados.get("bonus_forca", 0),
                bonus_resistencia=dados.get("bonus_resistencia", 0),
                bonus_inteligencia=dados.get("bonus_inteligencia", 0),
                roubo_vida=dados.get("roubo_vida", 0),
                taxa_critica=dados.get("taxa_critica", 0)
            )

    tipo = random.choice(["arma", "armadura", "item"])
    if tipo == "arma": 
        nome = random.choice(ARMAS)
    elif tipo == "armadura": 
        nome = random.choice(ARMADURAS)
    else: 
        nome = random.choice(CONSUMIVEIS)
        
    item = Item(nome=nome, tipo=tipo, raridade=raridade)
    todos_atributos = ["bonus_forca", "bonus_resistencia", "bonus_inteligencia", "roubo_vida", "taxa_critica"]

    if raridade in ["Comum", "Incomum"]:
        if tipo == "arma":
            item.bonus_forca = random.randint(3, 8)
            item.taxa_critica = random.randint(2, 6)
        elif tipo == "armadura":
            item.bonus_resistencia = random.randint(4, 10)
        elif tipo == "habilidade":
            item.bonus_inteligencia = random.randint(4, 10)
        else:
            item.bonus_inteligencia = random.randint(1, 4)
            
    elif raridade in ["Raro", "Épico", "Lendário", "Tesouro Nacional"]:
        multiplicador = 1.5 if raridade in ["Lendário", "Tesouro Nacional"] else 1.0
        if tipo == "arma":
            item.bonus_forca = int(random.randint(5, 12) * multiplicador)
            item.taxa_critica = int(random.randint(5, 15) * multiplicador)
            item.roubo_vida = int(random.randint(3, 10) * multiplicador)
        elif tipo == "armadura":
            item.bonus_resistencia = int(random.randint(6, 15) * multiplicador)
        elif tipo == "habilidade" or tipo == "item":
            item.bonus_inteligencia = int(random.randint(6, 15) * multiplicador)
            
    return item

def abrir_bau_roleta(tipo_bau: str):
    limpar_tela()
    print("==================================================")
    print(f"        🔑 ABRINDO: BAÚ DO {tipo_bau.upper()}...      ")
    print("==================================================")
    print("\nIniciando a roleta de recompensas...")
    time.sleep(0.5)

    lista_animacao = ["Comum", "Incomum", "Raro", "Épico", "Lendário", "Tesouro Nacional"]
    
    #Tipo do baú para o sorteio_calcular
    raridade_final = sortear_raridade(tipo_bau)
    item_ganho = criar_item_por_raridade(raridade_final)
    
    atraso_tempo = 0.04
    for i in range(15):
        limpar_tela()
        raridade_roleta = random.choice(lista_animacao)
        item_roleta = criar_item_por_raridade(raridade_roleta)
        print("==================================================")
        print(f"              🎰 ROLETA [{tipo_bau.upper()}] 🎰               ")
        print("==================================================")
        print(f"\n        GIRANDO:   >>>> {item_roleta.nome_colorido} <<<<")
        print("\n==================================================")
        time.sleep(atraso_tempo)
        atraso_tempo *= 1.15

    limpar_tela()
    print("==================================================")
    print("              🎉 RECOMPENSA CONQUISTADA! 🎉       ")
    print("==================================================")
    print(f"\n✨ Você obteve: {item_ganho.nome_colorido} !! ✨")
    print(f"📦 Tipo: {item_ganho.tipo.capitalize()}")
    print(f"🆔 ID Único: {item_ganho.id}")
    return item_ganho

def calcular_atributos():  
    forca_total = forca_base
    resistencia_total = resistencia_base
    inteligencia_total = inteligencia 
    velocidade_total = velocidade_base 
    roubo_vida_total = 0
    critico_total = 0
    
    if equipados["arma"]:
        forca_total += equipados["arma"].bonus_forca
        roubo_vida_total += equipados["arma"].roubo_vida
        critico_total += equipados["arma"].taxa_critica
        
    if equipados["armadura"]:
        resistencia_total += equipados["armadura"].bonus_resistencia

    if equipados["habilidade"]:
        inteligencia_total += equipados["habilidade"].bonus_inteligencia

    if equipados["item"]:
        inteligencia_total += equipados["item"].bonus_inteligencia
        
    return forca_total, resistencia_total, inteligencia_total, roubo_vida_total, critico_total, velocidade_total




@dataclass
class Item:
    nome: str
    tipo: str  
    raridade: str
    bonus_forca: int = 0
    bonus_resistencia: int = 0
    bonus_inteligencia: int = 0
    roubo_vida: int = 0          
    taxa_critica: int = 0         
    durabilidade_maxima: int = 5
    durabilidade_atual: int = 5
    custo_mana: int = 10
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])

    @property
    def nome_colorido(self) -> str:
        cor = RARIDADES.get(self.raridade, {"cor": "\033[0m"})["cor"]
        return f"{cor}[{self.raridade}] {self.nome}{RESET_COR}"

@dataclass
class Habilidade:
    nome: str # Nome da habilidade
    custo_mana: int # Custo de mana para usar a habilidade
    tipo: str      # Pode ser "Ataque", "Defesa", "Suporte", etc.
    descricao: str # Descrição detalhada da habilidade
    potencia: int = 0      # Potência do efeito ou dano
    efeito: str = "Nenhum" # Pode ser "Veneno", "Paralisia", "Cura", etc.
    duracao_base: int = 0   #tempo de duração do efeito em turnos
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    @property
    def nome_colorido(self) -> str:
        # Usa a cor roxa/magenta (\033[35m)
        return f"\033[35m[Habilidade] {self.nome}{RESET_COR}"


    
def limpar_tela(): 
    os.system('cls' if os.name == 'nt' else 'clear')

def sortear_raridade(tipo_bau: str) -> str:  #Baus lut
    global sorte, nivel_do_mundo
    sorteio = random.randint(1, 100 + nivel_do_mundo) + sorte
    
    if tipo_bau == "Aventureiro":
        if sorteio <= 40: return "Incomum"
        elif sorteio <= 75: return "Raro"
        elif sorteio <= 110: return "Épico"          
        elif sorteio <= 150: return "Lendário"       
        else: return "Tesouro Nacional"              
        
    else:
        # Baú Comum Roleta baseado no nivel do mundo e sorte do jogador
        if sorteio <= 50: return "Comum"         
        elif sorteio <= 85: return "Incomum"     
        elif sorteio <= 120: return "Raro"           
        elif sorteio <= 160: return "Épico"          
        elif sorteio <= 220: return "Lendário"       
        else: return "Tesouro Nacional"           

def iniciar_combate():
    global vida_atual, mana_atual, esquiva, vida_maxima
    
    # 1. Seleciona um inimigo aleatório do banco de inimigos
    nome_inimigo, dados = random.choice(list(BANCO_INIMIGOS.items()))
    inimigo_vida = dados["vida"]
    inimigo_forca = dados["forca"]
    inimigo_res = dados["resistencia"]
    
    # 2. Determina a velocidade do inimigo, com valor padrão caso não esteja definido
    inimigo_vel = dados.get("velocidade", 10) 
    
    # Calcula os atributos do jogador com base nos itens equipados
    forca_t, res_t, intel_t, roubo_t, crit_t, vel_t = calcular_atributos()
    jogador_vel = vel_t  
    
    # Efeitos de status
    status_jogador = {"veneno": 0, "paralisia": 0}
    status_inimigo = {"veneno": 0, "paralisia": 0}
    dano_veneno_fixo = 3
    
    # Calcula os tempos de ação (AV) iniciais para o jogador e inimigo
    av_jogador = 10000 / jogador_vel
    av_inimigo = 10000 / inimigo_vel
    
    limpar_tela()
    print("==================================================")
    print(f"⚔️ UM {nome_inimigo.upper()} EMBOSCOU VOCÊ!")
    print(f"📜 Descrição: {dados['descricao']}")
    print(f"🏃 Sua Velocidade: {jogador_vel} | 🏃 Vel. do Monstro: {inimigo_vel}")
    print("==================================================")
    time.sleep(2)
    
    # Ciclo de Combate baseado em Linha do Tempo
    while inimigo_vida > 0 and vida_atual > 0:
        # Determina quem age primeiro baseado no MENOR valor de AV atual
        if av_jogador <= av_inimigo:
            # --- TURNO DO JOGADOR ---
            tempo_passado = av_jogador
            av_inimigo -= tempo_passado # Avança a barra do inimigo pelo tempo decorrido
            av_jogador = 10000 / jogador_vel # Reseta o custo de ação do jogador para sua velocidade
            
            # Processa status no início do turno do jogador
            if status_jogador["veneno"] > 0:
                vida_atual -= dano_veneno_fixo
                print(f"\n🤢 Você sofreu {dano_veneno_fixo} de dano por Veneno! (Restam {status_jogador['veneno']} ações)")
                status_jogador["veneno"] -= 1
                if vida_atual <= 0: break
                time.sleep(1)
            
            defendendo = False
            limpar_tela()
            print("================== TURNO DO JOGADOR ==================")
            print(f"👹 {nome_inimigo} HP: {inimigo_vida} | [AV Próximo Ataque: {int(av_inimigo)}]")
            print(f"💖 Seu HP: {vida_atual}/{vida_maxima} | 🧪 Mana: {mana_atual}/{mana_maxima}")
            print("======================================================")
            print("1 - Ataque Físico")
            print("2 - Usar Habilidade")
            print("3 - Defender (Reduz dano recebido)")
            print("4 - Tentar Recuar")
            opcao_luta = input("Escolha sua ação: ")
            
            if opcao_luta == "1":
                dano = max(2, forca_t - inimigo_res)
                if random.randint(1, 100) <= crit_t:
                    dano *= 2
                    print("\n🎯 CRÍTICO! Dano duplicado!")
                inimigo_vida -= dano
                print(f"💥 Você causou {dano} de dano físico!")
                if roubo_t > 0:
                    cura = max(1, (dano * roubo_t) // 100)
                    vida_atual = min(vida_maxima, vida_atual + cura)
                    print(f"🧛 Roubo de Vida: Recuperou {cura} de HP.")
                    
            elif opcao_luta == "2":
                skills_disponiveis = [item for item in inventario.values() if item.tipo == "habilidade"][:3]
                if not skills_disponiveis:
                    print("\n❌ Você não possui nenhuma habilidade na mochila!")
                    input("Pressione Enter para voltar e escolher outra ação...")
                    av_jogador = 0 # Devolve o turno de graça para ele escolher de novo
                    continue
                    
                print("\n🔮 --- SEU GRIMÓRIO DE HABILIDADES ---")
                for idx, skill in enumerate(skills_disponiveis, start=1):
                    print(f"  {idx} - {skill.nome_colorido} (Custo: {skill.custo_mana} Mana)")
                print("  0 - Voltar")
                
                escolha_skill = input("Escolha a habilidade: ").strip()
                if escolha_skill == "0" or not escolha_skill.isdigit():
                    av_jogador = 0
                    continue
                    
                idx_skill = int(escolha_skill) - 1
                if 0 <= idx_skill < len(skills_disponiveis):
                    skill_usada = skills_disponiveis[idx_skill]
                    if mana_atual >= skill_usada.custo_mana:
                        mana_atual -= skill_usada.custo_mana
                        dano_magico = max(5, intel_t + skill_usada.bonus_inteligencia - inimigo_res)
                        inimigo_vida -= dano_magico
                        print(f"\n✨ Você conjurou {skill_usada.nome} e causou {dano_magico} de dano mágico!")
                        
                        # Aplica os turnos de efeito usando a propriedade duracao_base da classe nova
                        if getattr(skill_usada, 'duracao_base', 0) > 0:
                            efeito_nome = skill_usada.efeito.lower()
                            if efeito_nome in status_inimigo:
                                status_inimigo[efeito_nome] = skill_usada.duracao_base
                                print(f"🟢 {nome_inimigo} recebeu o efeito [{skill_usada.efeito}] por {skill_usada.duracao_base} turnos de ação!")
                    else:
                        print("\n❌ Mana insuficiente!")
                        input("Pressione Enter para voltar...")
                        av_jogador = 0
                        continue
                else:
                    av_jogador = 0
                    continue
                    
            elif opcao_luta == "3":
                defendendo = True
                print("\n🛡️ Você ergueu sua guarda até sua próxima ação!")
                
            else:
                if random.randint(1, 100) <= jogador_vel * 5:
                    print("\n🏃 Você conseguiu recuar do combate em segurança!")
                    time.sleep(1)
                    return
                print("\n❌ Falhou ao tentar recuar!")
                
            input("\nPressione Enter para continuar a linha do tempo...")
            
        else:
            # --- TURNO DO INIMIGO ---
            tempo_passado = av_inimigo
            av_jogador -= tempo_passado # Avança a barra do jogador pelo tempo decorrido
            av_inimigo = 10000 / inimigo_vel # Reseta o custo de ação do inimigo para sua velocidade
            
            # Processa status no início do turno do inimigo
            if status_inimigo["veneno"] > 0:
                inimigo_vida -= dano_veneno_fixo
                print(f"\n🤢 O {nome_inimigo} sofreu {dano_veneno_fixo} de dano por Veneno! (Restam {status_inimigo['veneno']} ações)")
                status_inimigo["veneno"] -= 1
                if inimigo_vida <= 0: break
                time.sleep(1)
                
            print(f"\n🥊 O {nome_inimigo} está agindo! [AV Próximo Ataque: {int(av_inimigo)}]")
            time.sleep(1)
            
            # Ataque do inimigo
            dano_sofrido = max(1, inimigo_forca - (res_t // 3))
            if 'defendendo' in locals() and defendendo:
                dano_sofrido = max(1, dano_sofrido // 2)
                print("🛡️ Guarda erguida! O dano do monstro foi reduzido pela metade!")
            
            vida_atual -= dano_sofrido
            print(f"💥 O monstro causou {dano_sofrido} de dano em você.")
            input("\nPressione Enter para continuar a linha do tempo...")

    # Resultado do combate
    limpar_tela()
    if vida_atual <= 0:
        print("💀 Você foi derrotado... Fim de jogo.")
        time.sleep(2)
        exit()
    else:
        print("==================================================")
        print(f"🏆 VITÓRIA! O {nome_inimigo} foi derrotado!")
        print("==================================================")
        
        if dados["tipo"] == "boss":
            print("\n👑 IMPRESSIONANTE! Você derrotou um CHEFE da floresta!")
            print("🎁 Você recebeu um: [BAÚ DO AVENTUREIRO]!")
            input("\nPressione Enter para girar o Baú de Chefe...")
            item_sorteado = abrir_bau_roleta("Aventureiro")
        else:
            print("\n⚔️ Limpeza concluída na masmorra!")
            print("🎁 Você recebeu um: [BAÚ COMUM]!")
            input("\nPressione Enter para girar o Baú Comum...")
            item_sorteado = abrir_bau_roleta("Comum")
            
        inventario[item_sorteado.id] = item_sorteado
        input("\nPressione Enter para retornar ao menu...")

        print("==================================================")
        print(f"🏆 VITÓRIA! O {nome_inimigo} foi derrotado!")
        print("==================================================")
        if dados["tipo"] == "boss":
            print("\n👑 IMPRESSIONANTE! Você derrotou um CHEFE da floresta!")
            print("🎁 Você recebeu um: [BAÚ DO AVENTUREIRO]!")
            input("\nPressione Enter para girar o Baú de Chefe...")
            item_sorteado = abrir_bau_roleta("Aventureiro")
        else:
            print("\n⚔️ Limpeza concluída na masmorra!")
            print("🎁 Você recebeu um: [BAÚ COMUM]!")
            input("\nPressione Enter para girar o Baú Comum...")
            item_sorteado = abrir_bau_roleta("Comum")
            inventario[item_sorteado.id] = item_sorteado
            input("\nPressione Enter para retornar ao menu...")

# Start do mundo
print("=== BEM-VINDO AO MUNDO ===")
nome_personagem = input('Nome do seu personagem: ')

# Inicialização de atributos do jogador randomizados
forca_base = random.randint(1, 15)
inteligencia = random.randint(1, 20)
vida_maxima = random.randint(20, 40)
vida_atual = vida_maxima
mana_maxima = random.randint(20, 50)
mana_atual = mana_maxima
resistencia_base = random.randint(1, 20)
esquiva = random.randint(1, 10)
sorte = random.randint(1, 20)
velocidade_base = random.randint(90, 110) 
forca_total = forca_base
resistencia_total = resistencia_base
nivel_do_mundo = 1

inventario = {}
# Slot de player
equipados = {"arma": None, "armadura": None, "habilidade": None, "item": None}

print("Escolha 1 ou 2\n1 - Continuar\n2 - Sair do Jogo")
if input("Sua opção: ") == "2": exit()
limpar_tela()

#inicio da aventura
jogo_rodando = True
while jogo_rodando and vida_atual > 0:
    forca_total, resistencia_total, inteligencia_total, roubo_vida_total, critico_total, velocidade_total = calcular_atributos()
    
    print("=== PRIMEIRA CAPTULO 01 ===")
    print("======== CAVERNA =======")
    time.sleep(2)
    limpar_tela()
    print(f"\n--- [STATUS ATRIBUÍDOS] ---")
    print(f"💪 Força: {forca_total} (Base: {forca_base}) | 🧠 Inteligência: {inteligencia_total}")
    print(f"🛡️ Resistência: {resistencia_total} | ❤️ Vida: {vida_atual}/{vida_maxima}")
    print(f"🧪 Mana do Jogador: {mana_atual}/{mana_maxima} | 🏃 Velocidade: {velocidade_total}")
    print(f"💨 Esquiva: {esquiva}% | 🍀 Sorte: {sorte}%")
    print(f"🧛 Roubo de Vida: {roubo_vida_total}% | 🎯 Chance Crítico: {critico_total}%")
    print("=========================================\n")
    print("O que você quer fazer?")
    print("1 - Abrir Mochila / Equipar Itens")
    print("2 - Descansar um pouco")
    print("3 - Sair do jogo")
    print("4 - Abrir um Baú Místico (Roleta)")
    print("5 - Explorar Floresta (Procurar Luta)")
    
    escolha = input("Sua opção: ")
    limpar_tela()
    
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
            if opcao_filtro == "1": tipo_filtrado = "arma"
            elif opcao_filtro == "2": tipo_filtrado = "armadura"
            elif opcao_filtro == "3": tipo_filtrado = "habilidade"
            elif opcao_filtro == "4": tipo_filtrado = "item"
            elif opcao_filtro == "5":
                mochila_ativa = False
                continue
            else:
                print("\n❌ Opção inválida.")
                time.sleep(1)
                continue
            
            
            itens_filtrados = [item for item in inventario.values() if item.tipo == tipo_filtrado]
            
            filtrando = True
            while filtrando:
                limpar_tela()
                print(f"🎒 ======= FILTRO: {tipo_filtrado.upper()}S =======")
                
                if not itens_filtrados:
                    print(f"   Você não carrega nenhuma {tipo_filtrado} na mochila.")
                    print("-----------------------------------------")
                    input("\nPressione Enter para voltar às categorias...")
                    filtrando = False
                    continue
                
                
                for indice, item in enumerate(itens_filtrados, start=1):
                    status_uso = " [EM USO]" if item in equipados.values() else ""
                    print(f"📦 SLOT: {indice} | {item.nome_colorido}{status_uso}")
                print("-----------------------------------------")
                
                print("O que deseja fazer?")
                print("1 - Selecionar um item (Equipar / Ver Detalhes)")
                print("2 - Voltar para as categorias")
                acao_filtro = input("Opção: ").strip()
                
                if acao_filtro == "1":
                    escolha_slot = input("Digite o número do SLOT do item: ").strip()
                    
                    if escolha_slot.isdigit() and 1 <= int(escolha_slot) <= len(itens_filtrados):
                        item_selecionado = itens_filtrados[int(escolha_slot) - 1]
                        
                        
                        detalhes_ativos = True
                        while detalhes_ativos:
                            limpar_tela()
                            print("🔍 ======= DETALHES DO EQUIPAMENTO =======")
                            print(f"📝 Nome: {item_selecionado.nome_colorido}")
                            print(f"📦 Categoria: {item_selecionado.tipo.capitalize()}")
                            print(f"⭐ Raridade: {item_selecionado.raridade}")
                            print("\n📊 ATRIBUTOS:")
                            print(f"  • Bônus de Força: +{item_selecionado.bonus_forca}")
                            print(f"  • Bônus de Defesa: +{item_selecionado.bonus_resistencia}")
                            print(f"  • Bônus de Magia: +{item_selecionado.bonus_inteligencia}")
                            print(f"  • Roubo de Vida: {item_selecionado.roubo_vida}%")
                            print(f"  • Chance de Crítico: {item_selecionado.taxa_critica}%")
                            
                            if item_selecionado.tipo == "item":
                                print(f"  • Durabilidade: {item_selecionado.durabilidade_atual}/{item_selecionado.durabilidade_maxima}")
                            if item_selecionado.tipo == "habilidade":
                                print(f"  • Custo de Mana: {item_selecionado.custo_mana} MP")
                            print("-----------------------------------------")
                            
                            print("1 - Equipar este item")
                            print("2 - Voltar à lista")
                            decisao = input("Escolha uma ação: ").strip()
                            
                            if decisao == "1":
                                
                                equipados[item_selecionado.tipo] = item_selecionado
                                print(f"\n✅ {item_selecionado.nome_colorido} foi equipado com sucesso!")
                                time.sleep(1.5)
                                detalhes_ativos = False
                                filtrando = False
                            elif decisao == "2":
                                detalhes_ativos = False
                    else:
                        print("\n❌ SLOT inválido.")
                        time.sleep(1)
                elif acao_filtro == "2":
                    filtrando = False
        limpar_tela()
    elif escolha == "2":
        vida_atual = min(vida_maxima, vida_atual + 10)
        mana_atual = min(mana_maxima, mana_atual + 15)
        print("\n💤 Você montou acampamento e recuperou 10 pontos de vida!")
        input("\nPressione Enter para continuar...")
        
    elif escolha == "3":
        jogo_rodando = False
        
    elif escolha == "4":
        item_sorteado = abrir_bau_roleta("Comum")
        inventario[item_sorteado.id] = item_sorteado
        input("\nPressione Enter para continuar...")
        
    elif escolha == "5":
        iniciar_combate()




#Coisas para fazer ou melhorar 
#Qualdade de vida: ok até
#Mosntros: ta muito ruim
#Combate: minimamente aceitavel (Ruim)
#Magia: muito ruim
#Lore: inexistente
#Bau: meio ruim
#Nivel do mundo: inexistente
#Dificuldade: fácil


#talvez fazer porque estou com preguiça
#Liga
#Mob lot unic
#craft
#Mesclar magia
#Combo de magia
#Fraquesa de inimigo
#Parte tecnica da magia

