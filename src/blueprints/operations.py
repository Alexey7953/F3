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

from src.database import db


bp = Blueprint('operations', __name__)


class OperationsView(MethodView):
    def get(self):
        pass

    def post(self):
        request_json = request.json

        type = request_json.get('type')

        category_id = request_json.get('category_id')
        category_dict = {}
        if category_id:





        # Обработка даты
        date = request_json.get('date')
        if date:
            date = int(time.mktime(time.strptime(date, "%Y-%m-%d %H:%M:%S")))
        else:
            date = int(time.time())

        # Обработка кол-во
        amount = request_json.get('amount')
        # Обработка описания
        description = request_json.get('description')


        operation = {
    "id": operation_id,
    "type": operation_dict["type"],
    "category": category_dict or "none",
    "date": date,
    "amount": operation_dict["amount"],
    "description": description or "none",
}


class OperationView(MethodView):
    def patch(self, operation_id):
        pass

    def delete(self, operation_id):
        pass



bp.add_url_rule('', view_func=OperationsView.as_view('operations'))
bp.add_url_rule('/<int:operation_id>', view_func=OperationView.as_view('operation'))
