import re
import pdfplumber
from pdf2image import convert_from_path
import pytesseract
from concurrent.futures import ThreadPoolExecutor
import sympy
from sympy.parsing.latex import parse_latex
from sympy.parsing.sympy_parser import ParseError

def extract_text_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
        return text

def extract_formulas_from_image(image):
    text = pytesseract.image_to_string(image, config='--psm 6')
    matches = re.findall('\$(.*?)\$', text)
    return matches

def extract_formulas_from_pdf(file_path):
    images = convert_from_path(file_path)
    formulas = []
    with ThreadPoolExecutor() as executor:
        future_formulas = executor.map(extract_formulas_from_image, images)
        for future_formula in future_formulas:
            formulas.extend(future_formula)
    return formulas

def save_formulas(functions_file, formulas):
    with open(functions_file, 'w') as f:
        for formula in formulas:
            try:
                # попробовать интерпретировать формулу с помощью sympy.parsing.latex.parse_latex
                sympy_formula = parse_latex(formula)
                f.write(str(sympy_formula) + '\n')
            except (ParseError, NotImplementedError):
                # если не получается, сохранить исходную формулу LaTeX
                f.write(formula + '\n')

file_path = 'path_to_your_pdf_file.pdf'
functions_file = 'interpreted_formulas.txt'

text = extract_text_from_pdf(file_path)
formulas = extract_formulas_from_pdf(file_path)
save_formulas(functions_file, formulas)

print('Extracted Text:')
print(text)
print('\nExtracted Formulas:')
print(formulas)
