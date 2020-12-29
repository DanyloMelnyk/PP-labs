import enum
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.schema import ForeignKey

engine = create_engine('postgres://postgres:nastya@localhost:5432/postgres', echo=False)

SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)

metadata = MetaData(engine)

Base = declarative_base(metadata)


class UserStatus(enum.Enum):
    notSignedIn = 'notSignedIn'
    SignedIn = 'SignedIn'
    pending = 'pending'

    def __str__(self):
        return self.value


class Currency(enum.Enum):
    UAH = 'UAH'
    USD = 'USD'
    EUR = 'EUR'
    PLN = 'PLN'
    RUB = 'RUB'

    def __str__(self):
        return self.value


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    firstName = Column(String)
    lastName = Column(String)
    email = Column(String)
    password = Column(Binary)
    phone = Column(String)
    userAuthStatus = Column(Enum(UserStatus), default=UserStatus.pending)

    wallet = relationship(
        "Wallet", back_populates="owner",
        cascade="all, delete",
        passive_deletes=True
    )

    def __str__(self):
        return f'User {self.id}, {self.username} ({self.firstName} {self.lastName})' \
               + f' {self.email} {self.phone} status: {self.userAuthStatus}'


class Wallet(Base):
    __tablename__ = 'wallets'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    balance = Column(Integer, default=0)
    currency = Column(Enum(Currency))

    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    owner = relationship("User", back_populates="wallet")

    def __str__(self):
        return f'Wallet {self.id} {self.name}, owner: {self.user_id}, balance: {self.balance} {self.currency}'


Base.metadata.create_all(engine)
