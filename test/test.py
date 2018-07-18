from lifted.util import *
from lifted.either import Either,isvalid,right_if,left_if, Right, Left

def test_either():  
    two_track = lambda fn: Right(fn).map( decorate(excepting) ).compose( Either.of )
    run = lambda val: Right(val).chain( two_track(float) ).chain( two_track(r.add(1)) ).chain( right_if(r.gt(10)) )
    test1 = run(1)
    print('[Test 1] Result: {}, {}, {}'.format(test1, isinstance(test1,Left), test1.map_left(r.equals(2.)) ))
    assert( isinstance(test1,Left) and  test1.map_left(r.equals(2.)) )
    print('[Test 1] Pass' )
    test2 = run('1')
    print('[Test 2] Result: {}'.format(test2))
    assert( isinstance(test2,Left) and  test2.map_left(r.equals(2.)) )
    print('[Test 2] Pass' )
    test3 = run(['1'])
    print('[Test 3] Result: {}'.format(test3))
    assert( isinstance(test3,Left) and  test3.map_left( r.isinstance(TypeError)) )
    print('[Test 3] Pass' )
    test4 = run(10)
    print('[Test 4] Result: {}'.format(test4))
    assert( isinstance(test4,Right) and  test4.map( r.equals(11.0) ) )
    print('[Test 4] Pass' )
    test5 = run('10')
    print('[Test 5] Result: {}'.format(test5))
    assert( isinstance(test5,Right) and  test4.map( r.equals(11.0) ) )
    print('[Test 5] Pass' )
    test6 = run(['10'])
    print('[Test 6] Result: {}'.format(test6))
    assert( isinstance(test6,Left) and  test6.map_left( r.isinstance(TypeError)) )
    print('[Test 6] Pass' )


if __name__=='__main__':
    print('Testing Either:')
    test_either()