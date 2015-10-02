from math import *

def calculate(expr_string):

    math_list = ['math', 'acos', 'asin', 'atan', 'atan2', 'ceil',
        'cos', 'cosh', 'degrees', 'e', 'exp', 'fabs', 'floor', 'fmod',
        'frexp', 'hypot', 'ldexp', 'log',  'log10', 'modf', 'pi',
        'pow', 'radians', 'sin', 'sinh', 'sqrt', 'tan', 'tanh']

    builtins_list = [abs]

    local_ctx = dict([ (k, globals().get(k, None)) for k in math_list ])
    local_ctx.update(dict([ (b.__name__, b) for b in builtins_list ]))

    try:
        return eval(expr_string, { "__builtins__": None }, local_ctx)
    except (SyntaxError, TypeError):
        return None
