from math import exp
from numpy import mat, dot, zeros

def file_process(path):
    fin = open(path)
    X = []
    Y = []
    for line in fin:
        dt = [float(item) for item in line.split()]  # data point
        X.append(tuple([1]+dt[:-1]))
        Y.append(dt[-1])
    return tuple(X), tuple(Y)

def stochastic_gradient(x, y, W):
    return -1*float(y)*x / (1+exp(float(y*dot(W.T, x))))

def batch_gradient(X, Y, W, d, N):
    gradient_sum = mat(zeros(d)).T
    for i in range(N):
        gradient_sum += stochastic_gradient(X[i].T, Y[i], W)
    return gradient_sum / N

def update_weights(W, Gradient, eta):
    return W - eta * Gradient

def batch_logistic_regression(eta, times):
    trainning_set = 'hw3_train.dat'
    ds = file_process(trainning_set)  # data set
    X, Y = mat(ds[0]), mat(ds[1]).T
    N = len(Y)
    d = len(X.tolist()[0])
    W = mat(zeros(d)).T
    for i in range(times):
        W = update_weights(W, batch_gradient(X, Y, W, d, N), eta)
    return W

def stochastic_logistic_regression(eta, times):
    trainning_set = 'hw3_train.dat'
    ds = file_process(trainning_set)  # data set
    X, Y = mat(ds[0]), mat(ds[1]).T
    N = len(Y)
    d = len(X.tolist()[0])
    W = mat(zeros(d)).T
    for i in range(times):
        W = update_weights(W, stochastic_gradient(X[i%N].T, Y[i%N], W), eta)
    return W

def theta(s):
    return 1/(1+exp(-1*s))

def h(W, x):
    s = float(dot(W.T, x.T))
    return theta(s)

def zero_one_error(h, y):
    flag = -1
    if h > 0.5:
        flag = 1
    if flag == y:
        return 0
    else:
        return 1

def Eout(eta=0.001, logistic_regression=batch_logistic_regression, times=2000):
    W = logistic_regression(eta, times)
    testing_set = 'hw3_test.dat'
    ds = file_process(testing_set)  # data set
    X, Y = mat(ds[0]), mat(ds[1]).T
    N = len(Y)
    sum_of_error = 0
    for i in range(N):
        sum_of_error += zero_one_error(h(W, X[i]), float(Y[i]))
    return sum_of_error/N

#print(Eout())  # problem 18
#print(Eout(0.01))  # problem 19
#print(Eout(0.001, stochastic_logistic_regression))  # problem 20
