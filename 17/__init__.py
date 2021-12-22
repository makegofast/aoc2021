import sys
sys.path.append('..')

import re
import lib.text

class ProbeTargetingSystem(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.x_pos = 0
        self.y_pos = 0
        self.x_vel_init = self.x_vel = 0
        self.y_vel_init = self.y_vel = 0
        self.track = []
        self.hit = self.miss = self.warpshot = self.overshot = self.undershot = None
        self.add_track_point(self.x_pos, self.y_pos)

    def add_track_point(self, x, y):
        self.track.append([x, y])

    def is_track_point(self, x, y):
        return any([True for p in self.track if p[0] == x and p[1] == y])

    def highest_track(self):
        return max([p[1] for p in self.track])

    def in_target(self, x, y):
        x_check = self.target['x1'] <= x <= self.target['x2']
        y_check = self.target['y1'] <= y <= self.target['y2']

        return True if x_check and y_check else False

    def detect_hit(self):
        for point in self.track:
            if self.in_target(point[0], point[1]):
                return point

    def fire(self, x_vel, y_vel):
        self.reset()

        self.x_vel = self.x_vel_init = x_vel
        self.y_vel = self.y_vel_init = y_vel

        while not self.hit and not self.miss: #self.x_pos < self.target['x2'] and self.y_pos > self.target['y2']:
            self.step()

        if self.hit:
            return self.detect_hit()

    def load_data(self, data):
        p = re.compile(r'target area: x=(?P<x1>[0-9-]+)..(?P<x2>[0-9-]+), y=(?P<y1>[0-9-]+)..(?P<y2>[0-9-]+)')
        m = p.match(data[0])

        self.target = {k: int(v) for k, v in m.groupdict().items()}

    def step(self):
        self.x_pos += self.x_vel
        self.y_pos += self.y_vel

        self.add_track_point(self.x_pos, self.y_pos)

        if self.in_target(self.x_pos, self.y_pos):
            self.hit = True
            self.miss = self.warpshot = self.overshot = self.undershot = False

        elif self.y_pos < self.target['y1']:
            self.hit = False
            self.miss = True
            if self.x_pos < self.target['x1']:
                self.undershot = True
            elif self.x_pos > self.target['x2']:
                self.overshot = True
            else:
                self.warpshot = True

        if self.x_vel != 0:
            self.x_vel += -1 if self.x_vel > 0 else 1

        self.y_vel -= 1

    def status(self):
        print("Initial:", self.x_vel_init, self.y_vel_init)
        print("Hit=%s Miss=%s Warpshot=%s Undershot=%s Overshot=%s:" % (self.hit, self.miss, self.warpshot, self.undershot, self.overshot))
        print(self.track)

        left = 0
        right = max(self.target['x2'], self.x_pos) 

        top = max(self.highest_track(), self.target['y2'], self.y_pos)
        bottom = min(self.target['y1'], self.y_pos)

        for y in range(top, bottom-1, -1):
            line = ''
            for x in range(left, right+1):
                if x == 0 and y == 0:
                    char = lib.text.bcolor('green', 'S')
                elif self.is_track_point(x, y) and self.in_target(x, y):
                    char = lib.text.bcolor('bred', 'X')
                    char = lib.text.bcolor('redbg', char)
                elif self.is_track_point(x, y):
                    char = lib.text.bcolor('bred', '#')
                elif self.in_target(x, y):
                    char = lib.text.bcolor('yellow', 'T')
                else:
                    char = '.'

                line += char
            print(line)

        hit = self.detect_hit()
        if hit:
            print('Hit:', hit)
        else:
            print('Miss :(')

        print("Overshot", self.overshot)
        print('Highest X:', self.highest_track())
        print()


def find_all_hits(pts):
    hits = []

    for x_vel in range(0, 1000):
        for y_vel in range(-1000, 1000):
            hit = pts.fire(x_vel, y_vel)

            if hit:
                hits.append([x_vel, y_vel]) 
            elif pts.overshot:
                break

    return hits

def find_coolest_shot(pts):
    x_vel = 1 
    y_vel = 1

    hits = []
    highest = 0

    for i in range(0, 1000):
        hit = pts.fire(x_vel, y_vel)

        this_xv = x_vel
        this_yv = y_vel

        if hit:
            highest = max(highest, pts.highest_track())
            hits.append([hit, pts.highest_track()])

            y_vel += 1
        else:
            overshot = pts.overshot
            if overshot: 
                y_vel += 1
                x_vel -= 1
            else:
                x_vel += 1

        print(i, 'HIT' if hit else 'MISS', highest, 'xv', this_xv, 'yv', this_yv, hit, 'over shot' if overshot else '')

    print("Highest Hit:", highest)

def get_data():
    return [l.rstrip() for l in open('data.txt', 'r').readlines()]

def get_test_data():
    return [l.rstrip() for l in open('test_data.txt', 'r').readlines()]

def solution_part_1(data):
    pts = ProbeTargetingSystem()
    pts.load_data(data) 
    find_coolest_shot(pts)

def test_part_1(data):
    pts = ProbeTargetingSystem()
    pts.load_data(data) 

    pts.fire(7, 2)
    pts.fire(6, 3)
    pts.fire(9, 0)
    pts.fire(17, -4)
    pts.fire(10, 0)
    pts.fire(0, 10)

def solution_part_2(data):
    pts = ProbeTargetingSystem()
    pts.load_data(data) 
    hits = find_all_hits(pts)
    print(hits)
    print('Hits:', len(hits))

if __name__ == '__main__':
    #test_part_1(get_test_data())

    #solution_part_1(get_test_data())
    #solution_part_1(get_data())

    #solution_part_2(get_test_data())
    solution_part_2(get_data())
