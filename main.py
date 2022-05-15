import turtle
import math

class Special_number:
    def __init__(self, name, func, n_args, search_limit_func):
        self.name = name
        self.func = func
        self.n_args = n_args
        self.search_limit_func = search_limit_func

    def compute(self, *args):
        return self.func(*args)


### Special numbers ###
def triangle_number(n):
    return n * (n + 1) / 2


def triangle_number_search_limit(g):
    return [int(- 1 / 2 + (2 * g + 1 / 4) ** (1 / 2)) + 1]


def layered_polygon_number(c, l):
    return 1 + c * l * (l - 1) / 2


def layered_polygon_number_search_limit(g):
    return [g - 1, int(1 / 2 + (2 * g - 7 / 4) ** (1 / 2)) + 1]


def star_number(c, l):
    return 1 + c * l * (l - 1)


### Finding special numbers ###
def naive_search(g):
    findings =[]
    for n in range(1000):
        if triangle_number(n) == g:
            findings.append(['tri', n])

    for c in range(11):
        for l in range(1000):
            if layered_polygon_number(c, l) == g:
                findings.append(['pol', c, l])
            elif star_number(c, l) == g:
                findings.append(['star', c, l])

    return findings


# not working
def search_for_special_numbers(g, number_class):
    findings = []
    max_args = number_class.search_limit_func(g)
    args = [1 for i in range(number_class.n_args)]
    arg_idx = len(args) - 1
    while args[arg_idx] <= max_args[arg_idx]:
        if number_class.compute(*args) == g:
            findings.append([number_class.name, args])
        args[arg_idx] += 1
        while args[arg_idx] > max_args[arg_idx]:
            args[arg_idx] = 1
            arg_idx -= 1
            if arg_idx < 0:
                return findings
        args[arg_idx] += 1
        arg_idx = len(args) - 1


# Assumes that the number type is growing in each variable. Cycles as 1 1 1, 1 1 2, ...
# and changes digit when f(1, 1, a) > g. Keeps going until f(b, 1, 1) > g. (But arbitrary number of variables.)
# Has multiple problems. One is that pl(c, 1) = 1 for agg c, som we never get pol(c, 1) > g
def find(n, number_class):
    findings = []
    args = [1 for i in range(number_class.n_args)]
    # Temporary solution of setting av maximum limit for first variable
    while args[0] < 100:
        arg_n = len(args) - 1
        test_number = number_class.compute(*args)
        while test_number < n:
            args[-1] += 1
            test_number = number_class.compute(*args)
        if test_number == n:
            findings.append([number_class.name, args])
        print(args)
        print(args[arg_n])
        while args[arg_n] == 1:
            print(arg_n)
            arg_n -= 1
            if arg_n <= 0:
                return findings
        args[arg_n] = 1
        args[arg_n - 1] += 1


### Graphics ###
def draw_triangle(t, x1, y1, x_len, y_len, v, n):
    dot_size = min(x_len, y_len) / (4 * n - 4)
    t.penup()
    for row in range(n):
        for col in range(row + 1):
            x = (1 + (2 * col - row) / (n - 1)) * x_len / 2
            y = y_len - row * y_len / (n - 1)
            t.goto(x1 + math.cos(v) * x - math.sin(v) * y,
                   y1 + math.sin(v) * x + math.cos(v) * y)
            t.dot(dot_size)


def draw_layered_polygon(t, x1, y1, diam, c, l):
    dot_size = diam / (8 * l - 8)
    t.penup()
    t.goto(x1, y1)
    t.dot(dot_size)
    for layer in range(1, l):
        t.goto(x1 + diam * layer / (2 * l - 2), y1)
        t.setheading(90 + 180 / c)
        step_size = (diam * layer / (2 * l - 2)) * math.sqrt(2 - 2 * math.cos(2 * math.pi / c))
        for corner in range(c):
            for point in range(layer):
                t.dot(dot_size)
                t.forward(step_size / layer)
            t.left(360 / c)


def draw_star(t, x1, y1, diam, c, l):
    draw_layered_polygon(t, x1, y1, diam, c, l)
    step_size = (diam / 2) * math.sqrt(2 - 2 * math.cos(2 * math.pi / c))
    for corner in range(c):
        draw_triangle(t, (diam / 2) * math.cos(corner * 2 * math.pi / c), (diam / 2) * math.sin(corner * 2 * math.pi / c),
                      step_size, step_size, math.pi * ((2 * corner - 1) / c - 1 / 2), l)


### UI and displaying ###
s = turtle.Screen()
t = turtle.Turtle()
t.speed(0)

#draw_triangle(t, 0, 0, 250, 250, 0, 15)
#draw_layered_polygon(t, 0, 0, 400, 14, 8)
draw_star(t, 0, 0, 400, 7, 4)
turtle.done()

# UI
#g = int(input('Enter number of glasses: '))

'''
tri = Special_number('tri', triangle_number, 1, triangle_number_search_limit)
pol = Special_number('pol', layered_polygon_number, 2, layered_polygon_number_search_limit)

special_number_classes = [tri, pol]

findings = []
for snc in special_number_classes:
    findings.append(find(g, snc))
'''

#print(naive_search(g))