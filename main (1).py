import pygame
from pygame import Vector2
from pygame import Vector2 as V2
import threading
import random
import numpy
class Goal:
    def __init__(this,x,y):
        this.pos = V2(x,y)
    def get_rect(this):
        return pygame.Rect(this.pos.x-50,this.pos.y-50,100,100)
    def draw(this,screen):
        pygame.draw.rect(screen,"green",this.get_rect())
class Idiot:
    def __init__(this,x,y,col="blue",training={((0,0),(0,0)): [1,1,1,1]},totalsteps=0):
        this.pos = Vector2(x,y)
        this.training=training
        this.totalsteps=totalsteps
        this.finished=False
        this.col=col
    def _weighteddir(this,dirs):
        poss = []
        for i in range(len(dirs)):
            x = dirs[i]
            for _ in range(x):
                poss.append(i)
        return random.choice(poss) #0 left 1 right 2 up 3 down
    def _keydist(this,key,testkey):
        return numpy.mean([V2(key[0]).distance_to(V2(testkey[0])),V2(key[1]).distance_to(V2(testkey[1]))])
    def move(this,goal):
        this.totalsteps += 1
        this.modpos = this.pos
        key = ((this.pos.x,this.pos.y),(goal.pos.x,goal.pos.y))
        if not key in this.training.keys():
            bestk=((0,0),(0,0))
            for k in this.training.keys():
                if this._keydist(key,k) < this._keydist(key,bestk):
                    bestk=k
            this.training[key]=this.training[bestk]
        movedir = this._weighteddir(this.training[key])
        this.pos += [V2(-1,0),V2(1,0),V2(0,-1),V2(0,1)][movedir]
        if this.pos.distance_to(goal.pos) < this.modpos.distance_to(goal.pos):
            this.training[key][movedir] += 1
        else:
            this.training[key][movedir] -= 1
            for i in range(4):
                this.training[key][i] += 1
        if this.get_rect().colliderect(goal.get_rect()):
            this.finished = True
    def get_rect(this):
        return pygame.Rect(this.pos.x-50,this.pos.y-50,100,100)
    def draw(this,screen):
        pygame.draw.rect(screen,this.col,this.get_rect())

pygame.init()
screen = pygame.display.set_mode((1280,720))
clock = pygame.Clock()
running = True
idiot1 = Idiot(50,50)
idiot2 = Idiot(50,50,"purple")
idiot3 = Idiot(50,50,"red")
idiot4 = Idiot(50,50,"pink")
goal = Goal(500,20)

def nav(idiot):
    global goal
    if not idiot.finished:
        idiot.move(goal)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("white")

    threads = []
    t1 = threading.Thread(target=nav,args=[idiot1])
    t2 = threading.Thread(target=nav,args=[idiot2])
    t3 = threading.Thread(target=nav,args=[idiot3])
    t4 = threading.Thread(target=nav,args=[idiot4])
    threads.extend([t1,t2,t3,t4])
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    idiot1.draw(screen)
    idiot2.draw(screen)
    idiot3.draw(screen)
    idiot4.draw(screen)
    goal.draw(screen)
    allfin = True
    for i in [idiot1,idiot2,idiot3,idiot4]:
        allfin = allfin and i.finished
    if allfin:
        goal.pos = V2(random.randint(100,1200),random.randint(100,600))
        newidpos = V2(random.randint(100,1200),random.randint(100,600))
        while newidpos.distance_to(goal.pos) < 120:
            newidpos = V2(random.randint(100,1200),random.randint(100,600))
        for i in [idiot1,idiot2,idiot3,idiot4]:
            i.finished = False
            i.pos = newidpos
    pygame.display.flip()
    clock.tick(60)
print(idiot1.training)
pygame.quit()
