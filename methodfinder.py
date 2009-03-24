'''
Simple usage:

>>> methodfinder('a', None, True)
all('a') == True
any('a') == True
bool('a') == True
len('a') == True
'a'.__len__() == True
'a'.isalnum() == True
'a'.isalpha() == True
'a'.islower() == True

>>> methodfinder('a', None, False)
callable('a') == False
'a'.isdigit() == False
'a'.isspace() == False
'a'.istitle() == False
'a'.isupper() == False

>>> methodfinder('a', None, 1)
all('a') == 1
any('a') == 1
bool('a') == 1
len('a') == 1
'a'.__len__() == 1
'a'.isalnum() == 1
'a'.isalpha() == 1
'a'.islower() == 1

>>> methodfinder('jon/bob', '/', ['jon', 'bob'])
'jon/bob'.rsplit('/') == ['jon', 'bob']
'jon/bob'.split('/') == ['jon', 'bob']

>>> methodfinder([1, 2, 3, 4], None, 4)
len([1, 2, 3, 4]) == 4
max([1, 2, 3, 4]) == 4
[1, 2, 3, 4].__len__() == 4
[1, 2, 3, 4].pop() == 4
    
>>> methodfinder([1, 2, 3, 4], 5, [1, 2, 3, 4, 5])
o = [1, 2, 3, 4]
o.append(5)
o == [1, 2, 3, 4, 5]

>>> methodfinder([1, 2, 3, 4], [5, 6], [1, 2, 3, 4, 5, 6])
[1, 2, 3, 4].__add__([5, 6]) == [1, 2, 3, 4, 5, 6]
[1, 2, 3, 4].__iadd__([5, 6]) == [1, 2, 3, 4, 5, 6]
o = [1, 2, 3, 4]
o.__iadd__([5, 6])
o == [1, 2, 3, 4, 5, 6]
o = [1, 2, 3, 4]
o.extend([5, 6])
o == [1, 2, 3, 4, 5, 6]

>>> methodfinder([5,4,1,2,3], None, [1,2,3,4,5])
sorted([5, 4, 1, 2, 3]) == [1, 2, 3, 4, 5]
o = [5, 4, 1, 2, 3]
o.sort()
o == [1, 2, 3, 4, 5]
'''

from pprint import pformat
from copy import copy

blacklist_builtins = ['raw_input', 'quit', 'exit', 'eval', 'file', 'apply', 'help', 'license', 'print']
builtins = dir(__builtins__)
[builtins.remove(x) for x in blacklist_builtins if x in builtins]

def methodfinder(obj, input=None, expected=None):
    if obj and input is None:
        for func in builtins:
            try_func(eval(func), obj, expected)
    for method in dir(obj):
        try_method(obj, method, input, expected)

def try_method(obj, method, input, expected):
    try:
        object_copy = copy(obj)
        bound_method = eval('object_copy.%s' % method)
        try_func(bound_method, input, expected)
        if input is not None:
            formatted_input = pformat(input)
        else:
            formatted_input = ''
        if object_copy == expected: # the horrors of side-effects
            print("o = %s\no.%s(%s)\no == %s" % (pformat(obj), bound_method.__name__, formatted_input, pformat(expected)))
    except:
        pass

def try_func(func, input, expected):
    try:
        original_self = copy(func.__self__)
    except:
        pass
    try:
        if input is not None:
            result = func(input)
            formatted_input = pformat(input)
        else:
            result = func()
            formatted_input = ''
        if result == expected:
            if hasattr(func, '__self__') and func.__self__:
                func_name = '%s.%s' % (pformat(original_self), func.__name__)
            else:
                func_name = func.__name__
            print("%s(%s) == %s" % (func_name, formatted_input, pformat(expected)))
    except:
        pass

if __name__ == "__main__":
    import doctest
    doctest.testmod()
