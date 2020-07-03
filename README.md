# gupshup consultas

Esse script realiza a consulta de saldo disponível
no gupshup para informar através de email. Eu uso
ele em um servidor linux com 2 cron jobs. 1 usa o
argumento "saldo_check" para verificar a cada 15
minutos o saldo disponível, e enviar um email com
mensagem personalizada caso esteja abaixo da média.
O outro usa o argumento "saldo_atual" para enviar
um email toda segunda feira às 9h a informação.
