#!/usr/bin/env python
# coding: utf-8

# In[57]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ======================
# 全局配置参数
# ======================
CONTINENT_MAP = {
    '亚洲': 'Asia',
    '北美洲': 'North America',
    '南美洲': 'South America',
    '大洋洲': 'Oceania',
    '欧洲': 'Europe',
    '非洲': 'Africa'
}

COLOR_PALETTE = [
    '#F28E2B',  # 0-亚洲
    '#4E79A7',  # 1-北美洲
    '#EDC948',  # 2-南美洲
    '#59A14F',  # 3-大洋洲
    '#76B7B2',  # 4-欧洲
    '#E15759'   # 5-非洲
]

def load_aligned_data(fileA, fileB):
    dfA = pd.read_excel(fileA, index_col=0).rename(columns=CONTINENT_MAP)
    dfB = pd.read_excel(fileB, index_col=0).rename(columns=CONTINENT_MAP)
    
    all_years = sorted(
        dfA.index.astype(int).union(dfB.index.astype(int)),
        reverse=False
    )
    
    return (
        dfA.reindex(all_years, fill_value=0),
        dfB.reindex(all_years, fill_value=0)
    )

def create_mirror_view(dfA, dfB, output_path):
    plt.rcParams.update({
        'font.family': 'Times New Roman',
        'legend.title_fontsize': 24,
        'legend.fontsize': 16,
        'axes.labelsize': 16,
        'xtick.labelsize': 14,
        'ytick.labelsize': 14
    })
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 12), 
                                 gridspec_kw={'wspace': 0.04})
    
    years = dfA.index.astype(str).tolist()
    y_pos = np.arange(len(years))
    bar_width = 0.85
    max_total = max(dfA.sum(1).max(), dfB.sum(1).max())
    
    # 生成强制600刻度的逻辑
    max_round = 600  # 强制设定最大刻度
    ticks = np.arange(0, max_round + 100, 100)

    # 左图处理
    left_base = np.zeros(len(years))
    for idx, col in enumerate(dfA.columns):
        ax1.barh(y_pos, dfA[col],
                left=max_round - left_base - dfA[col],
                height=bar_width,
                color=COLOR_PALETTE[idx],
                edgecolor='white',
                linewidth=0.8)
        left_base += dfA[col].values
    
    ax1.set_xlim(max_total * 1.12, 0)
    ax1.invert_xaxis()
    ax1.xaxis.tick_top()
    ax1.xaxis.set_label_position('top')
    ax1.set_xlabel('RSVA', fontweight='bold', labelpad=15)
    ax1.set_yticks([])
    ax1.set_xticks(ticks)
    ax1.set_xticklabels([f"{x}" for x in reversed(ticks)])
    ax1.tick_params(axis='x', length=5, width=1.5)
    ax1.set_ylim(y_pos[0]-0.8, y_pos[-1]+0.8)  # 调整纵坐标范围

    # 右图处理
    right_base = np.zeros(len(years))
    for idx, col in enumerate(dfB.columns):
        ax2.barh(y_pos, dfB[col],
                left=right_base,
                height=bar_width,
                color=COLOR_PALETTE[idx],
                edgecolor='white',
                linewidth=0.8)
        right_base += dfB[col].values
    
    ax2.set_xlim(0, max_total * 1.1)
    ax2.xaxis.tick_top()
    ax2.xaxis.set_label_position('top')
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(years)
    ax2.yaxis.tick_left()
    ax2.set_xlabel('RSVB', fontweight='bold', labelpad=15)
    ax2.set_xticks(ticks)
    ax2.set_xticklabels([f"{x}" for x in ticks])
    ax2.tick_params(axis='x', length=5, width=1.5)
    ax2.set_ylim(y_pos[0]-0.8, y_pos[-1]+0.8)  # 调整纵坐标范围

    # 轴样式强化
    for ax in (ax1, ax2):
        ax.spines['bottom'].set_bounds(0, max_round)  # 严格限制底边线范围
        ax.spines['bottom'].set_linewidth(1.5)
        ax.spines['top'].set_bounds(0, max_round)
        #ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.grid(True, axis='x', alpha=0.5, linestyle=':')

    # 带空行的图例标题
    handles = [plt.Rectangle((0,0),1,1, color=COLOR_PALETTE[i]) 
              for i in range(len(CONTINENT_MAP))]
    legend = fig.legend(handles, CONTINENT_MAP.values(),
              loc='upper center',
              ncol=6,
              bbox_to_anchor=(0.5, 1.08),
              title="Continents Distribution\n",  # 添加换行符
              title_fontproperties={'weight':'bold', 'size':26},
              frameon=False,
              fontsize=18,
              columnspacing=2.5,
              handletextpad=0.8)

    plt.savefig(output_path, dpi=600, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    fileA = r"F:\Desktop\respiratory syncytial virus\AB时间大洲细分Excel表\Figure1\A-Yearly_Statistics.xlsx"
    fileB = r"F:\Desktop\respiratory syncytial virus\AB时间大洲细分Excel表\Figure1\B-Yearly_Statistics.xlsx"
    output = r"F:\Desktop\RSV_Dual_Plot.tiff"
    
    try:
        df_A, df_B = load_aligned_data(fileA, fileB)
        create_mirror_view(df_A, df_B, output)
        print("可视化图表已成功生成！")
    except Exception as e:
        print(f"执行错误: {str(e)}")


# In[ ]:




