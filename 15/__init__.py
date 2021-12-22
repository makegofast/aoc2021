import time

class Vagrant(object):
    def __init__(self):
        self.data = []
        self.width = 0
        self.height = 0

    def load_data(self, data):
        for line in data:
            row = [int(c) for c in line]
            self.data.append(row)
            self.width = max(self.width, len(row))

        self.height = len(self.data)

        self.start = [0, 0]
        self.end = [self.height-1, self.width-1]

    def spaces_around(self, row, col):
        ret = []

        for pos in [ [row, col+1], [row+1, col], [row, col-1], [row-1, col] ]:
            if not self.in_bounds(*pos):
                continue

            ret.append(pos)

        return ret

    def in_bounds(self, row, col):
        if row < 0 or row >= self.height or col < 0 or col >= self.width:
            return False
        else:
            return True

    def value_at(self, row, col):
        if self.in_bounds(row, col):
            return self.data[row][col]

        return None

    def find_next_point(self, path, ahead=4):
        row, col = path[-1]
         
        if path[-1] == self.end:
            return

        print("find_next_point", row, col)

        if not self.in_bounds(row, col):
            print("find_next_point %s,%s is out of bounds" % (row, col))
            return

        rcost = dcost = None

        rpos = [row, col+1]
        if self.in_bounds(*rpos):
            rpath = path.copy() + [rpos] 
            for i in range(0, ahead):
                rnext = self.find_next_point(rpath, ahead - 1)

                if rnext:
                    rpath.append(rnext)

            rcost = self.calc_cost(rpath)

        dpos = [row+1, col]
        if self.in_bounds(*dpos):
            dpath = path.copy() + [dpos]
            for i in range(0, ahead):
                print('calling find_next_point with ', dpath, '-1')
                dnext = self.find_next_point(dpath, ahead - 1)
                print("dnext", dnext)
            
                if dnext:
                    dpath.append(dnext)

            dcost = self.calc_cost(dpath)

        print("rcost", rcost, "dcost", dcost)
        if not dcost and rcost:
            return rpos
        elif not rcost and dcost:
            return dpos
        elif not rcost and not dcost:
            return None
        elif rcost < dcost:
            return rpos
        else:
            return dpos

    def calc_cost(self, path):
        print(path)

        return sum([self.data[r][c] for r, c in path]) 

    def plot_paths(self):
        path = [self.start]

        while True:
            current = path[-1]
            if current == self.end:
                break

            next_point = self.find_next_point(path)

            if not next_point:
                break

            self.status(path)
            path.append(next_point)

        self.status(path)

    def status(self, path=[]):
        for row in range(0, self.height):
            line = ''
            for col in range(0, self.width):
                val = str(self.value_at(row, col))
                pos = [row, col]

                if pos == self.end:
                    val = bcolor('greenbg', val)

                if pos == self.start:
                    val = bcolor('bluebg', val)

                if pos == path[-1]:
                    val = bcolor('red', val)
                    val = bcolor('redbg', val)

                if [row, col] in path:
                    val = bcolor('red', val)

                line += val 

            print(line)
        print()
        print('cost', self.calc_cost(path))

def bcolor(color, text):
    colors = {
        'bred': '\033[31;1m',
        'redbg': '\033[41m',
        'red': '\033[91m',
        'green': '\033[92m',
        'greenbg': '\033[42m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'bluebg': '\033[44m',
        'reset': '\033[0m'
    }

    return colors[color] + str(text) + colors['reset']

def get_data():
    return [l.rstrip() for l in open('data.txt', 'r').readlines()]

def get_test_data():
    return [l.rstrip() for l in open('test_data.txt', 'r').readlines()]

def solution_part_1(data):
    hobo = Vagrant()
    hobo.load_data(data) 
    hobo.plot_paths()

def solution_part_2(data):
    pass

if __name__ == '__main__':
    solution_part_1(get_test_data())
    #solution_part_1(get_data())

    #solution_part_2(get_test_data())
    #solution_part_2(get_data())
