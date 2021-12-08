def get_data():
    return [l.rstrip() for l in open('data.txt', 'r').readlines()]

def get_test_data():
    return [l.rstrip() for l in open('test_data.txt', 'r').readlines()]

def union(a, b):
    return set([c for c in a + b if c in a and c in b])

def decode(signals):
    nmap = {}
    unknown = {}

    for signal in signals:
        unknown.setdefault(len(signal), [])
        letters = [c for c in signal]
        letters.sort()
        unknown[len(signal)].append(''.join(letters))

    nmap[1] = unknown[2][0]
    nmap[4] = unknown[4][0]
    nmap[7] = unknown[3][0]
    nmap[8] = unknown[7][0]

    for m in unknown[5]:
        if len(union(nmap[1], m)) == 2:
            nmap[3] = m
        elif len(union(nmap[4], m)) == 3:
            nmap[5] = m
        else:
            nmap[2] = m

    for m in unknown[6]:
        if set([c for c in nmap[3] + nmap[4]]) == set(m):
            nmap[9] = m
        elif len(union(nmap[5], m)) == 5:
            nmap[6] = m
        else:
            nmap[0] = m

    return {k: v for v, k in nmap.items()}
    
def solution(data):
    total = 0
    for line in data:
        signal_chunk, value_chunk = line.split(' | ')
        signals = signal_chunk.split()

        xlate = decode(signals)

        value = "" 

        tokens = value_chunk.split()
        for token in tokens:
            letters = [c for c in token]
            letters.sort()
            token = ''.join(letters)
           
            value += str(xlate[token])

        total += int(value)
        
    print("Total: %s" % total)
    return total

if __name__ == '__main__':
    solution(get_test_data()) 
    solution(get_data()) 
