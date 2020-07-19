import logging

from sqlalchemy.exc import SQLAlchemyError

from src import db


class DAO:
    @staticmethod
    def persist(entity: db.Model) -> None:
        db.session.add(entity)
        DAO.commit()

    @staticmethod
    def commit() -> None:
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            logging.exception(e)
        finally:
            db.session.close()
