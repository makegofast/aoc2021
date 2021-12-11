class OctopusDetector(object):
    def __init__(self):
        self.flashes = 0
        self.data = []
        self.reset_flash()

    def load_data(self, data):
        for line in data:
            self.data.append([int(c) for c in line])

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

    def step(self):
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

        self.status()

    def status(self):
        for row in self.data:
            line = ''
            for col in row:
                line += str(col)
            print(line)
        print()

def solution(data, steps):
    od = OctopusDetector()
    od.load_data(data)
    od.status()

    for i in range(0,steps):
        print('step',i+1)
        od.step()

    print(od.flashes)

def get_data():
    return [l.rstrip() for l in open('data.txt', 'r').readlines()]

def get_test_data():
    return [l.rstrip() for l in open('test_data.txt', 'r').readlines()]

if __name__ == '__main__':
    data = get_test_data()
    solution(data, 100)

    data = get_data()
    solution(data, 100)
