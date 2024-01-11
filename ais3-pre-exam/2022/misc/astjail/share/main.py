import sys
import ast
import re
from code import InteractiveConsole

WHITE_LIST = ['print', 'bool', 'int', 'float', 'str', 'len', 'pow',
              'abs', 'min', 'max', 'sum', 'chr', 'ord', 'hex', 'oct', 'bin']


def check(code):
    # Python ast: https://docs.python.org/3.10/library/ast.html
    def traverse(node):
        if isinstance(node, ast.Expression):
            return traverse(node.body)
        elif isinstance(node, ast.Name):
            if node.id not in WHITE_LIST:
                print('[!] Forbidden function: {}'.format(node.id))
                return False
            else:
                return True
        elif isinstance(node, ast.Call):
            return traverse(node.func) and \
                all(traverse(arg) for arg in node.args) and \
                all(traverse(key) for key in node.keywords)
        elif isinstance(node, ast.BoolOp):
            return all(traverse(n) for n in node.values)
        elif isinstance(node, ast.BinOp):
            return traverse(node.left) and traverse(node.right)
        elif isinstance(node, ast.UnaryOp):
            return traverse(node.operand)
        elif isinstance(node, ast.Compare):
            return all(traverse(n) for n in node.comparators) and traverse(node.left)
        elif isinstance(node, ast.List):
            return all(traverse(n) for n in node.elts)
        elif isinstance(node, ast.Tuple):
            return all(traverse(n) for n in node.elts)
        elif isinstance(node, ast.Subscript):
            return traverse(node.value) and traverse(node.slice)
        elif isinstance(node, ast.Slice):
            return traverse(node.lower) and traverse(node.upper)
        elif isinstance(node, ast.Constant) or node == None:
            return True
        else:
            print("[!] Forbidden node type:", type(node).__name__)
            return False
    try:
        if re.search(r'eval|exec|__import__', code):
            print("[!] Seems unsafe...")
            return False
        tree = ast.parse(code, mode='eval')
        return traverse(tree)
    except SyntaxError:
        print("[!] Syntax error")
        return False


class Sandbox(InteractiveConsole):
    def runsource(self, source: str, filename: str = "<input>", symbol: str = "single") -> bool:
        if not source or not check(source):
            return False
        return super().runsource(source, filename=filename, symbol=symbol)


if __name__ == '__main__':
    sandbox = Sandbox()
    banner = f'Python {sys.version} on {sys.platform}\nSupported Function: {", ".join(WHITE_LIST)}'
    sandbox.interact(banner=banner)
