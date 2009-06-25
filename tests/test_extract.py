from gpu import extract_terminals, extract_functions, extract_inferred_functions

def test_string_extraction():
    def fun():
        return 'simple string'

    assert extract_terminals(fun) == ['simple string']

def test_int_extraction():
    def fun():
        return 10

    assert extract_terminals(fun) == [10]

def test_builtin_fun_extraction():
    def fun():
        len([1, 2, 3])

    assert extract_functions(fun) == [len]

def global_gets_called():
    pass

def test_global_fun_extraction():
    def fun():
        global_gets_called()
    assert extract_functions(fun) == [global_gets_called]

def test_closure_fun_extraction():
    def closure_is_called():
        pass
    def fun():
       closure_is_called()
    assert extract_functions(fun) == [closure_is_called]

def test_local_and_global_extraction():
    def a_closure():
        pass
    def fun():
        global_gets_called()
        a_closure()
    assert extract_functions(fun) == [a_closure, global_gets_called]
    

def another_global():
    pass

def test_multiple_global_extraction():
    def fun():
        global_gets_called()
        another_global()
    assert extract_functions(fun) == [another_global, global_gets_called]

def test_multiple_local_extraction():
    def local1():
        pass
    def local2():
        pass
    def fun():
        local1()
        local2()
    assert extract_functions(fun) == [local1, local2]

def test_multiple_local_global_extraction():
    def local1():
        pass
    def local2():
        pass
    def fun():
        local1()
        local2()
        another_global()
        global_gets_called()
    assert extract_functions(fun) == [local1, local2, global_gets_called, another_global]

#class Monkey(object):
#    def eat_bananas(self):
#        pass

#a_monkey = Monkey()

#def test_inferred_fun_extraction():
#    class Monkey(object):
#        def eat_bananas(self):
#            pass
#    a_monkey = Monkey()
#    def fun():
#        a_monkey
#    inferred_fun = extract_inferred_functions(fun)[0]
#    assert inferred_fun.func == Monkey.insane
#    assert inferred_fun.args[0] == a_monkey
