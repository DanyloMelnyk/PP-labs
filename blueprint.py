from flask import Blueprint, request, jsonify
from sqlalchemy.orm.exc import NoResultFound

from ORM import db
from ORM.models import User
from shemas import Credentials, UserListFilter, UserData, UserToCreate, WalletListFilter, WalletToCreate, WalletData, \
    Transaction

blueprint = Blueprint('api', __name__)


@blueprint.route('/user', methods=['GET'])
def list_users():
    user_filter = UserListFilter().load(request.json)
    return jsonify(db.list_users(user_filter))


@blueprint.route('/user', methods=['POST'])
def create_user():
    user_to_create = UserToCreate().load(request.json)
    return jsonify(db.create_user(user_to_create))


@blueprint.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return jsonify(db.get_user(user_id))


@blueprint.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user_data = UserData().load(request.json)

    return jsonify(db.update_user(user_id, user_data))


@blueprint.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db.delete(User, user_id)
    return 'Deleting is successful', 200


@blueprint.route('/wallet', methods=['GET'])
def list_wallets():
    wallets_filter = WalletListFilter().load(request.json)

    return jsonify(db.list_wallets(wallets_filter))


@blueprint.route('/wallet', methods=['POST'])
def create_wallet():
    wallet_to_create = WalletToCreate().load(request.json)

    return jsonify(db.create_wallet(wallet_to_create))


@blueprint.route('/wallet/<string:wallet_name>', methods=['GET'])
def get_wallet(wallet_name):
    return jsonify(db.get_wallet(wallet_name))


@blueprint.route('/wallet/<string:wallet_name>', methods=['PUT'])
def update_wallet(wallet_name):
    wallet_data = WalletData().load(request.json)
    return jsonify(db.update_wallet(wallet_name, wallet_data))


@blueprint.route('/wallet/<string:wallet_name>', methods=['DELETE'])
def delete_wallet(wallet_name):
    db.delete_wallet(wallet_name)
    return 'Wallet is deleted', 200


@blueprint.route('/wallet/<string:wallet_name>/send_money', methods=['POST'])
def send_money(wallet_name):
    transaction = Transaction().load(request.json)
    return db.send_money(wallet_name, transaction)
