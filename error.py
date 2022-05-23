from flask import jsonify

class DSDException(Exception):
    pass

class APISyntaxError(DSDException):
    @staticmethod
    def handler(e):
        return jsonify({
            'error': str(e),
        }), 400


class UnauthorizedError(DSDException):
    @staticmethod
    def handler(e):
        return jsonify({
            'error': str(e),
        }), 401


class ForbiddenError(DSDException):
    @staticmethod
    def handler(e):
        return '', 403


class BadSignatureError(DSDException):
    @staticmethod
    def handler(e):
        return jsonify({
            'error': str(e),
        }), 400
