def ok(data):
    """成功响应：{ "success": true, "data": ... }"""
    return {"success": True, "data": data}


def fail(message):
    """失败响应：{ "success": false, "error": "..." }"""
    return {"success": False, "error": message}
