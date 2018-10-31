def verifica_fim(lista_bcp):
    
    for bcp in lista_bcp:
        if(bcp['estado'] != 'terminado'):
            return 0 # 0: Ainda tem processos
    return 1 # 1: Todos os processos foram terminados