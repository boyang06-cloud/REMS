import pymysql
from flask import Blueprint, jsonify, request

from database import get_connection
from utils.response import fail, ok

experiment_bp = Blueprint("experiment", __name__)


def _build_relation_map(rows, experiment_key, related_key):
    """把关联表查询结果整理成 { experiment_id: [related_id, ...] }"""
    relation_map = {}
    for row in rows:
        experiment_id = row[experiment_key]
        related_id = row[related_key]
        relation_map.setdefault(experiment_id, []).append(related_id)
    return relation_map


@experiment_bp.route("/api/experiments", methods=["GET"])
def get_experiments():
    """查询所有实验，附带 M:N 关联 ID"""
    conn = get_connection()
    if conn is None:
        return jsonify(fail("数据库连接失败")), 500

    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute(
            """
            SELECT experiment_id, experiment_name, status, config, created_at, description
            FROM experiment
            ORDER BY experiment_id
            """
        )
        experiments = cursor.fetchall()

        cursor.execute("SELECT project_id, experiment_id FROM conduct")
        project_map = _build_relation_map(cursor.fetchall(), "experiment_id", "project_id")

        cursor.execute("SELECT dataset_id, experiment_id FROM use_relation")
        dataset_map = _build_relation_map(cursor.fetchall(), "experiment_id", "dataset_id")

        cursor.execute("SELECT model_id, experiment_id FROM choose_relation")
        model_map = _build_relation_map(cursor.fetchall(), "experiment_id", "model_id")

        cursor.execute("SELECT tag_id, experiment_id FROM belong_to")
        tag_map = _build_relation_map(cursor.fetchall(), "experiment_id", "tag_id")

        for exp in experiments:
            experiment_id = exp["experiment_id"]
            exp["project_ids"] = project_map.get(experiment_id, [])
            exp["dataset_ids"] = dataset_map.get(experiment_id, [])
            exp["model_ids"] = model_map.get(experiment_id, [])
            exp["tag_ids"] = tag_map.get(experiment_id, [])
            if exp["created_at"]:
                exp["created_at"] = exp["created_at"].isoformat()

        return jsonify(ok(experiments))
    except Exception as e:
        return jsonify(fail(str(e))), 500
    finally:
        conn.close()


@experiment_bp.route("/api/experiments/<int:experiment_id>", methods=["GET"])
def get_experiment(experiment_id):
    """查询单个实验，附带 M:N 关联 ID"""
    conn = get_connection()
    if conn is None:
        return jsonify(fail("数据库连接失败")), 500

    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute(
            """
            SELECT experiment_id, experiment_name, status, config, created_at, description
            FROM experiment
            WHERE experiment_id=%s
            """,
            (experiment_id,),
        )
        exp = cursor.fetchone()
        if exp is None:
            return jsonify(fail("实验不存在")), 404

        cursor.execute(
            "SELECT project_id FROM conduct WHERE experiment_id=%s",
            (experiment_id,),
        )
        exp["project_ids"] = [r["project_id"] for r in cursor.fetchall()]

        cursor.execute(
            "SELECT dataset_id FROM use_relation WHERE experiment_id=%s",
            (experiment_id,),
        )
        exp["dataset_ids"] = [r["dataset_id"] for r in cursor.fetchall()]

        cursor.execute(
            "SELECT model_id FROM choose_relation WHERE experiment_id=%s",
            (experiment_id,),
        )
        exp["model_ids"] = [r["model_id"] for r in cursor.fetchall()]

        cursor.execute(
            "SELECT tag_id FROM belong_to WHERE experiment_id=%s",
            (experiment_id,),
        )
        exp["tag_ids"] = [r["tag_id"] for r in cursor.fetchall()]

        if exp["created_at"]:
            exp["created_at"] = exp["created_at"].isoformat()

        return jsonify(ok(exp))
    except Exception as e:
        return jsonify(fail(str(e))), 500
    finally:
        conn.close()


@experiment_bp.route("/api/experiments", methods=["POST"])
def create_experiment():
    """创建新实验及其关联"""
    data = request.get_json()
    if not data or not data.get("experiment_name"):
        return jsonify(fail("实验名称不能为空")), 400

    conn = get_connection()
    if conn is None:
        return jsonify(fail("数据库连接失败")), 500

    try:
        cursor = conn.cursor()

        # 插入实验记录
        cursor.execute(
            """
            INSERT INTO experiment (experiment_name, status, config, created_at, description)
            VALUES (%s, %s, %s, NOW(), %s)
            """,
            (
                data["experiment_name"],
                data.get("status", "Draft"),
                data.get("config", ""),
                data.get("description", ""),
            ),
        )
        experiment_id = cursor.lastrowid

        # 插入 M:N 关联
        _insert_relations(cursor, "conduct", "project_id", "experiment_id",
                          experiment_id, data.get("project_ids", []))
        _insert_relations(cursor, "use_relation", "dataset_id", "experiment_id",
                          experiment_id, data.get("dataset_ids", []))
        _insert_relations(cursor, "choose_relation", "model_id", "experiment_id",
                          experiment_id, data.get("model_ids", []))
        _insert_relations(cursor, "belong_to", "tag_id", "experiment_id",
                          experiment_id, data.get("tag_ids", []))

        conn.commit()
        return jsonify(ok({"experiment_id": experiment_id})), 201
    except Exception as e:
        conn.rollback()
        return jsonify(fail(str(e))), 500
    finally:
        conn.close()


@experiment_bp.route("/api/experiments/<int:experiment_id>", methods=["PUT"])
def update_experiment(experiment_id):
    """更新实验及其关联"""
    data = request.get_json()
    if not data:
        return jsonify(fail("请求体不能为空")), 400

    conn = get_connection()
    if conn is None:
        return jsonify(fail("数据库连接失败")), 500

    try:
        cursor = conn.cursor()

        # 更新实验记录
        cursor.execute(
            """
            UPDATE experiment
            SET experiment_name=%s, status=%s, config=%s, description=%s
            WHERE experiment_id=%s
            """,
            (
                data.get("experiment_name"),
                data.get("status", "Draft"),
                data.get("config", ""),
                data.get("description", ""),
                experiment_id,
            ),
        )
        if cursor.rowcount == 0:
            return jsonify(fail("实验不存在")), 404

        # 更新 M:N 关联（先删后插）
        _replace_relations(cursor, "conduct", "project_id", "experiment_id",
                           experiment_id, data.get("project_ids", []))
        _replace_relations(cursor, "use_relation", "dataset_id", "experiment_id",
                           experiment_id, data.get("dataset_ids", []))
        _replace_relations(cursor, "choose_relation", "model_id", "experiment_id",
                           experiment_id, data.get("model_ids", []))
        _replace_relations(cursor, "belong_to", "tag_id", "experiment_id",
                           experiment_id, data.get("tag_ids", []))

        conn.commit()
        return jsonify(ok({"experiment_id": experiment_id}))
    except Exception as e:
        conn.rollback()
        return jsonify(fail(str(e))), 500
    finally:
        conn.close()


@experiment_bp.route("/api/experiments/<int:experiment_id>", methods=["DELETE"])
def delete_experiment(experiment_id):
    """删除实验及其所有关联"""
    conn = get_connection()
    if conn is None:
        return jsonify(fail("数据库连接失败")), 500

    try:
        cursor = conn.cursor()
        # 先删除所有关联记录
        cursor.execute("DELETE FROM conduct WHERE experiment_id=%s", (experiment_id,))
        cursor.execute("DELETE FROM use_relation WHERE experiment_id=%s", (experiment_id,))
        cursor.execute("DELETE FROM choose_relation WHERE experiment_id=%s", (experiment_id,))
        cursor.execute("DELETE FROM belong_to WHERE experiment_id=%s", (experiment_id,))
        cursor.execute("DELETE FROM result WHERE experiment_id=%s", (experiment_id,))
        cursor.execute("DELETE FROM experiment WHERE experiment_id=%s", (experiment_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify(fail("实验不存在")), 404
        return jsonify(ok({"experiment_id": experiment_id}))
    except Exception as e:
        conn.rollback()
        return jsonify(fail(str(e))), 500
    finally:
        conn.close()


# ---------- 辅助函数 ----------

def _insert_relations(cursor, table, fk_column, experiment_column, experiment_id, ids):
    """批量插入 M:N 关联记录"""
    for id_val in ids:
        cursor.execute(
            f"INSERT INTO {table} ({fk_column}, {experiment_column}) VALUES (%s, %s)",
            (id_val, experiment_id),
        )


def _replace_relations(cursor, table, fk_column, experiment_column, experiment_id, ids):
    """先删除再插入 M:N 关联记录"""
    cursor.execute(
        f"DELETE FROM {table} WHERE {experiment_column}=%s",
        (experiment_id,),
    )
    _insert_relations(cursor, table, fk_column, experiment_column, experiment_id, ids)
