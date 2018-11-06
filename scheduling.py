"""
Neste arquivo são desenvolvidos os três escalonadores: Shortest Job First (SJF), Prioridade (PRIO) e RoundRobin (RR).

A função scheduler é responsável por chamar os escalonadores para tratar a execução dos processos passados pelo usuário.
Ela faz uma cópia da lista de BCPs e cria a estrutura para armazenar os dados de estatísticas para cada escalonador.
Após a execução dos três escalonadores, ela chama a função para o cálculo das estatísticas.

Os escalonadores foram implementados de forma recursiva, devendo ser passado para cada chamada a lista de BCPs, as filas de prontos e bloqueados, o número do clock em que aquela chamada deve ser executada, o BCP do processo que está na CPU no momento da chamada e os dados para estatísticas.
Em cada escalonador é feito:
    * Captura dos dados da fila de prontos para estatísticas;
    * Verificação do término da execução do escalonador;
    * Inicialização dos processos que estão no disco (traz processo para a RAM e os escalona);
    * Escalonamento de um processo pronto para a execução (leva em conta as regras de cada escalonador);
    * Verificação se o processo que está executando necessita de I/O. Se sim, direciona ele para a operação;
    * Verificação se o processo que está executando já terminou todas as suas operações;
    * Verificação se processos que estavam fazendo I/O já terminaram a operação. Se sim, torna-os prontos;
    * Chamada do escalonador novamente, com o próximo clock.
"""
import utilitarios
import operator
import copy
from random import randint
import time

# Chama os três escalonadores
def scheduler(lista_bcp, quantum):
    
    sjf_lista_bcp = copy.deepcopy(lista_bcp)        # Cria cópia da lista de BCPs para escalonador SJF
    prio_lista_bcp = copy.deepcopy(lista_bcp)       # Cria cópia da lista de BCPs para escalonador Prio
    rr_lista_bcp = copy.deepcopy(lista_bcp)         # Cria cópia da lista de BCPs para escalonador RR

    estatisticas_sjf = {                     # Guarda dados para cálculo das estatísticas do sistema usando o escalonador SJF
        'max_fila_pronto': 0,               # Tamanho máximo da fila de prontos
        'qtd_fila_pronto': []               # Tamanhos da fila de prontos, capturados a cada 5 ciclos de clock (usado para cálculo do tamanho médio da fila)
    }
    estatisticas_prio = {                    # Guarda dados para cálculo das estatísticas do sistema usando o escalonador Prio
        'max_fila_pronto': 0,               # Tamanho máximo da fila de prontos
        'qtd_fila_pronto': []               # Tamanhos da fila de prontos, capturados a cada 5 ciclos de clock (usado para cálculo do tamanho médio da fila)
    }
    estatisticas_rr = {                      # Guarda dados para cálculo das estatísticas do sistema usando o escalonador RR
        'max_fila_pronto': 0,               # Tamanho máximo da fila de prontos
        'qtd_fila_pronto': []               # Tamanhos da fila de prontos, capturados a cada 5 ciclos de clock (usado para cálculo do tamanho médio da fila)
    }
    
    tempoi_sjf = time.time()                                        # Captura tempo inicial da execução do sistema usando o escalonador SJF
    sjf(sjf_lista_bcp, [], [], 0, None, estatisticas_sjf)            # Chama escalonador SJF passando lista dos BCPs, lista de prontos, lista de bloqueados, clock inicial, processo que está executando no momento e dados para estatísticas
    tempof_sjf = time.time()                                        # Captura tempo final da execução do sistema usando o escalonador SJF
    utilitarios.calc_estatisticas(sjf_lista_bcp, tempoi_sjf, tempof_sjf, estatisticas_sjf)          # Faz cálculo das estatísticas para o uso do escalonador SJF
    

    tempoi_prio = time.time()                                       # Captura tempo inicial da execução do sistema usando o escalonador Prio
    prio(prio_lista_bcp, [], [], 0, None, estatisticas_prio)         # Chama escalonador Prio passando lista dos BCPs, lista de prontos, lista de bloqueados, clock inicial, processo que está executando no momento e dados para estatísticas
    tempof_prio = time.time()                                       # Captura tempo final da execução do sistema usando o escalonador Prio
    utilitarios.calc_estatisticas(prio_lista_bcp, tempoi_prio, tempof_prio, estatisticas_prio)      # Faz cálculo das estatísticas para o uso do escalonador Prio
    

    tempoi_rr = time.time()                                         # Captura tempo inicial da execução do sistema usando o escalonador RR
    rr(rr_lista_bcp, [], [], int(quantum), 0, None, estatisticas_rr) # Chama escalonador RR passando lista dos BCPs, lista de prontos, lista de bloqueados, quantum, clock inicial, processo que está executando no momento e dados para estatísticas
    tempof_rr = time.time()                                         # Captura tempo final da execução do sistema usando o escalonador RR
    utilitarios.calc_estatisticas(rr_lista_bcp, tempoi_rr, tempof_rr, estatisticas_rr)          # Faz cálculo das estatísticas para o uso do escalonador RR

    utilitarios.imprime_legenda()
    

# ESCALONADOR SHORTEST JOB FIRST (Não-preemptivo)
# Parâmetros: lista dos BCPs, lista de prontos, lista de bloqueados, clock no momento, processo que está executando no momento e dados para estatística
# Retorno: 0 -> ocorreu um erro na execução / 1 -> execução terminada com sucesso
def sjf(lista_bcp, fila_pronto, fila_bloqueado, clock, executando, estatisticas):
    if((clock % 5 == 0) & clock != 0 ):                                 # A cada 5 ciclos de clock captura dados da fila de prontos para estatísticas
        utilitarios.conta_fila(fila_pronto, estatisticas)               # Chama função que faz a captura

    if(utilitarios.verifica_fim(lista_bcp)):                            # Se todos os processos terminaram sua execução
        print("=== Shortest Job First: ===\n")
        utilitarios.imprime_historico(lista_bcp)                        # Imprime a linha do tempo do SJF
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

        # Calcula tempo que o processo esperou para executar
        executando['tempo_espera'][len(executando['tempo_espera']) - 1] = clock - executando['tempo_espera'][len(executando['tempo_espera']) - 1]
        if(executando['executou'] == 0):                                # Se o processo ainda não usou a CPU
            executando['executou'] = 1                                  # Sinaliza que processo já usou a CPU
            executando['tempo_resposta'] = clock - executando['tempo_cheg']   # Registra tempo de resposta
        
        fila_pronto.pop(0)                                              # Processo é retirado da fila de prontos
    
    utilitarios.adiciona_historico(lista_bcp)
    # Se há processo executando
    if(executando != None):
        executando['tempo_exec'] += 1                                   # Incrementa tempo já executado do processo em execução
        
        # Se o processo necessita de I/O na execução atual
        if((len(executando['fila_io']) > 0) and (executando['tempo_exec'] == executando['fila_io'][0])):
            executando['fila_io'].pop(0)                                                        # A necessidade de I/O é tirada da lista do processo
            utilitarios.bloqueia_processo(fila_bloqueado, clock, randint(1, 9), executando)     # Processo é bloqueado para operação de I/O
            executando = None                                                                   # Tira o processo de execução

        # Se o processo já terminou sua execução
        elif(executando['tempo_exec'] == executando['tempo_cpu']):
            executando['estado'] = 'terminado'                          # Processo é terminado
            executando = None                                           # Processo sai da CPU
    
    
    utilitarios.verifica_bloqueados(fila_pronto, fila_bloqueado, clock, 'tempo_cpu')            # Escalona processos que terminaram I/O para fila de prontos
    sjf(lista_bcp, fila_pronto, fila_bloqueado, clock + 1, executando, estatisticas)          # Chama recursivamente o escalonador, com próximo clock

# ESCALONADOR DE PRIORIDADE (Preemptivo)
# Parâmetros: lista dos BCPs, lista de prontos, lista de bloqueados, clock no momento, processo que está executando no momento e dados para estatística
# Retorno: 0 -> ocorreu um erro na execução / 1 -> execução terminada com sucesso
def prio(lista_bcp, fila_pronto, fila_bloqueado, clock, executando, estatisticas):    # Prioridade (Preemptivo)
    if((clock % 5 == 0) & clock != 0 ):                                 # A cada 5 ciclos de clock captura dados da fila de prontos para estatísticas
        utilitarios.conta_fila(fila_pronto, estatisticas)               # Chama função que faz a captura

    if(utilitarios.verifica_fim(lista_bcp)):                            # Se todos os processos terminaram sua execução
        print("=== Prioridade: ===\n")
        utilitarios.imprime_historico(lista_bcp)                        # Imprime a linha do tempo do Prioridade
        return 1                                                        # Execução terminada com sucesso
    
    # Inicia os processos que ainda estão no "disco"
    for bcp in lista_bcp:                                               # Para todos os processos
        if(bcp['tempo_cheg'] == clock):                                 # Se é hora do processo ser iniciado
            bcp['estado'] = 'pronto'                                    # Processo inicia pronto para a execução
            fila_pronto.append(bcp)                                     # Processo é escalonado para fila de prontos
            fila_pronto.sort(key = operator.itemgetter('prioridade'))   # Ordena fila de prontos pelo tempo de execução (ordem crescente)
    
    # Escalona processo pronto para execução
    if(len(fila_pronto) > 0):                                                                   # Se há algum processo pronto
        if(executando != None):                                                                 # Se há processo executando 

            # Se a prioridade do primeiro processo pronto é maior que a do que está executando (1 é a maior prioridade, que é menor que 2, que é menor que 3...)
            if(executando['prioridade'] > fila_pronto[0]['prioridade']):
                executando['estado'] = 'pronto'                                                 # Processo muda o estado de executando para pronto

                fila_pronto.append(executando)                                                  # Processo é adicionado na fila de prontos
                fila_pronto.sort(key = operator.itemgetter('prioridade'))                       # Ordena fila de prontos pela prioridade (ordem decrescente)

                executando = fila_pronto[0]                                                     # Processo pronto com maior prioridade ganha processador
                executando['estado'] = 'executando'                                             # Processo muda o estado de pronto para executando

                # Calcula tempo que o processo esperou para executar
                executando['tempo_espera'][len(executando['tempo_espera']) - 1] = clock - executando['tempo_espera'][len(executando['tempo_espera']) - 1]

                fila_pronto.pop(0)                                                              # Processo é retirado da fila de prontos

        elif(executando == None):                                                               # Se não há processo executando
            executando = fila_pronto[0]                                                         # Processo pronto com maior prioridade ganha processador
            executando['estado'] = 'executando'                                                 # Processo muda o estado de pronto para executando

            # Calcula tempo que o processo esperou para executar
            executando['tempo_espera'][len(executando['tempo_espera']) - 1] = clock - executando['tempo_espera'][len(executando['tempo_espera']) - 1]
                
            fila_pronto.pop(0)                                                                  # Processo é retirado da fila de prontos

        if(executando['executou'] == 0):                                                # Se o processo ainda não usou a CPU
            executando['executou'] = 1                                                  # Sinaliza que processo já usou a CPU
            executando['tempo_resposta'] = clock - executando['tempo_cheg']                   # Registra tempo de resposta
    
    utilitarios.adiciona_historico(lista_bcp)

    # Se há processo executando
    if(executando != None):
        executando['tempo_exec'] += 1                                   # Incrementa tempo já executado do processo em execução
        
        # Se o processo necessita de I/O na execução atual
        if((len(executando['fila_io']) > 0) and (executando['tempo_exec'] == executando['fila_io'][0])):
            executando['fila_io'].pop(0)                                                        # A necessidade de I/O é tirada da lista do processo
            utilitarios.bloqueia_processo(fila_bloqueado, clock, randint(1, 9), executando)     # Processo é bloqueado para operação de I/O
            executando = None                                                                   # Tira o processo de execução

        # Se o processo já terminou sua execução
        elif(executando['tempo_exec'] == executando['tempo_cpu']):
            executando['estado'] = 'terminado'                          # Processo é terminado
            executando = None                                           # Processo sai da CPU
    
    
    utilitarios.verifica_bloqueados(fila_pronto, fila_bloqueado, clock, 'prioridade')           # Escalona processos que terminaram I/O para fila de prontos
    
    prio(lista_bcp, fila_pronto, fila_bloqueado, clock + 1, executando, estatisticas)         # Chama recursivamente o escalonador, com próximo clock

# ESCALONADOR ROUND-ROBIN (Preemptivo)
# Parâmetros: lista dos BCPs, lista de prontos, lista de bloqueados, quantum do processador, clock no momento, processo que está executando no momento e dados para estatística
# Retorno: 0 -> ocorreu um erro na execução / 1 -> execução terminada com sucesso
def rr(lista_bcp, fila_pronto, fila_bloqueado, quantum, clock, executando, estatisticas): # Round-Robin (Preemptivo)
    if((clock % 5 == 0) & clock != 0 ):                                # A cada 5 ciclos de clock captura dados da fila de prontos para estatísticas
        utilitarios.conta_fila(fila_pronto, estatisticas)              # Chama função que faz a captura

    if(utilitarios.verifica_fim(lista_bcp)):                            # Se todos os processos terminaram sua execução
        print("=== Round-Robin: ===\n")
        utilitarios.imprime_historico(lista_bcp)                        # Imprime a linha do tempo do RR
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

        # Calcula tempo que o processo esperou para executar
        executando['tempo_espera'][len(executando['tempo_espera']) - 1] = clock - executando['tempo_espera'][len(executando['tempo_espera']) - 1]
        if(executando['executou'] == 0):                                # Se o processo ainda não usou a CPU
            executando['executou'] = 1                                  # Sinaliza que processo já usou a CPU
            executando['tempo_resposta'] = clock - executando['tempo_cheg']   # Registra tempo de resposta

        #print('tempo', executando['tempo_espera'][len(executando['tempo_espera']) - 1])

        fila_pronto.pop(0)                                              # Processo é retirado da fila de prontos
    
    utilitarios.adiciona_historico(lista_bcp)
    # Se há processo executando
    if(executando != None):
        executando['tempo_exec'] += 1                                   # Incrementa tempo já executado do processo em execução
        executando['quantum'] += 1                                      # Incrementa o quantum já utilizado pelo processo

        #print(executando['id'], executando['quantum'])
        
        # Se o processo necessita de I/O na execução atual
        if((len(executando['fila_io']) > 0) and (executando['tempo_exec'] == executando['fila_io'][0])):
            executando['fila_io'].pop(0)                                                        # A necessidade de I/O é tirada da lista do processo
            executando['quantum'] = 0                                                           # Reinicia quantum do processo
            utilitarios.bloqueia_processo(fila_bloqueado, clock, randint(1, 9), executando)     # Processo é bloqueado para operação de I/O
            executando = None                                                                   # Tira o processo de execução

        # Se processo terminou
        elif(executando['tempo_exec'] == executando['tempo_cpu']):
            executando['estado'] = 'terminado'                                                  # Processo é terminado
            executando = None                                                                   # Processo sai da CPU

        # Se o processo já utilizou todo o quantum
        elif(executando['quantum'] == quantum):
            fila_pronto.append(executando)                                                      # Processo é adicionado na fila de prontos
            executando['quantum'] = 0                                                           # Reinicia quantum do processo
            executando['estado'] = 'pronto'                                                     # Processo muda o estado de executando para pronto
            executando['tempo_espera'][len(executando['tempo_espera']) - 1] = clock + 1         # Processo recebe tempo em que entrou na fila de prontos

            executando = None                                                                   # Processo sai da CPU
            
    utilitarios.verifica_bloqueados(fila_pronto, fila_bloqueado, clock, '')                     # Escalona processos que terminaram I/O para fila de prontos
    # utilitarios.adiciona_historico(lista_bcp)
    rr(lista_bcp, fila_pronto, fila_bloqueado, quantum, clock + 1, executando, estatisticas)    # Chama recursivamente o escalonador, com próximo clock
