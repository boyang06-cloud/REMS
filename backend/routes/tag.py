import pymysql
from flask import Blueprint, jsonify, request

from database import get_connection
from utils.response import fail, ok

tag_bp = Blueprint("tag", __name__)


@tag_bp.route("/api/tags", methods=["GET"])
def get_tags():
    """查询所有标签"""
    conn = get_connection()
    if conn is None:
        return jsonify(fail("数据库连接失败")), 500

    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            """
            SELECT tag_id, tag_name
            FROM tag
            ORDER BY tag_id
            """
        )
        rows = cursor.fetchall()
        return jsonify(ok(rows))
    except Exception as e:
        return jsonify(fail(str(e))), 500
    finally:
        conn.close()


@tag_bp.route("/api/tags/<int:tag_id>", methods=["GET"])
def get_tag(tag_id):
    """查询单个标签"""
    conn = get_connection()
    if conn is None:
        return jsonify(fail("数据库连接失败")), 500

    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            """
            SELECT tag_id, tag_name
            FROM tag
            WHERE tag_id=%s
            """,
            (tag_id,),
        )
        row = cursor.fetchone()
        if row is None:
            return jsonify(fail("标签不存在")), 404
        return jsonify(ok(row))
    except Exception as e:
        return jsonify(fail(str(e))), 500
    finally:
        conn.close()


@tag_bp.route("/api/tags", methods=["POST"])
def create_tag():
    """创建新标签"""
    data = request.get_json()
    if not data or not data.get("tag_name"):
        return jsonify(fail("标签名称不能为空")), 400

    conn = get_connection()
    if conn is None:
        return jsonify(fail("数据库连接失败")), 500

    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO tag (tag_name)
            VALUES (%s)
            """,
            (data["tag_name"],),
        )
        conn.commit()
        new_id = cursor.lastrowid
        return jsonify(ok({"tag_id": new_id})), 201
    except Exception as e:
        conn.rollback()
        return jsonify(fail(str(e))), 500
    finally:
        conn.close()


@tag_bp.route("/api/tags/<int:tag_id>", methods=["PUT"])
def update_tag(tag_id):
    """更新标签"""
    data = request.get_json()
    if not data or not data.get("tag_name"):
        return jsonify(fail("标签名称不能为空")), 400

    conn = get_connection()
    if conn is None:
        return jsonify(fail("数据库连接失败")), 500

    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE tag
            SET tag_name=%s
            WHERE tag_id=%s
            """,
            (data["tag_name"], tag_id),
        )
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify(fail("标签不存在")), 404
        return jsonify(ok({"tag_id": tag_id}))
    except Exception as e:
        conn.rollback()
        return jsonify(fail(str(e))), 500
    finally:
        conn.close()


@tag_bp.route("/api/tags/<int:tag_id>", methods=["DELETE"])
def delete_tag(tag_id):
    """删除标签"""
    conn = get_connection()
    if conn is None:
        return jsonify(fail("数据库连接失败")), 500

    try:
        cursor = conn.cursor()
        # 先删除关联的 belong_to 记录
        cursor.execute("DELETE FROM belong_to WHERE tag_id=%s", (tag_id,))
        cursor.execute("DELETE FROM tag WHERE tag_id=%s", (tag_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify(fail("标签不存在")), 404
        return jsonify(ok({"tag_id": tag_id}))
    except Exception as e:
        conn.rollback()
        return jsonify(fail(str(e))), 500
    finally:
        conn.close()
