class SomeClass(object):
    def __init__(self):
        pass

    def load_data(self, data):
        for line in data:
            pass

    def status(self):
        pass

def get_data():
    return [l.rstrip() for l in open('data.txt', 'r').readlines()]

def get_test_data():
    return [l.rstrip() for l in open('test_data.txt', 'r').readlines()]

def solution_part_1(data):
    sc = SomeClass()
    sc.load_data(data) 
    sc.status()

def solution_part_2(data):
    pass

if __name__ == '__main__':
    solution_part_1(get_test_data())
    #solution_part_1(get_data())

    #solution_part_2(get_test_data())
    #solution_part_2(get_data())
