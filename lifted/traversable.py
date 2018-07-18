from dataclasses import dataclass 
from .adt import Monoid, Applicative, Chain
from collections import namedtuple
from typing import Any
from types import new_class
import pyramda as r

def get_tup_value(x):
    return x[0]

def get_ntup_value(x):
    return x.v 

def map(x,fn):
    return x.ap( x.of( fn ) )

def ap(x,fn):
    return type(x)( r.map( fn.get_fun(), x.get_value() ) )

def apt(x,fn):
    return x.of( r.map(fn.get_fun(),x.get_value()) )

@r.curry
def concat(x,y):
    return x.concat( y )

def bind(x,fn):
    return fn(x.get_value())

def chain(x,fn):
    return x.concat( fn(x.get_value()) ) 


def freduce( x, fn, val ):
    return r.reduce( lambda acc,v: acc.concat(x.map(fn)), val, x )


def lift2(a, b, f):
    print(a,b,f)
    return b.ap(a.map(f))

def reduce(xs,fn,val):
    return r.reduce( lambda acc,x: acc.concat( fn(x) ), val, xs )

def traverse(xs, T, fn):
    return r.reduce( lambda acc,x: acc.concat( fn(x) ), T.of( xs.empty() ) , xs )

Tuple = new_class('Tuple',bases=(tuple,))
Tuple.concat = lambda x,y: Tuple(x+y)
Tuple.of = classmethod( lambda cls, *x: cls( x ) )
Tuple.empty = classmethod( lambda cls: cls.of() )
Tuple.map = map
Tuple.ap = ap
Tuple.chain = chain
Tuple.reduce = freduce
Tuple.get_value = lambda x: x
Tuple.get_fun = lambda fn: fn[0]
Tuple.bind = bind
Tuple.reduce = reduce
Tuple.traverse = traverse
