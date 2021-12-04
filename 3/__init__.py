import sys
import pprint
import resource

class DiagnosticModule(object):
    def __init__(self):
        self.report_data = []

    def load_report_data(self, diag_report):
        self.report_data = list(diag_report)

    def filter_data(self, data, value, position):
        ret = []
        for datum in data:
            if datum[position] == str(value):
                ret.append(datum) 

        return ret

    def get_bit_width(self, data):
        return max((len(d) for d in data))

    def get_most_common(self, data, position):
        freq = self.get_bit_freq(data, position)
        ret = 0 if freq[0] > freq[1] else 1
        return ret

    def get_least_common(self, data, position):
        freq = self.get_bit_freq(data, position)
        ret = 1 if freq[1] < freq[0] else 0
        return ret
        
    def get_bit_freq(self, data, position):
        freq = {
            0: len(list(self.filter_data(data, 0, position))),
            1: len(list(self.filter_data(data, 1, position)))
        }
        return freq

    def get_power_gamma(self):
        gamma = []
            
        while len(gamma) < self.get_bit_width(self.report_data):
            freq = self.get_bit_freq(self.report_data, len(gamma))
            bit = max(freq, key=freq.get)
            gamma.append(str(bit))

        return int(''.join(gamma), 2)

    def get_power_epsilon(self):
        epsilon = []

        while len(epsilon) < self.get_bit_width(self.report_data):
            freq = self.get_bit_freq(self.report_data, len(epsilon))
            epsilon.append(str(min(freq, key=freq.get)))

        return int(''.join(epsilon), 2)

    def get_power_consumption(self):
        return self.get_power_gamma() * self.get_power_epsilon()

    def get_oxygen_generator_rating(self):
        data = self.report_data

        pos = 0
        while len(data) > 1:
            criteria = self.get_most_common(data, pos)
            data = self.filter_data(data, criteria, pos)
            pos += 1

        return int(data[0],2) 

    def get_co2_scrubber_rating(self):
        data = self.report_data

        pos = 0 
        while len(data) > 1:
            criteria = self.get_least_common(data, pos)
            data = self.filter_data(data, criteria, pos)
            pos += 1

        return int(data[0],2) 

    def get_life_support_rating(self):
        return self.get_oxygen_generator_rating() * self.get_co2_scrubber_rating()

    def status(self):
        pc = self.get_power_consumption()
        print("Power Consumption = %s" % pc)

        lsr = self.get_life_support_rating()
        print("Life Support Rating = %s" % lsr)

def read_input():
    for line in sys.stdin:
        yield line.rstrip()

def print_mem_usage():
    usage = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) / 1024 / 1024
    print("Memory usage: %s MB" % usage) 
    
if __name__ == "__main__":
    diag_report = read_input()

    dm = DiagnosticModule()
    dm.load_report_data(diag_report)
    dm.status()

    print_mem_usage();
