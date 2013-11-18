import math
from random import uniform
from numpy.linalg import pinv
from numpy import mat, dot

def sign(t):
    if t > 0:
        return 1
    else:
        return -1

def data_gen(n=1000):
    X = []
    Y = []
    for i in range(n):
        x1, x2 = uniform(-1, 1), uniform(-1, 1)
        y = sign(x1**2 + x2**2 - 0.6)
        noise = sign(uniform(0, 1) - 0.1)  # noise flipping frequency is 0.1
        y = noise * y  # flipping
        X.append((1, x1, x2))
        Y.append(y)
    return tuple(X), tuple(Y)

def transform(X):
    Z = []
    for t in X:
        Z.append((1, t[1], t[2], t[1]*t[2], t[1]**2, t[2]**2))
    return tuple(Z)

def linear_regression(X, Y):
    pseudo_inv = pinv(X)  # pseudo-inverse
    W = dot(pseudo_inv, Y).tolist()
    return W

def Ein():
    ds = data_gen()
    X, Y = ds[0], ds[1]
    W = linear_regression(mat(X), mat(Y).T)
    N = len(X)
    sum = 0
    for i in range(N):
        sum += (dot(mat(X[i]),mat(W)) - Y[i]) ** 2
    return sum / N

def average_E(E, n=1000):
    sum = 0
    for i in range(n):
        sum += E()
    return sum / n

def w_tilde():
    ds = data_gen()
    Z, Y = transform(ds[0]), ds[1]
    W = linear_regression(mat(Z), mat(Y).T)
    return W

def Eout():
    W = w_tilde()
    ds = data_gen()
    Z, Y = transform(ds[0]), ds[1]
    N = len(Z)
    sum = 0
    for i in range(N):
        sum += (dot(mat(Z[i]),mat(W)) - Y[i]) ** 2
    return sum / N

#print(average_E(Ein))
#print(w_tilde())
#print(average_E(Eout))
