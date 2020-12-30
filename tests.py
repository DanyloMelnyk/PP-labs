# from blueprint import *
from flask_testing import TestCase

from ORM.models import Session, Base, engine, User, Wallet

from ORM.check_models import create_objects
from main import app
import unittest
from marshmallow import ValidationError
from sqlalchemy.orm.exc import NoResultFound
from base64 import b64encode
from ORM.db import create_user, get_user


class TestAPI(TestCase):

    def create_app(self):
        app_ = app
        app_.config['TESTING'] = True
        return app_

    def setUp(self):
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        create_objects()

    def tearDown(self):
        Session.remove()
        Session.close()
        Base.metadata.drop_all(engine)

    def test_models(self):
        from flask_bcrypt import generate_password_hash
        user = User(username='terminator2000', firstName='admin', lastName='admin', email='example@gmail.com', phone='+38099', userAuthStatus='notSignedIn', password=generate_password_hash('admin'))
        self.assertEqual(str(user), 'User None, terminator2000 (admin admin) example@gmail.com +38099 status: notSignedIn')

        wallet = Wallet(name='MyFirstWallet', balance=10000, currency='USD', owner=user)
        self.assertEqual(str(wallet), f'Wallet {wallet.id} {wallet.name}, owner: {wallet.user_id}, balance: {wallet.balance} {wallet.currency}')

    def test_list_users(self):
        self.assert200(self.client.get('/user', json={}))

        self.assert200(self.client.get('/user', json={'email': 'example2@gmail.com'}))

        self.assert200(self.client.get('/user', json={'firstName': 'admin'}))

        self.assert200(self.client.get('/user', json={'lastName': 'admin'}))

    def test_create_user(self):
        self.assert200(self.client.post('/user', json={'email': 'new_example@gmail.com', 'username': 'new_terminator', 'password': 'admin'}))

        self.assertRaises(ValidationError, create_user, {'email': 'new_example@gmail.com', 'username': 'new_terminator', 'password': 'admin'})

    def test_get_user(self):
        credentials = b64encode(b"terminator2000:admin").decode('utf-8')
        self.assert200(self.client.get('/user/1', headers={'Authorization': f'Basic {credentials}'}))
        # self.assert404(self.client.get('/user/10', headers={'Authorization': f'Basic {credentials}'}))
        # self.assert404(self.client.get('/user/2', headers={'Authorization': f'Basic {credentials}'}))

    def test_update_user(self):
        credentials = b64encode(b"terminator2000:admin").decode('utf-8')
        self.assert200(self.client.put('/user/1', json={'id': 1, 'email': 'exem@gmail.com', 'password': 'admin'}, headers={'Authorization': f'Basic {credentials}'}))
        # self.assert404(self.client.put('/user/2', json={'id': 2, 'email': 'exem@gmail.com', 'password': 'admin'}, headers={'Authorization': f'Basic {credentials}'}))

        # self.assert404(self.client.put('/user/1000', json={'id': 1, 'email': 'exem@gmail.com', 'password': 'admin'}, headers={'Authorization': f'Basic {credentials}'}))

        # self.assert400(self.client.put('/user/1', json={'id': 3, 'email': 'exem@gmail.com', 'password': 'admin'}, headers={'Authorization': f'Basic {credentials}'}))
        # self.assert400(self.client.put('/user/1', json={'id': 1, 'email': 'example1@gmail.com', 'password': 'admin'}, headers={'Authorization': f'Basic {credentials}'}))

    def test_delete_user(self):
        credentials = b64encode(b"terminator2000:admin").decode('utf-8')
        self.assert200(self.client.delete('/user/1', headers={'Authorization': f'Basic {credentials}'}))

    def test_list_wallets(self):
        credentials = b64encode(b"terminator2000:admin").decode('utf-8')
        self.assert200(self.client.get('/wallet', headers={'Authorization': f'Basic {credentials}'}, json={'user_id': 1}))

    def test_create_wallet(self):
        credentials = b64encode(b"terminator2000:admin").decode('utf-8')
        self.assert200(self.client.post('/wallet', headers={'Authorization': f'Basic {credentials}'}, json={'user_id': 1, 'name': 'wallet_', 'currency': 'USD'}))

    def test_get_wallet(self):
        credentials = b64encode(b"terminator2000:admin").decode('utf-8')
        self.assert200(self.client.get('/wallet/MyWallet', headers={'Authorization': f'Basic {credentials}'}))

    def test_update_wallet(self):
        credentials = b64encode(b"terminator2000:admin").decode('utf-8')
        self.assert200(self.client.put('/wallet/MyWallet', headers={'Authorization': f'Basic {credentials}'}, json={'name':'MyNew'}))

    def test_delete_wallet(self):
        credentials = b64encode(b"terminator2000:admin").decode('utf-8')
        self.assert200(self.client.delete('/wallet/MyWallet', headers={'Authorization': f'Basic {credentials}'}))

    def test_send_money(self):
        credentials = b64encode(b"terminator2000:admin").decode('utf-8')
        self.assert200(self.client.post('/wallet/MyWallet/send_money', headers={'Authorization': f'Basic {credentials}'}, json={'wallet_recipient': 'MySecondWallet', 'cost': 100}))


if __name__ == '__main__':
    unittest.main()
