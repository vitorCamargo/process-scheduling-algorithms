import utilitarios

def scheduler(lista_bcp, quantum):
    sjf_lista_bcp = lista_bcp.copy()
    sjf(sjf_lista_bcp, [], [], 0)

    prio(lista_bcp, 0)
    rr(lista_bcp, quantum, 0)

def sjf(lista_bcp, lista_pronto, lista_bloqueado, tempo): # Shortest Job First (Não-preemptivo)
    if(utilitarios.verifica_fim(lista_bcp)):
        return 1

    # se finalizou, vaza

    # verifica se há processos para entrar na lista de pronto (disco e bloqueados)
    # insere em lista_pronto em ordem crescente

    # elege topo
    # executar topo

    # se é io vai para lista_bloqueado e troca contexto

    # incrementar histórico

    sjf(lista_bcp, lista_pronto, lista_bloqueado, tempo + 1)

def prio(lista_bcp, tempo): # Prioridade (Preemptivo)
    return 0

def rr(lista_bcp, quantum, tempo): # Round-Robin (Preemptivo)
    return 0


    