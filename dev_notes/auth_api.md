Пользователь логинится — сервер возвращает:

    Access токен в теле ответа (JSON)

    Refresh токен — в HttpOnly cookie

Клиент сохраняет access токен в памяти и добавляет в заголовок:

Authorization: Bearer <access_token>

При каждом API запросе access токен используется для авторизации.

Если access токен истек, клиент делает запрос к /auth/refresh:

    В запросе refresh токен автоматически отправляется браузером в cookie

    Сервер проверяет и, если токен валидный, выдает новый access токен

Клиент обновляет access токен в памяти и продолжает работу.




🔐 1. POST /auth/login

Описание: Аутентификация пользователя и выдача access_token + refresh_token.

Форма данных:

{
  "username": "user@example.com",
  "password": "your_password"
}

Ответ:

{
  "access_token": "<JWT>",
  "refresh_token": "<JWT>",
  "token_type": "bearer"
}

🔁 2. POST /auth/refresh

Описание: Обновление access_token по действующему refresh_token.

Форма данных:

{
  "refresh_token": "<JWT>"
}

Ответ:

{
  "access_token": "<NEW_JWT>",
  "token_type": "bearer"
}

🧾 3. GET /auth/me

Описание: Получение информации о текущем пользователе по access_token.

Заголовок запроса:

Authorization: Bearer <access_token>

Ответ:

{
  "id": 1,
  "username": "user",
  "is_admin": false,
  ...
}

🚪 4. POST /auth/logout (опционально)

Описание: Инвалидация refresh-токена. Полезно, если используешь список отозванных токенов или хранишь refresh'и в Redis/БД.
✏️ 5. POST /auth/register (если нужна регистрация)

Описание: Регистрация нового пользователя.
🧯 6. POST /auth/revoke (опционально)

Описание: Явная инвалидация токенов (например, для выхода со всех устройств).
📌 Итого — базовые ручки:
Метод	Путь	Назначение
POST	/auth/login	Логин и получение токенов
POST	/auth/refresh	Обновление access_token
GET	/auth/me	Текущий пользователь
POST	/auth/logout	Выход/отзыв refresh токена
POST	/auth/register	Регистрация
POST	/auth/revoke	Инвалидация токенов (опц.)
