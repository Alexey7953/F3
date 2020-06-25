from flask import (
    request,
)
from flask import (
    Blueprint,
    jsonify,
    session,
)
import sqlite3
from flask.views import MethodView
from src.services.categories import CategoriesService
from src.database import db

bp = Blueprint('categories', __name__)


class CategoriesView(MethodView):
    def post(self):
        pass


class CategoryView(MethodView):
    def patch(self, category_id: int):
        account_id = session.get('id')
        if not account_id:
            return '', 403

        request_json = request.json
        if not request_json:
            return '', 400

        parent_id = request_json.get('parent_id')
        name = request_json.get('name')
        new_data = {
            'account_id': account_id,
            'id': category_id,
        }

        if name is not None:
            new_data['name'] = name
        if parent_id is not None:
            if parent_id == 'null':
                parent_id = None
            new_data['parent_id'] = parent_id

        service = CategoriesService()

        if not service.check(category_id, account_id):
            return '', 404

        if not service.check(parent_id, account_id):
            return '', 400

        result = service.edit(data=new_data)
        return jsonify(result), 200

    def delete(self, category_id):
        # Если пользователь не авторизован -> 403
        session_id = session.get('user_id')
        if session_id is None:
            return '', 403

        con = db.connection
        try:
            # Ищем категорию
            cur_category = con.execute(
                'SELECT account_id '
                'FROM category '
                'WHERE id = ? ',
                (category_id,),
            )
            result_category = cur_category.fetchone()
            # Если категория не найдена -> 404
            if result_category is None:
                return '', 404
            # Если пользователю не принадлежит категория -> 403
            if result_category["account_id"] != session_id:
                return '', 403

            # Устанавливаем принадлежность категории таблице operation если нет -> 403
            cur_operation_category = con.execute(
                'SELECT category_id '
                'FROM operation '
                'WHERE category_id = ? ',
                (category_id,),
            )
            result_operation_category = cur_operation_category.fetchone()
            if result_operation_category:
                return '', 403

            # Удаление категории
            con.execute(f"""
                       DELETE FROM category
                       WHERE id = {category_id}
                   """)

            # Ищем дочернюю категорию в таблице category
            cur_category = con.execute(
                'SELECT id '
                'FROM category '
                'WHERE parent_id = ? ',
                (category_id,),
            )
            result_category = cur_category.fetchone()
            if result_category:
                # Запись в таблицу category parent_id = None
                category_query = f'UPDATE category SET parent_id = ? WHERE id = ?'
                con.execute(category_query, (None, result_category["id"]))

            con.commit()

        except sqlite3.IntegrityError:
            return '', 403

        return '', 204


bp.add_url_rule('', view_func=CategoriesView.as_view('categories'))
bp.add_url_rule('/<int:category_id>', view_func=CategoryView.as_view('category'))
