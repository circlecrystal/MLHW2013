from math import exp

def nabla(u, v):
    x = exp(u) + v*exp(u*v) + 2*u -2*v - 3
    y = 2*exp(2*v) + u*exp(u*v) -2*u +4*v - 2
    return x, y

def calc_E5(u, v):
    return exp(u) + exp(2*v) + exp(u*v) + u**2 - 2*u*v + 2*v**2 - 3*u - 2*v

uv = [(0,0)]
eta = 0.01
print('(u%d, v%d) = (%.0f, %.0f)' %
    (0, 0, uv[0][0], uv[0][1]))
for i in range(5):
    nabla_temp = nabla(*uv[i])
    list_temp = []
    for j in range(2):
        list_temp.append(uv[i][j] - eta*nabla_temp[j])
    uv.append(tuple(list_temp))
    print('(u%d, v%d) = (%.5f, %.5f)' %
            (i+1, i+1, uv[-1][0], uv[-1][-1]))
print('%.5f' %(calc_E5(uv[-1][0], uv[-1][-1]),))
print('%.5f' %(calc_E5(16/23, 2/23),))
