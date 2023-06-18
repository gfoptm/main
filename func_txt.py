import re
import random
from sympy import symbols, lambdify
from sympy.parsing.sympy_parser import parse_expr

def extract_formulas(text):
    formula_pattern = r"[a-zA-Z]*\s*=\s*[a-zA-Z0-9\s\+\-\*\/\(\)\^\.\,]*"
    formulas = re.findall(formula_pattern, text)
    return formulas

def create_function(formula):
    try:
        var, expr = formula.split('=')
        var = var.strip()
        expr = expr.strip()
        expr = parse_expr(expr)  
        f = lambdify(symbols(var), expr, "numpy")  
        return f
    except Exception as e:
        print(f"Error when processing formula '{formula}': {e}")
        return None

def read_formulas_from_file(filename):
    try:
        with open(filename, 'r') as file:
            text = file.read()
        formulas = extract_formulas(text)
        functions = [create_function(formula) for formula in formulas if formula]
        return formulas, functions
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return [], []

def save_formulas_to_file(filename, formulas):
    with open(filename, 'w') as file:
        file.writelines(f"{formula}\n" for formula in formulas)

# Замените 'input_file.txt' и 'output_file.txt' на названия ваших файлов
formulas, functions = read_formulas_from_file('input_file.txt')
save_formulas_to_file('output_file.txt', formulas)

# Пример использования случайной функции
x = 5
random_function = random.choice(functions)
if random_function is not None:
    print(random_function(x))
