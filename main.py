import turtle
import math


class Special_number:
    def __init__(self, name, get, find, draw):
        """Name is a string, get computes a number with given arguments,
        find tries to find arguments which compute to a given number and draw draws a shape."""
        self.name = name
        self.get = get
        self.find = find
        self.draw = draw


"""Get and find functions for each special number type. Get computes a number with given arguments,
find tries to find arguments which compute to a given number, and returns a list of all such argument tuples."""
def get_triangle_number(n):
    return n * (n + 1) / 2


def find_triangle_numbers(g):
    findings = []
    n = (math.sqrt(1 + 8 * g) - 1) / 2  # the exact argument...
    if int(n) == n:  # ...but we're only interested in integers
        findings.append((0, int(n)))  # currently returns a tuple with the angle which is used in the drawing function
    return findings


def get_layered_polygon_number(c, l):  # c stands for corners and l stands for layers
    return 1 + c * l * (l - 1) / 2


def find_layered_polygon_numbers(g):
    findings = []
    for l in range(2, math.floor((1 + math.sqrt(8 * g - 7)) / 2) + 1):  # only checks for l such that c >= 1
        c = (2 * g - 2) / (l * (l - 1))
        if c == int(c) and c > 2:  # we decide to only look for polygons with more than two corners
            findings.append((int(c), l))
    return findings


def get_star_number(c, l):  # c stands for corners and l stands for layers
    return 1 + c * l * (l - 1)


def find_star_numbers(g):
    findings = []
    for l in range(2, math.floor((1 + math.sqrt(4 * g - 3)) / 2) + 1):  # only checks for l such that c >= 1
        c = (g - 1) / (l * (l - 1))
        if c == int(c) and c > 2:  # we decide to only look for stars with more than two corners
            findings.append((int(c), l))
    return findings


def find_special_numbers(g, special_number_classes):
    """Returns a dictionary containing the findings for each number type in special_number_classes."""
    return {num.name: num.find(g) for num in special_number_classes}


### Graphics ###
def draw_triangle(t, x1, y1, diam, v, n):  # v is the rotation angle, which is used when drawing stars
    dot_size = diam / (4 * n - 4)
    t.penup()
    for row in range(n):
        for col in range(row + 1):
            x = (1 + (2 * col - row) / (n - 1)) * diam / 2
            y = diam - row * diam / (n - 1)
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
        draw_triangle(t, (diam / 2) * math.cos(corner * 2 * math.pi / c),
                      (diam / 2) * math.sin(corner * 2 * math.pi / c), step_size,
                      math.pi * ((2 * corner - 1) / c - 1 / 2), l)


### Creating special number classes ###
tri = Special_number('Triangle', get_triangle_number, find_triangle_numbers, draw_triangle)
pol = Special_number('Polygon', get_layered_polygon_number, find_layered_polygon_numbers, draw_layered_polygon)
star = Special_number('Star', get_star_number, find_star_numbers, draw_star)

special_number_classes = [tri, pol, star]


def user_chooses_type_and_args(findings):
    """After being presented with the findings, the user chooses which to display by choosing the number type and
     the arguments. The function returns (bool, str, tuple) that tells if the user wants to keep viewing the results and
     the type and arguments to draw from."""
    chosen_type_name = input('\tWrite a name (ex: Triangle) to choose a shape to display or write back to choose a new number: ')
    print('\n')
    if chosen_type_name == 'back':
        return False, None, None
    else:
        while chosen_type_name not in findings.keys():
            chosen_type_name = input('\tThe shape you entered is not available. Please choose a shape from above by entering its name excluding "number": ')

    if len(findings[chosen_type_name]) == 1:
        choosen_idx = 0
    else:
        choosen_idx = int(input(f'\t\tYour choices are numbered from 0 (left) to {len(findings[chosen_type_name]) - 1} (right). Please enter a number: '))
        print('\n')
        while choosen_idx not in range(len(findings[chosen_type_name])):
            choosen_idx = int(input(f'\t\tThe choice you entered is not available. Please reread the instructions above and try again: '))

    args = findings[chosen_type_name][choosen_idx]

    return True, chosen_type_name, args


### UI and displaying ###
s = turtle.Screen()
t = turtle.Turtle()
t.ht()
t.speed(0)

while True:

    g = int(input('Enter number of glasses: '))
    print('\n')
    while g <= 1:
        g = int(input('\tPlease enter a number larger than 1: '))
        print('\n')

    findings = find_special_numbers(g, special_number_classes)

    print('\tFindings:\n')
    for num in special_number_classes:
        print(f'\t{num.name} numbers: {findings[num.name]}')

    viewing, chosen_type_name, args = user_chooses_type_and_args(findings)

    while viewing:
        for num in special_number_classes:
            if chosen_type_name == num.name:
                num.draw(t, 0, 0, 300, *args)

        viewing, chosen_type_name, args = user_chooses_type_and_args(findings)

        t.clear()
