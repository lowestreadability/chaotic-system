import pygame
from pygame import gfxdraw
from colorsys import hls_to_rgb
def dot(v, u):
    vx, vy=v[0], v[1]
    ux, uy=u[0], u[1]
    dotproduct=vx*ux + vy*uy
    return dotproduct
num=fps=120
width, height=600, 600
x, y=1360 - width, 40
pygame.init()
screen=pygame.display.set_mode((width, height))
clock=pygame.time.Clock()
pygame.mixer.init()
bigr=height//2
centx, centy=width//2, height//2
a1=a2=a3=a4=frames=0
class Balls():
    trail=True
    balls=list()
    def __init__(self, color, radius, thicc, posx, posy):
        Balls.balls.append(self)
        self.color=color
        self.radius=radius
        self.thicc=thicc
        self.posx=posx
        self.posy=posy
        self.velx=0
        self.vely=0
        self.acc=-9.81/fps
        self.track=[]
        self.count=0
    def drawball(self):
        pygame.draw.circle(screen, [i*255 for i in hls_to_rgb(a3/360,.5,1)], (self.posx, self.posy), self.radius, self.thicc)
    def collision_handling(self):
        vel=(self.velx**2 + self.vely**2) ** .5
        x,y=centx, centy
        ballx, bally=self.posx, self.posy
        velx, vely=self.velx, self.vely
        center_to_ball=((x-ballx)**2 + (y-bally)**2) ** .5
        if center_to_ball >=(bigr - self.radius):
            self.count+=1
            pygame.mixer.Sound.play(pygame.mixer.Sound(f'{self.count%25+1}.mp3'))
            while ((x-self.posx)**2 + (y-self.posy)**2) ** .5 > (bigr - self.radius):
                step=0.2
                self.posx +=-self.velx*step/vel
                self.posy -=-self.vely*step/vel
            normal=ballx - x, bally - y
            normal_mag=center_to_ball
            n=normal[0]/normal_mag, normal[1]/normal_mag
            nx, ny=n[0], n[1]
            d=velx, -vely
            dx, dy=d[0], d[1]
            reflected=dx-2*dot(n,d)*nx, dy-2*dot(n,d)*ny
            self.velx=reflected[0]
            self.vely=-reflected[1]
    def motion(self):
        self.vely+=self.acc
        self.posx+=self.velx
        self.posy-=self.vely
        every=2
        period=5
        if Balls.trail:
            if frames % every==0:
                self.track.append((self.posx, self.posy))
                if len(self.track) > num:
                    self.track.pop(0)
        else:
            self.track.clear()
redball=Balls((245, 170,  10), 8, 0, width//2-bigr+10, height//2)
redball.vely=-5
while True:
    for event in pygame.event.get((pygame.QUIT,pygame.KEYDOWN)):
        if event.type==pygame.QUIT:
            exit()
        elif event.key==pygame.K_SPACE:
            Balls.trail=not Balls.trail
    screen.fill([i*255 for i in hls_to_rgb(a1/360,.5,1)])
    gfxdraw.aacircle(screen, 300, 300, 295, [i*255 for i in hls_to_rgb(a2/360,.5,1)])
    for ball in Balls.balls:
        if len(ball.track)> 2 and Balls.trail:
            pygame.draw.aalines(screen, [i*255 for i in hls_to_rgb(a4/360,.5,1)], False, ball.track, 2)
        ball.drawball()
        ball.collision_handling()
        ball.motion()
    pygame.display.flip()
    clock.tick(fps)
    frames +=1
    a1+=1
    a2+=2
    a3+=3
    a4+=4
