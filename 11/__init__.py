class OctopusDetector(object):
    def __init__(self):
        self.flashes = 0
        self.data = []
        self.reset_flash()
        self.sync_flashes = []

    def load_data(self, data):
        for line in data:
            self.data.append([int(c) for c in line])

    def get_first_sync_flash(self):
        try:
            return self.sync_flashes[0]
        except IndexError:
            return None

    def reset_flash(self):
        self.flashed = {}

    def has_flashed(self, row, col):
        try:
            return self.flashed[row][col]
        except:
            return False

    def increment(self, row, col):
        if row < 0 or col < 0:
            return None

        try:
            self.data[row][col] += 1
            return self.data[row][col]
        except:
            return None

    def flash(self, row, col):
        self.flashed.setdefault(row, {})
        self.flashed[row].setdefault(col, False)

        if self.has_flashed(row, col):
            return

        self.flashed[row][col] = True

        self.flashes += 1

        neighbors = [
            [row, col-1],
            [row, col+1],
            [row-1, col],
            [row+1, col],
            [row+1, col+1],
            [row-1, col-1],
            [row-1, col+1],
            [row+1, col-1]
        ]

        for r,c in neighbors:
            n = self.increment(r,c)
            if n and n > 9:
                self.flash(r, c)

    def step(self, step):
        self.reset_flash()

        for row in range(0, len(self.data)):
            for col in range(0, len(self.data)):
                self.data[row][col] += 1

        for row in range(0, len(self.data)):
            for col in range(0, len(self.data)):
                if self.data[row][col] > 9:
                    self.flash(row, col)

        for row in range(0, len(self.data)):
            for col in range(0, len(self.data)):
                if self.has_flashed(row, col):
                    self.data[row][col] = 0

        if sum(sum(v) for v in self.data) == 0:
            self.sync_flashes.append(step)
            print("FLASH")

        self.status(step)

    def status(self, step=None):
        if not step == None:
            print("Step",step)

        for row in self.data:
            line = ''
            for col in row:
                line += str(col)
            print(line)
        print()

def solution_part_1(data):
    od = OctopusDetector()
    od.load_data(data)
    od.status()

    for i in range(0,100):
        od.step(i+1)

    print('Number of flashes:', od.flashes)

    return od.flashes

def solution_part_2(data):
    od = OctopusDetector()
    od.load_data(data)
    od.status()

    step = 1 
    while not od.get_first_sync_flash():
        od.step(step)
        step += 1

    print('First sync flash:', od.get_first_sync_flash()),

    return od.get_first_sync_flash()

def get_data():
    return [l.rstrip() for l in open('data.txt', 'r').readlines()]

def get_test_data():
    return [l.rstrip() for l in open('test_data.txt', 'r').readlines()]

if __name__ == '__main__':
    data = get_test_data()
    solution_part_1(data)

    data = get_data()
    solution_part_1(data)

    data = get_test_data()
    solution_part_2(data)

    data = get_data()
    solution_part_2(data)
