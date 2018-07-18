
from types import new_class
import pyramda as r
def concat(that, this):
    return lambda x: this(x).concat( that(x) )

# this: fn of n parameters
# that: fn of >= n+1 parameters
# that(x, this(x))
def map(this, that):
    return ap(this,of(that))

def ap(this, that):
    return lambda x: ( that(x)(this(x)) ) 

def of(cls, fn):
    return lambda *x: fn

# this: fn of n parameters
# that: fn of >= n+1 parameters
# that(this(x), x)
def chain(this, that):
    return lambda x: that( this(x) )(x)

# f: preprocess input, x
# g: postprocess output, f(x)
def promap(this, f, g):
    return lambda x: g( this( f(x)) )

def compose(this, that):
    return lambda x: that(this(x))

def init(self,fn):
    self._fn = fn

@r.curry
def to_method(cls,fn):
    def method(*args):
        return cls( fn(*args) )
    return method
Function = new_class('Function',bases=(object,))
Function.__init__ = init
Function.__call__ = lambda self,x: self._fn(x)
m = to_method(Function)
Function.of = classmethod( m(of) )
Function.ap = m(ap)
Function.map = m(map)
Function.chain = m(chain)
Function.promap = m(promap)
Function.compose = m(compose)

# v = Function(r.add).map( excepting )