# ВШЭ‑Банк 

* Учебный проект по конструированию ПО на Python
* Цель: смоделировать домен финансового учета, соблюсти SOLID и GRASP, применить паттерны GoF, использовать DI‑контейнер
* Приложение ведет счета, категории и операции. Делает аналитику. Импортирует/экспортирует данные. Пересчитывает балансы. Измеряет время пользовательских сценариев. Использует базу данных

## Функции приложения

1. Создать счет
2. Список счетов
3. Создать категорию
4. Список категорий
5. Создать операцию
6. Список операций
7. Аналитика: разница за период
8. Аналитика: разница за период для аккаунта
9. Аналитика: по категориям за период
10. Экспорт данных (json/yaml)
11. Импорт данных (json/yaml)
12. Пересчитать балансы (автоматически)
13. Пересчитать баланс аккаунта вручную
14. Пересчитать баланс аккаунта автоматически
15. Показать статистику сценариев

## Инструкция по запуску

1. Установите Python 3.12 и git
2. Склонируйте репозиторий 
- Windows:
```
git clone https://github.com/chadamik2/software_design_HW1.git
cd software_design_HW1
```
- macOS/Linux:
```
git clone https://github.com/chadamik2/software_design_HW1.git
cd software_design_HW1
```
3. Откройте папку `software_design_HW2` через **File → Open…**
4. Интерпретатор: **File → Settings → Project → Python Interpreter**, добавьте Virtualenv из `.venv`
5. Конфигурация запуска:

   * **Run → Edit Configurations → + → Python**
   * **Name:** `HSE Bank CLI`
   * **Script path:** `main.py`
   * **Working directory:** корень проекта `src`
   * Интерпретатор: ваше `.venv`
   * Сохраните и запускайте
6. Чтобы использовать импорт и экспорт в yaml, установите его
   ```
   pip install yaml
   ```

## Структура проекта

```
src/
│
├── cli/                         # Входной слой (интерфейс командной строки)
│   ├── app.py                   # Точка запуска CLI-приложения
│   └── di.py                    # Конфигурация зависимостей (Dependency Injection)
│
├── commands/                    # Команды приложения (application layer)
│   ├── base_command.py          # Базовый класс для всех команд
│   ├── create_commands.py       # Создание сущностей (счёт, операция, категория)
│   ├── io_commands.py           # Импорт и экспорт данных (JSON, YAML)
│   ├── list_commands.py         # Отображение списка данных
│   ├── show_stats_commands.py   # Аналитика и статистика сценариев
│   ├── recalc_balance_commands.py # Пересчёт балансов
│   ├── analytics_commands.py    # Отчёты и аналитические операции
│   └── input_processing.py      # Обработка пользовательского ввода
│
├── domain/                      # Бизнес-логика (ядро системы)
│   ├── entities.py              # Доменные сущности (BankAccount, Category, Operation)
│   ├── exceptions.py            # Ошибки бизнес-уровня
│   └── factory.py               # Фабрика создания сущностей
│
├── io/                          # Ввод-вывод данных
│   ├── exporters/               # Экспорт данных
│   │   └── exporters.py         # Экспорт в JSON, YAML
│   └── importers/               # Импорт данных
│       ├── concrete_importers.py
│       └── data_importer.py
│
├── persistence/                 # Слой работы с данными (инфраструктура)
│   ├── dao/                     # DAO — прямое взаимодействие с БД
│   │   ├── bank_account_dao.py
│   │   ├── category_dao.py
│   │   └── operation_dao.py
│   │
│   ├── repositories/            # Репозитории — уровень абстракции над DAO, добавление кэша
│   │   ├── abstract_repository.py
│   │   ├── bank_account_repository_proxy.py
│   │   ├── category_repository_proxy.py
│   │   └── operation_repository_proxy.py
│   │
│   └── sqlite_db.py             # Инициализация и управление SQLite-базой
│
├── services/                    # Прикладные сервисы и фасады
│   ├── analytics_facade.py
│   ├── balance_service.py
│   ├── bank_account_facade.py
│   ├── category_facade.py
│   └── operation_facade.py
│
└── main.py                      # Главная точка входа

```

## Применение SOLID

1. **S — Single Responsibility**
   Одна причина для изменения у каждого класса

   * `domain/factory.py` — только создание и валидация доменных объектов
   * `persistence/dao` — только доступ к SQLite и SQL‑схема
   * `persistence/repositories` — только кэш‑прокси над DAO
   * `services/facades` — только бизнес‑сценарии
   * `io/importers` — только импорт по шаблону
   * `io/exporters` — только экспорт через посетителя
   * `patterns/commands` — только контракт команд и замер времени
   * `cli/app.py` — только консольный UI и оркестрация команд

2. **O — Open/Closed**
   Расширяемо новыми вариантами без модификации существующего

   * Новые форматы импорта: унаследоваться от `DataImporter` и реализовать `_parse`
   * Новые форматы экспорта: добавить реализацию `DataExporter` рядом и вернуть её в `get_exporter`
   * Новые источники хранения: новая реализация DAO и репозитория, интерфейсы не меняются

3. **L — Liskov Substitution**
   Подклассы и конкретные реализации взаимозаменяемы через абстракции

   * Экспортеры и импортеры подставимы вместо базовых типов в фабриках `get_*`
   * Репозитории подставимы вместо абстрактного `Repository[T]`
   * Конкретные команды подставимы вместо `Command`

4. **I — Interface Segregation**
   Узкие интерфейсы вместо жирных

   * `Repository[T]` объявляет только `add/update/delete/get/list_all`
   * Команда `Command` объявляет только `name` и `execute`

5. **D — Dependency Inversion**
   Верхний уровень зависит от абстракций, а не реализаций

   * CLI получает фасады и реестры через конструкторы команд
   * Связи настраиваются в `cli/app.build_container`

## GRASP

* **High Cohesion**

  * Фасады содержат правила домена по своей области: `BankAccountFacade`, `CategoryFacade`, `OperationFacade`, `AnalyticsFacade`, `BalanceService`
  * Импорт и экспорт изолированы по ответственности
* **Low Coupling**

  * Слои отделены: CLI → Фасады → Репозитории → DAO → SQLite
  * Инъекция зависимостей через контейнер. Минимум прямых связей
  * Импортеру передаются фасады и фабрика. Нет прямых SQL

* **Controller**
  * `cli/app.py` управляет сценариями, не зависит от бизнес-логики

* **Information Expert**
  * пересчет баланса в `BalanceService`, где хранятся операции и категории, аналитика в `AnalyticsFacade`, где хранятся операции, категории и аккаунты

## Паттерны GoF и где применены

1. **Facade**

   * `services/`: `BankAccountFacade`, `CategoryFacade`, `OperationFacade`, `AnalyticsFacade`, `BalanceService`
   * Скрывают детали репозиториев, дают простые методы сценариев

2. **Command**

   * `commands/base_command` интерфейс `Command`
   * `commands/`: `CreateAccountCommand`, `ListAccountsCommand`, `CreateCategoryCommand`, `ListCategoriesCommand`, `CreateOperationCommand`, `ListOperationsCommand`, `NetDiffCommand`, `GroupByCategoryCommand`, `ExportCommand`, `ImportCommand`, `RecalcOneBalanceCommand`, `RecalcAllBalanceCommand`, `ShowStatsCommand`
   * Каждый пункт меню — отдельная команда

3. **Decorator**

   * `TimedCommandDecorator` в `commands/base_command.py`
   * Оборачивает любую команду и пишет подсчитанное время в `StatsRegistry`

4. **Template Method**

   * `io/importers/data_importers.py`: базовый `DataImporter.import_data()` фиксирует алгоритм: чтение → парсинг → сохранение → пересчет
   * Подклассы `JsonImporter`, `YamlImporter`,  переопределяют только `_parse`

5. **Visitor**

   * `io/exporters/exporters.py`: `DataExportVisitor` обходит сущности
   * Экспортеры используют посетителя и не знают деталей сущностей

6. **Factory**

   * `domain/factory.py`: `DomainFactory` создает `BankAccount`, `Category`, `Operation`
   * Гарантирует единообразные `id`

7. **Proxy**

   * `persistence/repositories`: `*RepositoryProxy` держат in‑memory кэш и пишут в SQLite
   * Чтение и запись как в кэш, так и в базу данных

8. **Strategy**

   * `io/exporters/exporters.py`: `DataExporter` является базовым классом, а `JsonExporter` и `YamlExporter` реализуют стратегии для экспорта
## DI‑контейнер

* `cli/di.py`: минимальный контейнер с синглтонами и фабриками
* Конфигурация в `cli/app.build_container`
* Объекты верхнего уровня не создают зависимости напрямую. Это упрощает тестирование и замену инфраструктуры
