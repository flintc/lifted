import pyramda as r
from lifted.fn import Function
from functools import wraps
@r.curry
def traverse(T,fn,x):
    return x.traverse(T,fn)

@r.curry
def fmap(fn,x):
    return x.map(fn)

@r.curry
def excepting(fn,x):
    try:
        return fn(x)
    except Exception as e:
        return e

@r.curry
def chain(fn,x):
    return x.chain(fn)

@r.curry
def bichain(f,g,x):
    return x.chain(f,g)

@r.curry
def bind(val):
    return val.get_value()

ex = Function(excepting)

@r.curry
def bimap(f,g,x):
    x.bimap(lambda x: Tuple.of(x-10), lambda x: Tuple.of(x+7) ) 
