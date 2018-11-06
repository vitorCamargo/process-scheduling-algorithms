"""
 Este arquivo contém todas as funções auxiliares utilizadas pelos escalonadores.
"""
import operator

# Verifica se todas as execuções já acabaram
# Parâmetros: lista de BCPs
# Retorno: 0 -> Ainda há execuções / 1 -> Execuções terminadas
def verifica_fim(lista_bcp):
    for bcp in lista_bcp:                       # Para cada BCP na lista
        if(bcp['estado'] != 'terminado'):       # Verifica se terminou a execução
            return 0                            # Ainda tem processos para executar
    
    return 1                                    # Todos os processos foram terminados


# Coloca processos que finalizaram I/O (fila de bloqueados) na fila de prontos
# Parâmetros: fila de processos prontos, fila de processos bloqueados, clock atual e modo de ordenação
# Retorno: não há retorno
def verifica_bloqueados(fila_pronto, fila_bloqueado, clock, ordenacao):
    i = 0                                                                                           # Controla laço
    while(i < len(fila_bloqueado)):
        if (clock - fila_bloqueado[i]['cheg_bloqueado']) == fila_bloqueado[i]['tempo_bloqueado']:   # Se o processo já terminou o I/O
            
            if (fila_bloqueado[i]['tempo_cpu'] == fila_bloqueado[i]['tempo_exec']):                 # Se terminou sua execução
                fila_bloqueado[i]['estado'] = 'terminado'                                           # Processo termina
            else:                                                                                   # Se não terminou sua execução
                fila_bloqueado[i]['estado'] = 'pronto'                                              # Processo muda o estado de bloqueado para pronto
                fila_pronto.append(fila_bloqueado[i])                                               # Processo é adicionado na fila de prontos
                fila_bloqueado[i]['tempo_espera'].append(clock + 1)                                 # Processo recebe tempo em que entrou na fila de prontos
                #print('tempo_iniciado', fila_bloqueado[i]['tempo_espera'][len(fila_bloqueado[i]['tempo_espera']) - 1])
                
                if(ordenacao != ''):                                                                # Se algum modo de ordenação foi passado
                    fila_pronto.sort(key = operator.itemgetter(ordenacao))                          # Ordena fila de prontos pelo tempo de execução (ordem crescente)
            
            fila_bloqueado.pop(i)                                                                   # Processo é retirado da fila de bloqueados
            i -= 1                                                                                  # Se o processo mudou de estado, i é decrementado
        i += 1


# Adiciona processo na fila de bloqueado
# Parâmetros: fila de processos bloqueados, clock em que processo chegou na fila de bloqueados, tempo de bloqueio e processo a ser bloqueado
# Obs: tempo_bloqueado é um valor randômico entre 1 e 9
# Retorno: não há retorno 
def bloqueia_processo(fila_bloqueado, tempo_chegada, tempo_bloqueado, processo):
    fila_bloqueado.append(processo)                                 # Processo é adicionado na fila de bloqueados
    processo['cheg_bloqueado'] = tempo_chegada                      # Processo recebe tempo em que entrou na fila de bloqueados
    processo['tempo_bloqueado'] = tempo_bloqueado                   # Processo recebe tempo em que deve ficar bloqueado
    processo['estado'] = 'bloqueado'                                # Processo muda para o estado de bloqueado


# Armazena dados referênte à fila de prontos para cálculo de estatísticas
# Parâmetros: fila que se fará os cálculos, estatísticas
# Retorno: não há retorno
def conta_fila(fila, estatisticas):
    qtd = len(fila)                                 # Quantidade de processos na fila

    estatisticas['qtd_fila_pronto'].append(qtd)     # Adiciona qtd na lista de quantidades de estatisticas

    if(qtd > estatisticas['max_fila_pronto']):      # Se a qtd atual é maior que o maior tamanho da fila de prontos já registrado 
        estatisticas['max_fila_pronto'] = qtd       # qtd é o tamanho máximo da fila de prontos já registrado


# Faz o cálculo das estatísticas referente a execução dos processos
# Parâmetros: lista de BCPs, tempo inicial das execuções, tempo final das execuções, demais dados para o cálculo
# Retorno: não há retorno
def calc_estatisticas(lista_bcp, tempoi, tempof, estatisticas):

    tempo_medio_resposta = 0
    throughput = 0
    tam_medio_fila_pronto = 0
    tempo_medio_espera = 0
    quant_prontos = len(estatisticas['qtd_fila_pronto'])
    cont = 0
    
    if(tempof - tempoi != 0):
        throughput = float(len(lista_bcp)) / (tempof - tempoi)      # Cálculo do throughtput do sistema

    for tam in estatisticas['qtd_fila_pronto']:                     
        tam_medio_fila_pronto += tam                                # Soma os tamanhos da fila de processos coletados durante a execução
    
    if(quant_prontos != 0):
        tam_medio_fila_pronto /= quant_prontos                      # Cálculo do tamanho médio da fila de processos
    else:
        tam_medio_fila_pronto = 0

    for bcp in lista_bcp:                                           # Percorre todos os processos que executaram
        for tempo in bcp['tempo_espera']:                           # Percorre todos os tempo de espera do processo
            tempo_medio_espera += tempo                             # Soma tempo de espera
            cont += 1                                               # Conta número de esperas
    tempo_medio_espera /= cont                                      # Cálculo do tempo médio esperado pelos processos
    
 
    print("Throughput: " + str(round(throughput,2)) + " ms.")                
    print("Tempo Médio de Espera (TME): " + str(round(tempo_medio_espera, 2)))
    print("Tamanho Médio da Fila de Pronto: " + str(tam_medio_fila_pronto))
    
    
    for bcp in lista_bcp:
        tempo_medio_resposta += bcp['tempo_resposta']
        print("Tempo de Resposta P" + bcp['id'] + ": " + str(bcp['tempo_resposta']))

    if (len(lista_bcp) > 0):
        tempo_medio_resposta /= len(lista_bcp)
        print("Tempo Médio de Resposta: " + str(round(tempo_medio_resposta,2)))    
    print("________________________________\n")


# Adiciona os estados dos processos no histórico de estados
# Parâmetro: Lista de BCPs
# Retorno: Não há retorno
def adiciona_historico (lista_bcp):
    for bcp in lista_bcp:
        if (bcp['estado'] == 'pronto'):
            bcp['historico'] += "☑ "
        elif (bcp['estado'] == 'bloqueado'):
            bcp['historico'] += "☒ "
        elif (bcp['estado'] == 'executando'):
            bcp['historico'] += "ϵ "
        else:
            bcp['historico'] += "☐ "

# Imprime o histórico (linha do tempo dos processos)
# Parâmetro: Lista de BCPs
# Retorno: Não há retorno
def imprime_historico(lista_bcp):
    for bcp in lista_bcp:
        print("P" + bcp['id'] + ": " + bcp['historico'])
    print("\n")


# Imprime a legenda da linha do tempo
# Parâmetro: Não há parâmetros
# Retorno: Não há retorno
def imprime_legenda():
    print("=== Legenda: ===")
    print("☑ - Pronto")
    print("☒ - Bloqueado em I/O")
    print("ϵ - Executando")
    print("☐ - Outro (No disco ou Terminado)\n")
