import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial import Polynomial

# 生成数据点
x = np.linspace(0, 2 * np.pi, 100)
y = np.sin(x)

# 拟合多项式
coefficients = np.polyfit(x, y, 5)
polynomial = np.poly1d(coefficients)

# 计算多项式的拟合值
y_polyfit = polynomial(x)

# 绘图
plt.plot(x, y, label='sin(x)', color='blue')
plt.plot(x, y_polyfit, label='5th degree polynomial fit', linestyle='--', color='red')
plt.legend()
plt.title('5th Degree Polynomial Fit to sin(x)')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.show()
