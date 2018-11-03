import utilitarios
import operator
from random import randint

# Chama os três escalonadores
def scheduler(lista_bcp, quantum):
    sjf_lista_bcp = lista_bcp.copy()        # Cria cópia da lista de BCPs para escalonador SJF
    prio_lista_bcp = lista_bcp.copy()
    rr_lista_bcp = lista_bcp.copy()
    
    # sjf(sjf_lista_bcp, [], [], 0, None)     # Chama escalonador SJF passando lista dos BCPs, lista de prontos, lista de bloqueados, clock inicial e processo que está executando no momento

    # prio(prio_lista_bcp, [], [], 0, None)
    
    rr(rr_lista_bcp, [], [], int(quantum), 0, None)

# Escalonador Shortest Job First. Parâmetros: lista dos BCPs, lista de prontos, lista de bloqueados, clock no momento e processo que está executando no momento
# Retorno: 0 -> ocorreu um erro na execução / 1 -> execução terminada com sucesso
def sjf(lista_bcp, fila_pronto, fila_bloqueado, clock, executando):     # Shortest Job First (Não-preemptivo)
    if(utilitarios.verifica_fim(lista_bcp)):                            # Se todos os processos terminaram sua execução
        return 1                                                        # Execução terminada com sucesso
    
    # Inicia os processos que ainda estão no "disco"
    for bcp in lista_bcp:                                               # Para todos os processos
        if(bcp['tempo_cheg'] == clock):                                 # Se é hora do processo ser iniciado
            bcp['estado'] = 'pronto'                                    # Processo inicia pronto para a execução
            fila_pronto.append(bcp)                                     # Processo é escalonado para fila de prontos
            fila_pronto.sort(key = operator.itemgetter('tempo_cpu'))    # Ordena fila de prontos pelo tempo de execução (ordem crescente)
    
    # Escalona processo pronto para execução
    if((executando == None) & (len(fila_pronto) > 0)):                  # Se não há processo executando e há algum processo pronto
        executando = fila_pronto[0]                                     # Processo pronto com menor tempo de execução ganha processador
        executando['estado'] = 'executando'                             # Processo muda o estado de pronto para executando

        executando['tempo_espera'][len(executando['tempo_espera']) - 1] = clock - executando['tempo_espera'][len(executando['tempo_espera']) - 1]

        fila_pronto.pop(0)                                              # Processo é retirado da fila de prontos
    
    # Não há nenhum processo para executar
    if(executando == None):
        print('--')
    else:
        print(executando['id'])
    
    # Se há processo executando
    if(executando != None):
        executando['tempo_exec'] += 1                                   # Incrementa tempo já executado do processo em execução
        
        # Se o processo necessita de I/O na execução atual
        if((len(executando['fila_io']) > 0) and (executando['tempo_exec'] == executando['fila_io'][0])):
            executando['fila_io'].pop(0)
            utilitarios.bloqueia_processo(fila_bloqueado, clock, randint(1, 9), executando)
            executando = None

        elif(executando['tempo_exec'] == executando['tempo_cpu']):
            executando['estado'] = 'terminado'
            executando = None    
    
    
    utilitarios.verifica_bloqueados(fila_pronto, fila_bloqueado, clock, 'tempo_cpu')

    sjf(lista_bcp, fila_pronto, fila_bloqueado, clock + 1, executando)

# Escalonador de Prioridade. Parâmetros: lista dos BCPs, lista de prontos, lista de bloqueados, clock no momento e processo que está executando no momento
# Retorno: 0 -> ocorreu um erro na execução / 1 -> execução terminada com sucesso
def prio(lista_bcp, fila_pronto, fila_bloqueado, clock, executando):    # Prioridade (Preemptivo)
    if(utilitarios.verifica_fim(lista_bcp)):                            # Se todos os processos terminaram sua execução
        return 1                                                        # Execução terminada com sucesso
    
    # Inicia os processos que ainda estão no "disco"
    for bcp in lista_bcp:                                               # Para todos os processos
        if(bcp['tempo_cheg'] == clock):                                 # Se é hora do processo ser iniciado
            bcp['estado'] = 'pronto'                                    # Processo inicia pronto para a execução
            fila_pronto.append(bcp)                                     # Processo é escalonado para fila de prontos
            fila_pronto.sort(key = operator.itemgetter('prioridade'))   # Ordena fila de prontos pelo tempo de execução (ordem crescente)
    
    # Escalona processo pronto para execução
    if(len(fila_pronto) > 0):                                           # Se não há processo executando e há algum processo pronto
        if(executando != None):
            if(executando['prioridade'] > fila_pronto[0]['prioridade']):
                executando['estado'] = 'pronto'
                executando['tempo_espera'][len(executando['tempo_espera']) - 1] = clock + 1

                fila_pronto.append(executando)
                fila_pronto.sort(key = operator.itemgetter('prioridade'))

                executando = fila_pronto[0]
                executando['estado'] = 'executando'
                executando['tempo_espera'][len(executando['tempo_espera']) - 1] = clock - executando['tempo_espera'][len(executando['tempo_espera']) - 1]
                
                fila_pronto.pop(0)

        elif(executando == None):
            executando = fila_pronto[0]
            executando['estado'] = 'executando'
            executando['tempo_espera'][len(executando['tempo_espera']) - 1] = clock - executando['tempo_espera'][len(executando['tempo_espera']) - 1]
                
            fila_pronto.pop(0)
            
  
    # Não há nenhum processo para executar
    if(executando == None):
        print('--')
    else:
        print(executando['id'])
    
    if(executando != None):
        executando['tempo_exec'] += 1
        
        if((len(executando['fila_io']) > 0) and (executando['tempo_exec'] == executando['fila_io'][0])):
            executando['fila_io'].pop(0)
            utilitarios.bloqueia_processo(fila_bloqueado, clock, randint(1, 9), executando)
            executando = None

        elif(executando['tempo_exec'] == executando['tempo_cpu']):
            executando['estado'] = 'terminado'
            executando = None    
    
    
    utilitarios.verifica_bloqueados(fila_pronto, fila_bloqueado, clock, 'prioridade')

    prio(lista_bcp, fila_pronto, fila_bloqueado, clock + 1, executando)

# Escalonador Round-Robin. Parâmetros: lista dos BCPs, lista de prontos, lista de bloqueados, quantum do processador, clock no momento e processo que está executando no momento
# Retorno: 0 -> ocorreu um erro na execução / 1 -> execução terminada com sucesso
def rr(lista_bcp, fila_pronto, fila_bloqueado, quantum, clock, executando): # Round-Robin (Preemptivo)
    if(utilitarios.verifica_fim(lista_bcp)):                            # Se todos os processos terminaram sua execução
        return 1                                                        # Execução terminada com sucesso
    
    # Inicia os processos que ainda estão no "disco"
    for bcp in lista_bcp:                                               # Para todos os processos
        if(bcp['tempo_cheg'] == clock):                                 # Se é hora do processo ser iniciado
            bcp['estado'] = 'pronto'                                    # Processo inicia pronto para a execução
            fila_pronto.append(bcp)                                     # Processo é escalonado para fila de prontos
    
    # Escalona processo pronto para execução
    if((executando == None) & (len(fila_pronto) > 0)):                  # Se não há processo executando e há algum processo pronto
        executando = fila_pronto[0]                                     # Processo pronto com menor tempo de execução ganha processador
        executando['estado'] = 'executando'                             # Processo muda o estado de pronto para executando
        executando['tempo_espera'][len(executando['tempo_espera']) - 1] = clock - executando['tempo_espera'][len(executando['tempo_espera']) - 1]
        
        print('tempo', executando['tempo_espera'][len(executando['tempo_espera']) - 1])

        fila_pronto.pop(0)                                              # Processo é retirado da fila de prontos
    
    # Não há nenhum processo para executar
    if(executando == None):
        print('--', fila_bloqueado[0]['id'])
    
    # Se há processo executando
    if(executando != None):
        executando['tempo_exec'] += 1                                   # Incrementa tempo já executado do processo em execução
        executando['quantum'] += 1                                      # Incrementa o quantum já utilizado pelo processo

        print(executando['id'], executando['quantum'])
        
        # Se o processo necessita de I/O na execução atual
        if((len(executando['fila_io']) > 0) and (executando['tempo_exec'] == executando['fila_io'][0])):
            executando['fila_io'].pop(0)
            executando['quantum'] = 0 
            utilitarios.bloqueia_processo(fila_bloqueado, clock, randint(1, 9), executando)
            executando = None

        # Se processo terminou
        elif(executando['tempo_exec'] == executando['tempo_cpu']):
            executando['estado'] = 'terminado'
            executando = None

        # Se o processo já utilizou todo o quantum
        elif(executando['quantum'] == quantum):
            fila_pronto.append(executando)
            executando['quantum'] = 0
            executando['estado'] = 'pronto'
            executando['tempo_espera'][len(executando['tempo_espera']) - 1] = clock + 1

            executando = None
            
    
    utilitarios.verifica_bloqueados(fila_pronto, fila_bloqueado, clock, '')

    rr(lista_bcp, fila_pronto, fila_bloqueado, quantum, clock + 1, executando)
