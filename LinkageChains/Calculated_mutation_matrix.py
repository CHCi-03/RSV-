import numpy as np
import pandas as pd


def nan_num(m):
    n = 0
    for e in m:
        if np.isnan(e):
            n += 1
    return n


# 初始化变量
seqs = []
seqNum = 0
seqLen = 0
mutation = []
js = 0
data = {}
unitPositionA = []
unitPositionB = []
MutationRatioA = []
MutationRatioB = []
unitRatio = []
jd = 0

# 设置文件路径
CapsidSubtype = 'RSVB'
File = f'D:\\桌面。\\B-全长\\{CapsidSubtype}.fas'
ComparedFile = f'D:\\桌面。\\B-全长\\compared.fas'

# 读取待分析序列和参考序列
with open(File, 'r') as seqfile, open(ComparedFile, 'r') as compared:
    compared.readline()  # 跳过第一行
    comparedSeq = compared.readline().replace('\n', '')  # 读取参考序列
    line = seqfile.readline()

    while line:
        if '>' not in line:  # 只读取序列行
            seqs.append(line.replace('\n', ''))
        line = seqfile.readline()

# 获取序列长度和数量
seqLen = len(comparedSeq)
seqNum = len(seqs)
matrix = np.zeros((int(seqNum), int(seqLen)))

# 计算突变矩阵
for seq in seqs:
    for p in range(seqLen):
        if comparedSeq[p] != '-' and seq[p] != '-':
            if comparedSeq[p] != seq[p]:
                mutation.append(1)  # 突变
            else:
                mutation.append(0)  # 未突变
        else:
            mutation.append(np.nan)  # 缺失值
    matrix[js] = mutation
    js += 1
    mutation = []

# 转置矩阵
matrix = matrix.T

# 计算连锁位点
for i in range(seqLen):
    for j in range(seqLen):
        jd += 1
        if i != j:
            if (0.95 > np.sum(matrix[i] == 1) / (np.sum(matrix[i] == 1) + np.sum(matrix[i] == 0)) > 0.05 and
                    0.95 > np.sum(matrix[j] == 1) / (np.sum(matrix[j] == 1) + np.sum(matrix[j] == 0)) > 0.05):
                if (np.sum((matrix[j] - matrix[i]) == 0) + nan_num(matrix[j] - matrix[i])) / seqNum >= 0.95:
                    unitPositionA.append(str(i + 1))
                    unitPositionB.append(str(j + 1))
                    unitRatio.append(
                        (np.sum((matrix[j] - matrix[i]) == 0) + nan_num(matrix[j] - matrix[i])) / seqNum
                    )
                    MutationRatioA.append(np.sum(matrix[i] == 1) / (np.sum(matrix[i] == 1) + np.sum(matrix[i] == 0)))
                    MutationRatioB.append(np.sum(matrix[j] == 1) / (np.sum(matrix[j] == 1) + np.sum(matrix[j] == 0)))
            print(f"{jd}/{seqLen * seqLen} 进度：{format(jd / (seqLen * seqLen), '.3f')}")

# 保存数据到Excel
data['unitSiteA'] = unitPositionA
data['unitSiteB'] = unitPositionB
data['unitRatio'] = unitRatio
data['MutationRatioA'] = MutationRatioA
data['MutationRatioB'] = MutationRatioB
df = pd.DataFrame(data)
output_file_path = f'D:\\桌面。\\B-全长\\linkage-{CapsidSubtype}.xlsx'
df.to_excel(output_file_path, index=False)
