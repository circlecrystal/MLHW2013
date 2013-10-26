from random import seed, uniform


def sign(x):  # sign(0)=1
    if x >= 0:
        return 1
    else:
        return -1


def generate_1d_data():
    seed()
    x = uniform(-1, 1)
    seed()
    noise_rate = 0.2
    # noise flip the result with noise_rate probability
    noise = uniform(0, 1) <= noise_rate
    if noise:
        y = -1 * sign(x)
    else:
        y = sign(x)
    return (x, y)


def generate_1d_data_set():
    data_size = 20
    data_set = [generate_1d_data() for i in range(data_size)]
    return data_set


def generate_set_of_data_set(path):
    fin = open(path)
    set_of_data_set = []
    for line in fin:
        temp = line.split()
        x = []
        for item in temp[:-1]:
            x.append(float(item))
        data = x + [int(temp[-1])]
        set_of_data_set.append(data)
    fin.close()
    return set_of_data_set


def generate_data_set(set_of_data_set, i):
    return [(data_set[i], data_set[-1]) for data_set in set_of_data_set]


def decide(y, s, x, theta):
    return y == s * sign(x-theta)


def count_errors(data_set, s, theta):
    error_count = 0
    for data in data_set:
        (x, y) = data
        if decide(y, s, x, theta) == False:
            error_count += 1
    return error_count


# decision_stump_learning_algorithm_one_dimension
def dsla_1d(data_set):
    # possible_list_of_theta
    pst = []
    data_size = len(data_set)
    minimum_error_count = data_size
    for possible_theta in data_set:
        (theta_temp, temp) = possible_theta
        for s_temp in {-1, 1}:
            error_count = count_errors(data_set, s_temp, theta_temp)
            if error_count < minimum_error_count:
                pst = []
                pst.append(theta_temp)
            elif error_count == minimum_error_count:
                pst.append(theta_temp)
    theta = sum(pst) / len(pst)
    if count_errors(data_set, 1, theta) < data_size/2:
        return(1, theta)
    else:
        return(-1, theta)


# decision_stump_learning_algorithm
def dsla(path):
    pre_set_of_data_set = generate_set_of_data_set(path)
    dimension_of_x = len(pre_set_of_data_set[0]) - 1
    set_of_data_set = []
    set_of_s_theta = []
    sample_size = dimension_of_x * len(pre_set_of_data_set)
    minimum_sum_of_errors = sample_size
    s = 1
    theta = 0
    for d in range(dimension_of_x):
        data_set_temp = generate_data_set(pre_set_of_data_set, d)
        set_of_data_set.append(data_set_temp)
        set_of_s_theta.append(dsla_1d(data_set_temp))
    for (s_temp, theta_temp) in set_of_s_theta:
        sum_of_errors = 0
        for data_set in set_of_data_set:
            sum_of_errors += count_errors(data_set, s_temp, theta_temp)
        if sum_of_errors < minimum_sum_of_errors:
            minimum_sum_of_errors = sum_of_errors
            (s, theta) = (s_temp, theta_temp)
    return (s, theta)


def problem_17():
    repeat_times = 5000
    # sum_of_error_rate_in_sample
    seris = 0
    # sum_of_error_rate_out_of_sample
    seros = 0
    for i in range(repeat_times):
        data_set = generate_1d_data_set()
        (s, theta) = dsla_1d(data_set)
        # error_rate_in_sample
        eris = count_errors(data_set, s, theta) / len(data_set)
        # error_rate_out_of_sample
        eros = (1-0.6*s+0.6*s*abs(theta)) / 2
        seris += eris
        seros += eros
    # average_of_error_rate_in_sample
    aeris = seris / repeat_times
    # average_of_error_rate_out_of_sample
    aeros = seros / repeat_times
    print('Problem 17:')
    print('^Ein:\t', aeris)
    print('^Eout:\t', aeros)
    print('')


def problem_18():
    path = './hw2_train.dat'
    pre_set_of_data_set = generate_set_of_data_set(path)
    dimension_of_x = len(pre_set_of_data_set[0]) - 1
    set_of_data_set = []
    set_of_s_theta = []
    s = 1
    theta = 0
    for d in range(dimension_of_x):
        data_set_temp = generate_data_set(pre_set_of_data_set, d)
        set_of_data_set.append(data_set_temp)
        set_of_s_theta.append(dsla_1d(data_set_temp))
    sample_size = dimension_of_x * len(pre_set_of_data_set)
    minimum_sum_of_errors = sample_size
    for (s_temp, theta_temp) in set_of_s_theta:
        sum_of_errors = 0
        for data_set in set_of_data_set:
            sum_of_errors += count_errors(data_set, s_temp, theta_temp)
        if sum_of_errors < minimum_sum_of_errors:
            minimum_sum_of_errors = sum_of_errors
            (s, theta) = (s_temp, theta_temp)
    print('Problem 18:')
    print('Ein:\t', minimum_sum_of_errors/sample_size)
    print('')


def problem_19():
    path = './hw2_train.dat'
    pre_set_of_data_set = generate_set_of_data_set(path)
    dimension_of_x = len(pre_set_of_data_set[0]) - 1
    set_of_data_set = []
    set_of_s_theta = []
    s = 1
    theta = 0
    for d in range(dimension_of_x):
        data_set_temp = generate_data_set(pre_set_of_data_set, d)
        set_of_data_set.append(data_set_temp)
        set_of_s_theta.append(dsla_1d(data_set_temp))
    sample_size = dimension_of_x * len(pre_set_of_data_set)
    minimum_sum_of_errors = sample_size
    i = 1
    i_temp = 0
    for (s_temp, theta_temp) in set_of_s_theta:
        i_temp += 1
        sum_of_errors = 0
        for data_set in set_of_data_set:
            sum_of_errors += count_errors(data_set, s_temp, theta_temp)
        if sum_of_errors < minimum_sum_of_errors:
            i = i_temp
            minimum_sum_of_errors = sum_of_errors
            (s, theta) = (s_temp, theta_temp)
    print('Problem 19:')
    print('(s, i, theta):\t', (s, i, theta))
    print('')


def problem_20():
    train_file_path = './hw2_train.dat'
    test_file_path = './hw2_test.dat'

    (s, theta) = dsla(train_file_path)

    pre_set_of_data_set = generate_set_of_data_set(test_file_path)
    dimension_of_x = len(pre_set_of_data_set[0]) - 1
    sample_size = dimension_of_x * len(pre_set_of_data_set)
    set_of_data_set = []
    for d in range(dimension_of_x):
        data_set_temp = generate_data_set(pre_set_of_data_set, d)
        set_of_data_set.append(data_set_temp)
    sum_of_errors = 0
    for data_set in set_of_data_set:
        sum_of_errors += count_errors(data_set, s, theta)
    print('Problem 20:')
    print('Etest:\t', sum_of_errors/sample_size)
    print('')


#problem_17()
#problem_18()
#problem_19()
#problem_20()
