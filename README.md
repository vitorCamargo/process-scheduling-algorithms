# Process Scheduling Algorithms
👨🏽‍💻📝 Assignment for 'Operating Systems' subject about Process Scheduling Algorithms.

## More Informations
This project was developed by [Lucas Vinicius](https://github.com/lucasvribeiro), [Thais Zorawski](https://github.com/TZorawski) and [Vitor Camargo](https://github.com/vitorCamargo).

The project is divided into 2 parts, a python3 code and a web application (developed in Vue). The code base for this project has been commented and explained for each algorithm and is in the python file, but for a better understanding, a software has been created that simulates real time process scheduling algorithms through a web application.

### Python Application Usage
To execute the python program, you just need to type the following command:
```sh
$ cd /python
$ python main.py './processos.txt' 3
```

where, the first parameter is the input file, that contains the processes. The second parameter refers to *quantum* value.

### Web Application Usage
To execute the web application is necessary to follow the next steps:
```sh
$ cd ./web
$ npm install
$ npm run dev
```

after these steps, the application will be avaliable in [http://localhost:8080/](http://localhost:8080/).

Or if you just want to see this application without downloading it, you can check it on https://vitorcamargo.github.io/process-scheduling-algorithms/
