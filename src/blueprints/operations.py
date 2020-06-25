import sqlite3
from datetime import time
from flask import (
    request,
)
from flask import (
    Blueprint,
    jsonify,
    session,
)
from flask.views import MethodView

from src.services.categories import CategoriesService

from src.database import db
from src.services.operation import OperationService

bp = Blueprint('operations', __name__)


class OperationsView(MethodView):
    def get(self):
        pass

    def post(self):
        # Проверка авторизации
        account_id = session.get('id')
        if not account_id:
            return '', 403

        request_json = request.json

        # Обработка даты
        date = request_json.get('date')
        if date:
            date = int(time.mktime(time.strptime(date, "%Y-%m-%d %H:%M:%S")))
        else:
            date = int(time.time())

        # Обработка данных и валидация
        try:
            operation = {
                "date": date,
                "type": request_json['type'],
                "description": request_json['description'],
                "amount": request_json['amount'],
                "category_id": request_json.get('category_id')
            }
        except KeyError as e:
            return "", 400

        # Проверка существования указанной категории
        category_service = CategoriesService()
        if not category_service.check(category_id=operation['category_id'], account_id=account_id):
            return "", 403

        # Запись операции в базу
        operation_service = OperationService()
        operation_service.create_operation(data=operation)

        # Чтение операции из базы
        response = operation_service.read(operation=operation)
        return jsonify(response), 201

        # Чтение информации об операции в БД



class OperationView(MethodView):
    def patch(self, operation_id):
        pass

    def delete(self, operation_id):
        pass


bp.add_url_rule('', view_func=OperationsView.as_view('operations'))
bp.add_url_rule('/<int:operation_id>', view_func=OperationView.as_view('operation'))
