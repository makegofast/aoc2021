import sys

class Submarine(object):
    def __init__(self):
        self.pos_horiz = 0
        self.pos_vert = 0
        self.aim = 0

    def navigate(self, direction, distance):
        func = getattr(self, '_nav_%s' % direction)
        func(distance)

    def _nav_forward(self, distance):
        self.pos_horiz += distance
        self.pos_vert += self.aim * distance

    def _nav_up(self, distance):
        self.aim -= distance

    def _nav_down(self, distance):
        self.aim += distance

    def chart(self, course):
        for command in course:
            direction, distance = command.split(' ')
            distance = int(distance)

            print(command)
            self.navigate(direction, distance)

    def location(self):
        print("Location: pos_horiz={0.pos_horiz} pos_vert={0.pos_vert}".format(self))
        return self.pos_horiz * self.pos_vert

def read_input():
    for line in sys.stdin:
        yield line.rstrip()
    
if __name__ == "__main__":
    sub = Submarine()
    course = read_input()
    sub.chart(course)
    print("Sub location: %s" % sub.location())
