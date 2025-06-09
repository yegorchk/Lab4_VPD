import matplotlib.pyplot as plt
import numpy as np

data = np.loadtxt('py_coord.txt')

x = data[:, 0]
y = data[:, 1]

plt.plot(x, y)  
plt.xlabel('x')
plt.ylabel('y')
plt.title('График по точкам x, y')
plt.grid(True)
plt.show()