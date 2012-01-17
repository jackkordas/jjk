from sudoku import sudoku, IllegalPuzzleError
from nose.tools import raises, eq_

def test():
    f = open('input1')
    p = sudoku(inputfile=f)
    s = p.solve_brute_force()
    soln = sudoku(inputfile=open('soln1'))
    eq_(s, soln)

def test_row_box_col():
    f = open('soln1')
    p = sudoku(inputfile=f)
    box00 = p.box_values(0,0)
    box22 = p.box_values(2,2)
    eq_(box00, [3, 1, 6, 4, 8, 2, 5, 7, 9])
    eq_(box00, box22)
    box66 = p.box_values(6,6)
    eq_(box66, [3, 6, 1, 5, 4, 9, 7, 8, 2])
    box88 = p.box_values(8,8)
    eq_(box66, box88)

    row0 = p.row_values(0)
    eq_(row0, [3, 1, 6, 8, 7, 9, 4, 2, 5])

    col8 = p.col_values(8)
    eq_(col8, [5,7,3,4,8,6,1,9,2])

def test_logical():
    f = open('input1')
    p = sudoku(inputfile=f)
    s = p.solve_logical()
    soln = sudoku(inputfile=open('soln1'))
    print soln
    eq_(s, soln)

@raises(IllegalPuzzleError)
def test2():
    f = open('input2')
    p = sudoku(inputfile=f)
    p.solve_brute_force()
