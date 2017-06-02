from random import randint

class RandomBot:
    def __init__(self):
        self.myid = 1
        self.oppid = 2
    def get_move(self, pos, tleft):
        lmoves = pos.legal_moves()
        #rm = randint(0, len(lmoves)-1)
        #return lmoves[rm]
        return max(lmoves, key=lambda x: self.static_evaluation(pos, x))
    def static_evaluation(self, pos, move):
        score = 0
        (x, y) = move
        if x % 3 ==1 and y % 3 == 1:
            score = score + 1
        print(x, y, score)
        return score
