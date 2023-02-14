
# python -m pytest -v --driver Chrome --driver-path chromedriver.exe tests_rt.py
# набор автотестов

from time import sleep
from base_data import *
from settings import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_01_page_right_left(selenium):
    """ Проверяем форму «Авторизация», разделенную вертикально на два блока
    Сохраняем скриншот страницы Страница авторизации.jpg
    Проверяем отсутствие таба с текстом 'Номер'"""

    # Переходим на страницу авторизации
    page = AuthForm(selenium)
    # Сохраняем скриншот
    page.driver.save_screenshot('Страница авторизации.jpg')
    # Находим элементы на правой и левой странице, в соответствии с требованиями
    assert page.page_right.text == 'Авторизация'
    assert page.page_left.text == 'Личный кабинет'
    # Отсутствие таба с текстом "Номер"
    assert page.find_element(By.XPATH, "//*[@id='t-btn-tab-phone']").text != "Номер"


def test_02_auth_page_tab(selenium):
    """Проверка меню выбора типа аутентификации"""

    # Переходим на страницу авторизации
    page = AuthForm(selenium)

    # Таб выбора аутентификации по номеру телефона
    page.tab_phone.click()
    # Заполнение полей 'Телефон' и 'Почта'
    page.username.send_keys(valid_phone)
    page.password.send_keys(valid_pass)
    # Получаем значение поля плейсхолдера
    assert page.placeholder.text == 'Мобильный телефон'

    # очистка поля логина
    page.username.send_keys(Keys.CONTROL, 'a')
    page.username.send_keys(Keys.DELETE)
    # очистка поля пароля
    page.password.send_keys(Keys.CONTROL, 'a')
    page.password.send_keys(Keys.DELETE)

    # Таб выбора аутентификации по почте
    page.tab_email.click()
    # Заполнение полей 'Телефон' и 'Почта'
    page.username.send_keys(valid_email)
    page.password.send_keys(valid_pass)
    # Получаем значение поля плейсхолдера
    assert page.placeholder.text == 'Электронная почта'

    # очистка поля логина
    page.username.send_keys(Keys.CONTROL, 'a')
    page.username.send_keys(Keys.DELETE)
    # очистка поля пароля
    page.password.send_keys(Keys.CONTROL, 'a')
    page.password.send_keys(Keys.DELETE)

    # Таб выбора аутентификации по логину
    page.tab_login.click()
    # ввод логина и пароля
    page.username.send_keys(my_login)
    page.password.send_keys(valid_pass)
    # Получаем значение поля плейсхолдера
    assert page.placeholder.text == 'Логин'

    # очистка поля логина
    page.username.send_keys(Keys.CONTROL, 'a')
    page.username.send_keys(Keys.DELETE)
    # очистка поля пароля
    page.password.send_keys(Keys.CONTROL, 'a')
    page.password.send_keys(Keys.DELETE)

    # Таб выбора аутентификации по лицевому счёту
    page.tab_l_s.click()
    # ввод лицевого счёта и пароля
    page.username.send_keys(personal_account)
    page.password.send_keys(valid_pass)
    # Получаем значение поля плейсхолдера
    assert page.placeholder.text == 'Лицевой счёт'


def test_03_by_phone(selenium):
    """Проверяем, что по умолчанию выбрана форма авторизации по телефону."""

    # Переходим на страницу авторизации
    page = AuthForm(selenium)
    # Получаем значение поля плейсхолдера 'Мобильный телефон'
    assert page.placeholder.text == 'Мобильный телефон'


def test_04_positive_by_phone(selenium):
    """Проверка позитивного сценария авторизации по телефону."""

    # Переходим на страницу авторизации
    page = AuthForm(selenium)
    # ввод телефона и пароля
    page.username.send_keys(valid_phone)
    page.password.send_keys(valid_pass)
    # Нажимаем кнопку 'Войти'
    page.btn_click()
    # Проверяем, что открывшаяся страница не страница авторизации
    assert page.get_current_url() == '/account_b2c/page'


def test_05_positive_by_email(selenium):
    """Проверка позитивного сценария авторизации по почте."""

    # Переходим на страницу авторизации
    page = AuthForm(selenium)
    # ввод почты и пароля
    page.username.send_keys(valid_email)
    page.password.send_keys(valid_pass)
    # Нажимаем кнопку 'Войти'
    page.btn_click()
    # Проверяем, что открывшаяся страница не страница авторизации
    assert page.get_current_url() == '/account_b2c/page'


def test_06_get_code(selenium):
    """Проверка получения временного кода на телефон и открытия формы для ввода кода"""

    # Переходим на страницу авторизации
    page = CodeForm(selenium)
    # ввод телефона
    page.address.send_keys(valid_phone)
    # Нажимаем кнопку получить код
    page.get_click()
    # В открывшейся странице находится поле ввода для кода
    rt_code = page.driver.find_element(By.ID, 'rt-code-0')
    assert rt_code


def test_07_negative_by_phone(selenium):
    """Проверка негативного сценария авторизации по телефону"""

    # Переходим на страницу авторизации
    page = AuthForm(selenium)
    # ввод телефона и пароля
    page.username.send_keys(invalid_phone)
    page.password.send_keys(valid_pass)
    # Нажимаем кнопку 'Войти'
    page.btn_click()
    # Получаем сообщение об ошибке.
    err_mess = page.driver.find_element(By.ID, 'form-error-message')
    assert err_mess.text == 'Неверный логин или пароль'
    # Текст "Забыл пароль" перекрашивается в оранжевый цвет
    assert "rt-link--orange" in page.find_element(By.XPATH, '//*[@id="forgot_password"]').get_attribute('class')


def test_08_negative_by_email(selenium):
    """Проверка негативного сценария авторизации по почте"""

    # Переходим на страницу авторизации
    page = AuthForm(selenium)
    # ввод почты и пароля
    page.username.send_keys(invalid_email)
    page.password.send_keys(valid_pass)
    # Нажимаем кнопку 'Войти'
    page.btn_click()
    # Получаем сообщение об ошибке.
    err_mess = page.driver.find_element(By.ID, 'form-error-message')
    assert err_mess.text == 'Неверный логин или пароль'
    # 'Текст' Забыл пароль перекрашивается в оранжевый цвет
    assert "rt-link--orange" in page.find_element(By.XPATH, '//*[@id="forgot_password"]').get_attribute('class')


def test_09_auth_page_tab(selenium):
    """ Проверка перехода в форму восстановления пароля и её открытия
        Проверка автосмены "таб ввода" на странице восстановления пароля
        Проверка наличия капчи на странице восстановления пароля"""

    # Переходим на страницу авторизации
    page = AuthForm(selenium)
    # клик по надписи "Забыл пароль"
    page.forgot.click()
    # Клик по надписи 'Телефон'
    tab_phone = page.find_element(By.ID, 't-btn-tab-phone')
    tab_phone.click()
    captcha_image = page.find_element(By.XPATH, "//*[@class='rt-captcha__image']")
    # ввод почты и символов в значение капчи
    page.find_element(By.ID,'username').send_keys(valid_phone)
    page.find_element(By.ID, 'captcha').send_keys('_')
    # Получаем плейсхолдер с надписью 'Мобильный телефон'
    assert page.find_element(By.XPATH,
                             '//*[@id="page-right"]/div//div/form/div[1]//div/span[2]').text== 'Мобильный телефон'
    # на странице есть изображение капчи
    assert captcha_image

    # очистка поля логина
    page.find_element(By.ID,'username').send_keys(Keys.CONTROL, 'a')
    page.find_element(By.ID,'username').send_keys(Keys.DELETE)
    # Клик по надписи 'Почта'
    tab_email = page.find_element(By.ID, 't-btn-tab-mail')
    tab_email.click()
    # ввод почты и символов в значение капчи
    page.find_element(By.ID, 'username').send_keys(valid_email)
    page.find_element(By.ID, 'captcha').send_keys('_')
    # Получаем плейсхолдер с надписью 'Электронная почта'
    assert page.find_element(By.XPATH,
                             '//*[@id="page-right"]/div//div/form/div[1]//div/span[2]').text == 'Электронная почта'
    # на странице есть изображение капчи
    assert captcha_image

    # очистка поля логина
    page.find_element(By.ID, 'username').send_keys(Keys.CONTROL, 'a')
    page.find_element(By.ID, 'username').send_keys(Keys.DELETE)
    # Клик по надписи 'Логин'
    tab_login = page.find_element(By.ID, 't-btn-tab-login')
    tab_login.click()
    # ввод логина и символов в значение капчи
    page.find_element(By.ID, 'username').send_keys(my_login)
    page.find_element(By.ID, 'captcha').send_keys('_')
    # Получаем плейсхолдер с надписью 'Логин'
    assert page.find_element(By.XPATH,
                             '//*[@id="page-right"]/div//div/form/div[1]//div/span[2]').text == 'Логин'
    # на странице есть изображение капчи
    assert captcha_image

   # очистка поля логина
    page.find_element(By.ID, 'username').send_keys(Keys.CONTROL, 'a')
    page.find_element(By.ID, 'username').send_keys(Keys.DELETE)
    # Клик по надписи 'Лицевой счёт'
    tab_l_s = page.find_element(By.ID, 't-btn-tab-ls')
    tab_l_s.click()
    # ввод лицевого счета и символов в значение капчи
    page.find_element(By.ID, 'username').send_keys(personal_account)
    page.find_element(By.ID, 'captcha').send_keys('_')
    # Получаем плейсхолдер с надписью 'Лицевой счёт'
    assert page.find_element(By.XPATH,
                             '//*[@id="page-right"]/div//div/form/div[1]//div/span[2]').text == 'Лицевой счёт'
    # на странице есть изображение капчи
    assert captcha_image


def test_10_register(selenium):
    """Проверка перехода на страницу регистрации
    Проверка наличия обязательных полей"""

    # Переходим на страницу авторизации
    page = AuthForm(selenium)
    # клик по надписи "Зарегистрироваться"
    page.register.click()
    # сохраняем скриншот страницы
    page.driver.save_screenshot('Страница регистрации.jpg')
    # Проверяем наличие обязательных полей
    # ввод имени
    assert page.find_element(By.NAME, "firstName")
    # ввод фамилии
    assert page.find_element(By.NAME, "lastName")
    # ввод региона
    assert page.find_element(By.XPATH, "//*[@id='page-right']/div/div/div/form/div[2]/div/div/input")
    # ввод телефона или почты
    assert page.find_element(By.XPATH, "//*[@id='address']")
    # ввод пароля
    assert page.find_element(By.ID, "password")
    # ввод подтверждения пароля
    assert page.find_element(By.ID, "password-confirm")
    # пользовательское соглашение
    assert page.find_element(By.XPATH,'//*[@id="page-right"]/div/div/div/form/div[5]/a')
    # кнопка ввода "Продолжить" отсутствует
    assert page.find_element(By.XPATH, "//*[@id='page-right']/div/div/div/form/button").text != "Продолжить"

def test_11_register_first_name_with_valid_name(selenium):
    """Проверка ввода валидного имени"""

    # Переходим на страницу авторизации
    page = AuthForm(selenium)
    # клик по надписи "Зарегистрироваться"
    page.register.click()
    # очистка поля имени
    page.find_element(By.NAME, "firstName").send_keys(Keys.CONTROL + "a" + Keys.DELETE)
    # ввод имени
    page.find_element(By.NAME, "firstName").send_keys(valid_name + Keys.TAB)
    # Получаем плейсхолдер с надписью 'Имя'
    assert page.find_element(By.XPATH,
                             '//*[@id="page-right"]/div/div/div/form/div[1]/div[1]/div/span[2]').text == "Имя"


def test_12_register_first_name_with_invalid_name(selenium):
    """Проверка ввода не валидного имени"""

    # Переходим на страницу авторизации
    page = AuthForm(selenium)
    # клик по надписи "Зарегистрироваться"
    page.register.click()
    # очистка поля имени
    page.find_element(By.NAME, "firstName").send_keys(Keys.CONTROL + "a" + Keys.DELETE)
    # ввод имени
    page.find_element(By.NAME, "firstName").send_keys(invalid_name + Keys.TAB)
    # Получаем текст ошибки
    assert page.find_element(By.XPATH, "//span[contains(text(), 'Необходимо заполнить поле "
                                       "кириллицей. От 2 до 30 символов.')]")


def test_13_register_first_name_with_valid_name2(selenium):
    """Проверка ввода не валидного имени"""

    # Переходим на страницу авторизации
    page = AuthForm(selenium)
    # клик по надписи "Зарегистрироваться"
    page.register.click()
    # очистка поля имени
    page.find_element(By.NAME, "firstName").send_keys(Keys.CONTROL + "a" + Keys.DELETE)
    # ввод имени
    page.find_element(By.NAME, "firstName").send_keys(invalid_name2 + Keys.TAB)
    # Получаем текст ошибки
    assert page.find_element(By.XPATH, "//span[contains(text(), 'Необходимо заполнить поле "
                                        "кириллицей. От 2 до 30 символов.')]")


def test_14_register_with_valid_lastName(selenium):
    """Проверка ввода валидной фамилии"""

    # Переходим на страницу авторизации
    page = AuthForm(selenium)
    # клик по надписи "Зарегистрироваться"
    page.register.click()
    # очистка поля 'Фамилия'
    page.find_element(By.NAME, "lastName").send_keys(Keys.CONTROL + "a" + Keys.DELETE)
    # вввод фамилии
    page.find_element(By.NAME, "lastName").send_keys(valid_lastName + Keys.TAB)
    # Получаем плейсхолдер с надписью 'Фамилия'
    assert page.find_element(By.XPATH,
                             '//*[@id="page-right"]/div/div/div/form/div[1]/div[2]/div/span[2]').text == "Фамилия"



def test_15_register_with_valid_lastName(selenium):
    """Проверка ввода не валидной фамилии"""

    # Переходим на страницу авторизации
    page = AuthForm(selenium)
    # клик по надписи "Зарегистрироваться"
    page.register.click()
    # очистка поля 'Фамилия'
    page.find_element(By.NAME, "lastName").send_keys(Keys.CONTROL + "a" + Keys.DELETE)
    # ввод фамилии
    page.find_element(By.NAME, "lastName").send_keys(invalid_lastName + Keys.TAB)
    # Получаем текст ошибки
    assert page.find_element(By.XPATH,
                             "//span[contains(text(), 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.')]")

def test_16_register_with_valid_lastName2(selenium):
    """Проверка ввода валидной фамилии"""

    # Переходим на страницу авторизации
    page = AuthForm(selenium)
    # клик по надписи "Зарегистрироваться"
    page.register.click()
    # очистка поля 'Фамилия'
    page.find_element(By.NAME, "lastName").send_keys(Keys.CONTROL + "a" + Keys.DELETE)
    # ввод фамилии
    page.find_element(By.NAME, "lastName").send_keys(invalid_lastName2 + Keys.TAB)
    # Получаем текст ошибки
    assert page.find_element(By.XPATH,
                             "//span[contains(text(), 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.')]")


def test_17_register_with_valid_phone(selenium):
    """Проверка ввода валидного номера телефона"""

    # Переходим на страницу авторизации
    page = AuthForm(selenium)
    # клик по надписи "Зарегистрироваться"
    page.register.click()
    # очистка поля 'E-mail или мобильный телефон'
    page.find_element(By.ID, "address").send_keys(Keys.CONTROL + "a" + Keys.DELETE)
    # ввод телефона
    page.find_element(By.ID, "address").send_keys(valid_phone + Keys.TAB)
    # Получаем плейсхолдер с надписью "E-mail или мобильный телефон"
    assert page.find_element(By.XPATH,
                             '//*[@id="page-right"]/div/div/div/form/div[3]/div/span[2]').text == "E-mail или мобильный телефон"


def test_18_register_with_invalid_phone(selenium):
    """Проверка ввода не валидного номера телефона"""

    # Переходим на страницу авторизации
    page = AuthForm(selenium)
    # клик по надписи "Зарегистрироваться"
    page.register.click()
    # очистка поля 'E-mail или мобильный телефон'
    page.find_element(By.ID, "address").send_keys(Keys.CONTROL + "a" + Keys.DELETE)
    # ввод телефона
    page.find_element(By.ID, "address").send_keys(invalid_phone2 + Keys.TAB)
    # Получаем текст ошибки
    assert page.find_element(By.XPATH,
                             "//span[contains(text(), 'Введите телефон в формате +7ХХХХХХХХХХ "
                             "или +375XXXXXXXXX, или email в формате example@email.ru')]")

def test_19_register_with_valid_email(selenium):
    """Проверка ввода валидной почты"""

    # Переходим на страницу авторизации
    page = AuthForm(selenium)
    # клик по надписи "Зарегистрироваться"
    page.register.click()
    # очистка поля 'E-mail или мобильный телефон'
    page.find_element(By.ID, "address").send_keys(Keys.CONTROL + "a" + Keys.DELETE)
    # ввод телефона
    page.find_element(By.ID, "address").send_keys(valid_email + Keys.TAB)
    # Получаем плейсхолдер с надписью "E-mail или мобильный телефон"
    assert page.find_element(By.XPATH,
                             '//*[@id="page-right"]/div/div/div/form/div[3]/div/span[2]').text == "E-mail или мобильный телефон"


def test_20_register_with_invalid_email(selenium):
    """Проверка ввода не валидной почты"""

    # Переходим на страницу авторизации
    page = AuthForm(selenium)
    # клик по надписи "Зарегистрироваться"
    page.register.click()
    # очистка поля 'E-mail или мобильный телефон'
    page.find_element(By.ID, "address").send_keys(Keys.CONTROL + "a" + Keys.DELETE)
    # ввод почты
    page.find_element(By.ID, "address").send_keys(invalid_email + Keys.TAB)
    # Получаем плейсхолдер с надписью "E-mail или мобильный телефон"
    assert page.find_element(By.XPATH,
                             "//span[contains(text(), 'Введите телефон в формате +7ХХХХХХХХХХ"
                             " или +375XXXXXXXXX, или email в формате example@email.ru')]")

def test_21_register_with_valid_pass(selenium):
    """Проверка ввода валидного пароля"""

    # Переходим на страницу авторизации
    page = AuthForm(selenium)
    # клик по надписи "Зарегистрироваться"
    page.register.click()
    # очистка поля пароль
    page.find_element(By.ID,"password").send_keys(Keys.CONTROL + "a" + Keys.DELETE)
    # ввод пароля
    page.find_element(By.ID,"password").send_keys(valid_pass + Keys.ENTER)
    # Получаем плейсхолдер с надписью 'Пароль'
    assert page.find_element(By.XPATH,
                             '//*[@id="page-right"]/div/div/div/form/div[4]/div[1]/div/span[2]').text == "Пароль"

def test_22_register_with_invalid_pass(selenium):
    """Проверка ввода не валидного пароля"""

    # Переходим на страницу авторизации
    page = AuthForm(selenium)
    # клик по надписи "Зарегистрироваться"
    page.register.click()
    # очистка поля пароль
    page.find_element(By.ID,"password").send_keys(Keys.CONTROL + "a" + Keys.DELETE)
    # ввод пароля
    page.find_element(By.ID,"password").send_keys(invalid_pass + Keys.ENTER)
    # Получаем текст ошибки
    assert page.find_element(By.XPATH,
                             "//span[contains(text(),'Пароль должен содержать хотя бы одну заглавную букву')]")


def test_23_register_with_invalid_pass2(selenium):
    """Проверка ввода не валидного пароля"""

    # Переходим на страницу авторизации
    page = AuthForm(selenium)
    # клик по надписи "Зарегистрироваться"
    page.register.click()
    # очистка поля пароль
    page.find_element(By.ID,"password").send_keys(Keys.CONTROL + "a" + Keys.DELETE)
    # ввод пароля
    page.find_element(By.ID,"password").send_keys(invalid_pass2 + Keys.ENTER)
    # Получаем текст ошибки
    assert page.find_element(By.XPATH,
                             "//span[contains(text(),'Длина пароля должна быть не более 20 символов')]")


def test_24_register_with_invalid_pass3(selenium):
    """Проверка ввода не валидного пароля"""

    # Переходим на страницу авторизации
    page = AuthForm(selenium)
    # клик по надписи "Зарегистрироваться"
    page.register.click()
    # очистка поля пароль
    page.find_element(By.ID,"password").send_keys(Keys.CONTROL + "a" + Keys.DELETE)
    # ввод пароля
    page.find_element(By.ID,"password").send_keys(invalid_pass3 + Keys.ENTER)
    # Получаем текст ошибки
    assert page.find_element(By.XPATH,
                             "//span[contains(text(),'Пароль должен содержать хотя бы 1 спецсимвол "
                             "или хотя бы одну цифру')]")


def test_25_register_with_invalid_pass4(selenium):
    """Проверка ввода не валидного пароля"""

    # Переходим на страницу авторизации
    page = AuthForm(selenium)
    # клик по надписи "Зарегистрироваться"
    page.register.click()
    # очистка поля пароль
    page.find_element(By.ID,"password").send_keys(Keys.CONTROL + "a" + Keys.DELETE)
    # ввод пароля
    page.find_element(By.ID,"password").send_keys(invalid_pass4 + Keys.ENTER)
    # Получаем текст ошибки
    assert page.find_element(By.XPATH,
                             "//span[contains(text(),'Длина пароля должна быть не менее 8 символов')]")


def test_26_register_password_confirm(selenium):
    """Проверка ввода подтверждения пароля"""

    # Переходим на страницу авторизации
    page = AuthForm(selenium)
    # клик по надписи "Зарегистрироваться"
    page.register.click()
    # очистка поля пароль и подтверждение пароля
    page.find_element(By.ID,"password").send_keys(Keys.CONTROL + "a" + Keys.DELETE)
    page.find_element(By.ID, "password-confirm").send_keys(Keys.CONTROL + "a" + Keys.DELETE)
    # ввод пароля и подтверждение пароля
    page.find_element(By.ID, "password").send_keys(valid_pass + Keys.TAB)
    page.find_element(By.ID,"password-confirm").send_keys(valid_pass2 + Keys.ENTER)
    # Получаем текст ошибки
    assert page.find_element(By.XPATH,
                             "//span[contains(text(),'Пароли не совпадают')]")




