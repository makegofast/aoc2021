import math

class PolymerizationExtender(object):
    def __init__(self):
        self.pairs = {} 
        self.rules = {}

    def add_pair(self, key, count=1):
        #print('add_pair', key, count)
        self.pairs.setdefault(key, 0)
        self.pairs[key] += count 

    def remove_pair(self, key, count):
        #print('remove_pair', key, count)
        self.pairs[key] -= count
        if self.pairs[key] == 0:
            del(self.pairs[key])
    
    def load_data(self, data):
        #print('load_data')
        template = data.pop(0)

        for i in range(0, len(template)-1):
            key = template[i:i+2]
            self.add_pair(key)

        data.pop(0)

        for line in data:
            pair, insert = line.split(' -> ')
            self.rules[pair] = insert

    def extend(self):
        to_extend = self.pairs.copy()

        for key, val in to_extend.items():
            #print('extend', key, val)
            ichar = self.rules[key]
            self.remove_pair(key, val)
            self.add_pair(key[0:1] + ichar, val)
            self.add_pair(ichar + key[1:2], val)

    def get_score(self):
        counts = {}

        for key, val in self.pairs.items():
            #print(key, val)

            left = key[0:1]
            right = key[1:2]

            counts.setdefault(left, 0)
            counts[left] += val

            counts.setdefault(right, 0)
            counts[right] += val

        #print(counts)

        return max([math.ceil(v/2) for k, v in counts.items()]) - min([math.ceil(v/2) for k, v in counts.items()])

    def status(self):
        print('pairs:', self.pairs)
        print('rules:', self.rules)

def get_data():
    return [l.rstrip() for l in open('data.txt', 'r').readlines()]

def get_test_data():
    return [l.rstrip() for l in open('test_data.txt', 'r').readlines()]

def solution_part_1(data):
    pe = PolymerizationExtender()
    pe.load_data(data) 
    pe.status()

    for i in range(0,10):
        pe.extend()
        print('round', i+1, pe.pairs, pe.get_score())

def solution_part_2(data):
    pe = PolymerizationExtender()
    pe.load_data(data) 
    pe.status()

    for i in range(0,40):
        pe.extend()
        print('round', i+1, pe.get_score(), 'or maybe', pe.get_score()-1)

if __name__ == '__main__':
    solution_part_1(get_test_data())
    solution_part_1(get_data())

    solution_part_2(get_test_data())
    solution_part_2(get_data())
