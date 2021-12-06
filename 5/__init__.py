class AutoPilot(object):
    def __init__(self):
        self.vent_data = []
        self.map = {}

    def load_data(self, data):
        for line in data:
            start, end = line.split(' -> ')
            x1, y1 = start.split(',')
            x2, y2 = end.split(',')
            self.vent_data.append({'x1': int(x1), 'y1': int(y1), 'x2': int(x2), 'y2': int(y2)})

        self.prime_map()

    def prime_map(self):
        for line_data in self.vent_data:
            self.apply_line(**line_data)

    def apply_line(self, x1, y1, x2, y2):
        print('Applying line %s,%s -> %s,%s' % (x1,y1,x2,y2))

        print(x1, y1, x2, y2)

        if x1 - x2 > 0:
            xdir = -1
            x2 -= 1
        else:
            xdir = 1
            x2 += 1

        if y1 - y2 > 0:
            ydir = -1
            y2 -= 1 
        else:
            ydir = 1
            y2 += 1

        print('%s...%s (%s) %s...%s (%s)' % (x1, x2, xdir, y1, y2, ydir))

        xs = list(range(x1, x2, xdir))
        ys = list(range(y1, y2, ydir))

        print(xs, ys)

        if len(xs) == 1:
            xs = xs * len(ys)

        if len(ys) == 1:
            ys = ys * len(xs)

        print(xs, ys)

        for x,y in zip(xs, ys):
            print('extrapolate %s,%s' % (x, y))
            self.map.setdefault(x, {})
            self.map[x].setdefault(y, 0)
            self.map[x][y] += 1

    def print_map(self):
        height = max(self.map)+1
        width = max((max(yd)+1 for y, yd in self.map.items()))
        max_len = 0

        lines = []
        for x in range(0, height):
            line = []
            for y in range(0, width):
                val = self.map.get(x, {}).get(y, 0)
                if len(str(val)) > max_len:
                    max_len = len(str(val))
                line.append(val)
            lines.append(line)

        for line in lines:
            print(' '.join((str(val).replace('0', '.').center(max_len) for val in line)))

    def count_hotspots(self):
        count = 0
        for x, xd in self.map.items():
            for y, yd in xd.items():
                if self.map[x][y] > 1:
                    count += 1

        return(count)

    def status(self):
        self.print_map()
        print('Hot Spots: %s' % self.count_hotspots())

if __name__ == '__main__':
    data = []
    with open('data.txt', 'r') as fp:
        for line in fp.readlines():
            data.append(line.rstrip())

    ap = AutoPilot()
    ap.load_data(data)
    ap.status()
