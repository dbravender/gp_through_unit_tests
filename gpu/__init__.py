import ast, _ast
import inspect
import re
import types

def function_to_ast(fun):
    definition = inspect.getsource(fun)
    lines = definition.split("\n")
    # remove whitespace
    lines[0] = lines[0].rstrip()
    m = re.match('^\s*', lines[0])
    if m:
        space_offset = m.span()[1]
        new_source = []
        for line in lines:
            new_source.append(line[space_offset:])
        return ast.parse("\n".join(new_source))
    else:
        return ast.parse(definition)

def extract_terminals(fun):
    def get_terminal_value(node):
        if type(node) == ast.Str:
            return node.s
        if type(node) == ast.Num:
            return node.n
    return list(set(filter(lambda x: x, 
                   [get_terminal_value(x) 
                    for x in ast.walk(function_to_ast(fun))])))

def extract_functions(fun, locals=None):
    def get_closure_functions(fun):
        funcs = []
        if fun.func_closure:
            for cell in fun.func_closure:
                if type(cell.cell_contents) == types.FunctionType:
                    funcs.append(cell.cell_contents)
        return funcs

    def get_function(node):
        if type(node) == ast.Call:
            if hasattr(node, 'func') and hasattr(node.func, 'id'):
                if node.func.id in fun.func_globals:
                    return fun.func_globals[node.func.id]
                try:
                    return eval(node.func.id)
                except NameError:
                    pass

    return get_closure_functions(fun) + \
           list(set(filter(lambda x: x,
                   [get_function(x)
                    for x in ast.walk(function_to_ast(fun))])))

def extract_inferred_functions(fun):
    def get_inferred_function(node):
        if type(node) == ast.Name:
            if node.id in fun.func_globals:
                t = func.func_globals
                if type(t) == type:
                    pass
