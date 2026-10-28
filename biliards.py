
from ast import Try
import random
import sys
import pygame as pg
import math
from pygame.sprite import Group, Sprite
class background():###球桌背景图片
    def __init__(self):
        self.img=pg.image.load('resources/picture/background.png')
    def load(self,window):
        window.blit(self.img,(0,0))

def balldist(ball1,ball2):
    x=ball1.x-ball2.x
    y=ball1.y-ball2.y
    return math.sqrt(x**2+y**2)

class hole():
    def __init__(self,x,y,holelist):
        self.x=x
        self.y=y
        holelist.append(self)


def restart(ball0,ball1,ball2,ball3,ball4,ball5,ball6,ball7,ball8,ball9,ball10,ball11,ball12,ball13,ball14,ball15,every_ball,inholeball):
    ball0.x=300
    ball0.y=303
    ball1.x=772
    ball1.y=239
    ball2.x=678
    ball2.y=287
    ball3.x=678
    ball3.y=319
    ball4.x=772
    ball4.y=275
    ball5.x=741
    ball5.y=321
    ball6.x=741
    ball6.y=258
    ball7.x=741
    ball7.y=358
    ball8.x=710
    ball8.y=303
    ball9.x=710
    ball9.y=338
    ball10.x=710
    ball10.y=268
    ball11.x=772
    ball11.y=303
    ball12.x=772
    ball12.y=345
    ball13.x=741
    ball13.y=285
    ball14.x=660
    ball14.y=303
    ball15.x=772
    ball15.y=365
    for Ball in every_ball:
        Ball.Vx=0
        Ball.Vy=0
        Ball.visible=True
    inholeball.clear()

def crush(every_ball,holelist,inholeball):
    balllist=list(every_ball)
    crushed=set()
    for i in range(len(balllist)):
        ball_1=balllist[i]
        for k in range(len(holelist)):
            Hole=holelist[k]
            if balldist(Hole,ball_1)<=25:##进球
                ball_1.visible=False
                if not(i in inholeball):
                    inholeball.append(i)
                    print(inholeball)
        if ball_1.visible==False:
            continue
        for j in range(i+1,len(balllist)):
            ball_2=balllist[j]
            pair=frozenset({ball_1,ball_2})
            if pair in crushed or ball_2.visible==False:
                continue
            crushed.add(pair)
            if pg.sprite.collide_circle(ball_1, ball_2):
                dis=balldist(ball_1,ball_2)
        #         ##print(dis)
                Midx=(ball_1.x+ball_2.x)/2
                Midy=(ball_1.y+ball_2.y)/2

                n=((ball_1.x-ball_2.x)/dis,(ball_1.y-ball_2.y)/dis)
                t=(-(ball_1.y-ball_2.y)/dis,(ball_1.x-ball_2.x)/dis)
                ball_1.V=((ball_1.Vx*t[0]+ball_1.Vy*t[1])*t[0]+(ball_2.Vx*n[0]+ball_2.Vy*n[1])*n[0],(ball_1.Vx*t[0]+ball_1.Vy*t[1])*t[1]+(ball_2.Vx*n[0]+ball_2.Vy*n[1])*n[1])
                ball_2.V=((ball_1.Vx*n[0]+ball_1.Vy*n[1])*n[0]+(ball_2.Vx*t[0]+ball_2.Vy*t[1])*t[0],(ball_1.Vx*n[0]+ball_1.Vy*n[1])*n[1]+(ball_2.Vx*t[0]+ball_2.Vy*t[1])*t[1])

                ball_1.Vx=ball_1.V[0]
                ball_1.Vy=ball_1.V[1]
                ball_2.Vx=ball_2.V[0]
                ball_2.Vy=ball_2.V[1]                
                ball_1.x=Midx+(2*ball_1.radius/dis)*(ball_1.x-Midx)
                ball_1.y=Midy+(2*ball_1.radius/dis)*(ball_1.y-Midy)
                ball_2.x=Midx+(2*ball_2.radius/dis)*(ball_2.x-Midx)
                ball_2.y=Midy+(2*ball_2.radius/dis)*(ball_2.y-Midy)

def edge(a1,a2,a3,a4,y,side,self):
    if side=='down':
        return (self.y>=y-self.radius)and(((self.x>=a1)and(self.x<=a2))or((self.x>=a3)and(self.x<=a4)))
    if side=='up':
        return (self.y<=y+self.radius)and(((self.x>=a1)and(self.x<=a2))or((self.x>=a3)and(self.x<=a4)))
    if side=='left':
        x=a1
        y1=a2
        y2=a3
        return (self.x<=x+self.radius)and((self.y<=y1)and(self.y>=y2))
    if side=='right':
        x=a1
        y1=a2
        y2=a3
        return (self.x>=x-self.radius)and((self.y<=y1)and(self.y>=y2))
class button():###开始按钮
    def __init__(self,locate):
        self.img=pg.image.load(locate)
        self.width=self.img.get_size()[0]
        self.hight=self.img.get_size()[1]
        
    def press(self,ev,window,x,y,xt,yt):
        self.x=x
        self.y=y
        ##鼠标悬停变大
        if self.img.get_rect(topleft=(self.x, self.y)).collidepoint(pg.mouse.get_pos()):
            
            self.x=xt
            self.y=yt
            window.blit(pg.transform.scale(self.img,(self.width*1.16,self.hight*1.21)),(self.x,self.y))
            if ev.type==pg.MOUSEBUTTONDOWN and ev.button==1:
                current_button_rect = self.img.get_rect(topleft=(self.x, self.y))
                return 1
        else :
            window.blit(self.img,(self.x,self.y))
            return 0
def openfield(window,StartBackGround,GameTopic):###开始菜单背景加载
    topic_x=540-325
    topic_y=70
    topic_x+=random.randint(-2,2)
    topic_y+=random.randint(-2,2)
    window.blit(pg.transform.scale(StartBackGround,(1080,900)),(0,0))
    window.blit(GameTopic,(topic_x,topic_y))


        

class ball(pg.sprite.Sprite):
    def __init__(self,imglocate,spawn_x,spawn_y):
        super().__init__()
        self.img=pg.image.load(imglocate)
        self.radius=17
        self.x=spawn_x
        self.y=spawn_y
        self.rect=self.img.get_rect(center=(self.x,self.y))
        self.Vx=0
        self.Vy=0
        self.a=0.05##桌面摩擦系数
        self.add(every_ball)
        self.V=(self.Vx,self.Vy)
        self.visible=True
    def update(self,window):
        ###计算球和边界碰撞
        if edge(185,513,565,900,481,'down',self):
            self.y=481-18 
            self.Vy=-self.Vy*0.9
        if edge(185,513,565,900,125,'up',self):
            self.y=125+18
            self.Vy=-self.Vy*0.9
        if edge(157,456,146,0,0,'left',self):
            self.x=157+18
            self.Vx=-self.Vx*0.9
        if edge(924,456,146,0,0,'right',self):
            self.x=924-18
            self.Vx=-self.Vx*0.9
        ###摩擦减速
        V=math.sqrt(self.Vx**2+self.Vy**2)
        if (V-self.a)>0:
            self.Vx*=(V-self.a)/V
            self.Vy*=(V-self.a)/V
        else:
            self.Vx=0
            self.Vy=0
        ###生成位移
        self.x+=self.Vx
        self.y+=self.Vy
        self.rect=self.img.get_rect(center=(self.x,self.y))
        ###绘制
        if self.visible:
            window.blit(self.img,self.rect)
        
        ##print((self.Vx,self.Vx),self.a)
    def visible(self):
        self.visible=True

class stick(pg.sprite.Sprite):
    def __init__(self,imgadress,ball0):
        super().__init__()
        self.img=pg.image.load(imgadress)
        self.x=0
        self.y=0
        self.rect=self.img.get_rect(center=(self.x,self.y))
        self.mball=ball0
        self.visible=False
        self.angle=0
        self.kicking=False
        self.dis=300
        self.predis=300
        self.v=0
    def kick(self,window,ev):
        mx=pg.mouse.get_pos()[0]
        my=pg.mouse.get_pos()[1]
        


        if ev.type==pg.MOUSEBUTTONDOWN:
            if ev.button==1 and ((self.mball.x-mx)**2+(self.mball.y-my)**2)<=324:
                self.visible=True
            else:
                if ev.button==3:
                    self.visible=False
        if self.visible:
            try:
                self.angle=math.atan((self.mball.x-mx)/(self.mball.y-my))
                #print(self.angle)
                if my<self.mball.y:
                    self.y=self.mball.y-self.dis*math.cos(self.angle)
                    self.x=self.mball.x-self.dis*math.sin(self.angle)
                    self.rect=pg.transform.rotate(self.img,-90+math.degrees(self.angle)).get_rect(center=(self.x,self.y))
                    window.blit(pg.transform.rotate(self.img,90+math.degrees(self.angle)),self.rect)
                if my>=self.mball.y:
                    self.y=self.mball.y+self.dis*math.cos(self.angle)
                    self.x=self.mball.x+self.dis*math.sin(self.angle)
                    self.rect=pg.transform.rotate(self.img,-90+math.degrees(self.angle)).get_rect(center=(self.x,self.y))
                    window.blit(pg.transform.rotate(self.img,-90+math.degrees(self.angle)),self.rect)
                if pg.mouse.get_pressed()==(1,0,0) and ((self.mball.x-mx)**2+(self.mball.y-my)**2)>324: 
                    self.dis=270+math.sqrt(((self.mball.x-mx)**2+(self.mball.y-my)**2))*0.2
                    self.v=(self.predis-self.dis)*2
                    self.predis=self.dis
                    if self.dis<=300:
                        self.dis=300
                        self.visible=False
                        print(self.v)
                        if my>=self.mball.y:
                            self.mball.Vx=-self.v*math.sin(self.angle)
                            self.mball.Vy=-self.v*math.cos(self.angle)
                        if my<self.mball.y:
                            self.mball.Vx=self.v*math.sin(self.angle)
                            self.mball.Vy=self.v*math.cos(self.angle)
            except:
                pass



###创建窗口
pg.init()
window=pg.display.set_mode((1080,800))
pg.display.set_caption('台球模拟')

###设置帧数
clock=pg.time.Clock()

##载入资源
every_ball=Group()
bg=background()
btstart=button('resources/picture/startbuttom.png')
btrestart=button('resources/picture/restartbutton.png')
StartBackGround=pg.image.load('resources/picture/start.png')
GameTopic=pg.image.load('resources/picture/topic.png')
ball0=ball('resources/picture/ball0.png',300,303)
ball1=ball('resources/picture/ball1.png',772,239)
ball2=ball('resources/picture/ball2.png',678,287)
ball3=ball('resources/picture/ball3.png',678,319)
ball4=ball('resources/picture/ball4.png',772,275)
ball5=ball('resources/picture/ball5.png',741,321)
ball6=ball('resources/picture/ball6.png',741,258)
ball7=ball('resources/picture/ball7.png',741,358)
ball8=ball('resources/picture/ball8.png',710,303)
ball9=ball('resources/picture/ball9.png',710,338)
ball10=ball('resources/picture/ball10.png',710,268)
ball11=ball('resources/picture/ball11.png',772,303)
ball12=ball('resources/picture/ball12.png',772,345)
ball13=ball('resources/picture/ball13.png',741,285)
ball14=ball('resources/picture/ball14.png',660,303)
ball15=ball('resources/picture/ball15.png',772,365)
stick001=stick('resources/picture/cue_stick.png',ball0)
holelist=[]
hole1=hole(150,119,holelist)
hole2=hole(540,110,holelist)
hole3=hole(928,119,holelist)
hole4=hole(925,481,holelist)
hole5=hole(540,497,holelist)
hole6=hole(150,485,holelist)
inholeball=[]
##主循环
isRunning=True
isOpenning=True
while isRunning:
    clock.tick(60)
    window.fill(color='#FFFEF9E6')
    for ev in pg.event.get():                
        if ev.type==pg.QUIT:##关掉游戏
            isRunning=False
            break
    if isOpenning:
        openfield(window,StartBackGround,GameTopic)
        if btstart.press(ev,window,540-150,325-84+100,540-160-10,325-90+100-10):
            isOpenning=0
    else:
        bg.load(window)
        crush(every_ball,holelist,inholeball)
        every_ball.update(window)
        #print(pg.mouse.get_pos())
        #print(ball14.V)
        stick001.kick(window,ev)
        if btrestart.press(ev,window,5,5,0,0):
            restart(ball0,ball1,ball2,ball3,ball4,ball5,ball6,ball7,ball8,ball9,ball10,ball11,ball12,ball13,ball14,ball15,every_ball,inholeball)

    pg.display.update()
if isRunning==False:
    pg.quit()
    sys.exit(0)

