class TargetingSystem(object):
    def load_data(self, data):
        self.data = [int(v) for v in data.split(',')]

    def aim(self, cost_func):
        best = None 

        for target in range(1, len(self.data)+1):
            cost = cost_func(target)
            if not best or cost < best['cost']:
                best = {'target': target, 'cost': cost}

        return best

    def calc_cost_simple(self, target):
        return sum([abs(target-start) for start in self.data])

    def calc_cost_increasing(self, target):
        costs = []
        for start  in self.data:
           delta = abs(target-start)
           costs.append(delta*(delta+1)/2) 
        return int(sum(costs))

def get_data():
    return open('data.txt', 'r').readline().rstrip()

def get_test_data():
    return open('test_data.txt', 'r').readline().rstrip()

def run_tests():
    results = []

    results.append(solution(get_test_data(), 'simple') == 37)
    results.append(solution(get_test_data(), 'increasing') == 168)
    results.append(solution(get_data(), 'simple') == 348996)
    results.append(solution(get_data(), 'increasing') == 98231647)

    passed = sum(results)
    failed = len(results) - passed 

    print('Test: %s passed, %s failed' % (passed, failed))

    if failed:
        raise Exception('%s tests failed' % failed)

def solution(data, cost_type):
    ts = TargetingSystem()
    ts.load_data(data)

    cost_func = getattr(ts, 'calc_cost_%s' % cost_type)
    best = ts.aim(cost_func)
    print('%s best target %s costs %s' % (cost_type, best['target'], best['cost']))

    return best['cost']

if __name__ == '__main__':
    run_tests()

    solution(get_data(), 'simple') 
    solution(get_data(), 'increasing') 
