"""Parse every code cell in both notebooks with ast.parse to catch syntax errors."""
import ast, json, sys
sys.stdout.reconfigure(encoding='utf-8')

errs = 0
for path in ['phosphene-simulation/phosphene-simulation.ipynb',
             'phosphene-simulation/phosphene-simulation-solution.ipynb']:
    nb = json.load(open(path, encoding='utf-8'))
    n = 0
    for i, c in enumerate(nb['cells']):
        if c['cell_type'] != 'code':
            continue
        n += 1
        src = ''.join(c['source'])
        # %pip and %magic lines aren't valid python; strip them before ast.parse
        clean = '\n'.join('' if line.lstrip().startswith('%') else line
                          for line in src.split('\n'))
        try:
            ast.parse(clean)
        except SyntaxError as e:
            errs += 1
            print(f'{path} cell #{i}: line {e.lineno}: {e.msg}')
            print('    ' + (clean.split(chr(10))[e.lineno-1] if e.lineno else ''))
    print(f'{path}: {n} code cells')
print(f'TOTAL ERRORS: {errs}')
sys.exit(1 if errs else 0)
