# glass_patterns
Recommends patterns to put glasses in.

# Instructions to implement a new number type
    - define a get function with arbitrary number of arguments
    - define a find function with g (number of glasses) as argument
    - define a draw function
    - create an object using the class Special_number and add it to the list special_number_classes

# To do
    - Find functions return arguments used for drawing functions. The draw triangle function has the rotation angle as
    an additional argument, which is used for drawing stars. Perhaps this argument shouldn't be displayed to the user.
    - If no special numbers are found, search for g - 1, g - 2, ... and/or g // 2, g // 3, ... until  they are.
    - (Probably hard.) define "connection surface" or likewise for each number type. If two shapes of g_1 and g_2 glasses
    have a common connection surface of g_c glasses, then we get a new shape made g_1 + g_2 - g_c glasses by connecting them.
