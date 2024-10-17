import pandas as pd


def read_fas_file(file_path):
    """读取FAS文件并返回序列信息"""
    with open(file_path, 'r') as file:
        lines = file.readlines()

    sequences = []
    for i in range(1, len(lines), 2):  # 跳过头部行
        sequences.append(lines[i].strip())

    return sequences


def calculate_mutation_rate(ref_seq, target_seq, positions):
    """计算给定位点的突变率"""
    mutation_count = 0
    total_sequences = len(target_seq)

    # 遍历每个序列，检查给定位点是否突变
    for seq in target_seq:
        # 检查所有给定位点是否都突变
        if all(ref_seq[pos] != seq[pos] for pos in positions):
            mutation_count += 1

    return mutation_count / total_sequences if total_sequences > 0 else 0


def main():
    # 文件路径设置
    ref_file_path = "D:\\桌面。\\全长连锁分析\\4\\compared.fas"
    target_file_path = "D:\\桌面。\\全长连锁分析\\4\\RSVB.fas"
    reference_table_path = "D:\\桌面。\\全长连锁分析\\4\\RSVB-unit.xlsx"
    output_file_path = "D:\\桌面。\\全长连锁分析\\4\\RSVB-text4.xlsx"

    # 读取参考序列和待分析序列
    ref_sequences = read_fas_file(ref_file_path)
    target_sequences = read_fas_file(target_file_path)

    # 读取参考表格
    reference_table = pd.read_excel(reference_table_path, header=None)

    chains = []  # 存储链和对应的突变率

    for index in range(0, len(reference_table), 3):  # 读取第0行、第3行、第6行...
        if index >= len(reference_table):
            break

        # 获取当前行的位点数据
        positions = list(map(int, reference_table.iloc[index, :].dropna().tolist()))

        # 如果没有链，直接添加
        if not chains:
            new_chain_rate = calculate_mutation_rate(ref_sequences[0], target_sequences, positions)
            chains.append((positions, new_chain_rate))
            continue

        # 合并逻辑
        merged = False
        for i in range(len(chains)):
            existing_chain, existing_rate = chains[i]
            if set(existing_chain) & set(positions):  # 检查是否有公共点
                merged_chain = sorted(set(existing_chain + positions))
                merged_chain_rate = calculate_mutation_rate(ref_sequences[0], target_sequences, merged_chain)

                if 0.001 < merged_chain_rate < 0.999:
                    chains[i] = (merged_chain, merged_chain_rate)  # 更新现有链
                    merged = True
                break

        if not merged:
            # 计算新链的突变率
            new_chain_rate = calculate_mutation_rate(ref_sequences[0], target_sequences, positions)
            chains.append((positions, new_chain_rate))

    # 筛选突变率在0.1到0.9之间的链
    unique_chains = {}
    for chain, rate in chains:
        if 0.001 < rate < 0.999 :
            unique_chains[rate] = chain

    # 创建输出数据
    output_data = []
    for rate, chain in unique_chains.items():
        output_data.append(chain)  # 添加位点链数据
        output_data.append([rate])  # 添加突变率

    # 创建DataFrame并输出到Excel
    df = pd.DataFrame(output_data)
    df.to_excel(output_file_path, index=False, header=False)

    print("结果已保存至:", output_file_path)


if __name__ == "__main__":
    main()
