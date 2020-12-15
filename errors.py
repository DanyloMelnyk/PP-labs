import logging

from flask import jsonify

from shemas import Response


def validation_error(e):
    logging.exception(e)

    return jsonify(Response().dump({
        "code": 400,
        "type": "BAD_REQUEST",
        "message": f"Bad Request: {e.args[0]}"
    })), 400


def not_found_error(e):
    logging.exception(e)

    return jsonify(Response().dump({
        "code": 404,
        "type": "NOT_FOUND",
        "message": f"Not found: {e.args[0]}"
    })), 404
