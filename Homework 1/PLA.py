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


def getd(path):
    d = len(open(path).readline().split())
    return d


def getn(path):
    fin_preload = open(path)
    n = sum(1 for line in fin_preload)  # number of data
    fin_preload.close()
    return n


def xylist(path):
    d = getd(path)
    fin = open(path)
    listx, listy = [], []
    for line in fin:
        temp = line.split()
        templist = []
        for i in range(d - 1):
            templist.append(float(temp[i]))
        listx.append([1] + templist)
        listy.append(int(temp[d - 1]))
    fin.close()
    return (listx, listy)


def readxy(i, listxy):
    (listx, listy) = listxy
    return (listx[i], listy[i])


def nextxy(i, listxy, readlist=None):
    if readlist == None:
        return readxy(i, listxy)
    else:
        return readxy(readlist[i], listxy)


def nextxy_pure_random(randomlist, listxy):
    seed()
    shuffle(randomlist)
    return readxy(randomlist[-1], listxy)


def errorset(w, listxy):
    n = len(listxy[1])
    errorlist = []
    for i in range(n):
        (x, y) = readxy(i, listxy)
        temp = update_or_pass(w, x, y)
        if temp != -1:
            errorlist.append(i)
    return errorlist


def pla_core(path, longn=1, readlist=None):
    n = getn(path)
    d = getd(path)
    listxy = xylist(path)
    w = [0] * d  # w0
    count = 0  # number of updates
    s = 0  # number of continuous passes
    loop = 0  # number of loops
    while True:
        (x, y) = nextxy(loop % n, listxy, readlist)
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
    n = getn(path)
    d = getd(path)
    listxy = xylist(path)
    w = [0] * d
    count = 0
    w_pocket = w
    errornumber_pocket = n
    while count < pla_updates:
        errorlist = errorset(w, listxy)
        errornumber = len(errorlist)
        if  errornumber < errornumber_pocket:
            errornumber_pocket = errornumber
            w_pocket = w
            if errornumber_pocket == 0:
                break
        (x, y) = nextxy_pure_random(errorlist, listxy)
        w = update_or_pass(w, x, y)
        count += 1
    return (w_pocket, count)


def pla_fixed_sequential(path):
    (w, count) = pla_core(path)
    return count


def pla_fixed_random(path, times=2000, longn=0.5):
    n = getn(path)
    readlist = list(range(n))
    sumofcounts = 0
    for i in range(times):
        seed()
        shuffle(readlist)
        (w, count) = pla_core(path, longn, readlist)
        sumofcounts += count
    return sumofcounts / times


def pla_pure_random(path, pla_updates=50):
    return pla_random_core(path, pla_updates)


def test(listxy, w):
    n = len(listxy[1])
    error_count = 0
    for i in range(n):
        (x, y) = readxy(i, listxy)
        if update_or_pass(w, x, y) != -1:
            error_count += 1
    return error_count / n


def verify(trainpath, testpath, times):
    listxy = xylist(testpath)
    sum_of_error_rate = 0
    for i in range(times):
        (w_pocket, temp) = pla_pure_random(trainpath)
        sum_of_error_rate += test(listxy, w_pocket)
    return sum_of_error_rate / times


traindata = 'hw1_18_train.dat'
testdata = 'hw1_18_test.dat'
aer = verify(traindata, testdata, 200)
print('average error rate = ' + str(aer * 100) + '%')
