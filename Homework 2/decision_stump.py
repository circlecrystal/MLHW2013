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
    noise = uniform(0, 1) <= noise_rate  # Noise flip the result with this prob
    if noise:
        y = -1 * sign(x)
    else:
        y = sign(x)
    return (x, y)

def generate_1d_data_set():
    data_size = 20
    data_set = [generate_1d_data() for i in range(data_size)]
    return data_set

def decide(y, s, x, theta):
    return y == s * sign(x-theta)

def count_errors(data_set, s, theta):
    error_count = 0
    for data in data_set:
        (x, y) = data
        if decide(y, s, x, theta)) == False:
            error_count += 1
    return error_count

# decision_stump_learning_algorithm_one_dimension
def dsla_1d(data_set):
    s = 1
    theta = 0
    minimum_error_count = len(data_set)
    for data in data_set:
        (theta_temp, temp) = data
        for s_temp in {-1, 1}:
            if (
                    count_errors(data_set, s_temp, theta_temp)
                    < minimum_error_count):
               s = s_temp
               theta = theta_temp
    return(s, theta)
