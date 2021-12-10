class AutoNavigation(object):
    def __init__(self):
        self.basins = []
        self.visited = {}

    def in_basin(self, row, col):
        for basin in self.basins:
            for point in basin:
                if point[0] == row and point[1] == col:
                    return True

    def mark_visited(self, row, col):
        self.visited.setdefault(row, {})
        self.visited[row][col] = True

    def is_visited(self, row, col):
        try:
            return self.visited[row][col]
        except:
            return None

    def value_at(self, row, col):
        if row < 0 or col < 0 or row > self.height or col > self.width: 
            return None

        return self.data[row][col]

    def load_data(self, data):
        self.data = []

        self.width = 0
        self.height = 0

        for line in data:
            row = [int(c) for c in line]
            self.width = max(self.width, len(row)-1)
            self.data.append(row)

        self.height = len(self.data)-1

    def detect_basins(self, algorithm):
        algo_fn = getattr(self, algorithm)

        for row in range(0, self.height+1):
            for col in range(0, self.width+1):
                algo_fn(row, col)

        print(self.status())

    def status(self):
        ret = []

        print('Status')
        for row in range(0, self.height+1):
            line = ''
            for col in range(0, self.width+1):
                val = self.value_at(row, col)
                if self.in_basin(row, col):
                    val = bcolor('red', val)
                elif val == 9:
                    val = bcolor('green', val)
                elif self.is_visited(row, col):
                    val = bcolor('blue', val)
                line += str(val)
            print(line)

    def crawl_part_1(self, row, col):
        basin = []

        self.mark_visited(row, col)

        scan_points = [
            [row-1, col],
            [row+1, col],
            [row, col-1],
            [row, col+1]
        ]

        origin_val = self.value_at(row, col)

        if origin_val == 9:
            return None

        for target in scan_points:
            target_val = self.value_at(target[0], target[1])

            if target_val == None: #Out of bounds
                continue

            if target_val < origin_val:
                return None

        self.basins.append([[row, col, origin_val]])

    def crawl_part_2(self, row, col):
        pass

    def calculate_risk_level(self, basins):
        risk = 0

        for basin in self.basins:
            for p in basin:
                risk += 1 + p[2]
    
        return risk 


def bcolor(color, text):
    colors = {
        'blue': '\033[94m',
        'red': '\033[91m',
        'green': '\033[92m',
        'reset': '\033[0m'
    }

    return colors[color] + str(text) + colors['reset'] 

def get_data():
    return [l.strip() for l in open('data.txt', 'r').readlines()]

def get_test_data():
    return [l.strip() for l in open('test_data.txt', 'r').readlines()]

def solution_part_1(data):
    an = AutoNavigation()

    an.load_data(data)
    lp = an.detect_basins('crawl_part_1')

    rl = an.calculate_risk_level(lp)
    print('Risk Level:',rl)

def solution_part_2(data):
    an = AutoNavigation()

    an.load_data(data)
    lp = an.detect_basins('crawl_part_2')

    rl = an.calculate_risk_level(lp)
    print('Risk Level:',rl)

if __name__ == '__main__':
    data = get_test_data()
    solution_part_1(data)

    data = get_data()
    solution_part_1(data)
