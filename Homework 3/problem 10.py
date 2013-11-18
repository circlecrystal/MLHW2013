from math import exp
from numpy import mat, dot

def nabla(u, v):
    x = exp(u) + v*exp(u*v) + 2*u -2*v - 3
    y = 2*exp(2*v) + u*exp(u*v) -2*u +4*v - 2
    return mat((x, y)).T

def nabla_2(u, v):
    h1 = exp(u) + v**2*exp(u*v) + 2
    h2 = exp(u*v) + u*v*exp(u*v) - 2
    h3 = exp(u*v) + u*v*exp(u*v) - 2
    h4 = u**2*exp(u*v) + 4*exp(u*v) + 4
    return mat(((h1, h2),(h3, h4)))

def delta(u, v):
    return -1 * dot(nabla_2(u, v).I, nabla(u, v))

def Err(u, v):
    return exp(u) + exp(2*v) + exp(u*v) + u**2 - 2*u*v + 2*v**2 - 3*u - 2*v

def uv(n):
    uv = [(0, 0)]
    if n == 0:
        return uv[-1]
    for i in range(n):
        uv.append(tuple((mat(uv[-1]).T + delta(uv[-1][0],uv[-1][1])).T.tolist()[0]))
    return uv

i = 0
for item in uv(5):
    print(i, end='\t')
    print(item, end='\t')
    print(Err(*item))
    i += 1
