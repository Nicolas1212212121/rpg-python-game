# ==========================================
# LOCALIZAÇÃO: Motores/combate.py
# ==========================================
import random
import time
import os
from Classes.personagem import Jogador, Inimigo
from Classes.habilidade import Habilidade
from Classes.item import Item
from Motores.roleta import abrir_bau_roleta
from Dados.dados_jogo import BANCO_INIMIGOS

def iniciar_combate(jogador: Jogador, contexto_jogo: dict):
    """Executa o loop de combate por tempo de ação (AV) corrigido contra travamentos."""
    nome_inimigo, dados = random.choice(list(BANCO_INIMIGOS.items()))
    inimigo = Inimigo(nome_inimigo, dados, contexto_jogo["nivel_do_mundo"])
    
    f_t, r_t, intel_t, roubo_t, crit_t, vel_t = jogador.calcular_atributos()

    
    # Valores iniciais da Linha do Tempo (Action Value)
    av_jogador = 10000 / vel_t
    av_inimigo = 10000 / inimigo.velocidade
    
    defendendo = False

    os.system('cls' if os.name == 'nt' else 'clear')
    print("==================================================")
    print(f"⚔️ UM {inimigo.nome.upper()} EMBOSCOU VOCÊ!")
    print(f"📜 Descrição: {inimigo.descricao}")
    print(f"🏃 Sua Velocidade: {vel_t} | 🏃 Vel. do Monstro: {inimigo.velocidade}")
    print("==================================================")
    time.sleep(2.5)

    # Loop de Combate Seguro
    while inimigo.vida_atual > 0 and jogador.vida_atual > 0:
        if av_jogador <= av_inimigo:
            # --- TURNO DO JOGADOR ---
            # Avança o tempo do inimigo e reseta o custo do jogador de forma limpa
            av_inimigo -= av_jogador
            av_jogador = 10000 / vel_t
            defendendo = False
            
            if jogador.status["paralisia"] > 0:
                print("\n⚡ Você está paralisado e perdeu sua oportunidade de ação!")
                jogador.status["paralisia"] -= 1
                time.sleep(1.2)
                continue
                
            if jogador.status["veneno"] > 0:
                jogador.vida_atual -= 4
                print("\n🤢 Você sofreu 4 de dano por Veneno residual!")
                jogador.status["veneno"] -= 1
                if jogador.vida_atual <= 0: 
                    break

            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"================== TURNO DO JOGADOR ==================")
            print(f"👹 {inimigo.nome} HP: {inimigo.vida_atual}/{inimigo.vida_maxima}")
            print(f"💖 Seu HP: {jogador.vida_atual}/{jogador.vida_maxima} | 🧪 Mana: {jogador.mana_actual}/{jogador.mana_maxima}")
            print("======================================================")
            print("1 - Ataque Físico\n2 - Usar Habilidade\n3 - Defender\n4 - Tentar Recuar")
            
            opcao = input("Escolha sua ação: ").strip()
            
            if opcao == "1":
                dano = max(2, f_t - inimigo.resistencia)
                if random.randint(1, 100) <= crit_t:
                    dano *= 2
                    print("\n🎯 GOLPE CRÍTICO!")
                inimigo.vida_atual -= dano
                print(f"💥 Você causou {dano} de dano físico!")
                
                if roubo_t > 0:
                    cura = (dano * roubo_t) // 100
                    jogador.vida_atual = min(jogador.vida_maxima, jogador.vida_atual + cura)
                    print(f"🧛 Roubo de Vida recuperou +{cura} HP.")
                input("\nPressione Enter...")
                
            elif opcao == "2":
                # NOVO: Puxa APENAS as 3 habilidades que estão equipadas nos slots ativos do jogador
                slots_hab = ["habilidade_1", "habilidade_2", "habilidade_3"]
                skills_equipadas = [jogador.equipados[s] for s in slots_hab if jogador.equipados[s] is not None]
                
                if not skills_equipadas:
                    print("\n❌ Você não tem nenhuma habilidade equipada em seus slots ativos!")
                    # Retorna o turno sem descontar tempo
                    av_jogador = 0 
                    input("\nPressione Enter...")
                    continue
                
                print("\n🔮 --- SKILLS EQUIPADAS (SLOTS) ---")
                for i, sk in enumerate(skills_equipadas, start=1):
                    print(f" {i} - {sk.nome_colorido} (Custo: {sk.custo_mana} MP) -> {sk.descricao}")
                print(" 0 - Voltar")
                
                escolha_s = input("Escolha: ").strip()
                if escolha_s == "0" or not escolha_s.isdigit() or int(escolha_s) > len(skills_equipadas):
                    av_jogador = 0
                    continue
                    
                skill_usada = skills_equipadas[int(escolha_s) - 1]
                if jogador.mana_actual >= skill_usada.custo_mana:
                    jogador.mana_actual -= skill_usada.custo_mana
                    
                    if skill_usada.tipo_magia == "Ataque":
                        dano_m = max(4, skill_usada.potencia + (intel_t // 2) - inimigo.resistencia)
                        inimigo.vida_atual -= dano_m
                        print(f"\n✨ {skill_usada.nome} conjurado! Causou {dano_m} de dano mágico.")
                        if skill_usada.efeito == "Veneno":
                            inimigo.status["veneno"] = 3
                            print(f"🟢 {inimigo.nome} começou a passar mal com efeito de Veneno!")
                            
                    elif skill_usada.tipo_magia == "Efeito" and skill_usada.efeito == "Cura":
                        cura_m = skill_usada.potencia + (intel_t // 3)
                        jogador.vida_atual = min(jogador.vida_maxima, jogador.vida_atual + cura_m)
                        print(f"\n💚 Luz da cura! Você restaurou {cura_m} de vida.")
                else:
                    print("\n❌ Pontos de mana insuficientes!")
                    av_jogador = 0
                input("\nEnter para continuar...")
                
            elif opcao == "3":
                defendendo = True
                print("\n🛡️ Você levantou sua defesa para mitigar danos.")
                input("\nEnter...")
                
            elif opcao == "4":
                if random.randint(1, 100) <= 45:
                    print("\n🏃 Escape bem-sucedido!"); return
                print("\n❌ Falhou na tentativa de fuga!"); input()
        else:
            # --- TURNO DO INIMIGO ---
            # Avança o tempo do jogador de forma limpa e reseta o do monstro
            av_jogador -= av_inimigo
            av_inimigo = 10000 / inimigo.velocidade
            
            if inimigo.status["veneno"] > 0:
                inimigo.vida_atual -= 4
                print(f"\n🤢 O {inimigo.nome} sofreu 4 de dano por Veneno!")
                inimigo.status["veneno"] -= 1
                if inimigo.vida_atual <= 0: 
                    break

            print(f"\n🥊 O {inimigo.nome} está agindo na linha do tempo!")
            time.sleep(1.0)
            
            dano_s = 0
            # IA Baseada no Banco de Dados
            if inimigo.tipo == "boss" and random.randint(1, 100) <= 40:
                print("🔥 O Líder usou [FÚRIA DO DESERTO]!")
                dano_s = max(4, 22 - (r_t // 3))
            elif "Cobra" in inimigo.nome and random.randint(1, 100) <= 35:
                print("🐍 A Cobra executou o [SOPRO VENENOSO]!")
                dano_s = max(2, 14 - (r_t // 3))
                jogador.status["veneno"] = 3
            elif "Bat" in inimigo.nome and random.randint(1, 100) <= 35:
                print("🦇 O Morcego disparou [ONDAS ULTRASSÔNICAS]!")
                dano_s = max(1, 10 - (r_t // 3))
                if random.randint(1, 100) <= 50: 
                    jogador.status["paralisia"] = 1
            else:
                dano_s = max(1, inimigo.forca - (r_t // 3))
                print(f"💥 O monstro acertou um golpe comum!")

            if defendendo:
                dano_s = max(1, dano_s // 2)
                print("🛡️ Golpe amortecido pela guarda erguida!")
                
            jogador.vida_atual -= dano_s
            print(f"💔 Você sofreu {dano_s} de dano.")
            input("\nPressione Enter para avançar o tempo...")

    # Fim da Batalha
    os.system('cls' if os.name == 'nt' else 'clear')
    if jogador.vida_atual <= 0:
        print("💀 Você foi derrotado no combate... Fim de jogo.")
        time.sleep(2)
        exit()
    else:
        print("==================================================")
        print(f"🏆 VITÓRIA! O {inimigo.nome} FOI ELIMINADO!")
        print("==================================================")
        
        if inimigo.tipo == "boss":
            contexto_jogo["nivel_do_mundo"] += 1
            print(f"👑 INCRÍVEL! A dificuldade global subiu! Nível de Mundo: {contexto_jogo['nivel_do_mundo']}!")
            bau_t = "Aventureiro"
        else:
            bau_t = "Comum"
            
        item_sorteado = abrir_bau_roleta(bau_t, jogador, contexto_jogo["nivel_do_mundo"])
        jogador.inventario[item_sorteado.id] = item_sorteado
        input("\nEnter para retornar ao menu principal...")
