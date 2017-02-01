"""
Defines the base model that all of the bootstrap models inherit from
"""

from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey, func
from sqlalchemy import Column, Date, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

db_string = 'mysql+mysqldb://{}:{}@{}:{}/{}'.format(
    'root',
    '123456',
    'localhost',
    3306,
    'perkup'
)

engine = create_engine(db_string, echo=True, pool_recycle=360)
Base = declarative_base()
Base.metadata.bind = engine


class BaseModel:
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
    name = Column(String(200))
    host = Column(String(200))
    port = Column(Integer)
    user = Column(String(200))
    schema = Column(String(200))
    password = Column(String(200))
    type = Column(Enum(
        'Firebird',
        'Microsoft SQL Server',
        'MySQL',
        'Oracle',
        'PostgreSQL',
        'Sybase',
        name='type'))
    ssh_server = Column(String(200))
    ssh_port = Column(String(6))
    ssh_user = Column(String(200))
    ssh_password = Column(String(200))
    ssh_key_pub = Column(Text)
    ssh_key_pass_phrase = Column(String(200))

    # Foreign keys
    organization_id = Column(Integer, ForeignKey('organization.id'))
    organization_datasource = relationship(
        Organization,
        backref=backref(
            'organization_datasource',
            uselist=True,
            cascade='delete,all'
        )
    )

class DatasourceTable(BaseModel, Base):
    """"""
    __tablename__ = 'datasource_table'
    id = Column(Integer, primary_key=True, autoincrement=True)
    table_name = Column(Text)
    table_structure = Column(Text)
    serialized_table = Column(Text)
    # Foreign key
    datasource_id = Column(Integer, ForeignKey('datasource.id'))
    datasource_table = relationship(
        Datasource,
        backref=backref(
            'datasource_table',
            uselist=True,
            cascade='delete,all'
        )
    )


class User(BaseModel, Base):
    """"""
    __tablename__ = 'user'

    id = Column(Integer, Sequence('usr_seq'), primary_key=True)
    name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(100))
    password = Column(String(100))
    username = Column(String(50))
    avatar = Column(String(100))

    # Foreign keys
    organization_id = Column(Integer, ForeignKey('organization.id'))
    organization_user = relationship(
        Organization,
        backref=backref(
            'organization_user',
            uselist=True,
            cascade='delete,all'
        )
    )
