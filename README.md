# Описание проекта.
Разработка функций для взаимодействия с банковскими транзакциями.

---
## Установка
1. Клонирование репозитория
```
https://github.com/ragveil/coursework_1.git
```
2. Установка зависимостей
```
poetry install
```
3. Для работы с внешним API необходимо создать файл `.env` в корневой директории проекта и добавить в него переменную окружения:
```
API_TOKEN=your_api_token_here
```
---
### Модуль `main.py`
Содержит вызовы основных функций для удобства ознакомления с функционалом.

---
## Модуль `views.py`
Объединяет работу основных функций проекта, страница "События".

### Пример использования модуля `views.py`
```python
from src.views import get_events_json

result = get_events_json('21.03.2020', 'Y')

print(result)   # Вывод корректного JSON-ответа.
```
---
## Модуль `utils.py`
Содержит основные функции страницы "События": 
`form_data_frame` - формирует dataframe из excel-файла
`get_period` - вносит изменения в dataframe в соответствии с выбранной датой и временным периодом.
Варианты:
* `D` - транзакции на текущую дату;
* `W` - транзакции за неделю, начиная с понедельника;
* `M` - транзакции за месяц, начиная с первого дня месяца;
* `Y` - транзакции за год, начиная с первого дня года;
* `ALL` - транзакции за всё время.

`get_expenses` - рассчитывает общие траты по категориям в порядке убывания.
`get_income` - рассчитывает общие доходы по категориям в порядке убывания.
`get_currency_rates` - запрашивает текущие курсы валют посредством API.
`get_stock_rates` - запрашивает текущую стоимость акций посредством API.
---
## Модуль `services.py`
Содержит вспомогательные функции для поиска по транзакциям:
`search_items` - обеспечивает поиск по ключевому слову в категории или описании.
`search_telephone_numbers` - обеспечивает поиск транзакций, содержащих в описании номеров телефонов.
`search_personal_transactions` - обеспечивает поиск переводов физическим лицам.

### Примеры использования модуля `services.py`
```python
from src.services import list_of_transactions, search_item, search_personal_transactions, search_telephone_numbers

keyword_search = search_item(list_of_transactions, 'Супермаркеты')
print(keyword_search)   # Выведет транзакции по категории "Супермаркеты"

numbers_search = search_telephone_numbers(list_of_transactions)
print(numbers_search)   # Выведет транзакции, содержащие номера телефонов

personal_search = search_personal_transactions(list_of_transactions)
print(personal_search)  # Выведет транзакции, содержащие переводы физическим лицам.
```
## Модуль `reports.py`
Содержит вспомогательные функции для формирования отчетов:
`spending_by_category` - формирует отчет о тратах по определенной категории за последние три месяца от указанной даты.
`spending_by_weekday` - формирует отчет о средних тратах по дням недели за последние три месяца от указанной даты.
`spending_by_workday` - формирует отчет о средних тратах по выходным и будним дням за последние три месяца.

### Примеры использования модуля `services.py`
```python
from src.reports import data_frame, spending_by_category, spending_by_weekday, spending_by_workday

category_report = spending_by_category(data_frame, 'Супермаркеты', '21.03.2020')
print(category_report)  # Выведет траты по категории "Супермаркеты" за три месяца.

weekday_report = spending_by_weekday(data_frame, '21.03.2020')
print(weekday_report)   # Выведет средние траты по дням недели за три месяца.

workday_report = spending_by_workday(data_frame, '21.03.2020')
print(workday_report)   # Выведет средние траты по будним и выходным дням за три месяца.

```
## Модуль `logger.py` и декоратор `save_to_file` модуля `reports.py`
Модуль `logger.py` предназначен для логирования функций и отслеживания работы разных модулей.
Декоратор `save_to_file` модуля `reports.py` предназначен для записи результатов функций в файл отчета.
Логи и файлы отчета находятся в папке `logs` проекта.
---
## Тестирование
Все тесты выполняются без ошибок, тестами покрыто 91% кода.

---