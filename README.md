# API Bancaria v2

API REST para operacoes bancarias, construida com Django REST Framework. Versao expandida com transferencia atomica entre contas.

## Funcionalidades

- Autenticacao via JWT
- Isolamento de dados por usuario
- Multiplas contas por usuario
- Deposito e saque
- Transferencia entre contas usando transacao atomica do banco de dados (tudo ou nada)
- Validacao de saldo insuficiente
- Historico de transacoes por conta, com rastreio da conta relacionada em transferencias

## Stack

- Python / Django
- Django REST Framework
- djangorestframework-simplejwt
- SQLite

## Endpoints

POST /api/token/ - obter access e refresh token
GET/POST /api/accounts/ - listar ou criar contas
POST /api/accounts/{id}/deposit/ - depositar na conta
POST /api/accounts/{id}/withdraw/ - sacar da conta
POST /api/accounts/{id}/transfer/ - transferir para outra conta

## Como rodar localmente

python -m venv venv
venv\Scripts\activate
pip install django djangorestframework djangorestframework-simplejwt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

## Exemplo de transferencia

POST /api/accounts/1/transfer/
Authorization: Bearer <access_token>

{
  "to_account": 2,
  "amount": "300.00"
}

A operacao debita a conta de origem, credita a conta de destino e cria dois registros de transacao (transfer_out e transfer_in), tudo dentro de uma transacao atomica do banco. Se qualquer etapa falhar, nada e alterado.
