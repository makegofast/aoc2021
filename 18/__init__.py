import math
import json

class SnailNumber(object):
    class Rereduce(ValueError):
        pass

    def __init__(self, snum=None):
        #print('new SnailNumber(%s)' % snum)
        self.bitz = self.slice(snum) if snum else []
        
    def __radd__(self, other):
        if not other:
            return self

        return self + other

    def __add__(self, other):
        if not other:
            return self

        #print("Adding %s to %s" % (str(self), str(other)))
        new = SnailNumber(''.join([str(c) for c in ['['] + self.bitz + [','] + other.bitz + [']']]))

        #print("reducing new %s" % str(new))
        new.reduce()

        #print("  %s" % self)
        #print("+ %s" % other)
        #print("= %s" % new)
        #print()

        #print("reduced new: %s" % str(new))
        return new 

    def __str__(self):
        return ''.join([str(c) for c in self.bitz])

    def reduce(self):
        ret = self.bitz.copy()

        while True:
            #print('reducing %s' % ''.join([str(c) for c in ret]))

            try:
                depth = 0 

                for stage in ['explode', 'split']:
                    for i, c in enumerate(ret):
                        if c == "[":
                            depth += 1
                        elif c == "]":
                            depth -= 1

                        if stage == 'explode' and depth > 4 and isinstance(c, int):
                            #print("depth is >= 4 at %s" % i)
                            a = ret[i]
                            b = ret[i+2]
                            left = ret[:i-1]
                            right = ret[i+4:]

                            left = self.add_left(a, left)
                            right = self.add_right(b, right)

                            ret = left + [0] + right

                            raise self.Rereduce

                        if stage == 'split' and isinstance(c, int) and c >= 10:
                            #print("%s is >= 10 at %s" % (c, i))
                            a = math.floor(c / 2)
                            b = math.ceil(c / 2)
                            #print("before split: %s" % ret)
                            ret = ret[:i] + ['[', a, ',', b, ']'] + ret[i+1:]
                            #print(" after split: %s" % ret)
                            raise self.Rereduce

                self.bitz = ret
                return self.bitz 
            except self.Rereduce:
                continue
    
    def magnitude(self, num=None):
        ret = 0

        if num == None:
            num = json.loads(str(self))

        if isinstance(num, int):
            return num
        elif isinstance(num, list):
            ret += 3*self.magnitude(num[0]) + 2*self.magnitude(num[1])

        return ret

    @staticmethod
    def add_left(num, lst):
        for i in range(len(lst)-1, 0, -1):
            if isinstance(lst[i], int):
                #print("Left add %s to %s at pos %s" % (num, lst[i], i))
                lst[i] += num
                return lst 

        #print("Failed to left add %s to %s" % (num, lst))
        return lst

    @staticmethod
    def add_right(num, lst):
        for i in range(0, len(lst)):
            if isinstance(lst[i], int):
                #print("Right add %s to %s at pos %s" % (num, lst[i], i))
                lst[i] += num
                return lst 

        #print("Failed to right add %s to %s" % (num, lst))
        return lst

    @staticmethod
    def slice(snum):
        ret = []
        buf = ''
        for c in snum:
            if c in '[],':
                if buf:
                    ret.append(int(buf) if buf.isnumeric else buf)
                ret.append(c)
                buf = ''
            else:
                buf += c
        return ret

def get_data():
    return [l.rstrip() for l in open('data.txt', 'r').readlines()]

def get_test_data():
    return [l.rstrip() for l in open('test_data.txt', 'r').readlines()]

def solution_part_1(data):
    snums = []
    for snum in data:
        snums.append(SnailNumber(snum))

    sn = sum(snums)
    print('SnailNumber',sn, 'magnitude',sn.magnitude())

def solution_part_2(data):
    ll = []
    rl = []

    max_magnitude = 0

    for snum in data:
        sn = SnailNumber(snum)
        ll.append(sn)
        rl.insert(0, sn)

    for l in ll:
        for r in rl:
            if l == r:
                continue
            magnitude = (l+r).magnitude()
            #print(l, '+', r, '=', magnitude) 
            max_magnitude = max(max_magnitude, magnitude)

    print("Max magnitude", max_magnitude)

if __name__ == '__main__':
    solution_part_1(get_test_data())
    solution_part_1(get_data())

    solution_part_2(get_test_data())
    solution_part_2(get_data())
