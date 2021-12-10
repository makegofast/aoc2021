class AutoNavigation(object):
    def __init__(self):
        pass

    def load_data(self, data):
        self.data = []

        self.width = 0
        self.height = 0

        for line in data:
            row = [int(c) for c in line]
            self.width = max(self.width, len(row)-1)
            self.data.append(row)

        self.height = len(self.data)-1

    def value_at(self, row, col):
        if row < 0 or col < 0 or row > self.height or col > self.width: 
            return None

        return self.data[row][col]

    def detect_basins(self):
        basins = []

        for row in range(0, self.height+1):
            for col in range(0, self.width+1):
                basin, visited = self.crawl(row, col)
                if basin:
                    basins.append(basin)

        print(self.status(basins))
        return basins

    def crawl(self, row, col):
        visited = {}
        basin = []

        visited.setdefault(row, {})
        visited[row].setdefault(col, False)

        visited[row][col] = True

        my_val = self.value_at(row, col)

        if my_val == 9:
            return None, visited

        scan_points = [
            [row-1, col],
            [row+1, col],
            [row, col-1],
            [row, col+1]
        ]

        for point in scan_points:
            point_val = self.value_at(point[0], point[1])
            if point_val == None: #Out of bounds
                continue

            if point_val < my_val:
                return None, visited

        basin.append([row,col,my_val])

        return basin, visited

    def calculate_risk_level(self, basins):
        risk = 0

        for basin in basins:
            for p in basin:
                risk += 1 + p[2]
    
        return risk 

    def in_basin(self, basins, row, col):
        for basin in basins:
            for p in basin:
                if p[0] == row and p[1] == col:
                    return True

    def status(self, basins=[], visited={}):
        ret = []

        print('Status')
        for row in range(0, self.height):
            line = '' 

            for col in range(0, self.width):
                val = self.value_at(row, col)
                if self.in_basin(basins, row, col):
                    val = bcolor('red', val)
                elif visited.get(row, {}).get(col, False):
                    val = bcolor('blue', val)
                line += str(val)

            ret.append(line)

        ret.append('')
        return '\n'.join(ret)

def bcolor(color, text):
    colors = {
        'blue': '\033[94m',
        'red': '\033[91m',
        'reset': '\033[0m'
    }

    return colors[color] + str(text) + colors['reset'] 

def get_data():
    return [l.strip() for l in open('data.txt', 'r').readlines()]

def get_test_data():
    return [l.strip() for l in open('test_data.txt', 'r').readlines()]

def solution(data):
    an = AutoNavigation()

    an.load_data(data)
    lp = an.detect_basins()

    rl = an.calculate_risk_level(lp)
    print('Risk Level:',rl)

if __name__ == '__main__':
    data = get_test_data()
    solution(data)

    data = get_data()
    solution(data)
