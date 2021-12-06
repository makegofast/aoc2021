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
            if line_data['x1'] != line_data['x2'] and line_data['y1'] != line_data['y2']:
                print('%s not a straight line, ignoring' % line_data)
            else:
                self.apply_line(**line_data)

    def apply_line(self, x1, y1, x2, y2):
        print('Applying line %s,%s -> %s,%s' % (x1,y1,x2,y2))

        xs = [x1,x2]
        xs.sort()

        ys = [y1,y2]
        ys.sort()

        x1, x2 = xs
        y1, y2 = ys

        for x in range(x1, x2+1):
            for y in range(y1, y2+1):
                print('extrapolate %s,%s' % (x, y))
                self.map.setdefault(x, {})
                self.map[x].setdefault(y, 0)
                self.map[x][y] += 1

    def print_map(self):
        for x, xd in self.map.items():
            for y, yd in xd.items():
                print(x, y, self.map[x][y])

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
