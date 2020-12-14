import enum
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.schema import ForeignKey

engine = create_engine(f'postgresql://postgres:admin@localhost:5432/postgres?', echo=True)

SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)

metadata = MetaData(engine)

Base = declarative_base(metadata)


class UserStatus(enum.Enum):
    notSignedIn = 'notSignedIn'
    SignedIn = 'SignedIn'
    pending = 'pending'


class Currency(enum.Enum):
    UAH = 'UAH'
    USD = 'USD'
    EUR = 'EUR'
    PLN = 'PLN'
    RUB = 'RUB'


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(Binary)
    phone = Column(String)
    status = Column(Enum(UserStatus))


class Wallet(Base):
    __tablename__ = 'wallets'

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey(User.id))
    name = Column(String)
    balance = Column(Integer)
    currency = Column(Enum(Currency))

    owner = relationship(User, backref='wallets', lazy='joined')


Base.metadata.create_all(engine)
