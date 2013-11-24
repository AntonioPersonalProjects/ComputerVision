'''
Created on 09/11/2013

@author: eletro
'''

import pygame
import math
from pygame.locals import QUIT, MOUSEBUTTONDOWN

PRECISAO = 5
VERIFICACAO = 0.95
dimensions = (640, 480)
MAX_DISTANCE = int(math.sqrt( math.pow(dimensions[0], 2) + math.pow(dimensions[1], 2)))
points = [ [    {"contador":0, "pontos":[]} 
                 for p in range(0, MAX_DISTANCE, PRECISAO) ]   
                 for angulo in range (1, 180, PRECISAO) ]

pontos = 0

RAIO = 5

pygame.init()

screen = pygame.display.set_mode( dimensions, 0, 32 )

def drawPoint( scr, pos ):
    global pontos
    pygame.draw.circle(scr, (255, 255, 0), pos, RAIO )
    h, x1, y1, x2, y2 = 0, 0, 0, 0, 0
    pontos += 1
    x, y = pos
    tetaGrau = 1;
    for ponto in points:
        tetaRadius = (tetaGrau * math.pi) / 180
        if (tetaGrau < 90):
            h1 = y / math.sin( tetaRadius )
            h2 = x / math.cos( tetaRadius )
            y1 = 0
            x2 = 0
            x1 = ( math.cos( tetaRadius ) * h1 ) + x
            y2 = ( math.sin( tetaRadius ) * h2 + y)
            h = x1
            betaRadius = ((90 - tetaGrau) * math.pi) / 180
        else:
            alfaRadius = math.pi - tetaRadius
            h1 = x / math.cos( alfaRadius )
            h2 = (scr.get_height() - y) / math.sin( alfaRadius )
            y2 = scr.get_height()
            x1 = 0
            x2 = x  + ( math.cos( alfaRadius ) * h2 )
            y1 = y - ( math.sin( alfaRadius ) * h1)
            h = y1
            betaRadius = ((90 - (180 - tetaGrau)) * math.pi) / 180
            
        p = math.cos( betaRadius ) * h
        #pygame.draw.line( scr, (255, 255, 255), (x1, y1), (x2, y2) )
        #pX = math.cos( betaRadius ) * p
        #pY = math.sin( betaRadius ) * p
        #pygame.draw.line( scr, (255, 0, 255), (0, 0), (pX, pY) )
        
        pWorked = int(abs(p / PRECISAO))
        pWorked = min(pWorked, (MAX_DISTANCE / PRECISAO) - 1)
        ponto[pWorked]["contador"] += 1
        ponto[pWorked]["pontos"].append(pos)
        
        tetaGrau += PRECISAO

def showLines(scr):
    global points
    for ang in points:
        for dis in ang:
            contador = dis["contador"]
#             print str( contador ),
            if (contador >= ( pontos * VERIFICACAO) ):
                print contador, ( pontos * VERIFICACAO)
                pontoAnterior = dis["pontos"][0]
                for ponto in dis["pontos"]:
                    pygame.draw.line(scr, (255, 255, 0), pontoAnterior, ponto)
                    pontoAnterior = ponto                
#         print "" 

while (True):
    pygame.display.update()
    
    for e in pygame.event.get():
        if (e.type == QUIT):
            exit()
        if (e.type == MOUSEBUTTONDOWN):
            if (e.button == 1):
                drawPoint( screen, e.pos )
            else:
                showLines ( screen )