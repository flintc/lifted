from types import new_class
from dataclasses import dataclass 
import pyramda as r
from typing import Any, Callable, TypeVar, NewType
import inspect 
from abc import ABCMeta
from collections import namedtuple


#class Lifted(ABCMeta):
#    pass
@dataclass
class Lifted:
    pass

@dataclass
class Semigroup(Lifted):
    concat: Callable


@dataclass
class Monoid(Lifted):
    empty: Any

@dataclass
class Group(Monoid):
    invert: Any

@dataclass
class Setoid(Lifted):
    equals: Any

@dataclass
class Ord(Setoid):
    lte: Any

@dataclass
class Semigroupoid:
    compose: Any


@dataclass
class Category(Semigroupoid):
    id: Any

@dataclass
class Functor(Lifted):
    map: Any


@dataclass
class Apply(Functor):
    ap: Any

@dataclass
class Applicative(Apply):
    of: Any


@dataclass
class Chain(Apply):
    chain: Any

@dataclass
class Foldable(Lifted):
    reduce: Any


@dataclass
class Traversable(Foldable):
    traverse: Any

@dataclass
class Monad(Applicative,Chain):
    pass



def sequence(TypeR,x):
    pass

