import sys
import pprint

class PowerConsumptionRate(object):
    def __init__(self):
        self.bit_counter = {} 

    def add_data(self, data):
        for i,b in enumerate(data):
            self.bit_counter.setdefault(i, {})
            self.bit_counter[i].setdefault(b, 0)
            self.bit_counter[i][b] += 1

    def get_most_common(self):
        ret = []
        for i, b in self.bit_counter.items():
            ret.append(max(b, key=b.get))

        return int(''.join(ret),2)

    def get_least_common(self):
        ret = []
        for i, b in self.bit_counter.items():
            ret.append(min(b, key=b.get))

        return int(''.join(ret),2)
            
    def report(self):
        pprint.pprint(self.bit_counter)

class PowerConsumption(object):
    def __init__(self):
        self.gamma_rate = PowerConsumptionRate()
        self.epsilon_rate = PowerConsumptionRate()

    def process_report(self, diag_report):
        for data in diag_report:
            self.gamma_rate.add_data(data)
            self.epsilon_rate.add_data(data)

    def status(self):
        gr = self.gamma_rate.get_most_common()
        er = self.epsilon_rate.get_least_common()
        print("gr %s * er %s = %s" % (gr, er, gr*er))

def read_input():
    for line in sys.stdin:
        yield line.rstrip()
    
if __name__ == "__main__":
    diag_report = read_input()

    pc = PowerConsumption()
    pc.process_report(diag_report)
    pc.status()
