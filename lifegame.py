import numpy as np
import pygame as pg
isrunning = True
is_paused = True
clock = pg.time.Clock()
def initialize():
    pg.init()
    global size
    size = eval(input("输入窗口大小(x,y):"))
    global maze
    maze=np.zeros((int(size[0]/10),int(size[1]/10)))
    maze[40][30]=1
    maze[40][30-1]=1
    maze[40][30-2]=1
    maze[40+1][30-3]=1
    maze[40+2][30-4]=1
    maze[40+3][30-3]=1
    maze[40+4][30-2]=1
    maze[40+1][30]=1
    maze[40+3][30]=1
    maze[40+5][30-1]=1
def counting():
    global maze
    new_maze=maze.copy()
    for i in range(maze.shape[0]):
        for j in range(maze.shape[1]):
                a=0
                row_start=max(0,i-1)
                row_end=min(maze.shape[0]-1,i+2)
                col_start=max(0,j-1)
                col_end=min(maze.shape[1]-1,j+2)
                sum=maze[row_start:row_end,col_start:col_end].sum()
                a=sum-maze[i,j]
                if a==3:
                    new_maze[i][j]=1
                elif a==2 and maze[i][j]==1:
                    new_maze[i][j]=1
                else:
                    new_maze[i][j]=0
    maze=new_maze.copy()


def draw():
    x,y=maze.nonzero()
    site=list(zip(x,y))
    for location in site:
        pg.draw.rect(window,"black",(location[0]*10,location[1]*10,10,10))



# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    count=0
    initialize()

    window = pg.display.set_mode(size)
    pg.display.set_caption('life_game')
    window.fill(color="white")
    while isrunning:
        if count==60:
            count=0
        clock.tick(60)
        count+=1
        for event in pg.event.get():
            if event.type == pg.QUIT:
                isrunning = False
            #关闭窗口
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                    print (f"paused=",{is_paused})
                    is_paused = not is_paused#按下p触发暂停
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mx, my = pg.mouse.get_pos()
                    mx=int(mx)//10
                    my=int(my)//10
                    maze[mx][my] = 1
                    pg.draw.rect(window,"black",(int(mx*10),int(my*10),10,10))

        if is_paused==False:
            if not count%10:
                window.fill(color="white")
                draw()
                counting()
        pg.display.flip()

    if isrunning==False:
        pg.quit()


