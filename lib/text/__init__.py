def bcolor(color, text):
    colors = {
        'bred': '\033[31;1m',
        'redbg': '\033[41m',
        'red': '\033[91m',
        'green': '\033[92m',
        'greenbg': '\033[42m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'bluebg': '\033[44m',
        'reset': '\033[0m'
    }

    return colors[color] + str(text) + colors['reset']
