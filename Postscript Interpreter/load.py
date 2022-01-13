import sys

from psParser import read
from stacks import Stacks
from colors import *

testinput1 = """
    /x 3 def 
    /square {dup mul} def
    [x 1 x sub 1] /arr exch def  
    arr 0 get dup
    0 gt 
    {square} {dup} ifelse
"""
testinput2 = """
    /x 1 def
    /y 2 def
    /x 10 def
    /y 20 def
    0 x 1 y {add} for
"""

testinput3 = """
    /f {dup length} def
    [1 2 (322) (451) length]
    [1 -2 4 5 add (long) length]
    (123456)  f
"""

testinput4 = """
        /x 1 def
        /y 2 def
        1 dict begin
        /x 10 def
        1 dict begin /y 3 def x y end
        /y 20 def
        x y
        end
        x y
"""

testinput5 = """
        1 2 3 4 5 count copy 15 1 1 5 {pop exch sub} for 0 eq
"""
testinput6 = """
        /str (CptS355) def 
        /loadarr {/arr exch def 0 1 arr length 1 sub {arr exch dup str exch get put } for arr} def
        [0 0 0 0 0 0 0] loadarr
"""
testinput7 = """
    (Vaccine)
    dup 0  get 86 eq
        {
            (Vaccine) eq
            { (yay) }
            { (nope)  }
            ifelse
        } if
"""

testinput8 = """
        /n 5 def
        /fact {
            0 dict begin
            /n exch def
            n 2 lt
            { 1}
            {n 1 sub fact n mul }
            ifelse
            end
        } def
        n fact
"""
testinput9 = """
    /fact {
            0 dict
            begin
                /n exch def
                1
                n -1 1 { mul /n n 1 sub def } for 
            end
        } def
        6 fact
"""

testinput10 = """
        /loadarray {/arr exch def 0 1 arr length 1 sub {arr exch get} for } def
        /sumArray {0 exch loadarray count n sub -1 1 {pop add} for /n n 1 add def } def
        /x 5 def
        /y 10 def
        /n 1 def
        [x y x y add] sumArray
"""

testinput11 = """
    [49 50 51 52 53 54]
    [49 50 51 52 53 54] dup dup /arr1 exch def
    (12345)
    (12345) dup dup /str1 exch def
    arr1 1 get
    str1 1 get
    eq 
    pop
    arr1 4 100 put
    str1 4 100 put
    arr1 length
    str1 length 
    lt
"""
testinput12 = """
   []
"""
testinput13 = """ """

testinput14 = """
            (or)
            dup 0  get 2 eq
                {
                    (Easy) eq
                    { (n) }
                    { (t)  }
                    ifelse
                } if
        """
testinput15 = """
                10 20 90 40 50 count copy 15 60 10 50 {pop exch sub} for 1 eq
        """
testinput16 = """
            /x 9 def
            /y 9 def
            /x 1 def
            /y 2 def
            0 x 1 y {add} for
        """

tests = [testinput1, testinput2, testinput3, testinput4, testinput5, testinput6,
         testinput7, testinput8, testinput9, testinput10, testinput11, testinput12, testinput13, testinput14, testinput15, testinput16]

# program start
if __name__ == '__main__':

    psstacks = Stacks()
    testnum = 1
    for testcase in tests:
        try:
            expr_list = read(testcase)
            for expr in expr_list:
                expr.eval(psstacks)
            print("--test {}--".format(testnum))
            testnum += 1
            print(CYAN+'opstack '+CEND, psstacks.opstack)
            # print('dictstack ' , psstacks.dictstack)
            psstacks.clearBoth()
        except (SyntaxError, NameError, TypeError, Exception) as err:
            print(type(err).__name__ + ':', err)
