import os
import pandas as pd

# 定义病毒类型和基础目录
CapsidSubtype = 'RSVB'  # 确保这个值与你的文件名匹配
base_dir = 'D:\\桌面。\\B-全长'  # 使用双反斜杠或原始字符串

# 构建文件路径
File = os.path.join(base_dir, CapsidSubtype + '.fas')
ComparedFile = os.path.join(base_dir, 'compared.fas')

# 初始化变量
seqs = []
MutationDirection = {}
MutationDirection_list = []
MutationRatio_list = []

# 读取序列数据
with open(ComparedFile, 'r') as compared:
    compared.readline()  # 跳过compared文件的第一行
    ComparedSeq = compared.readline().strip()  # 读取参照序列并去除换行符

with open(File, 'r') as f:
    for line in f:
        if line.startswith('>'):  # 忽略以'>'开头的行
            continue
        seqs.append(line.strip())  # 读取序列数据并去除换行符

# 假设所有序列长度相同，取第一个序列长度作为SeqLen
SeqLen = len(seqs[0]) if seqs else 0

# 进行突变分析
for position in range(SeqLen):
    num_diff = 0
    gapNum = 0
    MutationDirection.clear()  # 重置MutationDirection字典
    for seq in seqs:
        if seq[position] != '-' and ComparedSeq[position] != '-':
            if seq[position] != ComparedSeq[position]:
                mut_key = ComparedSeq[position] + '→' + seq[position]
                MutationDirection[mut_key] = MutationDirection.get(mut_key, 0) + 1
                num_diff += 1
        else:
            gapNum += 1

    # 计算突变比率
    MutationRatio = num_diff / (len(seqs) - gapNum) if (len(seqs) - gapNum) > 0 else 0
    MutationRatio_list.append(MutationRatio)
    # 将MutationDirection信息转换为字符串列表形式
    MutationDirection_str = ';'.join([f"{key}:{value}" for key, value in MutationDirection.items()])
    MutationDirection_list.append(MutationDirection_str)

# 准备DataFrame数据
data = {
    'site': list(range(1, SeqLen + 1)),
    'MutationRatio': MutationRatio_list,
    'MutationDirection': MutationDirection_list
}

# 创建DataFrame并写入Excel
df = pd.DataFrame(data)
excel_path = os.path.join(base_dir, f"{CapsidSubtype}-Mutation.xlsx")
df.to_excel(excel_path, index=False)

print(f"Data saved to {excel_path}")
