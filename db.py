## Импортируем необходимые модули и классы из SQLAlchemy.
from sqlalchemy import create_engine  # Создание подключения к базе данных.
from sqlalchemy import Column, Integer, VARCHAR, Date, Boolean, Float, \
    TIMESTAMP  # Определение типов данных для колонок в таблице.
from sqlalchemy.orm import declarative_base  # Базовый класс для всех моделей (таблиц).

## Создаем базовый класс для всех таблиц, от которого будут наследоваться модели.
Base = declarative_base()

## Импортируем дополнительные модули для работы с сессиями.
from sqlalchemy.orm import sessionmaker  # Класс для создания сессий для взаимодействия с базой данных.
import datetime as datetime  # Для работы с датой и временем.

## Настройка пути для импорта файла конфигурации (где, вероятно, хранится строка подключения к БД).
import sys

sys.path.append("..")  # Добавляем родительскую директорию в sys.path для импорта модуля config.

## Импорт строки подключения к базе данных из файла конфигурации.
from config import SQLALCHEMY_DATABASE_URI

## Создаем объект подключения к базе данных с помощью create_engine.
## SQLALCHEMY_DATABASE_URI - это строка подключения, содержащая информацию о базе данных (тип базы, имя пользователя, пароль, хост и т.д.).
engine = create_engine(SQLALCHEMY_DATABASE_URI)

## Создаем все таблицы, которые определены в базовых классах (наследниках Base).
## Если таблицы еще не существуют, они будут созданы.
Base.metadata.create_all(bind=engine)

## Создаем фабрику сессий с помощью sessionmaker. Это будет использоваться для работы с транзакциями.
## autocommit=False - транзакции не будут автоматически коммититься.
## autoflush=False - данные не будут автоматически сбрасываться в базу до явного вызова commit.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

## Создаем объект сессии, который будет использоваться для выполнения запросов к базе данных.
session_local = SessionLocal()


## Определяем модель таблицы в базе данных.
## Модель `Record` представляет таблицу `usdtorub2`, где будут храниться данные о курсе валюты.
class Record(Base):
    __tablename__ = 'usdtorub2'  # Имя таблицы в базе данных.

    # Определение колонок таблицы:
    id = Column(Integer, nullable=False, unique=True, primary_key=True,
                autoincrement=True)  # Уникальный идентификатор записи, автоинкремент.
    r_value = Column(Float, nullable=False)  # Колонка для значения курса (например, курс доллара к рублю).
    r_date = Column(TIMESTAMP, nullable=False,
                    index=True)  # Колонка для даты и времени записи, проиндексирована для быстрого поиска.


## Функция для добавления новой записи в таблицу.
def new_record(value):
    # Создаем новую запись, заполняя столбцы таблицы значениями.
    record = Record(
        r_value=value,  # Переданное значение курса.
        r_date=datetime.datetime.utcnow()  # Текущая дата и время по UTC.
    )

    # Добавляем объект записи в текущую сессию.
    session_local.add(record)

    # Сохраняем (коммитим) изменения в базе данных.
    session_local.commit()


