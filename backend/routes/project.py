import pymysql
from flask import Blueprint, jsonify, request

from database import get_connection
from utils.response import fail, ok

project_bp = Blueprint("project", __name__)


@project_bp.route("/api/projects", methods=["GET"])
def get_projects():
    """查询所有项目"""
    conn = get_connection()
    if conn is None:
        return jsonify(fail("数据库连接失败")), 500

    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            """
            SELECT project_id, project_name, description, created_at
            FROM project
            ORDER BY project_id
            """
        )
        rows = cursor.fetchall()

        for row in rows:
            if row["created_at"]:
                row["created_at"] = row["created_at"].isoformat()

        return jsonify(ok(rows))
    except Exception as e:
        return jsonify(fail(str(e))), 500
    finally:
        conn.close()


@project_bp.route("/api/projects/<int:project_id>", methods=["GET"])
def get_project(project_id):
    """查询单个项目"""
    conn = get_connection()
    if conn is None:
        return jsonify(fail("数据库连接失败")), 500

    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            """
            SELECT project_id, project_name, description, created_at
            FROM project
            WHERE project_id=%s
            """,
            (project_id,),
        )
        row = cursor.fetchone()
        if row is None:
            return jsonify(fail("项目不存在")), 404

        if row["created_at"]:
            row["created_at"] = row["created_at"].isoformat()

        return jsonify(ok(row))
    except Exception as e:
        return jsonify(fail(str(e))), 500
    finally:
        conn.close()


@project_bp.route("/api/projects", methods=["POST"])
def create_project():
    """创建新项目"""
    data = request.get_json()
    if not data or not data.get("project_name"):
        return jsonify(fail("项目名称不能为空")), 400

    conn = get_connection()
    if conn is None:
        return jsonify(fail("数据库连接失败")), 500

    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO project (project_name, description, created_at)
            VALUES (%s, %s, NOW())
            """,
            (data["project_name"], data.get("description", "")),
        )
        conn.commit()
        new_id = cursor.lastrowid
        return jsonify(ok({"project_id": new_id})), 201
    except Exception as e:
        conn.rollback()
        return jsonify(fail(str(e))), 500
    finally:
        conn.close()


@project_bp.route("/api/projects/<int:project_id>", methods=["PUT"])
def update_project(project_id):
    """更新项目"""
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
            UPDATE project
            SET project_name=%s, description=%s
            WHERE project_id=%s
            """,
            (data.get("project_name"), data.get("description", ""), project_id),
        )
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify(fail("项目不存在")), 404
        return jsonify(ok({"project_id": project_id}))
    except Exception as e:
        conn.rollback()
        return jsonify(fail(str(e))), 500
    finally:
        conn.close()


@project_bp.route("/api/projects/<int:project_id>", methods=["DELETE"])
def delete_project(project_id):
    """删除项目"""
    conn = get_connection()
    if conn is None:
        return jsonify(fail("数据库连接失败")), 500

    try:
        cursor = conn.cursor()
        # 先删除关联的 conduct 记录
        cursor.execute("DELETE FROM conduct WHERE project_id=%s", (project_id,))
        cursor.execute("DELETE FROM project WHERE project_id=%s", (project_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify(fail("项目不存在")), 404
        return jsonify(ok({"project_id": project_id}))
    except Exception as e:
        conn.rollback()
        return jsonify(fail(str(e))), 500
    finally:
        conn.close()
