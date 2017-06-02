from random import randint

class RandomBot:
    def __init__(self):
        self.myid = 1
        self.oppid = 2
    def get_move(self, pos, tleft):
        lmoves = pos.legal_moves()
        return max(lmoves, key=lambda x: self.static_evaluation(pos, x))
    def static_evaluation(self, pos, move):
        score = 0
        (x, y) = move
        #check center
        if x % 3 ==1 and y % 3 == 1:
            score = score + 1
        #check local
        local_board = [pos.board[i + j * 9] for i in range(x / 3 * 3, x / 3 * 3 + 3) for j in range(y / 3 * 3, y / 3 * 3 + 3)]
        score = score + self.align_num(local_board, x % 3, y % 3) * 10
        #check global
        if score >= 20:
            if (x / 3 == 1 and y / 3 == 1):
                score = score + 100
            score = score + self.align_num(pos.macroboard, x/3, y/3) * 1000
        print(x, y, score)
        return score
    def align_num(self, local_board, local_x, local_y):
        num_max = 0
        delta = [[(1,0), (2,0)], [(0,1), (0,2)], [(1,1),(2,2)]]
        for d in delta:
            num = 0
            for (dx, dy) in d:
                if local_board[(local_x + dx) % 3 * 3 + (local_y + dy) % 3] == self.myid:
                    num = num + 1
                if num == 2:
                    return num
                if num > num_max:
                    num_max = num
        return num_max