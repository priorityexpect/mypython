import tkinter as tk
import random

CELL_SIZE = 30  # 功能：每个方块的大小
COLUMNS = 10 # 功能：游戏区域的列数
ROWS = 20   # 功能：游戏区域的行数
DELAY = 400 

SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]],  # L
]

# 添加功能：得分
class Score:
    def __init__(self):
        self.score = 0

    def add(self, points):
        self.score += points

    def reset(self):
        self.score = 0

    def get_score(self):
        return self.score



COLORS = ["cyan", "yellow", "purple", "green", "red", "blue", "orange"]

class Tetris:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=COLUMNS*CELL_SIZE, height=ROWS*CELL_SIZE, bg="black")
        self.canvas.pack()
        self.board = [[None for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.score = 0
        self.game_over = False
        self.new_piece()
        self.root.bind("<Key>", self.key_press)
        self.tick()

    def new_piece(self):
        idx = random.randint(0, len(SHAPES)-1)
        self.shape = SHAPES[idx]
        self.color = COLORS[idx]
        self.x = COLUMNS // 2 - len(self.shape[0]) // 2
        self.y = 0
        if self.collision(self.x, self.y, self.shape):
            self.game_over = True

    def rotate(self, shape):
        return [list(row)[::-1] for row in zip(*shape)]

    def collision(self, x, y, shape):
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    nx, ny = x + j, y + i
                    if nx < 0 or nx >= COLUMNS or ny < 0 or ny >= ROWS:
                        return True
                    if self.board[ny][nx]:
                        return True
        return False

    def freeze(self):
        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                if cell:
                    self.board[self.y + i][self.x + j] = self.color
        self.clear_lines()
        self.new_piece()

    def clear_lines(self):
        new_board = [row for row in self.board if any(cell is None for cell in row)]
        lines_cleared = ROWS - len(new_board)
        for _ in range(lines_cleared):
            new_board.insert(0, [None for _ in range(COLUMNS)])
        self.board = new_board
        self.score += lines_cleared

    def move(self, dx, dy):
        if not self.collision(self.x + dx, self.y + dy, self.shape):
            self.x += dx
            self.y += dy
            return True
        return False

    def drop(self):
        if not self.move(0, 1):
            self.freeze()

    def key_press(self, event):
        if self.game_over:
            return
        if event.keysym == "Left":
            self.move(-1, 0)
        elif event.keysym == "Right":
            self.move(1, 0)
        elif event.keysym == "Down":
            self.drop()
        elif event.keysym == "Up":
            new_shape = self.rotate(self.shape)
            if not self.collision(self.x, self.y, new_shape):
                self.shape = new_shape
        self.draw()

    def tick(self):
        if not self.game_over:
            self.drop()
            self.draw()
            self.root.after(DELAY, self.tick)
        else:
            self.canvas.create_text(COLUMNS*CELL_SIZE//2, ROWS*CELL_SIZE//2, text="Game Over", fill="white", font=("Arial", 24))

    def draw(self):
        self.canvas.delete("all")
        # Draw board
        for y in range(ROWS):
            for x in range(COLUMNS):
                color = self.board[y][x]
                if color:
                    self.draw_cell(x, y, color)
        # Draw current piece
        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                if cell:
                    self.draw_cell(self.x + j, self.y + i, self.color)
        # Draw score
        self.canvas.create_text(60, 10, text=f"Score: {self.score}", fill="white", anchor="nw")

    def draw_cell(self, x, y, color):
        x0 = x * CELL_SIZE
        y0 = y * CELL_SIZE
        x1 = x0 + CELL_SIZE
        y1 = y0 + CELL_SIZE
        self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="gray")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("俄罗斯方块")
    game = Tetris(root)
    root.mainloop()