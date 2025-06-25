 нужно доработать несколько сервисов чтобы авторизация в них происходила через единую точку с возможностью авторизации как по АПИ, так и по MQTT. С хранением сессий, логированием и панелью управления для создания пользователей и назначения прав


21.06.2025 17:09

Авторизация в прошиваторе сейчас:
```python
 data=json.dumps({'username':username, 'company': os.getenv('COMPANY')})
```

Принимающий:
```python
data = json.loads(request.data)
if chat_id := db.get_user_chat_id(data['username'], 'company'):
    send_password_to_messenger(data['username'], chat_id, data['company'])
```

С полученым через месенджер паролем:
```python
data=json.dumps({'username': username, 'password': password, 'new_firm_keeper': new_firm_keeper})
```
Ответ:
```python
json_response = response.json()
access_token = json_response.get("access_token")
token_storage[f'{username}_key'] = access_token
```

Запрос файла:
```python
token = token_storage.get(f'{username}_key')
headers = { 'Authorization': f'Bearer {token}'}
response = await client.get(url, headers=headers)
f.write(response.content)
```