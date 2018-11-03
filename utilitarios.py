"""
 Este arquivo contém todas as funções auxiliares utilizadas pelos escalonadores.
"""

import operator

# Verifica se todas as execuções já acabaram
# Retorno: 0 -> Ainda há execuções / 1 -> Execuções terminadas
def verifica_fim(lista_bcp):
    for bcp in lista_bcp:                       # Para cada BCP na lista
        if(bcp['estado'] != 'terminado'):       # Verifica se terminou a execução
            return 0                            # Ainda tem processos para executar
    
    return 1                                    # Todos os processos foram terminados

# Coloca processos que finalizaram I/O (fila de bloqueados) na fila de prontos
# Retorno: não há retorno
def verifica_bloqueados(fila_pronto, fila_bloqueado, clock, ordenacao):
    i = 0
    while(i < len(fila_bloqueado)):
        if (clock - fila_bloqueado[i]['cheg_bloqueado']) == fila_bloqueado[i]['tempo_bloqueado']:   # Se o processo já terminou o I/O
            
            if (fila_bloqueado[i]['tempo_cpu'] == fila_bloqueado[i]['tempo_exec']):                 # Se terminou sua execução
                fila_bloqueado[i]['estado'] = 'terminado'                                           # Processo termina
            else:                                                                                   # Se não terminou sua execução
                fila_bloqueado[i]['estado'] = 'pronto'                                              # Processo muda o estado de bloqueado para pronto
                fila_pronto.append(fila_bloqueado[i])                
                fila_bloqueado[i]['tempo_espera'].append(clock + 1)
                #print('tempo_iniciado', fila_bloqueado[i]['tempo_espera'][len(fila_bloqueado[i]['tempo_espera']) - 1])
                
                if(ordenacao != ''):                                                                # Volta para fila de prontos
                    fila_pronto.sort(key = operator.itemgetter(ordenacao))                          # Ordena fila de prontos pelo tempo de execução (ordem crescente)
            
            fila_bloqueado.pop(i)                                                                   # Processo é retirado da fila de bloqueados
            i -= 1
        i += 1

# Adiciona processo na fila de bloqueado
# O tempo_bloqueado é um valor randômico entre 1 e 9
# Retorno: não há retorno 
def bloqueia_processo(fila_bloqueado, tempo_chegada, tempo_bloqueado, processo):
    fila_bloqueado.append(processo)
    print('id: ', processo['id'], 'tempo: ', tempo_bloqueado)
    processo['cheg_bloqueado'] = tempo_chegada
    processo['tempo_bloqueado'] = tempo_bloqueado
    processo['estado'] = 'bloqueado'

