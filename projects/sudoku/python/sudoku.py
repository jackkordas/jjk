import copy

class Cell:

    def __init__(self, value):
        if value == '':
            self.value = None
        else:
            self.value = int(value)
            assert self.value > 0 and self.value < 10, 'value is ' + value

    def __eq__(self, other):
        if type(other) != type(self): return False
        return self.value == other.value

    def __ne__(self,other):
        return not self == other

class IllegalPuzzleError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class sudoku:

    def __init__(self, inputfile=None, puzzle=None):
        assert inputfile or puzzle
        if inputfile:
            lines = inputfile.readlines()
            assert len(lines) == 9
            self.cells=[]
            for line in lines:
                line = line.strip()
                entries = line.split(',')
                assert len(entries) == 9
                row = []
                for e in entries:
                    cell = Cell(e)
                    row.append(cell)
                self.cells.append(row)
        else:
            self.cells = copy.deepcopy(puzzle.cells)

        self.check_legal()

    def __eq__(self, other):
        if type(other) != type(self): return False
        if len(self.cells) != len(other.cells): return False
        for row in range (0, len(self.cells)):
            for col in range(0, len(self.cells)):  # assume square
                if self.cells[row][col] != other.cells[row][col]:
                    return False

        return True

    def __ne__(self,other):
        return not self == other


    def __str__(self):
        tmp = ''
        assert self.cells
        for row in self.cells:
            for cell in row:
                tmp += '%s, ' % cell.value
            tmp += '\n'
        return tmp


    def check_legal(self):
        for i in range(0,9):
            if not self.check_row(i): raise IllegalPuzzleError('row %d illegal' % i)
            if not self.check_col(i): raise IllegalPuzzleError('col %d illegal' % i)
            if not self.check_box(i): raise IllegalPuzzleError('box %d illegal' % i)
        return True

    def check_values(self, values):
        taken = {}
        for v in values:
            if v.value and taken.has_key(v.value):
                return False
            taken[v.value] = v

        return True

    def check_row(self, row):
        return self.check_values(self.cells[row])

    def check_col(self, col):
        values = []
        for row in self.cells:
            values.append(row[col])
        return self.check_values(values)

    def row_values(self, row):
        return [cell.value for cell in self.cells[row]]

    def col_values(self, col):
        values = []
        for row in self.cells:
            values.append(row[col].value)
        return values

    def box_values(self, row, col):
        start_row = row / 3 * 3
        start_col = col / 3 * 3

        values = []
        for row in range(0,3):
            for col in range(0,3):
                values.append(
                        self.cells[start_row + row][start_col + col].value)
        return values


    def check_box(self, box):
        '''
        0 --> (0,0), (0,1), (0,2)
              (1,0), (1,1), (1,2)
              (2,0), (2,1), (2,2)
        3 --> (3,0), (3,1), (3,2)
              (4,0), (4,1), (4,2)
              (5,0), (5,1), (5,2)
        '''
        start_row = (box / 3) * 3
        start_col = (box % 3) * 3

        values = []
        for row in range(0,3):
            for col in range(0,3):
                values.append(self.cells[start_row + row][start_col + col])
        return self.check_values(values)

    def solve_brute_force(self):
        solved = True
        puzzle = sudoku(puzzle=self)
        for row in range(0,9):
            for col in range(0,9):
                if not puzzle.cells[row][col].value:
                    cell = puzzle.cells[row][col]
                    solved = False
                    for value in range (1,10):
                        cell.value = value
                        try:
                            if not puzzle.check_legal(): continue
                        except IllegalPuzzleError as ex:
                            continue

                        newpuzzle = puzzle.solve_brute_force()
                        if newpuzzle:
                            return newpuzzle

        if solved:
            return puzzle

        return None

    def solve_logical(self):
        for row in range(0,9):
            for col in range(0,9):
                offset = row*9 + col
                r = set(self.row_values(row))
                c = set(self.col_values(col))
                b = set(self.box_values(row, col))
                all = r | c | b
        return None
            
