import pymysql
from flask import Blueprint, jsonify, request

from database import get_connection
from utils.response import fail, ok

result_bp = Blueprint("result", __name__)


@result_bp.route("/api/results", methods=["GET"])
def get_results():
    """查询所有实验结果"""
    conn = get_connection()
    if conn is None:
        return jsonify(fail("数据库连接失败")), 500

    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            """
            SELECT result_id, experiment_id, metric_name, metric_value, record_time
            FROM result
            ORDER BY result_id
            """
        )
        rows = cursor.fetchall()

        for row in rows:
            if row["record_time"]:
                row["record_time"] = row["record_time"].isoformat()

        return jsonify(ok(rows))
    except Exception as e:
        return jsonify(fail(str(e))), 500
    finally:
        conn.close()


@result_bp.route("/api/results/<int:result_id>", methods=["GET"])
def get_result(result_id):
    """查询单个结果"""
    conn = get_connection()
    if conn is None:
        return jsonify(fail("数据库连接失败")), 500

    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            """
            SELECT result_id, experiment_id, metric_name, metric_value, record_time
            FROM result
            WHERE result_id=%s
            """,
            (result_id,),
        )
        row = cursor.fetchone()
        if row is None:
            return jsonify(fail("结果不存在")), 404

        if row["record_time"]:
            row["record_time"] = row["record_time"].isoformat()

        return jsonify(ok(row))
    except Exception as e:
        return jsonify(fail(str(e))), 500
    finally:
        conn.close()


@result_bp.route("/api/results", methods=["POST"])
def create_result():
    """创建新结果"""
    data = request.get_json()
    if not data or not data.get("experiment_id") or not data.get("metric_name"):
        return jsonify(fail("实验ID和指标名称不能为空")), 400

    conn = get_connection()
    if conn is None:
        return jsonify(fail("数据库连接失败")), 500

    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO result (experiment_id, metric_name, metric_value, record_time)
            VALUES (%s, %s, %s, NOW())
            """,
            (data["experiment_id"], data["metric_name"], data.get("metric_value", 0)),
        )
        conn.commit()
        new_id = cursor.lastrowid
        return jsonify(ok({"result_id": new_id})), 201
    except Exception as e:
        conn.rollback()
        return jsonify(fail(str(e))), 500
    finally:
        conn.close()


@result_bp.route("/api/results/<int:result_id>", methods=["PUT"])
def update_result(result_id):
    """更新结果"""
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
            UPDATE result
            SET metric_name=%s, metric_value=%s
            WHERE result_id=%s
            """,
            (data.get("metric_name"), data.get("metric_value", 0), result_id),
        )
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify(fail("结果不存在")), 404
        return jsonify(ok({"result_id": result_id}))
    except Exception as e:
        conn.rollback()
        return jsonify(fail(str(e))), 500
    finally:
        conn.close()


@result_bp.route("/api/results/<int:result_id>", methods=["DELETE"])
def delete_result(result_id):
    """删除结果"""
    conn = get_connection()
    if conn is None:
        return jsonify(fail("数据库连接失败")), 500

    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM result WHERE result_id=%s", (result_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify(fail("结果不存在")), 404
        return jsonify(ok({"result_id": result_id}))
    except Exception as e:
        conn.rollback()
        return jsonify(fail(str(e))), 500
    finally:
        conn.close()
