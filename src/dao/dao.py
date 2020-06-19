import logging

from sqlalchemy.exc import SQLAlchemyError

from src import db


class DAO:
    @staticmethod
    def persist(entity: db.Model) -> None:
        try:
            db.session.add(entity)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            logging.exception(e)
        finally:
            db.session.close()
