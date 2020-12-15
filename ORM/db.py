from flask_bcrypt import generate_password_hash
from marshmallow import ValidationError
from sqlalchemy.orm.exc import NoResultFound

from ORM.models import Session, User, Wallet
from shemas import UserData, WalletData
from utils import convert_currency


def list_users(users_filter):
    session = Session()
    query = session.query(User)

    if users_filter.get('email'):
        query = query.filter_by(email=users_filter.get('email'))

    if users_filter.get('firstName'):
        query = query.filter_by(firstName=users_filter.get('firstName'))

    if users_filter.get('lastName'):
        query = query.filter_by(lastName=users_filter.get('lastName'))

    return UserData(many=True).dump(query.all())


def create_user(user_to_create):
    session = Session()

    try:
        session.query(User).filter_by(email=user_to_create.get('email')).one()
    except NoResultFound:
        password = generate_password_hash(user_to_create.get('password'))
        user = User(email=user_to_create.get('email'), username=user_to_create.get('username'), password=password)
        session.add(user)
        session.commit()
        session.refresh(user)

        return UserData().dump(user)
    else:
        raise ValidationError("Email must be unique")


def get_user(user_id):
    session = Session()
    try:
        user = session.query(User).filter_by(id=user_id).one()
    except NoResultFound:
        raise NoResultFound('Invalid id')

    return UserData().dump(user)


def update_user(user_id, user_data):
    session = Session()

    try:
        user = session.query(User).filter_by(id=user_id).one()
    except NoResultFound:
        raise NoResultFound('Invalid id')

    if user_data.get('id') and user_data.get('id') != user_id:
        raise ValidationError(f"Different id {user_data.get('id')} != {user_id}")

    if user_data.get('email') and user.email != user_data.get('email'):
        try:
            session.query(User).filter_by(email=user_data.get('email')).one()
        except NoResultFound:
            pass
        else:
            raise ValidationError("Email must be unique")

    for k, val in user_data.items():
        if k == 'password':
            setattr(user, k, generate_password_hash(val))
        else:
            setattr(user, k, val)

    session.commit()

    return UserData().dump(user)


def delete(model, id):
    session = Session()
    try:
        session.query(model).filter_by(id=id).one()
    except NoResultFound:
        raise NoResultFound('Invalid id')

    session.query(model).filter_by(id=id).delete()
    session.commit()


def list_wallets(wallets_filter):
    session = Session()
    query = session.query(Wallet)

    if wallets_filter.get('user_id'):
        try:
            session.query(User).filter_by(id=wallets_filter.get('user_id')).one()
        except NoResultFound:
            raise NoResultFound('Invalid id')

        query = query.filter_by(user_id=wallets_filter.get('user_id'))

    return WalletData(many=True).dump(query.all())


def create_wallet(wallet_to_create):
    session = Session()

    try:
        session.query(Wallet).filter_by(name=wallet_to_create.get('name')).one()
    except NoResultFound:
        wallet = Wallet(name=wallet_to_create.get('name'), currency=wallet_to_create.get('currency'),
                        user_id=wallet_to_create.get('user_id'))
        session.add(wallet)
        session.commit()
        session.refresh(wallet)

        return WalletData().dump(wallet)
    else:
        raise ValidationError("Wallet name must be unique")


def get_wallet(wallet_name):
    session = Session()
    try:
        wallet = session.query(Wallet).filter_by(name=wallet_name).one()
    except NoResultFound:
        raise NoResultFound('Invalid wallet name')

    return WalletData().dump(wallet)


def delete_wallet(wallet_name):
    session = Session()
    try:
        session.query(Wallet).filter_by(name=wallet_name).one()
    except NoResultFound:
        raise NoResultFound('Invalid wallet name')

    session.query(Wallet).filter_by(name=wallet_name).delete()
    session.commit()


def update_wallet(wallet_name, wallet_data):
    session = Session()

    try:
        wallet = session.query(Wallet).filter_by(name=wallet_name).one()
    except NoResultFound:
        raise NoResultFound('Invalid wallet name')

    if wallet_data.get('name') and wallet_data.get('name') != wallet_name:
        try:
            session.query(Wallet).filter_by(name=wallet_data.get('name')).one()
        except NoResultFound:
            pass
        else:
            raise ValidationError("Wallet name must be unique")

    for k, val in wallet_data.items():
        if k == 'user_id':
            session.query(User).filter_by(id=val).one()

        setattr(wallet, k, val)

    session.commit()

    return WalletData().dump(wallet)


def send_money(wallet_name, transaction):
    session = Session()

    try:
        sender = session.query(Wallet).filter_by(name=wallet_name).one()
        recipient = session.query(Wallet).filter_by(name=transaction.get('wallet_recipient')).one()
    except NoResultFound:
        raise NoResultFound('Invalid wallet name')

    if sender.balance < transaction.get('cost'):
        raise ValidationError("Not enough balance")

    amount_received = convert_currency(transaction.get('cost'), sender.currency, recipient.currency)

    sender.balance -= transaction.get('cost')
    recipient.balance += amount_received

    session.commit()
    session.refresh(sender)

    return WalletData().dump(sender)
