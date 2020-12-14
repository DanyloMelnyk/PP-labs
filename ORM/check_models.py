from models import Session, User, Wallet, Currency, UserStatus

session = Session()

user = User(
    id=1,
    username='terminator2000',
    first_name='admin',
    last_name='admin',
    email='example@gmail.com',
    phone='+38099',
    status=UserStatus.notSignedIn,
)

user2 = User(
    id=2,
    username='terminator2002',
    first_name='admin',
    last_name='admin',
    email='example1@gmail.com',
    phone='+380990',
    status=UserStatus.notSignedIn,
)


user3 = User(
    id=3,
    username='terminator2003',
    first_name='admin',
    last_name='admin',
    email='example2@gmail.com',
    phone='+380940',
    status=UserStatus.notSignedIn,
)

wallet13 = Wallet(
    id=3,
    name='MyFirstWallet',
    balance=10000,
    currency=Currency.USD,
    owner=user3,
)

wallet23 = Wallet(
    id=4,
    name='MySecondWallet',
    balance=100,
    currency=Currency.UAH,
    owner=user3,
)

wallet1 = Wallet(
    id=1,
    name='MyFirstWallet',
    balance=10000,
    currency=Currency.USD,
    owner=user,
)

wallet2 = Wallet(
    id=2,
    name='MySecondWallet',
    balance=100,
    currency=Currency.UAH,
    owner=user,
)

session.add(user)
session.add(user2)
session.add(wallet1)
session.add(wallet2)

session.add(user3)
session.add(wallet13)
session.add(wallet23)

session.commit()


# psql -h localhost -d postgres -U postgres -p 5432 -a -q -f ORM/create_tables.sql