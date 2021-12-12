import copy

class AutoNavigation(object):
    def __init__(self):
        pass

    def load_data(self, data):
        self.connections = {}
        for line in data:
            src, dst = line.split('-')
            self.connections.setdefault(src, [])
            self.connections[src].append(dst)

            self.connections.setdefault(dst, [])
            self.connections[dst].append(src)

    def find_next_hops(self, start):
        try:
            return self.connections[start]
        except KeyError:
            return None
    
    def find_paths(self, history):
        paths = []

        if history[-1] == 'end':
            return [history]

        try:
            next_hops = self.connections[history[-1]]
        except KeyError:
            return [history]

        for hop in next_hops: 
            if hop.islower() and hop in history:
                print("can't traverse %s twice (history=%s)" % (hop, history))
                continue

            new_path = history.copy()
            new_path.append(hop)

            for branch in self.find_paths(new_path):
                paths.append(branch)

        return paths 

    def status(self):
        print(self.connections)

def get_data():
    return [l.rstrip() for l in open('data.txt', 'r').readlines()]

def get_test_data():
    return [l.rstrip() for l in open('test_data.txt', 'r').readlines()]

def solution(data):
    an = AutoNavigation()
    an.load_data(data) 
    an.status()

    paths = an.find_paths(['start'])
    print('found paths', paths)

    successful_paths = len([1 for p in paths if p[0] == 'start' and p[-1] == 'end'])
    print("Successful paths: %s" % successful_paths)

if __name__ == '__main__':
    solution(get_test_data())
    solution(get_data())
