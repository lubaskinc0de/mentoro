## Crudik - Yet another шаблон для крудов
![coverage](https://gitlab.prodcontest.ru/team-6/prod-backend/badges/master/coverage.svg?min_good=80&min_acceptable=70&min_medium=50)

1. Бизнес логику пишете в application (взаимодействие с моделями, удаление, обновление, создание). Желательно под каждую бизнес-операцию отдельный файлик с классом команды.

2. Логику чтения лучше выносить в adapters/gateway

3. Модели алхимии описываются в models/, не забудьте экспоузить их в ините чтобы алембик их подхватил

4. В presentation находятся HTTP эндпоинты, в основном они просто вызывают эти самые команды application.

5. В проекте используется dishka, настройки IoC контейнера находятся в bootstrap/di

6. По умолчанию загружается базовая конфигурация сервера + подключения к бд + доступен клиент редис + настроены миграции

7. Для примера взят фастапи но можно взять любой фреймворк

8. По умолчанию у всех эндпоинтов есть префикс /api

### Проект служит шаблоном для хакатонов/MVP

Установить зависимости + зависимости для линтинга + запустить линтеры

```
pip install -e ".[lint]"
mypy
ruff check
ruff format
```

Запуск приложения:
```
docker compose up --build
```

По умолчанию приложение при запуске само запускает миграции бд, чтобы сгенерировать миграцию поменяйте команду в ENTRYPOINT образа на 

```
crudik migrations autogenerate имя_миграции
```
