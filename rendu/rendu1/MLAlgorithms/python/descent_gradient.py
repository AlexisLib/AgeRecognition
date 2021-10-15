import matplotlib.pyplot as plt
import numpy as np

# Fonction de coût
def error(m, b, X, Y):
    return sum(((m * x + b) - Y[idx])**2 for idx, x in enumerate(X)) / float(len(X))

# Gradient du paramètre m
def m_grad(m, b, X, Y):
    return sum(-2 * x * (Y[idx] - (m * x + b)) for idx, x in enumerate(X)) / float(len(X))

# Gradient du paramètre b
def b_grad(m, b, X, Y):
    return sum(-2 * (Y[idx] - (m * x + b)) for idx, x in enumerate(X)) / float(len(X))

def gradient_descent_LR(X, Y, epochs, lr):
    assert(len(X) == len(Y))
    m = 0
    b = 0
    for e in range(epochs):
        m = m - lr * m_grad(m, b, X, Y)
        b = b - lr * b_grad(m, b, X, Y)
    return m, b

if __name__ == '__main__':
    # Génération du jeu de données
    X = np.linspace(-1, 1, 100) + np.random.normal(0, 0.25, 100)
    # print(X)
    Y = np.linspace(-1, 1, 100) + np.random.normal(0, 0.25, 100)
    # print(Y)

    # Exécution de l'algorithme
    m, b = gradient_descent_LR(X, Y, epochs=10000, lr=0.001)

    # Visualisation de la droite avec les valeurs de m et b trouvées par descente de gradient
    # line_x = [min(X), max(X)]
    # line_y = [(m * i) + b for i in line_x]
    # plt.plot(line_x, line_y, 'b')
    # plt.plot(X, Y, 'ro')
    # plt.show()