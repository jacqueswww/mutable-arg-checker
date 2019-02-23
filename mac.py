import argparse
import ast
import os

from ast import NodeVisitor


parser = argparse.ArgumentParser(
        description='Mutable Argument Checker',
)
parser.add_argument('paths', help='Paths to check', nargs='?', default=".")
args = parser.parse_args()


class MutableException(Exception):

    def __init__(self, message, item=None, source_code=None):
        self.message = message
        self.lineno = None
        self.col_offset = None
        self.source_code = source_code.splitlines()

        if isinstance(item, tuple):  # is a position.
            self.lineno, self.col_offset = item
        elif item and hasattr(item, 'lineno'):
            self.set_err_pos(item.lineno, item.col_offset)

    def set_err_pos(self, lineno, col_offset):
        if not self.lineno:
            self.lineno = lineno

            if not self.col_offset:
                self.col_offset = col_offset

    def __str__(self):
        output = self.message

        if self.lineno and self.source_code:

            output = 'line %d: %s\n%s' % (
                self.lineno,
                output,
                self.source_code[self.lineno - 1]
            )

            if self.col_offset:
                col = '-' * self.col_offset + '^'
                output += '\n' + col

        return output


class FuncArgVisitor(NodeVisitor):

    def __init__(self, file_name, source_code):
        self.file_name = file_name
        self.source_code = source_code

    def print_error(self, node, error_msg):
        print(os.path.abspath(self.file_name) + ':')
        print(MutableException(error_msg, item=node, source_code=self.source_code))

    def visit_FunctionDef(self, node):
        for def_node in node.args.defaults + node.args.kw_defaults:
            if isinstance(def_node, ast.Dict):
                self.print_error(def_node, 'Mutable dict parameter')
            if isinstance(def_node, ast.List):
                self.print_error(def_node, 'Mutable list parameter')
            elif isinstance(def_node, ast.Call):
                if def_node.func.id in ('dict', 'list'):
                    self.print_error(def_node, f'Mutable {def_node.func.id} parameter')


def check_args(file_name, code):
    nodes = ast.parse(code)
    FuncArgVisitor(file_name, code).visit(nodes)


def walk_path(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            file_name = os.path.join(root, name)
            with open(file_name) as f:
                check_args(file_name, f.read())


if __name__ == '__main__':
    for path in args.paths:
        walk_path(path)

