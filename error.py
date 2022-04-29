from flask import jsonify


class APISyntaxError(Exception):
    @staticmethod
    def handler(e):
        return jsonify({
            'error': str(e),
        }), 400


class NotLoggedIn(Exception):
    @staticmethod
    def handler(e):
        return jsonify({
            'error': str(e),
        }), 401


class Forbidden(Exception):
    @staticmethod
    def handler(e):
        return jsonify({
            'error': str(e),
        }), 403


class SignatureError(Exception):
    @staticmethod
    def handler(e):
        return jsonify({
            'error': str(e),
        }), 400
