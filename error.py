from flask import jsonify

class DSDException(Exception):
    pass

class APISyntaxError(DSDException):
    @staticmethod
    def handler(e):
        return jsonify({
            'error': str(e),
        }), 400


class NotLoggedIn(DSDException):
    @staticmethod
    def handler(e):
        return jsonify({
            'error': str(e),
        }), 401


class Forbidden(DSDException):
    @staticmethod
    def handler(e):
        return '', 403


class SignatureError(DSDException):
    @staticmethod
    def handler(e):
        return jsonify({
            'error': str(e),
        }), 400
