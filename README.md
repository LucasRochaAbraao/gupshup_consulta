# gupshup consultas

Esse script realiza a consulta de saldo disponível no gupshup para informar através de email. Eu uso ele em um servidor linux com 2 cron jobs. O primeiro usa o argumento `saldo_check` para verificar a cada 15 minutos o saldo disponível, e enviar um email com
mensagem personalizada caso esteja abaixo da média. O outro usa o argumento `saldo_atual` para enviar um email toda segunda feira às 9h a informação.

Para instalar, configurar e executar o script, siga as instruções abaixo.

## instalação
Primeiro é necessário instalar o pacote de gerenciamento de ambiente e pacotes `pipenv`, para um melhor gerenciamento dos seus projetos.
```
pip3 install pipenv
```
Em seguida, instale o pacote `requests`.
```
pipenv install requests
```
Para finalizar, dê permissão de execução ao script principal.
```
sudo chmod +x email_aviso.py
```


## Configuração

Renomeie o `config_sample.py` para `config.py` e preencha com as informações de credenciais do e-mail. Coloque também o `api_token` fornecido na plataforma gupshup.

No meu cenário, utilizo uma conta do gmail para enviar os e-mails. Para autenticar pelo gmail, foi necessário habilitar a opção de login "menos segura" para aplicativos, nesse [link](https://myaccount.google.com/lesssecureapps). *Eu recomendo muito criar uma conta apenas para o envio desses e-mails*, para não perder uma conta com dados pessoais por ter que utilizar uma opção de autenticação menos segura.

No email_aviso.py, coloque as informações corretas nas variáveis de configuração dos e-mails, de acordo com o arquivo config.py.


## Execução

Primeiro teste se o `gupshup_api_saldo.py` está coletando os dados corretamente. Para isso, basta executar esse script individualmente. Ele deve retornar a *quantidade* de mensagens disponíveis no gupshup, ou *False*.
```
python3 gupshup_api_saldo.py
```

Após ter validado a coleta dos dados do gupshup, execute o arquivo email_aviso.py com um dos argumentos `saldo_check` ou `saldo_atual`, da seguinte forma:
```
./email_aviso.py saldo_atual
./email_aviso.py saldo_check
```

Para automatizar esse processo, utilizo o cronjob dos sistemas linux da seguinte forma.

```
# rodar quando o minuto de cada hora for divisível por 15 (cada 15 minutos)
*/15 * * * * /home/lucas/gupshup.py saldo_check
```
```
# rodar toda segunda feira às 09:00
0 9 * * 1 /home/lucas/gupshup.py saldo_atual
```
