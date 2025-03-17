import os
def is_valid_csv_path(resource_path):
    """
    判断给定的 resource_path 是否为有效的文件路径，且该文件是否为 CSV 文件。

    参数：
        resource_path (str): 文件路径。

    返回：
        bool: 如果是有效的 CSV 文件路径，则返回 True，否则返回 False。
    """

    # 1. 判断是否为路径以及文件是否存在
    if not os.path.exists(resource_path):
        print(f"错误：路径 '{resource_path}' 不存在。")
        return False

    if not os.path.isfile(resource_path):
        print(f"错误：'{resource_path}' 不是一个文件。")
        return False

    # 2. 判断是否为 CSV 文件
    if not resource_path.lower().endswith(".csv"):
        print(f"错误：'{resource_path}' 不是一个 CSV 文件。")
        return False

    return True

__all__ = (
    "is_valid_csv_path"
)