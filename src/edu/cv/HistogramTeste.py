'''
Created on 09/11/2013

@author: eletro
'''

import pygame
import math
from pygame.locals import QUIT, MOUSEBUTTONDOWN, MOUSEMOTION, MOUSEBUTTONUP, Rect

PRECISAO = 5
VERIFICACAO = 0.95
FRAMESPERSECOND = 500
dimensions = (640, 480)

imageX1, imageY1, imageX2, imageY2, distX, distY = (0, 0, 0, 0, 0, 0)
desenhaQuadro = False
countDraw = 0

pygame.init()

screen = pygame.display.set_mode( dimensions, 0, 32 )
def multiplicaMatriz( matriz1, matriz2 ):
    novaMatriz = [[0 for _ in m] for m in matriz1]
    for l in range(len(novaMatriz)):
        for c in range(len(novaMatriz[l])):
            soma = 0
            for indice in range(len(matriz1[l])):
                soma += (matriz1[l][indice] * matriz2[indice][c])
            novaMatriz[l][c] = soma
    return novaMatriz 

def normalizaPixel ( pixel ):
    return 1- ((pixel[0] + pixel[1] + pixel[2]) / (3 * 255))

def normalizaVetor( vetor ):
    soma = 0
    for valor in vetor:
        soma += math.pow( valor, 2)
    return math.sqrt( soma )

def aplicaMascaraNoPixel( surface, i, j, mascara ):
#     resultante = [[0 for _ in range(len(mascara[linha]))] for linha in range(len(mascara))]
    comp = len(mascara[0])
    alt = len(mascara)
    x1 = i - (comp / 2)
    y1 = j - (alt / 2)
#     x2 = i + (comp / 2)
#     y2 = j + (alt / 2)
#     sur = pygame.Surface
#     sur.get_a
    soma = 0    
    for l in range( len(mascara) ):
        for c in range( len(mascara[l]) ):
            color = surface.get_at( (x1 + c, y1 + l))
            #color = (0,0,0)
            pixel = normalizaPixel( color )
            soma += mascara[l][c] * pixel
    return soma

def displayBar( surface, titulo, pos, total ):
    global countDraw, FRAMESPERSECOND
    countDraw += 1
    if ((countDraw % FRAMESPERSECOND) == 0):
        comp = surface.get_width()
        alt = surface.get_height()
        compBar = int(comp * 0.90)
        altBar = int(alt * 0.10)
        x = int ((comp - compBar) / 2)
        y = int (alt * 0.10)
        filled = int (pos * compBar / total)
        surface.fill( (0, 0, 0 ) )
        pygame.draw.rect( surface, (0, 255, 0), Rect(x, y, compBar, altBar), 2 );
        pygame.draw.rect( surface, (0, 180, 0), Rect(x, y, filled, altBar), 0 );
        pygame.display.update()
    
def aplicaMascaraDetectaBorda( surface, x1, y1, x2, y2 ):
    mascaraV = [   [1, 0, -1],
                   [2, 0, -2],
                   [1, 0, -1] 
               ]
    mascaraH = [   [1, 2, 1],
                   [0, 0, 0],
                   [-1, -2, -1] 
               ]
    
    magnitudeMatriz = [[0 for _ in range(abs(x2 - x1))] for _ in range(abs(y2 - y1))]
    newSurface = pygame.Surface( (abs(x2 - x1), abs(y2 - y1)), 0, 32)
    total = abs (x2 - x1 ) * abs (y2 - y1)
    c = 1
    for y in range( y1, y2 ):
        for x in range( x1, x2 ):
            gV = aplicaMascaraNoPixel( surface, x, y, mascaraV )
            gH = aplicaMascaraNoPixel( surface, x, y, mascaraH )
            gMagnitude = normalizaVetor( [gV, gH] )
            gPhase = math.atan( gV / gH )
            if gMagnitude > 255 :
                gMagnitude = 255
            newSurface.set_at( (x, y), (gMagnitude, gMagnitude, gMagnitude) )
            magnitudeMatriz[y][x] = (gMagnitude, gPhase)
            displayBar(screen, "Aplicando Mascara de Sobel", c, total)
            c += 1
    return newSurface
#     
# def drawPoint( scr, pos ):
#     global pontos

# def showLines(scr):
#     global points
#     for ang in points:
#         for dis in ang:
#             contador = dis["contador"]
# #             print str( contador ),
#             if (contador >= ( pontos * VERIFICACAO) ):
#                 print contador, ( pontos * VERIFICACAO)
#                 pontoAnterior = dis["pontos"][0]
#                 for ponto in dis["pontos"]:
#                     pygame.draw.line(scr, (255, 255, 0), pontoAnterior, ponto)
#                     pontoAnterior = ponto                
#         print ""

# m1 = [  [1, 2, 3],
#         [2, 3, 1],
#         [1, 1, 1] ]
# 
# m2 = [  [1, 1, 0],
#         [0, 1, 0],
#         [0, 2, 1] ]
# 
# mf = multiplicaMatriz(m1, m2)
# 
# for l in mf:
#     print l 
# # 

# imagemName = 'C:/Temp/Luneta30xa.jpg'
imagemName = 'C:/Temp/Barcode/images/IMG112.jpg'
# imagemName = 'C:/Temp/shutterstock_28649449.jpg'
imagem = pygame.image.load(imagemName).convert_alpha()
imagemProportion = (imagem.get_width() / imagem.get_height())
if (imagem.get_width() > dimensions[0]):
    imagem = pygame.transform.scale( imagem, (dimensions[0], dimensions[1]))
# imagem = aplicaMascaraDetectaBorda(imagem, 3, 3, imagem.get_width() - 6, imagem.get_height() - 6)

while (True):
    countDraw += 1
    if (countDraw % FRAMESPERSECOND == 0):
        screen.fill( (0, 0, 0 ) )
        screen.blit( imagem, (0,0))
        if( desenhaQuadro ):
            pygame.draw.rect(screen, (0, 0, 255), Rect( (imageX1, imageY1), (distX, distY)), 1)
        pygame.display.update()
     
        for e in pygame.event.get():
            if (e.type == QUIT):
                exit()
            if (e.type == MOUSEBUTTONDOWN):
                if (e.button == 1):
                    imageX1, imageY1 = e.pos
                    desenhaQuadro = True
            if (e.type == MOUSEBUTTONUP):
                if (e.button == 1):
                    imageX2, imageY2 = e.pos
                    desenhaQuadro=False
                    inicio = long(pygame.time.get_ticks())
                    imagem = aplicaMascaraDetectaBorda(imagem, imageX1, imageY1, imageX2, imageY2)
                    termino = long(pygame.time.get_ticks())
                    print "Demorou ", termino - inicio, "ms"
            if (e.type == MOUSEMOTION):
                if (e.buttons[0] == True):
                    tempX2, tempY2 = e.pos
                    distX = tempX2 - imageX1
                    distY = tempY2 - imageY1