import logging
from typing import NoReturn

from sqlalchemy.exc import SQLAlchemyError

from src import db


class DAO:
    @staticmethod
    def persist(entity: db.Model) -> NoReturn:
        db.session.add(entity)
        DAO.commit()

    @staticmethod
    def commit() -> NoReturn:
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            logging.exception(e)
        finally:
            db.session.close()
