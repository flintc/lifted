import pyramda as r
from .fn import Function
from functools import wraps
from .traversable import Tuple
from .either import Either,Right,Left
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

@r.curry
def unwrap(val):
    return val.get_value()

ex = Function(excepting)

@r.curry
def bimap(f,g,x):
    return x.bimap(f, g) 


@r.curry
def promap(before,after,fn,x):
    return after( fn( before(x) ) )

@r.curry
def decorate(decorating_fn,fn_to_decorate):
    return Function( decorating_fn(fn_to_decorate) )


# #two_track = lambda cls, fn: cls.right(fn).map( decorate(excepting) )
# class TwoTrack(Either):
#     pass
# class Result(TwoTrack, Right):
#     def chain(self,fn):
#         result = super().chain( self.of( fn ) ) 
#         #return self.of( T.Tuple(result) if r.isinstance(Iterable,result) else result )
#         return self.of( result )
#     @classmethod
#     def of(cls,val):
#         return cls.right(val).map( decorate(excepting) ) if val is callable else \
#             super().of( val )
# class Error(TwoTrack, Left):
#     pass

# TwoTrack.right = Result
# TwoTrack.left = Error
# #TwoTrack.two_track = classmethod(two_track)

# #def two_track(start_value):


two_track = lambda cls, fn: cls.right(fn).map( decorate(excepting) )
class TwoTrack(Either):
    pass
class Result(TwoTrack, Right):
    def chain(self,fn):
        result = super().chain(self.two_track(fn)) 
        #return self.of( T.Tuple(result) if r.isinstance(Iterable,result) else result )
        return self.of( result )
class Error(TwoTrack, Left):
    pass

TwoTrack.right = Result
TwoTrack.left = Error
TwoTrack.two_track = classmethod(two_track)

traverse_results = r.compose( promap(Tuple,unwrap),traverse(Result) )
fmap_results = r.compose( promap(Tuple,unwrap), fmap )

def  printer(*args,**kwargs):
    print('args: {}, kwargs: {}'.format(args,kwargs))

from functools import wraps
def curry(fn):
    varnames = ['']
    if hasattr(fn,'__code__'):
        kwonly = inspect.getfullargspec(baz).kwonlyargs
        varnames = tuple( set(fn.__code__.co_varnames) - set(['args','kwargs']) - set(kwonly) )
    def wrapped(cum_args=(),cumkwargs=dict()):
        @wraps(fn)
        def wrapper(*args,**kwargs):
            # print('cum_args: {}, args: {}'.format(cum_args,args))
            # print('cumkwargs: {}, kwargs: {}'.format(cumkwargs,kwargs))
            ca = cum_args+args
            ckw = dict(**cumkwargs,**kwargs)
            # print('varname: {}, ckw: {}'.format(varnames,ckw))
            if hasattr(fn,'__code__'): 
                remvarnames = set(varnames) - set(ckw.keys())
                nonkwonly_items = dict( [ (k,v) for k,v in ckw.items() if (k not in kwonly) and (k in varnames) ] )
                kwonly_or_kwargs_items = dict( [ (k,v) for k,v in ckw.items() if (k in kwonly) and (k not in varnames) ] )
                ckwargs = dict( list( zip( remvarnames, ca[0:len(remvarnames)] ) ),**nonkwonly_items )
                # print('varnames: {}, remvarnames: {}'.format(varnames,remvarnames))
                # print('kwonly: {}, kwonly_or_kwargs_items: {}'.format(kwonly,kwonly_or_kwargs_items))
                # print('nonkwonly_items: {}, ckwargs: {}'.format(nonkwonly_items,ckwargs))
                try:
                    # print('args applied: {}, *args applied: {}'.format(list(( ckwargs[k] for k in varnames )),ca[len(remvarnames):] ))
                    printer(*( ckwargs[k] for k in varnames ), *ca[len(remvarnames):], **kwonly_or_kwargs_items )
                except:
                    pass
            try:
                if hasattr(fn,'__code__'): 
                    result = fn( *( ckwargs[k] for k in varnames ), *ca[len(remvarnames):], **kwonly_or_kwargs_items )
                else:
                    result = fn(*ca,**ckw)
                if callable(result):
                    if result.__name__ == fn.__name__:
                        return wrapped(ca,ckw)
                    else:
                        return result
                else:
                    return result
            except:
                return wrapped(ca,ckw)
        return wrapper
    return wrapped()
        
