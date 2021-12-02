import sys

def read_input():
    for line in sys.stdin:
        yield line.rstrip()
    
def detect_depth_increases():
    increases = 0
    previous = None

    for current in read_input():
        current = int(current)
        if previous and current > previous:
            print("%s increase" % current)
            increases += 1
        else:
            print("%s not increase" % current)

        previous = current

    return increases

if __name__ == "__main__":
    print("Depth Increases: %s" % detect_depth_increases())
