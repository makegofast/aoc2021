class Aquarium(object):
    def __init__(self):
        self.day = 0
        self.fish = [0] * 9

    def stock(self, fish):
        for f in fish:
            self.fish[int(f)] += 1

    def status(self):
        print("Day %s: %s = %s" % (self.day, self.fish, sum(self.fish)))

    def end_day(self):
        self.day += 1
        spawning = self.fish[0]
        self.fish.append(spawning)
        self.fish.pop(0)
        self.fish[6] += spawning
        self.status()

if __name__ == '__main__':
    fp = open('data.txt')
    data = fp.readline().rstrip().split(',')

    aq = Aquarium()
    aq.stock(data)

    for day in range(0,256):
        aq.end_day()
