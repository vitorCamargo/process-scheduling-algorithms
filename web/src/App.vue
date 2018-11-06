<template>
  <a-layout :style = "{ minHeight: '100%' }">
    <a-modal title = "Adicione os Processos:" :visible = "visible" :closable = "false">
      <template slot = "footer">
        <a-button key = "submit" type = "primary" @click = "addProcessos"> Adicionar </a-button>
      </template>

      <a-form :autoFormCreate = "(form) => { this.form = form }">
        <a-form-item fieldDecoratorId = "arquivo" :fieldDecoratorOptions = "{ rules: [{ required: true, message: 'Campo Obrigatório' }] }">
          <a-textarea placeholder = "# ID – DF – PRI – TC – FIO" :autosize = "{ minRows: 3, maxRows: 6 }" />
        </a-form-item>

        <a-form-item fieldDecoratorId = "quantum" :fieldDecoratorOptions = "{ rules: [{ required: true, message: 'Campo Obrigatório' }] }">
          <a-input placeholder = "Quantum" type = "number" min = "1" />
        </a-form-item>
      </a-form>
    </a-modal>

    <a-modal :title = "estatisticas.titulo" :visible = "estatisticas.visible" @cancel = "handleCancel">
      <template slot = "footer">
        <a-button key = "back" @click = "handleCancel"> Voltar </a-button>
      </template>
      <h3>
        <p> <b> Throughput: </b> {{ estatisticas.throughput }}ms </p>
        <p> <b> Tempo Médio de Espera: </b> {{ estatisticas.tempoMedioEspera }} </p>
        <p> <b> Tamanho da Fila de Pronto: </b> {{ estatisticas.tamMedioFilaPronto }} </p>
        <p> <b> Tempo Médio de Resposta: </b> {{ estatisticas.tempoMedioResposta }} </p>
        <br />
        <p> <b> Tempo de Resposta por Processo: </b> </p>
        <span v-for = "processo in this[estatisticas.escalonador].lista_bcp" :key = "processo.id">
          <p> <b> P{{processo['id']}}: </b> {{ processo['tempo_resposta'] }} </p>
        </span>
      </h3>
    </a-modal>

    <a-layout-content :style = "{ margin: '24px 16px', padding: '24px', background: '#fff' }">
      <a-collapse :bordered = "false">
        <a-collapse-panel class = "accordion" key = "sjf">
          <template slot = "header">
            <i> Shortest Job First </i> &nbsp;
            <b v-if = "sjf.status !== ''"> {{ sjf.clock }} </b>
          </template>

          <a-row v-if = "sjf.status !== 'terminado'" style = "margin-bottom: 10px;">
            <a-button type = "primary" style = "width: 100%;" v-if = "sjf.status === ''" @click = "inicia('sjf')"> <a-icon type = "play-circle" /> </a-button>
            <a-button type = "primary" style = "width: 100%;" v-else-if = "sjf.status === 'continua'" @click = "pausa('sjf')"> <a-icon type = "pause-circle-o" /> </a-button>
            <a-button type = "primary" style = "width: 100%;" v-else @click = "inicia('sjf')"> <a-icon type = "play-circle-o" /> </a-button>
          </a-row>

          <a-row v-else style = "margin-bottom: 10px;">
            <a-button type = "danger" style = "width: 100%;" @click = "calc_estatisticas('sjf')"> <a-icon type = "area-chart" /> </a-button>
          </a-row>

          <a-row :gutter = "16">
            <a-col :span = "5">
              <a-card title = "Disco" style = "width: 100%;">
                <a-tag v-for = "processo in sjf.lista_bcp" v-if = "processo.estado == ''" :key = "processo.id" color = "blue"> <b> P{{processo.id}} </b> </a-tag>
              </a-card>
            </a-col>
            
            <a-col :span = "5">
              <a-card title = "Bloqueados por I/O" style = "width: 100%;">
                <a-avatar slot = "extra" shape = "square"> - </a-avatar>
                <a-tag v-for = "processo in sjf.fila_bloqueado" v-if = "processo.estado == 'bloqueado'" :key = "processo.id" color = "gray"> <b> P{{processo.id}} ({{ processo['tempo_bloqueado'] - (sjf.clock - processo['cheg_bloqueado']) + 1 }}) </b> </a-tag>
              </a-card>
            </a-col>

            <a-col :span = "4">
              <a-card title = "Executando" style = "width: 100%;">
                <a-avatar slot = "extra" shape = "square" :style = "{ backgroundColor: '#87d068' }"> X </a-avatar>
                <a-tag v-if = "sjf.executando" color = "green"> <b> P{{sjf.executando.id}} </b> </a-tag>
              </a-card>
            </a-col>
            
            <a-col :span = "5">
              <a-card title = "Prontos/Aptos" style = "width: 100%;">
                <a-avatar slot = "extra" shape = "square" :style = "{ backgroundColor: '#f56a00' }" />
                <a-tag v-for = "processo in sjf.fila_pronto" v-if = "processo.estado == 'pronto'" :key = "processo.id" color = "orange"> <b> P{{processo.id}} </b> </a-tag>
              </a-card>
            </a-col>
            
            <a-col :span = "5">
              <a-card title = "Terminados" style = "width: 100%;">
                <a-tag v-for = "processo in sjf.lista_bcp" v-if = "processo.estado == 'terminado'" :key = "processo.id" color = "purple"> <b> P{{processo.id}} </b> </a-tag>
              </a-card>
            </a-col>
          </a-row>

          <a-row style = "margin-top: 30px;">
            <a-table :dataSource = "sjf.lista_bcp" rowKey = "id" :scroll = "{ x: 1300 }">
              <a-table-column dataIndex = "id" key = "id" width = "50px" fixed = "left">
                <b slot-scope = "text, record"> P{{ text }} </b>
              </a-table-column>

              <a-table-column dataIndex = "id" key = "1" title = "Escalonador SJF (Execução)">
                <b slot-scope = "text, record" class = "scroller">
                  <span v-for = "(exec, index) in record.historico" :key = "record.historico[index]['id']">
                    <a-avatar v-if = "exec === 'p'" shape = "square" :style = "{ backgroundColor: '#f56a00' }" />
                    <a-avatar v-else-if = "exec === 'b'" shape = "square"> - </a-avatar> 
                    <a-avatar v-else-if = "exec === 'e'" shape = "square" :style = "{ backgroundColor: '#87d068' }"> X </a-avatar>
                    <a-avatar v-else shape = "square" :style = "{ backgroundColor: 'white' }" />
                  </span>
                </b>
              </a-table-column>
            </a-table>
          </a-row>
        </a-collapse-panel>

        <a-collapse-panel class = "accordion" key = "prio">
          <template slot = "header">
            <i> Prioridade </i> &nbsp;
            <b v-if = "prio.status !== ''"> {{ prio.clock }} </b>
          </template>

          <a-row v-if = "prio.status !== 'terminado'" style = "margin-bottom: 10px;">
            <a-button type = "primary" style = "width: 100%;" v-if = "prio.status === ''" @click = "inicia('prio')"> <a-icon type = "play-circle" /> </a-button>
            <a-button type = "primary" style = "width: 100%;" v-else-if = "prio.status === 'continua'" @click = "pausa('prio')"> <a-icon type = "pause-circle-o" /> </a-button>
            <a-button type = "primary" style = "width: 100%;" v-else @click = "inicia('prio')"> <a-icon type = "play-circle-o" /> </a-button>
          </a-row>

          <a-row v-else style = "margin-bottom: 10px;">
            <a-button type = "danger" style = "width: 100%;" @click = "calc_estatisticas('prio')"> <a-icon type = "area-chart" /> </a-button>
          </a-row>

          <a-row :gutter = "16">
            <a-col :span = "5">
              <a-card title = "Disco" style = "width: 100%;">
                <a-tag v-for = "processo in prio.lista_bcp" v-if = "processo.estado == ''" :key = "processo.id" color = "blue"> <b> P{{processo.id}} </b> </a-tag>
              </a-card>
            </a-col>
            
            <a-col :span = "5">
              <a-card title = "Bloqueados por I/O" style = "width: 100%;">
                <a-avatar slot = "extra" shape = "square"> - </a-avatar>
                <a-tag v-for = "processo in prio.fila_bloqueado" v-if = "processo.estado == 'bloqueado'" :key = "processo.id" color = "gray"> <b> P{{processo.id}} ({{ processo['tempo_bloqueado'] - (prio.clock - processo['cheg_bloqueado']) + 1 }}) </b> </a-tag>
              </a-card>
            </a-col>

            <a-col :span = "4">
              <a-card title = "Executando" style = "width: 100%;">
                <a-avatar slot = "extra" shape = "square" :style = "{ backgroundColor: '#87d068' }"> X </a-avatar>
                <a-tag v-if = "prio.executando" color = "green"> <b> P{{prio.executando.id}} </b> </a-tag>
              </a-card>
            </a-col>
            
            <a-col :span = "5">
              <a-card title = "Prontos/Aptos" style = "width: 100%;">
                <a-avatar slot = "extra" shape = "square" :style = "{ backgroundColor: '#f56a00' }" />
                <a-tag v-for = "processo in prio.fila_pronto" v-if = "processo.estado == 'pronto'" :key = "processo.id" color = "orange"> <b> P{{processo.id}} </b> </a-tag>
              </a-card>
            </a-col>
            
            <a-col :span = "5">
              <a-card title = "Terminados" style = "width: 100%;">
                <a-tag v-for = "processo in prio.lista_bcp" v-if = "processo.estado == 'terminado'" :key = "processo.id" color = "purple"> <b> P{{processo.id}} </b> </a-tag>
              </a-card>
            </a-col>
          </a-row>

          <a-row style = "margin-top: 30px;">
            <a-table :dataSource = "prio.lista_bcp" rowKey = "id" :scroll = "{ x: 1300 }">
              <a-table-column dataIndex = "id" key = "id" width = "50px" fixed = "left">
                <b slot-scope = "text, record"> P{{ text }} </b>
              </a-table-column>

              <a-table-column dataIndex = "id" key = "1" title = "Escalonador por Prioridade (Execução)">
                <b slot-scope = "text, record" class = "scroller">
                  <span v-for = "(exec, index) in record.historico" :key = "record.historico[index]['id']">
                    <a-avatar v-if = "exec === 'p'" shape = "square" :style = "{ backgroundColor: '#f56a00' }" />
                    <a-avatar v-else-if = "exec === 'b'" shape = "square"> - </a-avatar> 
                    <a-avatar v-else-if = "exec === 'e'" shape = "square" :style = "{ backgroundColor: '#87d068' }"> X </a-avatar>
                    <a-avatar v-else shape = "square" :style = "{ backgroundColor: 'white' }" />
                  </span>
                </b>
              </a-table-column>
            </a-table>
          </a-row>
        </a-collapse-panel>

        <a-collapse-panel class = "accordion" key = "rr">
          <template slot = "header">
            <i> Round-Robin </i> &nbsp;
            <b v-if = "rr.status !== ''"> {{ rr.clock }} </b>
          </template>

          <a-row v-if = "rr.status !== 'terminado'" style = "margin-bottom: 10px;">
            <a-button type = "primary" style = "width: 100%;" v-if = "rr.status === ''" @click = "inicia('rr')"> <a-icon type = "play-circle" /> </a-button>
            <a-button type = "primary" style = "width: 100%;" v-else-if = "rr.status === 'continua'" @click = "pausa('rr')"> <a-icon type = "pause-circle-o" /> </a-button>
            <a-button type = "primary" style = "width: 100%;" v-else @click = "inicia('rr')"> <a-icon type = "play-circle-o" /> </a-button>
          </a-row>

          <a-row v-else style = "margin-bottom: 10px;">
            <a-button type = "danger" style = "width: 100%;" @click = "calc_estatisticas('rr')"> <a-icon type = "area-chart" /> </a-button>
          </a-row>

          <a-row :gutter = "16">
            <a-col :span = "5">
              <a-card title = "Disco" style = "width: 100%;">
                <a-tag v-for = "processo in rr.lista_bcp" v-if = "processo.estado == ''" :key = "processo.id" color = "blue"> <b> P{{processo.id}} </b> </a-tag>
              </a-card>
            </a-col>
            
            <a-col :span = "5">
              <a-card title = "Bloqueados por I/O" style = "width: 100%;">
                <a-avatar slot = "extra" shape = "square"> - </a-avatar>
                <a-tag v-for = "processo in rr.fila_bloqueado" v-if = "processo.estado == 'bloqueado'" :key = "processo.id" color = "gray"> <b> P{{processo.id}} ({{ processo['tempo_bloqueado'] - (rr.clock - processo['cheg_bloqueado']) + 1 }}) </b> </a-tag>
              </a-card>
            </a-col>

            <a-col :span = "4">
              <a-card title = "Executando" style = "width: 100%;">
                <a-avatar slot = "extra" shape = "square" :style = "{ backgroundColor: '#87d068' }"> X </a-avatar>
                <a-tag v-if = "rr.executando" color = "green"> <b> P{{rr.executando.id}} </b> </a-tag>
              </a-card>
            </a-col>
            
            <a-col :span = "5">
              <a-card title = "Prontos/Aptos" style = "width: 100%;">
                <a-avatar slot = "extra" shape = "square" :style = "{ backgroundColor: '#f56a00' }" />
                <a-tag v-for = "processo in rr.fila_pronto" v-if = "processo.estado == 'pronto'" :key = "processo.id" color = "orange"> <b> P{{processo.id}} </b> </a-tag>
              </a-card>
            </a-col>
            
            <a-col :span = "5">
              <a-card title = "Terminados" style = "width: 100%;">
                <a-tag v-for = "processo in rr.lista_bcp" v-if = "processo.estado == 'terminado'" :key = "processo.id" color = "purple"> <b> P{{processo.id}} </b> </a-tag>
              </a-card>
            </a-col>
          </a-row>

          <a-row style = "margin-top: 30px;">
            <a-table :dataSource = "rr.lista_bcp" rowKey = "id" :scroll = "{ x: 1300 }">
              <a-table-column dataIndex = "id" key = "id" width = "50px" fixed = "left">
                <b slot-scope = "text, record"> P{{ text }} </b>
              </a-table-column>

              <a-table-column dataIndex = "id" key = "1" title = "Escalonador Round-Robin (Execução)">
                <b slot-scope = "text, record" class = "scroller">
                  <span v-for = "(exec, index) in record.historico" :key = "record.historico[index]['id']">
                    <a-avatar v-if = "exec === 'p'" shape = "square" :style = "{ backgroundColor: '#f56a00' }" />
                    <a-avatar v-else-if = "exec === 'b'" shape = "square"> - </a-avatar> 
                    <a-avatar v-else-if = "exec === 'e'" shape = "square" :style = "{ backgroundColor: '#87d068' }"> X </a-avatar>
                    <a-avatar v-else shape = "square" :style = "{ backgroundColor: 'white' }" />
                  </span>
                </b>
              </a-table-column>
            </a-table>
          </a-row>
        </a-collapse-panel>
      </a-collapse>
    </a-layout-content>
  </a-layout>
</template>

<script>
  export default {
    name: 'app',
    data () {
      return {
        visible: true,
        estatisticas: {
          visible: false,
          titulo: '',
          escalonador: 'sjf',
          tempoMedioResposta: 0,
          throughput: 0,
          tempoMedioEspera: 0,
          tamMedioFilaPronto: 0
        },
        sjf: {
          status: '',
          lista_bcp: [],
          fila_bloqueado: [],
          fila_pronto: [],
          executando: '',
          max_fila_pronto: 0,
          qtd_fila_pronto: [],
          tempo_inicial: 0,
          tempo_final: 0,
          clock: 0
        },
        prio: {
          status: '',
          lista_bcp: [],
          fila_bloqueado: [],
          fila_pronto: [],
          executando: '',
          tempo_resposta: 0,
          executou: 0,
          max_fila_pronto: 0,
          qtd_fila_pronto: [],
          tempo_inicial: 0,
          tempo_final: 0,
          clock: 0
        },
        rr: {
          status: '',
          lista_bcp: [],
          fila_bloqueado: [],
          fila_pronto: [],
          executando: '',
          max_fila_pronto: 0,
          qtd_fila_pronto: [],
          tempo_inicial: 0,
          tempo_final: 0,
          clock: 0
        }
      }
    },
    methods: {
      verifica_fim (escalonador) {
        let res = true

        this[escalonador].lista_bcp.forEach(function (bcp) {
          if (bcp['estado'] !== 'terminado') {
            res = false
          }
        })

        if (res) {
          this[escalonador]['tempo_final'] = new Date()
          this[escalonador].status = 'terminado'
        }
        return res
      },
      verifica_bloqueados (escalonador, ordenacao) {
        let _this = this
        let i = 0

        while (i < _this[escalonador].fila_bloqueado.length) {
          if (_this[escalonador].clock - _this[escalonador].fila_bloqueado[i]['cheg_bloqueado'] === _this[escalonador].fila_bloqueado[i]['tempo_bloqueado']) {
            if (_this[escalonador].fila_bloqueado[i]['tempo_cpu'] === _this[escalonador].fila_bloqueado[i]['tempo_exec']) {
              _this[escalonador].fila_bloqueado[i]['estado'] = 'terminado'
            } else {
              _this[escalonador].fila_bloqueado[i]['estado'] = 'pronto'
              _this[escalonador].fila_pronto.push(_this[escalonador].fila_bloqueado[i])
              _this[escalonador].fila_bloqueado[i]['tempo_espera'].push(_this[escalonador].clock + 1)

              if (ordenacao !== '') {
                _this[escalonador].fila_pronto.sort(function (a, b) {
                  return a[ordenacao] - b[ordenacao]
                })
              }
            }

            _this[escalonador].fila_bloqueado.splice(i, 1)
            i -= 1
          }
          i += 1
        }
      },
      bloqueia_processo (escalonador, tempoChegada, tempoBloqueado, processo) {
        let _this = this

        _this[escalonador].fila_bloqueado.push(processo)
        processo['cheg_bloqueado'] = tempoChegada
        processo['tempo_bloqueado'] = tempoBloqueado
        processo['estado'] = 'bloqueado'
      },
      adiciona_historico (escalonador) {
        let _this = this

        _this[escalonador].lista_bcp.forEach(function (bcp) {
          if (bcp['estado'] === 'pronto') {
            bcp['historico'].push('p')
          } else if (bcp['estado'] === 'bloqueado') {
            bcp['historico'].push('b')
          } else if (bcp['estado'] === 'executando') {
            bcp['historico'].push('e')
          } else {
            bcp['historico'].push('o')
          }
        })
      },
      conta_fila (escalonador) {
        let qtd = this[escalonador]['fila_pronto'].length

        this[escalonador]['qtd_fila_pronto'].push(qtd)

        if (qtd > this[escalonador]['max_fila_pronto']) {
          this[escalonador]['max_fila_pronto'] = qtd
        }
      },
      calc_estatisticas (escalonador) {
        let _this = this[escalonador]

        let tempoMedioResposta = 0
        let throughput = 0
        let tamMedioFilaPronto = 0
        let tempoMedioEspera = 0
        let qtdProntos = _this['qtd_fila_pronto'].length
        let tempoTotal = (_this['tempo_final'].getTime() - _this['tempo_inicial'].getTime()) / 1000

        if (tempoTotal !== 0) {
          throughput = parseFloat((_this['lista_bcp'].length) / (tempoTotal - this[escalonador]['clock']))
        }

        _this['qtd_fila_pronto'].forEach(function (tam) {
          tamMedioFilaPronto += tam
        })

        if (qtdProntos !== 0) {
          tamMedioFilaPronto /= qtdProntos
        } else {
          tamMedioFilaPronto = 0
        }

        this[escalonador]['lista_bcp'].forEach(function (bcp) {
          tempoMedioResposta += bcp['tempo_resposta']

          bcp['tempo_espera'].forEach(function (tempo) {
            tempoMedioEspera += tempo
          })
        })

        tempoMedioEspera /= this[escalonador]['lista_bcp'].length

        if (_this['lista_bcp'].length > 0) {
          tempoMedioResposta /= _this['lista_bcp'].length
        }

        if (escalonador === 'sjf') {
          this.estatisticas['titulo'] = 'Shortest Job First'
        } else if (escalonador === 'prio') {
          this.estatisticas['titulo'] = 'Escalonador por Prioridade'
        } else {
          this.estatisticas['titulo'] = 'Round-Robin'
        }

        this.estatisticas['escalonador'] = escalonador
        this.estatisticas['throughput'] = Math.round(throughput * 100) / 100
        this.estatisticas['tempoMedioEspera'] = Math.round(tempoMedioEspera * 100) / 100
        this.estatisticas['tempoMedioResposta'] = Math.round(tempoMedioResposta * 100) / 100
        this.estatisticas['tamMedioFilaPronto'] = tamMedioFilaPronto
        this.estatisticas['visible'] = true
      },
      inicia (escalonador) {
        if (this[escalonador].status === '') {
          this[escalonador]['tempo_inicial'] = new Date()
        }

        this[escalonador].status = 'continua'

        if (escalonador === 'sjf') {
          this.escalonador_sjf()
        } else if (escalonador === 'prio') {
          this.escalonador_prio()
        } else {
          this.escalonador_rr()
        }
      },
      pausa (escalonador) {
        this[escalonador].status = 'pausado'
      },
      escalonador_sjf () {
        let _this = this

        if ((_this.sjf.clock % 5 === 0) && (_this.sjf.clock !== 0)) {
          _this.conta_fila('sjf')
        }

        if (_this.verifica_fim('sjf') || _this.sjf.status === 'pausado') {
          return 1
        }

        _this.sjf.lista_bcp.forEach(function (bcp, index) {
          if (bcp['tempo_cheg'] === _this.sjf.clock) {
            bcp['estado'] = 'pronto'

            _this.sjf.fila_pronto.push(bcp)

            _this.sjf.fila_pronto.sort(function (a, b) {
              return a['tempo_cpu'] - b['tempo_cpu']
            })
          }
        })

        if ((_this.sjf.executando === '') & (_this.sjf.fila_pronto.length > 0)) {
          _this.sjf.executando = _this.sjf.fila_pronto[0]
          _this.sjf.executando['estado'] = 'executando'

          _this.sjf.executando['tempo_espera'][_this.sjf.executando['tempo_espera'].length - 1] = _this.sjf.clock - _this.sjf.executando['tempo_espera'][_this.sjf.executando['tempo_espera'].length - 1]
          if (_this.sjf.executando['executou'] === 0) {
            _this.sjf.executando['executou'] = 1
            _this.sjf.executando['tempo_resposta'] = _this.sjf.clock - _this.sjf.executando['tempo_cheg']
          }

          _this.sjf.fila_pronto.shift()
        }

        _this.adiciona_historico('sjf')

        if (_this.sjf.executando !== '') {
          _this.sjf.executando['tempo_exec'] += 1

          if ((_this.sjf.executando['fila_io'].length > 0) && (_this.sjf.executando['tempo_exec'] === _this.sjf.executando['fila_io'][0])) {
            _this.sjf.executando['fila_io'].shift()
            _this.bloqueia_processo('sjf', _this.sjf.clock, Math.floor((Math.random() * 9) + 1), _this.sjf.executando)

            _this.sjf.executando = ''
          } else if (_this.sjf.executando['tempo_exec'] === _this.sjf.executando['tempo_cpu']) {
            _this.sjf.executando['estado'] = 'terminado'
            _this.sjf.executando = ''
          }
        }

        _this.verifica_bloqueados('sjf', 'tempo_cpu')

        _this.sjf.clock += 1

        setTimeout(function () { _this.escalonador_sjf() }, 1000)
      },
      escalonador_prio () {
        let _this = this

        if ((_this.prio.clock % 5 === 0) && (_this.prio.clock !== 0)) {
          _this.conta_fila('prio')
        }

        if (_this.verifica_fim('prio') || _this.prio.status === 'pausado') {
          return 1
        }

        _this.prio.lista_bcp.forEach(function (bcp, index) {
          if (bcp['tempo_cheg'] === _this.prio.clock) {
            bcp['estado'] = 'pronto'

            _this.prio.fila_pronto.push(bcp)

            _this.prio.fila_pronto.sort(function (a, b) {
              return a['prioridade'] - b['prioridade']
            })
          }
        })

        if (_this.prio.fila_pronto.length > 0) {
          if (_this.prio.executando !== '') {
            if (_this.prio.executando['prioridade'] > _this.prio.fila_pronto[0]['prioridade']) {
              _this.prio.executando['estado'] = 'pronto'
              _this.prio.executando['tempo_espera'][_this.prio.executando['tempo_espera'].length - 1] = _this.prio.clock + 1

              _this.prio.fila_pronto.push(_this.prio.executando)
              _this.prio.fila_pronto.sort(function (a, b) {
                return a['prioridade'] - b['prioridade']
              })

              _this.prio.executando = _this.prio.fila_pronto[0]
              _this.prio.executando['estado'] = 'executando'

              _this.prio.executando['tempo_espera'][_this.prio.executando['tempo_espera'].length - 1] = _this.prio.clock - _this.prio.executando['tempo_espera'][_this.prio.executando['tempo_espera'].length - 1]

              _this.prio.fila_pronto.pop(0)
            }
          } else if (_this.prio.executando === '') {
            _this.prio.executando = _this.prio.fila_pronto[0]
            _this.prio.executando['estado'] = 'executando'

            _this.prio.executando['tempo_espera'][_this.prio.executando['tempo_espera'].length - 1] = _this.prio.clock - _this.prio.executando['tempo_espera'][_this.prio.executando['tempo_espera'].length - 1]

            _this.prio.fila_pronto.shift()
          }

          if (_this.prio.executando['executou'] === 0) {
            _this.prio.executando['executou'] = 1
            _this.prio.executando['tempo_resposta'] = _this.prio.clock - _this.prio.executando['tempo_cheg']
          }
        }

        _this.adiciona_historico('prio')

        if (_this.prio.executando !== '') {
          _this.prio.executando['tempo_exec'] += 1

          if ((_this.prio.executando['fila_io'].length > 0) && (_this.prio.executando['tempo_exec'] === _this.prio.executando['fila_io'][0])) {
            _this.prio.executando['fila_io'].shift()
            _this.bloqueia_processo('prio', _this.prio.clock, Math.floor((Math.random() * 9) + 1), _this.prio.executando)
            _this.prio.executando = ''
          } else if (_this.prio.executando['tempo_exec'] === _this.prio.executando['tempo_cpu']) {
            _this.prio.executando['estado'] = 'terminado'
            _this.prio.executando = ''
          }
        }

        _this.verifica_bloqueados('prio', 'prioridade')

        _this.prio.clock += 1

        setTimeout(function () { _this.escalonador_prio() }, 1000)
      },
      escalonador_rr () {
        let _this = this

        if ((_this.rr.clock % 5 === 0) && (_this.rr.clock !== 0)) {
          _this.conta_fila('rr')
        }

        if (_this.verifica_fim('rr') || _this.rr.status === 'pausado') {
          return 1
        }

        _this.rr.lista_bcp.forEach(function (bcp, index) {
          if (bcp['tempo_cheg'] === _this.rr.clock) {
            bcp['estado'] = 'pronto'
            _this.rr.fila_pronto.push(bcp)
          }
        })

        if ((_this.rr.executando === '') && (_this.rr.fila_pronto.length > 0)) {
          _this.rr.executando = _this.rr.fila_pronto[0]
          _this.rr.executando['estado'] = 'executando'
          _this.rr.executando['tempo_espera'][_this.rr.executando['tempo_espera'].length - 1] = _this.rr.clock - _this.rr.executando['tempo_espera'][_this.rr.executando['tempo_espera'].length - 1]

          if (_this.rr.executando['executou'] === 0) {
            _this.rr.executando['executou'] = 1
            _this.rr.executando['tempo_resposta'] = _this.rr.clock - _this.rr.executando['tempo_cheg']
          }

          _this.rr.fila_pronto.shift()
        }

        _this.adiciona_historico('rr')

        if (_this.rr.executando !== '') {
          _this.rr.executando['tempo_exec'] += 1
          _this.rr.executando['quantum'] += 1

          if ((_this.rr.executando['fila_io'].length > 0) && (_this.rr.executando['tempo_exec'] === _this.rr.executando['fila_io'][0])) {
            _this.rr.executando['fila_io'].shift()
            _this.rr.executando['quantum'] = 0
            this.bloqueia_processo('rr', _this.rr.clock, Math.floor((Math.random() * 9) + 1), _this.rr.executando)
            _this.rr.executando = ''
          } else if (_this.rr.executando['tempo_exec'] === _this.rr.executando['tempo_cpu']) {
            _this.rr.executando['estado'] = 'terminado'
            _this.rr.executando = ''
          } else if (_this.rr.executando['quantum'] === _this.rr.quantum) {
            _this.rr.fila_pronto.push(_this.rr.executando)
            _this.rr.executando['quantum'] = 0
            _this.rr.executando['estado'] = 'pronto'
            _this.rr.executando['tempo_espera'][_this.rr.executando['tempo_espera'].length - 1] = _this.rr.clock + 1

            _this.rr.executando = ''
          }
        }

        _this.verifica_bloqueados('rr', '')

        _this.rr.clock += 1

        setTimeout(function () { _this.escalonador_rr() }, 1000)
      },
      addProcessos () {
        let _this = this

        this.form.validateFields(async (err, values) => {
          if (!err) {
            _this.sjf.quantum = parseInt(values.quantum)
            _this.prio.quantum = parseInt(values.quantum)
            _this.rr.quantum = parseInt(values.quantum)

            let proc = values.arquivo.split('\n')
            proc.forEach(function (p) {
              let aux = p.split(' ').map(Number)

              _this.sjf.lista_bcp.push({
                'id': aux[0],
                'tempo_cpu': aux[1],
                'prioridade': aux[2],
                'tempo_cheg': (aux[3]),
                'fila_io': aux.slice(4, aux.length),
                'tempo_exec': 0,
                'estado': '',
                'cheg_bloqueado': 0,
                'tempo_bloqueado': 0,
                'tempo_espera': [aux[3]],
                'tempo_resposta': 0,
                'executou': 0,
                'quantum': 0,
                'historico': []
              })

              _this.prio.lista_bcp.push({
                'id': aux[0],
                'tempo_cpu': aux[1],
                'prioridade': aux[2],
                'tempo_cheg': (aux[3]),
                'fila_io': aux.slice(4, aux.length),
                'tempo_exec': 0,
                'estado': '',
                'cheg_bloqueado': 0,
                'tempo_bloqueado': 0,
                'tempo_espera': [aux[3]],
                'tempo_resposta': 0,
                'executou': 0,
                'quantum': 0,
                'historico': []
              })

              _this.rr.lista_bcp.push({
                'id': aux[0],
                'tempo_cpu': aux[1],
                'prioridade': aux[2],
                'tempo_cheg': (aux[3]),
                'fila_io': aux.slice(4, aux.length),
                'tempo_exec': 0,
                'estado': '',
                'cheg_bloqueado': 0,
                'tempo_bloqueado': 0,
                'tempo_espera': [aux[3]],
                'tempo_resposta': 0,
                'executou': 0,
                'quantum': 0,
                'historico': []
              })
            })

            _this.visible = false
          }
        })
      },
      handleCancel (e) {
        this.estatisticas.visible = false
      }
    }
  }
</script>

<style>
  .scroller {
    height: 100%;
    overflow-x: auto;
    white-space: nowrap;
  }

  .accordion {
    border-radius: 4px;
    margin-bottom: 24px;
    border: 0;
    overflow: hidden;
  }

  .ant-pagination {
    display: none;
  }
</style>