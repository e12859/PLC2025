import re
import sys

def lexical_analyzer(query):

    token_patterns = [
        ('COMMENT',   r'\#.*'),
        ('SELECT',    r'(?i)\bselect\b'),
        ('WHERE',     r'(?i)\bwhere\b'),
        ('LIMIT',     r'(?i)\blimit\b'),
        ('A',         r'\ba\b'),
        ('VAR',       r'\?[A-Za-z_][A-Za-z0-9_]*'),
        ('PREFIXED',  r'[A-Za-z_][A-Za-z0-9_-]*:[A-Za-z_][A-Za-z0-9_-]*'),
        ('LANG',      r'@[A-Za-z]+(?:-[A-Za-z0-9]+)*'),
        ('STRING',    r'"(?:[^"\\]|\\.)*"'),
        ('NUMBER',    r'\d+'),
        ('LBRACE',    r'\{'),
        ('RBRACE',    r'\}'),
        ('DOT',       r'\.'),
        ('SKIP',      r'[ \t\r\n]+'),
        ('ERROR',     r'.'),
    ]

    master_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_patterns)
    tokens = []

    for match in re.finditer(master_regex, query):
        kind = match.lastgroup
        value = match.group()

        if  kind == 'SKIP':
            continue
        elif kind == 'COMMENT':
            continue
        elif kind == 'ERROR':
            print(f"Error: Unexpected character '{value}'")
            sys.exit(1)
        else:
            tokens.append((kind, value))
    return tokens

query_input = """
# DBPedia: obras de Chuck Berry

select ?nome ?desc where {
    ?s a dbo:MusicalArtist.
    ?s foaf:name "Chuck Berry"@en .
    ?w dbo:artist ?s.
    ?w foaf:name ?nome.
    ?w dbo:abstract ?desc
} LIMIT 1000
"""

print(f"{'TOKEN TYPE'} | {'VALUE'}")
print("----------------------------------")

token_stream = lexical_analyzer(query_input)

for token_type, token_value in token_stream:
    print(f"{token_type} | {token_value}")