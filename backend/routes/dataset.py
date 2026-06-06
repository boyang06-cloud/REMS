import pymysql
from flask import Blueprint, jsonify, request

from database import get_connection
from utils.response import fail, ok

dataset_bp = Blueprint("dataset", __name__)


@dataset_bp.route("/api/datasets", methods=["GET"])
def get_datasets():
    """查询所有数据集"""
    conn = get_connection()
    if conn is None:
        return jsonify(fail("数据库连接失败")), 500

    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            """
            SELECT dataset_id, dataset_name, modality, description
            FROM dataset
            ORDER BY dataset_id
            """
        )
        rows = cursor.fetchall()
        return jsonify(ok(rows))
    except Exception as e:
        return jsonify(fail(str(e))), 500
    finally:
        conn.close()


@dataset_bp.route("/api/datasets/<int:dataset_id>", methods=["GET"])
def get_dataset(dataset_id):
    """查询单个数据集"""
    conn = get_connection()
    if conn is None:
        return jsonify(fail("数据库连接失败")), 500

    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            """
            SELECT dataset_id, dataset_name, modality, description
            FROM dataset
            WHERE dataset_id=%s
            """,
            (dataset_id,),
        )
        row = cursor.fetchone()
        if row is None:
            return jsonify(fail("数据集不存在")), 404
        return jsonify(ok(row))
    except Exception as e:
        return jsonify(fail(str(e))), 500
    finally:
        conn.close()


@dataset_bp.route("/api/datasets", methods=["POST"])
def create_dataset():
    """创建新数据集"""
    data = request.get_json()
    if not data or not data.get("dataset_name"):
        return jsonify(fail("数据集名称不能为空")), 400

    conn = get_connection()
    if conn is None:
        return jsonify(fail("数据库连接失败")), 500

    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO dataset (dataset_name, modality, description)
            VALUES (%s, %s, %s)
            """,
            (data["dataset_name"], data.get("modality", ""), data.get("description", "")),
        )
        conn.commit()
        new_id = cursor.lastrowid
        return jsonify(ok({"dataset_id": new_id})), 201
    except Exception as e:
        conn.rollback()
        return jsonify(fail(str(e))), 500
    finally:
        conn.close()


@dataset_bp.route("/api/datasets/<int:dataset_id>", methods=["PUT"])
def update_dataset(dataset_id):
    """更新数据集"""
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
            UPDATE dataset
            SET dataset_name=%s, modality=%s, description=%s
            WHERE dataset_id=%s
            """,
            (data.get("dataset_name"), data.get("modality", ""), data.get("description", ""), dataset_id),
        )
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify(fail("数据集不存在")), 404
        return jsonify(ok({"dataset_id": dataset_id}))
    except Exception as e:
        conn.rollback()
        return jsonify(fail(str(e))), 500
    finally:
        conn.close()


@dataset_bp.route("/api/datasets/<int:dataset_id>", methods=["DELETE"])
def delete_dataset(dataset_id):
    """删除数据集"""
    conn = get_connection()
    if conn is None:
        return jsonify(fail("数据库连接失败")), 500

    try:
        cursor = conn.cursor()
        # 先删除关联的 use_relation 记录
        cursor.execute("DELETE FROM use_relation WHERE dataset_id=%s", (dataset_id,))
        cursor.execute("DELETE FROM dataset WHERE dataset_id=%s", (dataset_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify(fail("数据集不存在")), 404
        return jsonify(ok({"dataset_id": dataset_id}))
    except Exception as e:
        conn.rollback()
        return jsonify(fail(str(e))), 500
    finally:
        conn.close()
