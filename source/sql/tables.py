from dotenv import load_dotenv
from typing import Annotated

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

load_dotenv()

intpk = Annotated[int, mapped_column(primary_key=True)]


class Base(DeclarativeBase):
    pass


# Создание модели (таблицы в БД).
class MainTable(Base):
    """ Хранение данных пользователей."""
    __tablename__ = 'main_table'

    id: Mapped[intpk]
    user_id: Mapped[int]
    day: Mapped[int]
    month: Mapped[int]
    year: Mapped[int]
    kind: Mapped[str]
    category: Mapped[str]
    value: Mapped[float]
