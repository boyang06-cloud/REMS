# REMS — Research Experiment Management System

科研实验管理系统，数据库课程设计项目。

---

## 技术栈

| 层级 | 技术 |
|---|---|
| **前端** | React 19 + TypeScript + TanStack Start |
| **样式** | Tailwind CSS v4 + shadcn/ui |
| **后端** | Flask (Python) |
| **数据库** | MySQL + PyMySQL |
| **包管理器** | Bun (前端) / pip (后端) |

---

## 项目结构

```
REMS/
├── frontend/                  # React 前端
│   ├── src/
│   │   ├── routes/            # 页面路由（TanStack Router）
│   │   ├── components/        # UI 组件（shadcn/ui）
│   │   └── lib/
│   │       ├── api.ts         # 后端 API 调用层
│   │       ├── rems-store.ts  # 前端状态管理
│   │       ├── rems-types.ts  # TypeScript 类型定义
│   │       └── use-data-loader.ts  # 数据加载 Hook
│   ├── package.json
│   └── vite.config.ts
│
├── backend/                   # Flask 后端
│   ├── app.py                 # 入口，注册蓝图 + CORS
│   ├── config.py              # 数据库连接配置
│   ├── database.py            # 数据库连接函数
│   ├── requirements.txt       # Python 依赖
│   ├── test_connection.py     # 数据库连接测试
│   ├── routes/                # API 路由（每张表一个文件）
│   │   ├── project.py
│   │   ├── experiment.py
│   │   ├── dataset.py
│   │   ├── model.py
│   │   ├── result.py
│   │   └── tag.py
│   └── utils/
│       └── response.py        # 统一响应格式
│
├── database/                  # SQL 脚本
│   ├── createTABLE_sql.sql    # 建表语句
│   └── createRECORD_sql.sql   # 示例数据
│
└── docs/                      # 设计文档
    ├── REMS.cdm / REMS.ldm    # 概念/逻辑数据模型
    └── ...
```

---

## 数据库设计

### 实体

- **Project** — 项目
- **Experiment** — 实验
- **Dataset** — 数据集
- **Model** — 模型
- **Result** — 实验结果
- **Tag** — 标签

### 关系

- Project ↔ Experiment（M:N，通过 `conduct` 桥接）
- Experiment ↔ Dataset（M:N，通过 `use_relation` 桥接）
- Experiment ↔ Model（M:N，通过 `choose_relation` 桥接）
- Experiment ↔ Tag（M:N，通过 `belong_to` 桥接）
- Experiment → Result（1:N）

关系模型如图:
![关系模型](docs\screenshots\logical schema.png)
ER图：
![ER图](docs\screenshots\ER.png)
---

## 快速开始

### 前置条件

- Python 3.9+
- MySQL 8.0+
- Bun（前端包管理器，[安装](https://bun.sh)）
- Node.js 18+

### 1. 创建数据库

```sql
CREATE DATABASE rems CHARACTER SET utf8mb4;
```

### 2. 导入表结构和示例数据

```bash
# 方法一：命令行导入
mysql -u root -p rems < database/createTABLE_sql.sql
mysql -u root -p rems < database/createRECORD_sql.sql

# 方法二：MySQL Workbench 等 GUI 工具直接执行 SQL 文件
```

### 3. 配置数据库连接

编辑 `backend/config.py`，修改为你的 MySQL 连接信息：

```python
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "你的密码",
    "database": "rems",
    "charset": "utf8mb4",
}
```

### 4. 启动后端

```bash
cd backend
pip install -r requirements.txt
python app.py
```

后端运行在 `http://localhost:5000`。

### 5. 启动前端

```bash
cd frontend
bun install
bun run dev
```

前端运行在 `http://localhost:8080`）。

### 6. 访问

浏览器打开 `http://localhost:8080` 即可使用。

---

## API 接口

所有接口返回统一格式：

```json
{
  "success": true,
  "data": [...]
}
```

错误时：

```json
{
  "success": false,
  "error": "错误信息"
}
```

### 接口列表

| 方法 | 路径 | 说明 |
|---|---|---|
| `GET` | `/api/health` | 健康检查 |
| `GET` | `/api/projects` | 获取所有项目 |
| `GET` | `/api/projects/<id>` | 获取单个项目 |
| `POST` | `/api/projects` | 创建项目 |
| `PUT` | `/api/projects/<id>` | 更新项目 |
| `DELETE` | `/api/projects/<id>` | 删除项目 |
| `GET` | `/api/experiments` | 获取所有实验（含关联 ID） |
| `GET` | `/api/experiments/<id>` | 获取单个实验 |
| `POST` | `/api/experiments` | 创建实验（含 M:N 关联） |
| `PUT` | `/api/experiments/<id>` | 更新实验（替换 M:N 关联） |
| `DELETE` | `/api/experiments/<id>` | 删除实验（级联删除关联） |
| `GET` | `/api/datasets` | 获取所有数据集 |
| `GET` | `/api/datasets/<id>` | 获取单个数据集 |
| `POST` | `/api/datasets` | 创建数据集 |
| `PUT` | `/api/datasets/<id>` | 更新数据集 |
| `DELETE` | `/api/datasets/<id>` | 删除数据集 |
| `GET` | `/api/models` | 获取所有模型 |
| `GET` | `/api/models/<id>` | 获取单个模型 |
| `POST` | `/api/models` | 创建模型 |
| `PUT` | `/api/models/<id>` | 更新模型 |
| `DELETE` | `/api/models/<id>` | 删除模型 |
| `GET` | `/api/results` | 获取所有结果 |
| `GET` | `/api/results/<id>` | 获取单个结果 |
| `POST` | `/api/results` | 创建结果 |
| `PUT` | `/api/results/<id>` | 更新结果 |
| `DELETE` | `/api/results/<id>` | 删除结果 |
| `GET` | `/api/tags` | 获取所有标签 |
| `GET` | `/api/tags/<id>` | 获取单个标签 |
| `POST` | `/api/tags` | 创建标签 |
| `PUT` | `/api/tags/<id>` | 更新标签 |
| `DELETE` | `/api/tags/<id>` | 删除标签 |

---

## 数据流

```
用户操作页面
    ↓
前端组件（React）
    ↓
api.ts（HTTP 请求）
    ↓
Flask 路由（backend/routes/）
    ↓
database.py（PyMySQL）
    ↓
MySQL 数据库
    ↓
JSON 响应返回前端
    ↓
rems-store.ts（状态更新）
    ↓
页面实时刷新
```

---

## 注意事项

- **config.py** 中的数据库密码仅用于本地开发，不要提交到公开仓库
- 前端通过 localhost 调用后端 API，如需修改端口请同步更新 `frontend/src/lib/api.ts`
- 后端使用 raw SQL + 参数化查询，未使用 ORM

