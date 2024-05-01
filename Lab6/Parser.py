import re
import enum
from graphviz import Digraph

class TokenType(enum.Enum):
    NUMBER = 1
    KEYWORD = 2
    IDENTIFIER = 3
    LEFT_PAREN = 4
    RIGHT_PAREN = 5
    LEFT_SQUARE = 6
    RIGHT_SQUARE = 7
    LEFT_CURLY = 8
    RIGHT_CURLY = 9
    LESS_THAN = 10
    GREATER_THAN = 11
    EQUAL = 12
    DOUBLE_EQUAL = 13
    PLUS = 14
    MINUS = 15
    ASTERISK = 16
    SLASH = 17
    HASH = 18
    DOT = 19
    COMMA = 20
    COLON = 21
    SEMICOLON = 22
    SINGLE_QUOTE = 23
    DOUBLE_QUOTE = 24
    COMMENT = 25
    PIPE = 26
    END = 27
    UNEXPECTED = 28

TOKEN_TYPES = [
    (TokenType.NUMBER, r'\b\d+(\.\d*)?([eE][+-]?\d+)?\b'),
    (TokenType.KEYWORD, r'\b(abstract|continue|for|new|switch|assert|default|goto|package|synchronized|boolean|do|if|private|this|break|double|implements|protected|throw|byte|else|import|public|throws|case|enum|instanceof|return|transient|catch|extends|int|short|try|char|final|interface|static|void|class|finally|long|strictfp|volatile|const|float|native|super|while)\b'),
    (TokenType.IDENTIFIER, r'[a-zA-Z_]\w*'),
    (TokenType.LEFT_PAREN, r'\('),
    (TokenType.RIGHT_PAREN, r'\)'),
    (TokenType.LEFT_SQUARE, r'\['),
    (TokenType.RIGHT_SQUARE, r'\]'),
    (TokenType.LEFT_CURLY, r'\{'),
    (TokenType.RIGHT_CURLY, r'\}'),
    (TokenType.LESS_THAN, r'<'),
    (TokenType.GREATER_THAN, r'>'),
    (TokenType.EQUAL, r'='),
    (TokenType.DOUBLE_EQUAL, r'=='),
    (TokenType.PLUS, r'\+'),
    (TokenType.MINUS, r'-'),
    (TokenType.ASTERISK, r'\*'),
    (TokenType.SLASH, r'/'),
    (TokenType.HASH, r'#'),
    (TokenType.DOT, r'\.'),
    (TokenType.COMMA, r','),
    (TokenType.COLON, r':'),
    (TokenType.SEMICOLON, r';'),
    (TokenType.SINGLE_QUOTE, r'\''),
    (TokenType.DOUBLE_QUOTE, r'"'),
    (TokenType.COMMENT, r'\/\/.*|\/\*(.|\n)*?\*\/'),
    (TokenType.PIPE, r'\|'),
    (TokenType.END, r'\0'),
    (TokenType.UNEXPECTED, r'.')
]

class ASTNode:
    def __init__(self, type, children=None, value=None):
        self.type = type
        self.value = value
        self.children = children if children is not None else []

    def __repr__(self):
        type_name = self.type.name if isinstance(self.type, enum.Enum) else self.type
        return f"{type_name}({self.value}, {self.children})"

def lexer(code):
    tokens = []
    while code:
        code = code.strip()
        for token_type, token_regex in TOKEN_TYPES:
            regex = re.compile(token_regex)
            match = regex.match(code)
            if match:
                value = match.group(0)
                tokens.append((token_type, value))
                code = code[match.end():]
                break
        else:
            raise SyntaxError(f'Illegal character: {code[0]}')
    return tokens

def parse(tokens):
    root = ASTNode(TokenType.IDENTIFIER, value="ROOT")
    current_node = root

    i = 0
    while i < len(tokens):
        token_type, value = tokens[i]
        if token_type == TokenType.KEYWORD:
            current_node = ASTNode(token_type, value=value)
            root.children.append(current_node)
        elif token_type == TokenType.IDENTIFIER:
            identifier_node = ASTNode(token_type, value=value)
            current_node.children.append(identifier_node)
            # Expecting a SEMICOLON token next
            if i+1 < len(tokens) and tokens[i+1][0] == TokenType.SEMICOLON:
                i += 1  # Move past the SEMICOLON token
        i += 1

    return root

def add_nodes_edges(tree, graph=None):
    if graph is None:
        graph = Digraph()
        graph.node(name=str(id(tree)), label=f'{tree.type.name}({tree.value})')

    for child in tree.children:
        child_label = f'{child.type.name}({child.value})' if child.value else child.type.name
        graph.node(name=str(id(child)), label=child_label)
        graph.edge(str(id(tree)), str(id(child)))
        graph = add_nodes_edges(child, graph)

    return graph

cpp_code = """
#include <iostream>

int main() {
    int number;
    std::cout << "Enter a number: ";
    std::cin >> number;
    std::cout << "You entered: " << number << std::endl;
    return 0;
}
"""

tokens = lexer(cpp_code)
ast = parse(tokens)
graph = add_nodes_edges(ast)
graph.render('ast', view=True)  # Generates a PDF and opens it
