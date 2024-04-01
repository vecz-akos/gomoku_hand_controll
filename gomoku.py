from enum import Enum

class GomokuState:
    def __init__(self, size=3, previous_board=None):
        if previous_board is None or not isinstance(previous_board, GomokuState):
            self.step = 0
            self.size = size
            self.board = [[Sign.EMPTY for j in range(size)] for i in range(size)]
        else:
            self.step = previous_board.step + 1
            self.size = len(previous_board[0])
            self.board = [[sign for sign in row] for row in previous_board.board]
        self.prev_board = previous_board
        self.current_step = [-1, -1]
    
    @property
    def next_sign(self):
        return Sign.X if sum([sum([sign.value for sign in row]) for row in self.board]) == 0 else Sign.O
    
    @property
    def is_end_state(self):
        return self.get_winner() is not Sign.EMPTY

    def get_winner(self):
        # horizontal check
        for row in self.board:
            rowsum = sum([sign.value for sign in row])
            if abs(rowsum) == self.size:
                return Sign.X if rowsum > 0 else Sign.O
        # vertical
        for col_i in range(self.size):
            colsum = sum([row[col_i].value for row in self.board])
            if abs(colsum) == self.size:
                return Sign.X if colsum > 0 else Sign.O
        # diagonal
        diagsum = sum([row[i].value for i, row in enumerate(self.board)])
        if abs(diagsum) == self.size:
            return Sign.X if diagsum > 0 else Sign.O
        diagsum = sum([row[self.size-1-i].value for i, row in enumerate(self.board)])
        if abs(diagsum) == self.size:
            return Sign.X if diagsum > 0 else Sign.O
        return Sign.EMPTY
    
    def set_step(self, row, col):
        if self.is_end_state or self.current_step != [-1, -1]:
            raise Exception(f"Not valid step!")
        if 0 <= row < len(self.board) and 0 <= col < len(self.board[0]) and self[row, col] is Sign.EMPTY:
            self.current_step = [row, col]
            next_sign = self.next_sign
            self.board[row][col] = next_sign
            return GomokuState(previous_board=self)
        raise Exception(f"Invalid row or column number! (row: {row}, col: {col})")
    
    def __str__(self):
        return "\n".join(["\t".join([str(sign) for sign in row]) for row in self.board])
    
    def __getitem__(self, indexes):
        if isinstance(indexes, int):
            row = indexes
            col = None
        elif isinstance(indexes, tuple):
            row, col = indexes
        
        if col == None and isinstance(row, (int, slice)):
            return self.board[row]
        elif isinstance(row, int) and isinstance(col, int):
            return self.board[row][col]
        else:
            raise TypeError(f"Invalid type: {type(indexes)}")

class Sign(Enum):
    EMPTY = 0
    X = 1
    O = -1

    def __str__(self):
        return self.name

def main():
    state = GomokuState()

    print(state)

    state2 = state.set_step(0, 0)
    state3 = state2.set_step(2, 0)

    state4 = state3.set_step(0, 1)
    state5 = state4.set_step(1, 1)

    state6 = state5.set_step(0, 2)
    state7 = state6.set_step(2, 1)

    print(state3.get_winner())
    print(state5.get_winner())
    print(state7.get_winner())

    print(state7)

if __name__ == "__main__":
    main()
