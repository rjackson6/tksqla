from sqlalchemy import (
    Column, ForeignKey, ForeignKeyConstraint, Table, UniqueConstraint, event,
    Boolean, Date, Text
)  # Integer, String
# noinspection PyProtectedMember
from sqlalchemy.engine import Engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import sqlalchemy.types


class Integer(sqlalchemy.types.TypeDecorator):
    impl = sqlalchemy.types.Integer

    def process_bind_param(self, value, dialect):
        if isinstance(value, str):
            value = int(value)
        else:
            assert isinstance(value, int)
        return value


class String(sqlalchemy.types.TypeDecorator):
    impl = sqlalchemy.types.String

    def process_bind_param(self, value, dialect):
        assert isinstance(value, str)
        value = value.strip()
        assert value
        return value


@compiles(sqlalchemy.types.String, 'sqlite')
def compile_string_sqlite(element, compiler, **kwargs):
    return '{} COLLATE NOCASE'.format(element)


class Base(object):
    @classmethod
    def __table_cls__(cls, *args, **kwargs):
        t = Table(*args, **kwargs)
        t.decl_class = cls
        return t


class_registry = {}
Base = declarative_base(cls=Base, class_registry=class_registry)


# SQLite Foreign Key
@event.listens_for(Engine, 'connect')
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


# Validators (per zzzeek, stackoverflow/questions/8980735)
def validate_int(value):
    if isinstance(value, str):
        value = int(value)
    else:
        assert isinstance(value, int)
    return value


def validate_str(value):
    assert isinstance(value, str)
    return value


validators = {
    Integer: validate_int,
    String: validate_str
}


@event.listens_for(Base, 'attribute_instrument')
def configure_listener(class_, key, inst):
    if not hasattr(inst.property, 'columns'):
        return

    @event.listens_for(inst, 'set', retval=True)
    def set_(instance, value, oldvalue, initiator):
        validator = validators.get(inst.property.columns[0].type.__class__)
        if validator:
            return validator(value)
        else:
            return value


# Tables
class VehicleMake(Base):
    __tablename__ = 'tksqla_vehiclemake'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    vehiclemodels = relationship('VehicleModel', back_populates='vehiclemake')

    def __repr__(self):
        return 'VehicleMake({})'.format(self.name)


class VehicleModel(Base):
    __tablename__ = 'tksqla_vehiclemodel'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    vehiclemake_id = Column(Integer, ForeignKey('tksqla_vehiclemake.id'), nullable=False)
    __table_args__ = (
        UniqueConstraint('name', 'vehiclemake_id'),
    )

    vehiclemake = relationship('VehicleMake', back_populates='vehiclemodels')
    vehicletrims = relationship('VehicleTrim', back_populates='vehiclemodel')

    def __repr__(self):
        return 'VehicleModel({})'.format(self.name)


class VehicleTrim(Base):
    __tablename__ = 'tksqla_vehicletrim'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    vehiclemodel_id = Column(Integer, ForeignKey('tksqla_vehiclemodel.id'), nullable=False)
    __table_args__ = (
        UniqueConstraint('name', 'vehiclemodel_id'),
    )

    vehiclemodel = relationship('VehicleModel', back_populates='vehicletrims')
    # vehicles = relationship('Vehicle', back_populates='vehicletrim')

    def __repr__(self):
        return 'VehicleTrim({})'.format(self.name)
