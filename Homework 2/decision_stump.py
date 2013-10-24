from random import seed, uniform

def sign(x):
    if x > 0:
        return 1
    else:
        return -1


def generate_data():
    seed()
    x = uniform(-1, 1)

    seed()
    noise_rate = 0.2
    noise = uniform(0, 1) <= noise_rate  # Noise flip the result with this prob

    if noise:
        y = -1 * sign(x)
    else:
        y = sign(x)

for i in range()
generate_data()
