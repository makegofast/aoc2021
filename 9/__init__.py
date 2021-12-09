class AutoNavigation(object):
    def __init__(self):
        pass

    def load_data(self, data):
        self.data = []
        self.low_points = {} 

        for line in data:
            self.data.append([c for c in line])

    def detect_low_points(self):
        low_points = {} 

        for row in range(0, len(self.data)):
            for col in range(0, len(self.data[row])):
                val = self.data[row][col]
                lower = self.check_neighbors(row, col)
                if lower == 0:
                    print('low point %s %s' % (row, col))
                    low_points.setdefault(row, {})
                    low_points[row][col] = val 

        self.low_points = low_points
        return low_points

    def check_neighbors(self, row, col):
        lower = 0 
        same = 0
        checked = 0
        me = self.data[row][col]
        neighbors = [[row,col-1], [row, col+1], [row-1,col], [row+1, col]]
        for neighbor in neighbors:
            nr, nc = tuple(neighbor)
            print("checking %s,%s's neighbor %s,%s" % (row, col, nr, nc))

            if nr < 0 or nc < 0 or nr > len(self.data)-1 or nc > len(self.data[row])-1:
                print('%s,%s is out of bounds' % (nr, nc))
                continue

            checked += 1 

            nval = self.data[nr][nc]

            if nval == me:
                same += 1
            elif nval < me:
                lower += 1

        if same == checked:
            print('all the same')
            return checked
        else:
            return lower

    def calculate_risk_level(self, low_points):
        count = 0
        for i, row in low_points.items():
            count += sum(int(v)+1 for k,v in row.items())
    
        return count

    def status(self):
        ret = []
        for row in range(0, len(self.data)):
            line = []
            for col in range(0, len(self.data[row])):
                val = self.data[row][col]
                is_low = self.low_points.get(row, {}).get(col, 0)
                if is_low:
                    val = '(%s)' % val
                line.append(val.center(3))
            ret.append(' '.join(line))

        print('\n'.join(ret))
        return ret

def get_data():
    return [l.strip() for l in open('data.txt', 'r').readlines()]

def get_test_data():
    return [l.strip() for l in open('test_data.txt', 'r').readlines()]

def solution(data):
    an = AutoNavigation()
    an.load_data(data)
    lp = an.detect_low_points()
    print(lp)
    an.status()
    rl = an.calculate_risk_level(lp)
    print(rl)

if __name__ == '__main__':
    data = get_test_data()
    solution(data)

    data = get_data()
    solution(data)
