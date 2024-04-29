import re
from prettytable import PrettyTable

# Define the token types and their corresponding regex patterns
TOKEN_TYPES = [
    ('SELECTOR', r'[\.#]?[a-zA-Z][\w-]*'),
    ('LEFT_CURLY', r'\{'),
    ('RIGHT_CURLY', r'\}'),
    ('PROPERTY', r'[a-zA-Z-]+'),
    ('COLON', r':'),
    ('VALUE', r'[^;]+'),
    ('SEMICOLON', r';'),
    ('COMMENT', r'\/\*.*?\*\/'),
    ('WHITESPACE', r'\s+'),
    ('UNEXPECTED', r'.')
]


def tokenize(code):
    tokens = []
    while code:
        code = code.strip()
        for token_type, pattern in TOKEN_TYPES:
            regex = re.compile(pattern)
            match = regex.match(code)
            if match:
                value = match.group(0)
                tokens.append((token_type, value))
                code = code[len(value):]
                break
        else:
            raise SyntaxError(f'Illegal character: {code[0]}')
    return tokens


css_code = """
/* This is a CSS comment */
body {
    font-family: Arial, sans-serif;
    background-color: #ffffff;
}

h1 {
    color: green;
    text-align: center;
}

.container {
    width: 70%;
    margin: 0 auto;
}
"""

tokens = tokenize(css_code)

pt = PrettyTable()
pt.field_names = ["Token Type", "Token Value"]

for token in tokens:
    pt.add_row([token[0], token[1]])

print(pt)