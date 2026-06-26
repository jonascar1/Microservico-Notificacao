import requests

url = "http://127.0.0.1:8002/api/notificacoes/criar/"

headers = {
    "X-Api-Key": "SEU_HASH",
}

dados = {
    "user_id": 1,
    "titulo": "Teste Python",
    "mensagem": "Notificação enviada pelo script."
}

r = requests.post(url, json=dados, headers=headers)

print(r.status_code)
print(r.json())