class Fish(object):
    def __init__(self, timer):
        self.timer = timer

    def __str__(self):
        return '%s' % self.timer

    def goodnight(self):
        self.timer -= 1
        if self.timer < 0:
            self.timer = 6
            return Fish(8)

class Aquarium(object):
    def __init__(self, fish_timers):
        self.day = 0
        self.fish = []

        for timer in fish_timers:
            self.fish.append(Fish(int(timer)))

    def end_day(self):
        print('Ending day %s' % self.day)
        fry = []
        for fish in self.fish:
            spawn = fish.goodnight()
            if spawn:
                fry.append(spawn)

        self.day += 1

        print('New fry: %s' % len(fry))

        self.fish.extend(fry)

    def status(self):
        print(' '.join((str(f) for f in self.fish))) 
        print('Day %s fish count: %s' % (self.day, len(self.fish)))
        print('-------------')

if __name__ == '__main__':
    fp = open('data.txt')
    data = fp.readline().rstrip().split(',')
    aq = Aquarium(data)
    #aq.status()

    for day in range(0,256):
        aq.end_day()
        #aq.status()
