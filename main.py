"""
 Este programa faz a simulação dos escalonadores Shortest Job First (SJF), Prioridade (PRIO) e RoundRobin (RR).

 Exemplo de chamada do programa:    $ python main.py 'nome_do_arquivo_com_os_processos' 4
 O primeiro argumento da chamada é o arquivo que contém os dados dos processos a serem executados
 O segundo argumento é o Quantum que será utilizado na simulação.

"""
import sys
import scheduling


# Lê o arquivo passado na chamada do programa
def read_file():
    lista_bcp = []                      # Lista que guarda todos os BCPs

    file_name = sys.argv[1]             # Recebe nome do arquivo com os processos
    file_name = str(file_name)          # Converte nome do arquivo para string
    file = open(file_name, 'r')         # Abre arquivo
    
    for i in file:                      # Percorre cada linha do arquivo
        bcp = i.strip('\n').split(' ')  # Captura os dados da linha e insere em bcp

        # Monta BCP (mapa) e insere na lista de BCPs
        lista_bcp.append({
            'id': bcp[0],                       # ID do Processo
            'tempo_cpu': int(bcp[1]),           # Tempo Total do Processo
            'prioridade': int(bcp[2]),          # Prioridade
            'tempo_cheg': int(bcp[3]),          # Tempo de Chegada
            'fila_io': list(map(int, bcp[4:])), # Fila de Evento de I/O
            'tempo_exec': 0,                    # Tempo já executado
            'estado': "",                       # Estado do processo. Processo inicia no disco, então não tem estado
            'cheg_bloqueado': 0,                # (Usado apenas quando há evento de I/O) Clock da hora de chegada no bloqueio
            'tempo_bloqueado': 0,               # (Usado apenas quando há evento de I/O) Tempo que o processo deve gastar no I/O
            'tempo_espera': list(map(int, [bcp[3]])),           # Lista dos tempos de espera do processo
            'quantum': 0,                       # (Usado apenas em alguns tipos de escalonadores) Tempo máximo que o processo pode usar a CPU
            'tempo_resposta': 0,                # Tempo de resposta
            'executou': 0                       # Marca se o processo já entrou na CPU. 0 -> ainda não entrou / 1 -> já entrou
        })

    return lista_bcp                    # Retorna lista de BCPs montada

def main():
    scheduling.scheduler(read_file(), sys.argv[2]) # Chama função scheduler, passando a lista de BCPs e o Quantum
main()
