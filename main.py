import sys
import scheduling

def read_file():
    lista_bcp = []

    file_name = sys.argv[1]
    file_name = str(file_name)
    file = open(file_name, 'r')
    
    for i in file:
        bcp = i.strip('\n').split(' ')

        lista_bcp.append({
            'id': bcp[0],              # ID do Processo
            'tempo_cpu': bcp[1],       # Tempo Total do Processo
            'prioridade': bcp[2],      # Prioridade
            'temp_cheg': bcp[3],       # Tempo de Chegada
            'fila_io': bcp[4:],        # Fila de Evento de I/O
            'tempo_exec': 0,           # Tempo já executado
            'estado': ""               # Estado do processo. Processo inicia no disco, então não tem estado
        })

    return lista_bcp

def main():
    scheduling.scheduler(read_file(), sys.argv[2])
main()
