class TransparentOrigami(object):
    def __init__(self):
        self.dots = {}
        self.folds = []
        self.width = 0
        self.height = 0

    def add_dot(self, x, y):
        self.dots.setdefault(y, {})
        self.dots[y][x] = 1

        self.width = max(self.width, x)
        self.height = max(self.height, y)

    def has_dot(self, x, y):
        try:
            return self.dots[y][x]
        except KeyError:
            return False

    def fold(self, direction, index):
        fn = getattr(self, 'fold_' + direction)
        fn(index)

    def fold_y(self, index):
        print('before fold_y %s' % index)
        self.status()

        for y in range(index+1, self.height+1):
            for x in range(0, self.width+1):
                if self.has_dot(x, y):
                    new_y = index - (y - index)
                    self.add_dot(x, new_y)

        self.dots = {k: v for k, v in self.dots.items() if k < index}
        self.height = index-1

        print('after fold_y %s' % index)
        self.status()

    def fold_x(self, index):
        print('before fold_x %s' % index)
        self.status()

        new_dots = {}
        for y in range(0, self.height+1):
            new_dots.setdefault(y, {})
            for x in range(0, self.width+1):
                if x < index and self.has_dot(x, y):
                   new_dots[y][x] = 1
                elif x > index and self.has_dot(x, y):
                    new_x = index - (x - index)
                    new_dots[y][new_x] = 1

        self.dots = new_dots
        self.width = index-1

        print('after fold_x %s' % index)
        self.status()

    def load_data(self, data):
        loading_dots = True

        for line in data:
            if line.startswith('fold'):
                direction, index = line.split()[-1].split('=')
                self.folds.append([direction, int(index)])
            elif ',' in line:
                print('dot line', line)
                x, y = line.split(',')
                self.add_dot(int(x), int(y))
            elif line == '':
                pass
            else:
                print("Ignoring load_data line:", line)

    def status(self):
        print(self.dots)

        for y in range(0, self.height+1):
            line = str(y).rjust(5) + ' '
            for x in range(0, self.width+1):
                line += '#' if self.has_dot(x, y) else '.' 
            print(line)

        print('dot count:', sum(len(l) for i,l in self.dots.items()))

def get_data():
    return [l.rstrip() for l in open('data.txt', 'r').readlines()]

def get_test_data():
    return [l.rstrip() for l in open('test_data.txt', 'r').readlines()]

def solution_part_1(data):
    to = TransparentOrigami()
    to.load_data(data) 
    to.status()

    fold = to.folds[0]
    to.fold(fold[0], fold[1])

def solution_part_2(data):
    to = TransparentOrigami()
    to.load_data(data) 
    to.status()

    for fold in to.folds:
        to.fold(fold[0], fold[1])

if __name__ == '__main__':
    solution_part_1(get_test_data())
    solution_part_1(get_data())

    solution_part_2(get_test_data())
    solution_part_2(get_data())
