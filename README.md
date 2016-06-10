# Linguagem Fazedores


A linguagem Fazedores é uma linguagem de alto nível bem semelhante a linguagem natural que vai permitir usar os seguintes dispositivos de prototipação eletrônica:

- LED;

- Buzzer;

- LCD;

- Botão;

- Sensor de toque;

- Potenciômetro;

Para isso usaremos parte da especificação da linguagem LA e vamos adicionar algumas funções de alto nível próprias para manipulação dos dispositivos listados anteriormente. O objetivo final dessa aplicação é que a partir da linguagem Fazedores seja possível executar comandos em uma placa arduino que terá um servidor Python, no nosso caso será um Intel Edison com um servidor Python usando a biblioteca mraa para executar os comandos.

## Estrutura

### MVC:
Model: vai ser responsável por todo o interpretador. 
 * Pega o que vem da view/controller e interpreta. 
    * Se der erro retorna para view e ela apresenta o erro.
    * Se funcionar chama uma função que envia os comandos para o servidor da placa Edison, retorna pra view mensagem de sucesso;

Controller:

View:
  * Uma view com instruções;
  * Uma view para testar conexão com a placa;
  * Uma view para o usuário digitar;
  * Outra view apresentando se deu erro ou não.

### Servidor Edison:
* Socket esperando uma mensagem, de inicio um servidor monothread;
* Uso do mraa: https://github.com/intel-iot-devkit/mraa
