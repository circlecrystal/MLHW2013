from random import seed, shuffle

def update_or_pass(w, x, y, longn=1):
    """x is (input space dimension + 1) length input data vector,
    w is same victor length with x. y is a single number result.
    Return -1 if no update.
    """
    s = 0 # temporary sum
    temp = range(len(w))
    for i in temp:
        s += w[i]*x[i]
    if s * y > 0:
        return -1
    else:
        return list(w[j] + longn*y*x[j] for j in temp)


def get_d(path):
    d = len(open(path).readline().split())
    return d


def get_n(path):
    fin_preload = open(path)
    n = sum(1 for line in fin_preload)  # number of data
    fin_preload.close()
    return n


def get_list_xy(path):
    d = get_d(path)
    fin = open(path)
    list_x, list_y = [], []
    for line in fin:
        temp = line.split()
        temp_list = []
        for i in range(d - 1):
            temp_list.append(float(temp[i]))
        list_x.append([1] + temp_list)
        list_y.append(int(temp[d - 1]))
    fin.close()
    return (list_x, list_y)


def read_xy(i, list_xy):
    (list_x, list_y) = list_xy
    return (list_x[i], list_y[i])


def next_xy(i, list_xy, readlist=None):
    if readlist == None:
        return read_xy(i, list_xy)
    else:
        return read_xy(readlist[i], list_xy)


def nextxy_random(randomlist, list_xy):
    seed()
    shuffle(randomlist)
    return read_xy(randomlist[-1], list_xy)


def get_errorset(w, list_xy):
    n = len(list_xy[1])
    errorlist = []
    for i in range(n):
        (x, y) = read_xy(i, list_xy)
        temp = update_or_pass(w, x, y)
        if temp != -1:
            errorlist.append(i)
    return errorlist


def pla_core(path, longn=1, readlist=None):
    n = get_n(path)
    d = get_d(path)
    list_xy = get_list_xy(path)
    w = [0] * d  # w0
    count = 0  # number of updates
    s = 0  # number of continuous passes
    loop = 0  # number of loops
    while True:
        (x, y) = next_xy(loop % n, list_xy, readlist)
        t = update_or_pass(w, x, y, longn)
        loop += 1
        if t == -1:
            s += 1
            if s == n:
                break
        else:
            s = 0
            count += 1
            w = t
    return (w, count)


def pla_random_core(path, pla_updates):
    n = get_n(path)
    d = get_d(path)
    list_xy = get_list_xy(path)
    w = [0] * d
    count = 0
    w_pocket = w
    errornumber_pocket = n
    while count < pla_updates:
        errorlist = get_errorset(w, listxy)
        errornumber = len(errorlist)
        if  errornumber < errornumber_pocket:
            errornumber_pocket = errornumber
            w_pocket = w
            if errornumber_pocket == 0:
                break
        (x, y) = nextxy_random(errorlist, list_xy)
        w = update_or_pass(w, x, y)
        count += 1
    return (w_pocket, count)


def pla_fixed_sequential(path):
    (w, count) = pla_core(path)
    return count


def pla_fixed_random(path, times=2000, longn=0.5):
    n = get_n(path)
    readlist = list(range(n))
    sum_of_counts = 0
    for i in range(times):
        seed()
        shuffle(readlist)
        (w, count) = pla_core(path, longn, readlist)
        sum_of_counts += count
    return sum_of_counts / times


def pla_pure_random(path, pla_updates=50):
    return pla_random_core(path, pla_updates)


def test(list_xy, w):
    n = len(list_xy[1])
    error_count = 0
    for i in range(n):
        (x, y) = read_xy(i, list_xy)
        if update_or_pass(w, x, y) != -1:
            error_count += 1
    return error_count / n


def verify(train_path, test_path, times):
    list_xy = get_list_xy(test_path)
    sum_of_error_rate = 0
    for i in range(times):
        (w_pocket, temp) = pla_pure_random(trainpath)
        sum_of_error_rate += test(list_xy, w_pocket)
    return sum_of_error_rate / times


train_data = 'hw1_18_train.dat'
test_data = 'hw1_18_test.dat'
average_errror_rate = verify(train_data, test_data, 200)
print('average error rate = ' + str(average_error_rate * 100) + '%')
