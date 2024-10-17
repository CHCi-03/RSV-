import pandas as pd
from collections import defaultdict

# 读取Excel表格"
input_file_path = r"D:\桌面。\副本linkage-A-all-rename-1-考虑突变方向.xlsx"
output_file_path = r"D:\桌面。\副本linkage-A-all-rename-1.xlsx"

# 读取数据
df = pd.read_excel(input_file_path)

# 打印读取的数据
print("读取的数据:")
print(df)

# 创建一个图结构
graph = defaultdict(set)

# 遍历DataFrame中的每一列
for col_index in range(len(df.columns)):
    if col_index % 3 == 0:  # 选择第0、3、6列
        col_str = str(col_index)  # 列索引转换为字符串
        print(f"处理列索引: {col_index}")

        # 获取当前列的数据并去除NaN
        column_data = df.iloc[:, col_index].dropna()

        # 打印列数据以调试
        print(f"列数据: {column_data.tolist()}")

        # 尝试提取顶点
        vertices = []
        for item in column_data:
            if isinstance(item, (int, float)):  # 处理整数和浮点数
                vertices.append(int(item))  # 确保将数字转换为整数

        vertices = list(set(vertices))  # 去重
        print(f"提取的顶点: {vertices}")

        # 将所有顶点连接起来
        for i in range(len(vertices) - 1):
            graph[vertices[i]].add(vertices[i + 1])
            graph[vertices[i + 1]].add(vertices[i])


# 查找所有连通分量
def find_connected_components(graph):
    visited = set()
    components = []

    def dfs(node, component):
        visited.add(node)
        component.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor, component)

    for node in graph:
        if node not in visited:
            component = []
            dfs(node, component)
            components.append(component)
    return components


# 获取连通分量
connected_components = find_connected_components(graph)

# 打印连通分量以调试
print("找到的连通分量:")
print(connected_components)

# 准备输出数据
output_data = []
for component in connected_components:
    output_data.append(sorted(component))

# 转换为DataFrame
output_df = pd.DataFrame({f'Path {i + 1}': pd.Series(path) for i, path in enumerate(output_data)})

# 保存到Excel文件
output_df.to_excel(output_file_path, index=False)
print(f'数据已保存到: {output_file_path}')
