class TargetingSystem(object):
    def __init__(self):
        pass

    def load_data(self, data):
        self.data = data

    def aim(self):
        best = None 
        for t in range(1, len(self.data)+1):
            cost = self.calc_cost(t) 
            print('aim %s cost %s' % (t, cost)) 
            if not best or cost < best['cost']:
                best = {'target': t, 'cost': cost}

        return best

    def calc_cost(self, t):
        return sum([abs(t-p) for p in self.data])

    def status(self):
        print(self.data)

if __name__ == '__main__':
    data = [int(l) for l in open('data.txt', 'r').readline().rstrip().split(',')]

    ts = TargetingSystem()
    ts.load_data(data)
    best = ts.aim()
    print('Best target %s costs %s' % (best['target'], best['cost']))

    ts.status()
