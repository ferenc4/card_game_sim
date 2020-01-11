from cards.deck import Deck


class TexasHoldem:
    def __init__(self, player_count: int, seed=None, starter_chips=100000, chip_to_blind_ratio=50):
        self.players = [None] * player_count
        self.shared = [None] * 5
        self.deck = Deck(seed)
        self.pot_size = 0
        self.player_chips = [starter_chips]
        self.chip_to_blind_ratio = chip_to_blind_ratio

    def deal_hands(self):
        for i in range(0, self.players.__len__()):
            self.players[i] = [self.deck.draw(), self.deck.draw()]

    def reveal(self, index):
        self.shared[index] = self.deck.draw()

    def flop(self):
        for i in range(0, 3):
            self.reveal(i)

    def turn(self):
        self.reveal(3)

    def river(self):
        self.reveal(4)

    def betting(self, betting: BettingRound):
        self.pot += betting.get_pot()

    def status(self):
        for i in range(0, self.players.__len__()):
            current_player = self.players[i]
            print("Player {}: {:>4} {:>4}".format(i + 1, str(current_player[0]), str(current_player[1])))
        print("Board: ", end="")
        for i in range(0, self.shared.__len__()):
            current_shared: str = str(self.shared[i])
            print("{:5}".format(current_shared), end="")
