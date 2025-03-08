from dotenv import load_dotenv

import sqlalchemy as sa
from sqlalchemy.orm import Session

from source.sql.tables import Base
from source.settings.settings import DB_URL, SPLIT_SYM


load_dotenv()


main_engine = sa.create_engine(
    DB_URL,
    echo=False
)


class SQLmain:

    @staticmethod
    def create_all_tables():
        Base.metadata.create_all(bind=main_engine)

    @staticmethod
    def restart_all_tables():
        Base.metadata.drop_all(bind=main_engine)
        Base.metadata.create_all(bind=main_engine)

    @staticmethod
    def insert_data(data, table):
        with Session(bind=main_engine) as s:
            Base.metadata.drop_all(
                bind=main_engine,
                tables=[table.__table__]
            )
            Base.metadata.create_all(
                bind=main_engine,
                tables=[table.__table__]
            )

            s.execute(sa.insert(table).values(data))
            s.commit()

    @staticmethod
    def append_data(data, table):
        with Session(bind=main_engine) as s:
            s.execute(sa.insert(table).values(data))
            s.commit()

    @classmethod
    def get_all_data(self, table):
        with Session(bind=main_engine) as s:

            return self.correct_data_in_dict(data=s.execute(
                sa.select('*').select_from(table)
            ).all())

    @classmethod
    def get_data_on_user_id(self, table, user_id):
        with Session(bind=main_engine) as s:

            return self.correct_data_in_dict(data=s.execute(
                sa.select('*').select_from(table).where(
                    table.user_id == user_id
                )
            ))

    @classmethod
    def get_data_on_id(self, table, id):
        with Session(bind=main_engine) as s:

            return self.correct_data_in_dict(data=s.execute(
                sa.select('*').select_from(table).where(
                    table.id == id
                )
            ))

    @classmethod
    def change_data_on_id(self, table, id, data):
        with Session(bind=main_engine) as s:
            entry = s.query(table).filter(table.id == id).first()
            if entry:
                date = data['date'].split(SPLIT_SYM)
                entry.day = date[0]
                entry.month = date[1]
                entry.year = date[2]
                entry.user_id = data['user_id']
                entry.kind = data['kind']
                entry.category = data['category']
                entry.value = data['value']
            s.commit()

    @classmethod
    def delete_operation(self, table, id):
        with Session(bind=main_engine) as s:

            s.delete(s.query(table).get(id))
            s.commit()

    @staticmethod
    def correct_data_in_dict(data):
        result = []
        for el in data:
            result.append(el._asdict())
        return result
