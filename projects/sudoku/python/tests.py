from sudoku import sudoku, IllegalPuzzleError
from nose.tools import raises, eq_

def test():
    f = open('input1')
    p = sudoku(inputfile=f)
    s = p.solve_brute_force()
    print s
    soln = sudoku(inputfile=open('soln1'))
    eq_(s, soln)


@raises(IllegalPuzzleError)
def test2():
    f = open('input2')
    p = sudoku(inputfile=f)
    p.solve_brute_force()
