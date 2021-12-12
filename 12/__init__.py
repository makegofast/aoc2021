import copy

class AutoNavigation(object):
    def __init__(self):
        pass

    def load_data(self, data):
        self.connections = {}
        self.small_caves = []

        for line in data:
            src, dst = line.split('-')

            self.connections.setdefault(src, [])
            self.connections[src].append(dst)

            self.connections.setdefault(dst, [])
            self.connections[dst].append(src)

            if src.islower() and src not in self.small_caves:
                self.small_caves.append(src)

            if dst.islower() and dst not in self.small_caves:
                self.small_caves.append(dst)

    def find_next_hops(self, start):
        try:
            return self.connections[start]
        except KeyError:
            return None
    
    def find_paths(self, history, can_visit_twice):
        paths = []

        if history[-1] == 'end':
            return [history]

        try:
            next_hops = self.connections[history[-1]]
        except KeyError:
            return [history]

        for hop in next_hops: 
            if hop == 'start':
                continue

            visit_limit = 2 if hop == can_visit_twice else 1
            previous_visits = sum([1 for h in history if h==hop])

            if hop.islower() and previous_visits >= visit_limit:
                continue

            new_path = history.copy()
            new_path.append(hop)

            for branch in self.find_paths(new_path, can_visit_twice):
                paths.append(branch)

        return paths 

    def status(self):
        print(self.connections)

def get_data():
    return [l.rstrip() for l in open('data.txt', 'r').readlines()]

def get_test_data():
    return [l.rstrip() for l in open('test_data.txt', 'r').readlines()]

def solution_part_1(data):
    an = AutoNavigation()
    an.load_data(data) 

    paths = an.find_paths(['start'], can_visit_twice=False)

    successful_paths = len([1 for p in paths if p[0] == 'start' and p[-1] == 'end'])
    print("Successful paths: %s" % successful_paths)

def solution_part_2(data):
    an = AutoNavigation()
    an.load_data(data) 

    paths = []
    for small_cave in an.small_caves:
        paths += an.find_paths(['start'], small_cave)

    paths = list(set(tuple(p) for p in paths))

    successful_paths = len([1 for p in paths if p[0] == 'start' and p[-1] == 'end'])
    print("Successful paths: %s" % successful_paths)

if __name__ == '__main__':
    solution_part_1(get_test_data())
    solution_part_1(get_data())

    solution_part_2(get_test_data())
    solution_part_2(get_data())
