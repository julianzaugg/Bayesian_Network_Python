
def seed(seed):
    pass


i = 0
random_numbers = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
def random():
    global i
    i = (i + 1) % len(random_numbers)
#    print random_numbers[i]
    return random_numbers[i]

def gauss(a, b):
    return 0.1
