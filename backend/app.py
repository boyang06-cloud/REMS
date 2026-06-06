from flask import Flask, jsonify

# 导入每张表的蓝图
from routes.dataset import dataset_bp
from routes.experiment import experiment_bp
from routes.model import model_bp
from routes.project import project_bp
from routes.result import result_bp
from routes.tag import tag_bp
from utils.response import ok

app = Flask(__name__)
app.register_blueprint(project_bp)
app.register_blueprint(tag_bp)
app.register_blueprint(dataset_bp)
app.register_blueprint(model_bp)
app.register_blueprint(result_bp)
app.register_blueprint(experiment_bp)

# 允许前端（Vite 5173）访问后端，解决跨域 CROS 问题
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    return response


# 处理前端 OPTIONS 预检请求
@app.route("/api/<path:path>", methods=["OPTIONS"])
def handle_options(path):
    return jsonify(ok("options"))


@app.route("/api/health")
def health():
    return jsonify(ok("ok"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
