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
        self.solved = False #XXX
        self.init_combination_map()

    def init_combination_map(self):
        """ assume we need at most 6 """
        map = []
        num_values = 6
        for i in range(num_values):
            for j in range(i+1, num_values):
                map.append((j, [i,j]))

        found = True
        next_start = 0
        while found:
            found = False
            this_start = next_start
            next_start = len(map)
            for (index, values) in map[this_start:]:
                i = index + 1
                while i < num_values:
                    new_values = values[:]
                    new_values.append(i)
                    map.append((i, new_values))
                    found = True
                    i += 1
        self._combination_map = map
        print 'combination map'
        for (index, values) in map:
            print index, values

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
                if cell.value:
                    tmp += '%s, ' % cell.value
                else:
                    tmp += '(' + '|'.join([str(v) for v in cell.valid_values]) + '), '
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
        return [cell.value for cell in self.cells[row] if cell.value is not None]

    def col_values(self, col):
        values = []
        for row in self.cells:
            if row[col].value:
                values.append(row[col].value)
        return values

    def col_cells(self, col):
        return [row[col] for row in self.cells]

    def box_values(self, row, col):
        start_row = row / 3 * 3
        start_col = col / 3 * 3

        values = []
        for row in range(0,3):
            for col in range(0,3):
                cell = self.cells[start_row + row][start_col + col]
                if cell.value:
                    values.append(cell.value)
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

    full = set([1,2,3,4,5,6,7,8,9])

    def init_valid_values(self):
        changed = False
        for row in range(0,9):
            for col in range(0,9):
                if self.cells[row][col].value: continue
                r = set(self.row_values(row))
                c = set(self.col_values(col))
                b = set(self.box_values(row, col))
                all_used = r | c | b
                valid = self.full - all_used
                if len(valid) == 1:
                    self.cells[row][col].value = valid.pop()
                    self.cells[row][col].valid_values = None
                    changed = True
                else:
                    self.cells[row][col].valid_values = valid

        return changed

    def get_reduction_combos(self, members):
        # XXX - should use a map here that is generated once and used repeatedly
        combos = []
        num_members = len(members)
        for (index, values) in self._combination_map:
            if index >= num_members:  
                continue
            entry = [members[i] for i in values]
            combos.append(entry)

        return combos


    def reduce(self, cells, exclusive_set, owning_indices):
        for index in range(9):
            if cells[index].value: continue
            if index in owning_indices: continue
            if len(cells[index].valid_values.intersection(exclusive_set)) > 0:
                print 'winner, winner, chicken dinner'

    def try_reduce(self):
        for col in range(9):
            cells = self.col_cells(col)
            undecided_indices = []
            for index in range(9):
                if not cells[index].value:
                    undecided_indices.append(index)
            reduction_combinations = self.get_reduction_combos(
                                                        undecided_indices)
            for reduction in reduction_combinations:
                s = set()
                for index in reduction:
                    s = s.union(cells[index].valid_values)
                if len(s) == len(reduction):
                    print 'found reduction for col %d, ' % col, reduction
                    self.reduce(cells, s, reduction)
            print 'column ', col
            print 'combos ', reduction_combinations
        for row in range(9):
            pass
        for box in range(9):
            pass

        return False

    def solve_logical(self):
        while not self.solved:
            changed = self.init_valid_values()
            print self
            if changed:
                continue
            changed = self.try_reduce()
            if changed:
                continue
            import pdb; pdb.set_trace()
        print 'logical solution'
        print self

    def solve_logicalxxx(self):
        unsolved = True
        choice_made = True
        while unsolved and choice_made:
            unsolved = False
            choice_made = False
            lens = []
            for row in range(0,9):
                for col in range(0,9):
                    if self.cells[row][col].value: continue
                    unsolved = True
                    r = set(self.row_values(row))
                    c = set(self.col_values(col))
                    b = set(self.box_values(row, col))
                    all = r | c | b
                    lens.append((row, col, len(all)))
                    print "row %d col %d len %d" % (row, col, len(all))
                    if len(all) == 8:
                        tmp = self.full - all
                        assert len(tmp) == 1
                        choice = tmp.pop()
                        print "(%d,%d) choose %d" % (row, col, choice)
                        self.cells[row][col].value = choice
                        choice_made = True
        if unsolved:
            for cell_len in lens:
                #import pdb; pdb.set_trace()
                #print 'foo'
                print "(%d, %d): %d" % (cell_len[0], cell_len[1], cell_len[2])
        return self
            
