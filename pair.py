from types import new_class
from collections import namedtuple

def bimap(x,f,g):
    return x.of( f(x.left), g(x.right) )


Pair = namedtuple('Pair','left, right')
Pair.of = classmethod( lambda cls,x,y: Pair(x,y) )
Pair.bimap = bimap
