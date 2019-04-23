import matplotlib.pyplot as plt
import numpy as np

n = 12
x = np.arange(n)
y1 = (1-x/float(n))*np.random.uniform(0.5, 1, n)
y2 = (1-x/float(n))*np.random.uniform(0.5, 1, n)

plt.bar(x, +y1)
plt.bar(x, -y2)

plt.xlim(-.5, n)
plt.xticks(())
plt.ylim(-1.25, 1.25)
plt.yticks(())

plt.bar(x, +y1, facecolor='#9999ff', edgecolor='white')
plt.bar(x, -y2, facecolor='#ff9999', edgecolor='white')

for a, b in zip(x, y1):
    # ha: horizontal alignment
    # va: vertical alignment
    plt.text(a + 0.4, b + 0.05, '%.2f' % b, ha='center', va='bottom')

for x, y in zip(x, y2):
    # ha: horizontal alignment
    # va: vertical alignment
    plt.text(a + 0.4, -b - 0.05, '%.2f' % b, ha='center', va='top')

plt.show()
