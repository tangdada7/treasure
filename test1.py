import torch
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# 加载并清洗数据
def load_and_clean_data(file_path):
    # 模拟数据加载，这里使用随机数据替代
    data_cleaned = pd.DataFrame({
        '小区名称': ['小区1', '小区2', '小区3'],
        '总价': ['100万', '120万', '90万'],
        '平方米': ['80平米', '100平米', '70平米']
    })
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

def set_chinese_font():
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

# 测试不同学习率，绘制学习率和最终损失的关系
def find_optimal_lr(features, labels, lr_list, num_epochs):
    final_losses = []
    for lr in lr_list:
        _, _, loss_list = train(features, labels, lr, num_epochs)
        final_losses.append(loss_list[-1])
    set_chinese_font()
    # 绘制学习率和最终损失的关系
    plt.figure(figsize=(10, 6))
    plt.plot(lr_list, final_losses, marker='o', color='blue')
    plt.xlabel('学习率')
    plt.ylabel('最低损失 (MSE)')
    plt.title(f'不同学习率的最低损失')
    plt.xscale('log') # 学习率通常取对数坐标
    plt.grid(True)
    plt.show()


# 主函数模拟
def main():
    # 模拟数据
    data_cleaned = load_and_clean_data('小区房屋信息.xlsx')
    features = torch.tensor(data_cleaned['平方米'].values.reshape(-1, 1), dtype=torch.float32)
    labels = torch.tensor(data_cleaned['总价'].values.reshape(-1, 1), dtype=torch.float32)

    # 测试不同学习率
    lr_list = [1e-6, 1e-5, 1e-4, 1e-3, 1e-2]  # 学习率范围
    find_optimal_lr(features, labels, lr_list, num_epochs=300)


if __name__ == '__main__':
    main()
