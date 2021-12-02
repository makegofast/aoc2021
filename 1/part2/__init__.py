import sys

def read_input():
    for line in sys.stdin:
        yield line.rstrip()
    
def detect_depth_increases():
    increases = 0
    window_size = 3

    buffer = []

    for current in read_input():
        print(current)

        buffer.append(int(current))
        if len(buffer) < window_size + 1:
            continue

        buffer = buffer[-window_size-1:]

        left = buffer[:window_size]
        right = buffer[-window_size:]

        print("b %s l %s r %s" % (buffer, left, right))

        if sum(right) > sum(left):
            print("%s %s increase" % (sum(left), sum(right)))
            increases += 1
        else:
            print("%s %s not increase" % (sum(left), sum(right)))

    return increases

if __name__ == "__main__":
    print("Depth Increases: %s" % detect_depth_increases())
