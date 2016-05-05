import math
import random
import sys

n = 4
# p = 0.5

def safe_div(nominator, denominator):
    try:
        return nominator / denominator
    except ZeroDivisionError:
        return float('NaN')

def compute_SE(mean, array, multiply_small_values=4):
    cleaned = [x for x in array if not math.isnan(x)]
    n = len(cleaned)
    ret = safe_div(math.sqrt(sum((x - mean) ** 2 for x in cleaned) / (n - 1)), math.sqrt(n))

    if (ret <= 0.00001):
        ret *= multiply_small_values
    return ret

def compute_mean(array):
    return safe_div(sum(array), len(array))

def compute(array):
    mean = compute_mean(array)
    samples = []
    # for _ in range(n):
    #     random_sample = random.sample(array, 1)
    #     samples.append(compute_mean(random_sample))
    samples = array

    SE = compute_SE(mean, samples)

    vals = [mean, SE, mean + SE, mean - SE]
    return ["{:6.4f}".format(n) for n in vals]

array = [float(x) for x in sys.argv[1:]]

print(compute(array))
