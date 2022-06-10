"""Сборник строк и прочих постоянных значений.
"""
# to datetime.isoformat
TIMESPEC = 'seconds'

# for core.users
JWT_LIFE_TIME = 60 * 60   # seconds

USER_IS_SIGNED = 'Пользователь был зарегистрирован'

# names for endpoints in api.charity_projects
GET_ALL_CHARITY_PROJECTS = 'Просмотреть все благотворительные проекты'
CREATE_CHARITY_PROJECTS = 'Создать новый благотворительный проект'
UPDATE_CHARITY_PROJECT = 'Изменить благотворительный проект'
DELETE_CHARITY_PROJECTS = 'Удалить благотворительный проект'

# names for endpoints in api.donations
GET_ALL_DONATIONS = 'Просмотреть все пожеотвования'
CREATE_DONATION = 'Добавить пожертвование'
GET_MY_DONATIONS = 'Просмотреть все мои пожертвования'

# names for endpoints in api.google
GET_REPORT_TO_GOOGLE = 'Добавить данные из БД в Google-таблицу'

# for googlesheets
TABLE_NAME = 'Отчеты QRkot'
SHEET_NAME_RATING_SPEED_CLOSING = 'Рейтинг проектов по скорости закрытия'

# error messages
ERR_LEN_PASSWORD = 'Password should be at least 3 characters'
ERR_EMAIL_IN_PASSWORD = 'Пароль содержит Ваш e-mail!'
ERR_NO_DELETE_USER = 'Удаление пользователей запрещено!'

ERR_NAME_EXIST = 'Проект с таким именем уже существует!'
ERR_PROJECT_CLOSED = 'Закрытый проект нельзя редактировать!'
ERR_FULL_AMOUNT = 'Введённая сумма превышает уже инвестированную!'
ERR_HAS_INVEST = 'Удаление запрещено! В проект уже внесено %s денег'

ERR_NOT_FOUND = 'Объект с `id=%s` не найден!'
ERR_NO_TABLE_FIELD = 'Указанное поле `%s` отсутствует в таблице!'
ERR_BASE_ANY = 'Ошибка при соединении с БД!'
ERR_BASE_INTEGRITY = 'Попытка записи некорректных данных в БД!'
