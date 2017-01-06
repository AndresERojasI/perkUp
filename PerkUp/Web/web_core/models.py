"""
Defines the base model that all of the bootstrap models inherit from
"""

from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey, func
from sqlalchemy import Column, Date, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker

engine = create_engine('mysql://root:123456@localhost/perkup', echo=True)
Base = declarative_base()
Base.metadata.bind = engine

class BaseModel():
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())

class Organization(BaseModel, Base):
    """"""
    __tablename__ = 'organization'

    id = Column(Integer, Sequence('org_seq'), primary_key=True)
    name = Column(String(50))
    logo = Column(String(100))
    address = Column(String(100))
    unique_domain = Column(String(50))
    lat_lang = Column(String(50))

class Datasource(BaseModel, Base):
    """"""
    __tablename__ = 'datasource'

    id = Column(Integer, Sequence('datasource_seq'), primary_key=True)
    host = Column(String(200))
    port = Column(SmallInteger)
    user = Column(String(200))
    schema = Column(String(200))
    password = Column(String(200))

    #Foreign keys
    organization_id = Column(Integer, ForeignKey('organization.id'))
    organization_datasource = relationship(
        Organization,
        backref=backref('organization_datasource',
                         uselist=True,
                         cascade='delete,all'))

class User(BaseModel, Base) :
    """"""
    __tablename__ = 'user'

    id = Column(Integer, Sequence('usr_seq'), primary_key=True)
    name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(100))
    password = Column(String(100))
    username = Column(String(50))
    avatar = Column(String(100))

    #Foreign keys#
    organization_id = Column(Integer, ForeignKey('organization.id'))
    organization_user = relationship(
        Organization,
        backref=backref('organization_user',
                         uselist=True,
                         cascade='delete,all'))

Base.metadata.create_all(engine)