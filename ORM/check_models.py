from ORM.models import Session, User, Wallet, Currency, UserStatus
from flask_bcrypt import generate_password_hash


def create_objects():
    session = Session()

    user = User(
        username='terminator2000',
        firstName='admin',
        lastName='admin',
        email='example@gmail.com',
        phone='+38099',
        userAuthStatus=UserStatus.notSignedIn,
        password=generate_password_hash('admin')
    )

    user2 = User(
        username='terminator2002',
        firstName='admin',
        lastName='admin',
        email='example1@gmail.com',
        phone='+380990',
        userAuthStatus=UserStatus.notSignedIn,
        password=generate_password_hash('admin')
    )

    user3 = User(
        username='terminator2003',
        firstName='admin',
        lastName='admin',
        email='example2@gmail.com',
        phone='+380940',
        userAuthStatus=UserStatus.notSignedIn,
        password=generate_password_hash('admin')
    )

    wallet13 = Wallet(
        name='MyFirstWallet',
        balance=10000,
        currency=Currency.USD,
        owner=user3,
    )

    wallet23 = Wallet(
        name='MySecondWallet',
        balance=100,
        currency=Currency.UAH,
        owner=user3,
    )

    wallet1 = Wallet(
        name='MyWallet',
        balance=10000,
        currency=Currency.USD,
        owner=user,
    )

    wallet2 = Wallet(
        name='MySecoWallet',
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


create_objects()

# psql -h localhost -d postgres -U postgres -p 5432 -a -q -f ORM/create_tables.sql