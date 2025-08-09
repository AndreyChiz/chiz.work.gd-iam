https://medium.com/%40kavicastelo/secure-auth-flow-for-spas-access-token-in-memory-refresh-token-in-cookie-ac6409e208b5

    Пользователь входит в систему → фронтенд отправляет учётные данные на сервер авторизации.

    Сервер авторизации отвечает:

        Access Token (фронтенд хранит в памяти)

        Refresh Token (устанавливается в cookie с флагом HttpOnly)

    Фронтенд делает запросы к API, используя access token из памяти.

    Access token истекает → фронтенд отправляет тихий запрос на обновление (браузер автоматически включает HttpOnly-cookie).

    Сервер авторизации проверяет refresh token, возвращает новый access token.

    Пользователь продолжает работу без перебоев ✨

При выходе из системы:

    Удалить cookie

    Очистить access token из памяти