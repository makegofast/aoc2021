import math

class CorruptedLine(object):
    def __init__(self, score):
        self.score = score

    def __int__(self):
        return int(self.score)

class IncompleteLine(object):
    def __init__(self, repair_total):
        self.repair_total = repair_total

    def __int__(self):
        return int(self.repair_total)

class SyntaxParser(object):
    def __init__(self):
        self.cmap = {
            '(': ')',
            '[': ']',
            '{': '}',
            '<': '>'
        }

        self.corrupted_values = {
            ')': 3,
            ']': 57,
            '}': 1197,
            '>': 25137
        }

        self.repair_values = {
            ')': 1,
            ']': 2,
            '}': 3,
            '>': 4
        }

    def load_data(self, data):
        self.data = data

    def parse_lines(self):
        corrupted_total = 0
        incomplete_lines = []

        for line in self.data:
            pl = self.parse_line(line)
            if isinstance(pl, CorruptedLine):
                corrupted_total += int(pl)
            elif isinstance(pl, IncompleteLine):
                incomplete_lines.append(int(pl))
            else:
                print("This is fine")

        print("Corrupted Score:",corrupted_total)

        incomplete_lines.sort()
        i = math.floor(len(incomplete_lines)/2)
        print("Repair Score:",incomplete_lines[i])

    def parse_line(self, line):
        stack = [] 

        for c in line:
            if c in self.cmap.keys():
                stack.append({ 'open': c, 'close': self.cmap[c], })
            else:
                expected = stack[-1]['close']
                if c != expected:
                    return CorruptedLine(self.corrupted_values[c])
                else:
                    stack.pop(-1)

        repair_total = 0

        if not stack:
            return

        while len(stack):
            i = stack.pop(-1)
            repair_total = repair_total * 5 + self.repair_values[i['close']]

        return IncompleteLine(repair_total)

def solution(data):
    sp = SyntaxParser()
    sp.load_data(data)
    sp.parse_lines()

def get_data():
    return [l.rstrip() for l in open('data.txt', 'r').readlines()]

def get_test_data():
    return [l.rstrip() for l in open('test_data.txt', 'r').readlines()]

if __name__ == '__main__':
    solution(get_test_data())
    solution(get_data())
