# Project_RT

Тестирование формы авторизации Личного кабинета Ростелеком https://b2c.passport.rt.ru

По заданию тестирования необходимо:

Протестировать требования.

Разработать тест-кейсы (не менее 15).

Провести автоматизированное тестирование продукта (не менее 15 автотестов). Заказчик ожидает по одному автотесту на каждый написанный тест-кейс.

Оформите свой набор автотестов в GitHub.

Оформить описание обнаруженных дефектов ( составить баг-репорты). Во время обучения вы работали с разными сервисами и шаблонами, используйте их для оформления

тест-кейсов и обнаруженных дефектов. (если дефекты не будут обнаружены, то составить описание трех дефектов).

Для составления и написания тест-кейсов использовались такие техники тест-дизайна как: классы эквивалентности, анализ граничных значений, предугадывание ошибок.

Проведены позитивные и негативные тесты. 

Проведено тестирование страницы Авторизация: 

Проверка соответствия ТЗ и элементов, кнопок на странице.

Проверка соответствия ТЗ и отображаемых ошибок, действий при нажатии кнопок. 

Тестирование страницы Регистрация :

Проверка соответствия ТЗ и элементов, кнопок на странице.

Структура проекта:

base_data.py - базовые классы, процедуры, функции и локаторы для автотестов

settings.py - регистрационные данные для автотестов

tests_rt.py - набор автотестов

Запуск тестов:

Установить все внешние зависимости командой pip install pytest, pytest-selenium, termcolor, selenium

Скачать версию Selenium WebDriver для Chrome 

Запустить тесты можно прописав команду:

python -m pytest -v --driver Chrome --driver-path <Путь до вебдрайвера>\chromedriver.exe tests_rt.py 