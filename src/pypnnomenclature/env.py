from os import environ
from importlib import import_module

from flask_marshmallow import Marshmallow

from flask_sqlalchemy import SQLAlchemy



db_path = environ.get('FLASK_SQLALCHEMY_DB')
if db_path:
    db_module_name, db_object_name = db_path.rsplit('.', 1)
    db_module = import_module(db_module_name)
    DB = getattr(db_module, db_object_name)
else:
    DB = SQLAlchemy()

marsmallow_path = environ.get('MARSHMALLOW_OBJ')
if marsmallow_path:
    ma_module_name, ma_object_name = marsmallow_path.rsplit('.', 1)
    print(ma_object_name)
    ma_module = import_module(ma_module_name)
    MA = getattr(ma_module, ma_object_name)
else:
    MA = Marshmallow()


__all__ = ['db']
