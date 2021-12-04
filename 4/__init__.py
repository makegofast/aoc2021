class BingoHall(object):
    class MotherFuckingWinner(Exception):
        pass

    def __init__(self):
        self.cards = []

    def add_card(self, card):
        card.name = 'Card %s' % (len(self.cards)+1)
        self.cards.append(card)

    def remove_card(self, target_card):
        self.cards.remove(target_card)

    def get_cards(self):
        return self.cards

    def print_cards(self):
        for card in self.get_cards():
            print(card)
            print()

    def call_numbers(self):
        print('Calling numbers %s' % self.ball_order)
        for number in self.ball_order:
            self.call_number(number)
            #self.print_cards()

            while True:
                winner = self.check_for_winner()
                if winner:
                    print("Winner winner chicken dinner!")
                    print(winner)
                    print('Score: %s' % winner.calc_score(number))
                    self.remove_card(winner)
                else:
                    break

    def call_number(self, number):
        print('Calling number %s' % number)
        for card in self.get_cards():
            card.mark_called_number(number)

    def check_for_winner(self):
        for card in self.get_cards():
            if card.is_winner():
                return card

    def set_ball_order(self, numbers):
        self.ball_order = list(int(n) for n in numbers)

    def load_data(self, filename):
        with open(filename, 'r') as fp:
            self.set_ball_order(fp.readline().split(','))

            buffer = []
            for line in fp.readlines():
                line = line.rstrip()

                if line == "":
                    if len(buffer):
                        card = self.add_card(BingoCard(buffer))
                        buffer = []
                else:
                    buffer.append(line)
             
            if len(buffer):
                self.add_card(BingoCard(buffer))
                buffer = []

    def play(self):
        self.call_numbers()
        self.print_cards()
                
class BingoCardNumber(object):
    def __init__(self, number):
        self.number = int(number)
        self.marked = False

    def __str__(self):
        ret = str(self.number).rjust(2)
        if self.marked:
            ret = "(%s)" % ret

        return ret

    def mark_if_match(self, number):
        if self.number == number:
            self.marked = True

    def is_marked(self):
        return self.marked

class BingoCard(object):
    def __init__(self, data):
        self.name = 'No Name'
        self.data = []

        for line in data:
            numbers = list(BingoCardNumber(n) for n in line.split())
            self.data.append(numbers)

    def __str__(self):
        ret = [self.name]
        for row in self.data:
            ret.append(''.join(str(n).center(6) for n in row))

        return '\n'.join(ret)

    def calc_score(self, number):
        return sum((n.number for n in self.get_unmarked())) * number

    def get_unmarked(self):
        ret = []
        for row in self.data:
            for n in row:
                if not n.is_marked():
                    ret.append(n)

        return ret

    def mark_called_number(self, called_number):
        for row in self.data:
            for card_number in row:
                card_number.mark_if_match(called_number)

    def is_winner(self):
        for row in self.data:
            if sum((n.is_marked() for n in row)) == len(row):
                return True

        for col in zip(*self.data): 
            if sum((n.is_marked() for n in col)) == len(col):
                return True

if __name__ == "__main__":
    bh = BingoHall()
    bh.load_data('data.txt')

    try:
        bh.play()
    except bh.MotherFuckingWinner:
        pass

