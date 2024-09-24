#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2024/9/22 下午1:29
# @Author : MiuziZhou
import torch
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 加载并清洗数据
def load_and_clean_data(file_path):
    data = pd.read_excel(file_path)
    data_cleaned = data.dropna(subset=['小区名称', '总价', '平方米'])
    data_cleaned['总价'] = data_cleaned['总价'].str.replace('万', '').astype(float)
    data_cleaned['平方米'] = data_cleaned['平方米'].str.replace('平米', '').astype(float)
    return data_cleaned

# 训练函数
def train(features, labels, lr, num_epochs):
    w = torch.randn(features.shape[1], 1, requires_grad=True)
    b = torch.zeros(1, requires_grad=True)
    loss_list = []

    for epoch in range(num_epochs):
        total_cost = calc_cost(features, w, b, labels, len(labels))
        if w.grad is not None:
            w.grad.data.zero_()
        if b.grad is not None:
            b.grad.data.zero_()
        total_cost.backward()
        with torch.no_grad():
            w -= lr * w.grad
            b -= lr * b.grad
        loss_list.append(total_cost.item())
    return w, b, loss_list

# 计算损失的函数
def calc_cost(X, w, b, labels, m):
    prices = torch.matmul(X, w) + b
    cost = torch.sum((prices - labels) ** 2) / (2 * m)
    return cost

# 设置中文字体
def set_chinese_font():
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

# 绘制损失曲线并标记临界值
def plot_loss_curve(loss_list, threshold):
    set_chinese_font()
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(loss_list) + 1), loss_list, label='损失 (Loss)', color='blue')

    # 计算损失的变化率
    loss_changes = np.diff(loss_list)

    # 找到损失变化率小于阈值的点
    critical_point = None
    for i, change in enumerate(loss_changes):
        if abs(change) < threshold:
            critical_point = i + 1  # 索引要加1才能对齐原始数据
            break

    # 如果找到了临界点，在图中标记
    if critical_point is not None:
        plt.axvline(x=critical_point, color='red', linestyle='--', label=f'临界点: {critical_point}轮')
        plt.scatter(critical_point, loss_list[critical_point], color='red', zorder=5)
        plt.text(critical_point, loss_list[critical_point], f'临界点: {critical_point}', color='red', fontsize=12)

    plt.xlabel('迭代次数')
    plt.ylabel('损失 (MSE)')
    plt.title(f'损失随迭代变化的曲线')
    plt.legend()
    plt.grid(True)
    plt.show()

from mpl_toolkits.mplot3d import Axes3D


# 绘制 w, b 和损失的三维图像
def plot_3d_loss_surface(features, labels):
    set_chinese_font()

    # 生成一组 w 和 b 的值
    w_values = np.linspace(-100, 100, 1000)
    b_values = np.linspace(-5000, 1000, 1000)
    W, B = np.meshgrid(w_values, b_values)

    # 计算每一组 w 和 b 对应的损失，注意将 w 和 b 转为 torch.Tensor
    Z = np.array([
        [
            calc_cost(features, torch.tensor([[w]], dtype=torch.float32), torch.tensor(b, dtype=torch.float32), labels,
                      len(labels)).item()
            for w in w_values
        ]
        for b in b_values
    ])

    # 检查损失值范围，确保没有负数
    assert np.all(Z >= 0), "Error: Some loss values are negative!"

    # 创建三维图形
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')

    # 绘制曲面
    ax.plot_surface(W, B, Z, cmap='viridis')

    # 设置轴标签
    ax.set_xlabel('w')
    ax.set_ylabel('b')
    ax.set_zlabel('损失 (Loss)')
    ax.set_title('w, b 和损失之间的关系')

    plt.show()


# 绘制 w, b 和损失的二维等高线图
def plot_2d_contour_w_b(features, labels):
    set_chinese_font()

    # 生成一组 w 和 b 的值
    w_values = np.linspace(-100, 100, 1000)
    b_values = np.linspace(-5000, 10000, 1000)
    W, B = np.meshgrid(w_values, b_values)

    # 计算每一组 w 和 b 对应的损失，注意将 w 和 b 转为 torch.Tensor
    Z = np.array([
        [
            calc_cost(features, torch.tensor([[w]], dtype=torch.float32), torch.tensor(b, dtype=torch.float32), labels,
                      len(labels)).item()
            for w in w_values
        ]
        for b in b_values
    ])

    # 检查损失值范围
    assert np.all(Z >= 0), "Error: Some loss values are negative!"

    # 创建二维等高线图
    plt.figure
    cp = plt.contour(W, B, Z, levels=200, cmap='viridis')
    plt.colorbar(cp)

    # 设置轴标签
    plt.xlabel('w')
    plt.ylabel('b')
    plt.title('w, b 和损失的等高线图')

    plt.show()


# 主函数
def main():
    file_path = '小区房屋信息.xlsx'
    data_cleaned = load_and_clean_data(file_path)
    features = torch.tensor(data_cleaned['平方米'].values.reshape(-1, 1), dtype=torch.float32)
    labels = torch.tensor(data_cleaned['总价'].values.reshape(-1, 1), dtype=torch.float32)

    # 训练模型
    w, b, loss_list = train(features, labels, lr=1e-5, num_epochs=300)

    # 绘制损失曲线并标记临界值
    plot_loss_curve(loss_list, threshold=1e-3)  # 调整阈值以找到合适的临界点
    file_path = '小区房屋信息.xlsx'
    data_cleaned = load_and_clean_data(file_path)
    features = torch.tensor(data_cleaned['平方米'].values.reshape(-1, 1), dtype=torch.float32)
    labels = torch.tensor(data_cleaned['总价'].values.reshape(-1, 1), dtype=torch.float32)

    # 绘制三维 w, b 和损失的图像
    plot_3d_loss_surface(features, labels)

   # 绘制二维等高线图
    plot_2d_contour_w_b(features, labels)

if __name__ == '__main__':
    main()
