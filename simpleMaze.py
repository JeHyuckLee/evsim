import tkinter
from tkinter import *
from tkinter import messagebox


class Player():

    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.id = canvas.create_oval(x * 30,
                                     y * 30,
                                     x * 30 + 30,
                                     y * 30 + 30,
                                     fill="red")
        self.x, self.y = x, y
        self.nx, self.ny = x, y

    def move(self, direction):
        # 키보드에서 누른 키에 따라서 움직임
        if direction == 'w':
            self.nx, self.ny = self.x, self.y - 1
        elif direction == 'a':
            self.nx, self.ny = self.x - 1, self.y
        elif direction == 's':
            self.nx, self.ny = self.x, self.y + 1
        elif direction == 'd':
            self.nx, self.ny = self.x + 1, self.y

        # 이동한 곳이 벽이 아닐 경우 이동시키며 x, y 갱신
        if not self.is_collide():
            self.canvas.move(self.id, (self.nx - self.x) * 30,
                             (self.ny - self.y) * 30)
            self.x, self.y = self.nx, self.ny

        # 골인 지점에 도달할 경우
        if map[self.y][self.x] == 3:
            messagebox.showinfo(title="성공", message="미로 찾기에 성공하셨습니다")

    # 이동한 곳이 벽인지 아닌지 판별
    def is_collide(self):
        if map[self.ny][self.nx] == 1:
            return True
        else:
            return False


# 키리스너 이벤트
def keyEvent(event):
    player.move(repr(event.char).strip("'"))


root = Tk()
root.title("미로 찾기 게임")
root.resizable(False, False)

# 창 너비, 높이, 위치 설정
width, height = 540, 540
x, y = (root.winfo_screenwidth() - width) / 2, (root.winfo_screenheight() -
                                                height) / 2
root.geometry("%dx%d+%d+%d" % (width, height, x, y))

# canvas를 추가하고 키이벤트를 부착
canvas = Canvas(root, width=width, height=height, bg="white")
canvas.bind("<Key>", keyEvent)
canvas.focus_set()
canvas.pack()

# 1 : 벽, 2 : 플레이어 시작 지점, 3 : 골인 지점
map = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
       [1, 2, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1],
       [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1],
       [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1],
       [1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
       [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
       [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
       [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1],
       [1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1],
       [1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1],
       [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1],
       [1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1],
       [1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1],
       [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
       [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1],
       [1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 3, 1],
       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

# canvas에 맵을 그림
for y in range(len(map[0])):
    for x in range(len(map[y])):
        if map[y][x] == 1:
            canvas.create_rectangle(x * 30,
                                    y * 30,
                                    x * 30 + 30,
                                    y * 30 + 30,
                                    fill="black")
        elif map[y][x] == 2:
            player = Player(canvas, x, y)
        elif map[y][x] == 3:
            canvas.create_oval(x * 30,
                               y * 30,
                               x * 30 + 30,
                               y * 30 + 30,
                               fill="blue")

root.mainloop()