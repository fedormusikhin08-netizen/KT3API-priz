# КТ3 API tests

Автотесты petstore.swagger.io — пользователи (user) и заказы (store), 4 CRUD-запроса на каждую сущность.

## Файлы

- base_request.py — базовый класс запросов
- test_user.py — тесты пользователя
- test_store.py — тесты заказов и инвентаря
- mock_petstore.py — локальный заменитель petstore

## Запуск

Открыть папку в Visual Studio, поставить библиотеки (pip install -r requirements.txt), запустить python -m pytest -v.

petstore может отдавать 403 по региону. Тогда в отдельной вкладке поднимается python mock_petstore.py, а в переменных окружения указывается PETSTORE_BASE_URL=http://127.0.0.1:8090/v2
