import pymysql
from flask import Blueprint, jsonify, request

from database import get_connection
from utils.response import fail, ok

model_bp = Blueprint("model", __name__)


@model_bp.route("/api/models", methods=["GET"])
def get_models():
    """查询所有模型"""
    conn = get_connection()
    if conn is None:
        return jsonify(fail("数据库连接失败")), 500

    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            """
            SELECT model_id, model_name, type, version, description
            FROM model
            ORDER BY model_id
            """
        )
        rows = cursor.fetchall()
        return jsonify(ok(rows))
    except Exception as e:
        return jsonify(fail(str(e))), 500
    finally:
        conn.close()


@model_bp.route("/api/models/<int:model_id>", methods=["GET"])
def get_model(model_id):
    """查询单个模型"""
    conn = get_connection()
    if conn is None:
        return jsonify(fail("数据库连接失败")), 500

    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            """
            SELECT model_id, model_name, type, version, description
            FROM model
            WHERE model_id=%s
            """,
            (model_id,),
        )
        row = cursor.fetchone()
        if row is None:
            return jsonify(fail("模型不存在")), 404
        return jsonify(ok(row))
    except Exception as e:
        return jsonify(fail(str(e))), 500
    finally:
        conn.close()


@model_bp.route("/api/models", methods=["POST"])
def create_model():
    """创建新模型"""
    data = request.get_json()
    if not data or not data.get("model_name"):
        return jsonify(fail("模型名称不能为空")), 400

    conn = get_connection()
    if conn is None:
        return jsonify(fail("数据库连接失败")), 500

    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO model (model_name, type, version, description)
            VALUES (%s, %s, %s, %s)
            """,
            (data["model_name"], data.get("type", ""), data.get("version", "1.0"), data.get("description", "")),
        )
        conn.commit()
        new_id = cursor.lastrowid
        return jsonify(ok({"model_id": new_id})), 201
    except Exception as e:
        conn.rollback()
        return jsonify(fail(str(e))), 500
    finally:
        conn.close()


@model_bp.route("/api/models/<int:model_id>", methods=["PUT"])
def update_model(model_id):
    """更新模型"""
    data = request.get_json()
    if not data:
        return jsonify(fail("请求体不能为空")), 400

    conn = get_connection()
    if conn is None:
        return jsonify(fail("数据库连接失败")), 500

    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE model
            SET model_name=%s, type=%s, version=%s, description=%s
            WHERE model_id=%s
            """,
            (data.get("model_name"), data.get("type", ""), data.get("version", "1.0"), data.get("description", ""), model_id),
        )
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify(fail("模型不存在")), 404
        return jsonify(ok({"model_id": model_id}))
    except Exception as e:
        conn.rollback()
        return jsonify(fail(str(e))), 500
    finally:
        conn.close()


@model_bp.route("/api/models/<int:model_id>", methods=["DELETE"])
def delete_model(model_id):
    """删除模型"""
    conn = get_connection()
    if conn is None:
        return jsonify(fail("数据库连接失败")), 500

    try:
        cursor = conn.cursor()
        # 先删除关联的 choose_relation 记录
        cursor.execute("DELETE FROM choose_relation WHERE model_id=%s", (model_id,))
        cursor.execute("DELETE FROM model WHERE model_id=%s", (model_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify(fail("模型不存在")), 404
        return jsonify(ok({"model_id": model_id}))
    except Exception as e:
        conn.rollback()
        return jsonify(fail(str(e))), 500
    finally:
        conn.close()
