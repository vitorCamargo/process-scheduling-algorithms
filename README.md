# Process-Scheduling-Algorithms (Algoritmos de Escalonamento de Processo)
Este projeto foi desenvolvido por: Lucas Vinicius, Thais Zorawski e Vitor Bueno para a matéria de Sistemas Operacionais.

O projeto está dividido em 2 partes, um código em python e um software web (desenvolvido em Vue). O código base para este trabalho, comentado e exeplicado cada função está no arquivo em python, porém, para um entendimento maior, foi criado um software que simula em tempo real os processos (aplicativo Web).

## Execução dos programas

Para executar o programa em python deve digitar o seguinte:

`$ cd /python`

`$ python main.py './processos.txt' 3`

onde o primeiro parâmetro é o arquivo contendo os processos e o segundo é referente ao tamanho do quantum.

Para executar o aplicativo web é necessário os seguintes passos:

`$ cd ./web`

`$ npm install`

`$ npm run dev`

após o carregamento, a página estará disponível em [http://localhost:8080/](http://localhost:8080/).
