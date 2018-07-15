from dataclasses import dataclass 
from lifted.adt import Monoid, Applicative, Chain
from collections import namedtuple
from typing import Any
from types import new_class
import pyramda as r
from lifted.traversable import Tuple

def bimap(x,f,g): 
    return (
        x.of( r.if_else(
            r.isinstance(x.left), 
            r.compose(f,r.getattr('v')),
            r.compose(g,r.getattr('v')) 
        )(x) )
    ) 

def isvalid(x):
    if hasattr(x,'map'):
        return all( x.map(r.complement((r.isinstance(Exception)) ) ) )
    else:
        return r.complement( r.isinstance(Exception) )(x)

def left_id(x):
    return r.always(x.left(x))

def chain(x,right_track,left_track=left_id):
    return fn(x.get_value()) if r.isinstance(x.right,x) else left_track( x.get_value() )

class Either(object):
    pass

def concat(x,y):
    xv = x.v if isinstance(x.v,Tuple) else Tuple.of(x.v)
    yv = y.v if isinstance(y.v,Tuple) else Tuple.of(y.v)
    return x.of( xv.concat(yv) )
 
Either.of = classmethod( lambda cls,x: cls.right(x) if isvalid(x) else cls.left(x) )
Either.bimap = bimap
Either.empty = classmethod( lambda cls: cls.right(Tuple.empty()) )
Either.concat = concat
Either.get_value = lambda x: x.v
Either.chain = chain

@dataclass
class Right(Either):
    v: Any
@dataclass
class Left(Either): 
    v: Any

Either.right = Right
Either.left = Left

'''

from lifted.either import Either, Tuple
from lifted.fn import Function, of
from lifted.util import *
t = Either.of(10)
add1 = Function( excepting(r.add(1)) ).compose( Either.of )
add10 = Function( excepting(r.add(10)) ).compose( Either.of )
t.chain( add1 ).chain( add10 ).chain( r.compose(Either.of, lambda x: Tuple.of( (x,x,str(x) ) ) ) )
t.chain( add1 ).chain( add10 ).chain( r.compose(Either.of, lambda x: Tuple( (x,x,str(x) ) ) ) ).chain( fmap( add10 ) )
right_val = t
right_val
    .chain( add1 )
    .chain( add10 )
    .chain( r.compose(Either.of, lambda x: Tuple( (x,x,str(x) ) ) ) ) # Either<Float> => Either<Tuple>
    .chain( fmap( add10 ) ) # Either<Tuple> => Tuple<Either>
    .map( chain( add10) ) # Tuple<Either> => Tuple<Either>

left_of_tuple = (
    right_val
        .chain( add1 )
        .chain( add10 )
        .chain( r.compose(Either.of, lambda x: Tuple( (x,x,str(x) ) ) ) )
        .chain( traverse(Either, add10 ) ) # some fail resulting in left of tuple    
)

tuple_of_rights_and_left = (
    right_of_tuple
        .chain( add1 )
        .chain( add10 )
        .chain( r.compose(Either.of, lambda x: Tuple( (x,x,str(x) ) ) ) )
        .chain( fmap(Either, add10 ) ) # some fail resulting in a tuple of 2 rights, one left    
)s


Should have the same third value, error str + int
t.chain( add1 ).chain( add10 ).chain( r.compose(Either.of, lambda x: Tuple( (x,x,str(x) ) ) ) ).chain( fmap( add10 ) )

t.chain( add1 ).chain( add10 ).chain( r.compose(Either.of, lambda x: Tuple( (x,x,str(x) ) ) ) ).chain( traverse( add10 ) )

t.chain( add1 ).chain( add10 ).chain( r.compose(Either.of, lambda x: Tuple( (x,x,str(x) ) ) ) ).chain( fmap( add10 ) ).map( chain( add10) )

'''