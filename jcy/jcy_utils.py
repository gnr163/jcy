
def human_size(num_bytes: int) -> str:
    """将字节数格式化为可读字符串，例如 1536000 -> '1.46 MB'"""
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    size = float(num_bytes)
    idx = 0
    while size >= 1024 and idx < len(units) - 1:
        size /= 1024
        idx += 1
    return f"{size:.2f} {units[idx]}"
