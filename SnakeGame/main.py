import pygame
from pygame.font import SysFont                   #importa a biblioteca
from pygame.locals import *     #importa todos as funçções e constantres do submodulos
from sys import exit            #importa função exit de sys

from random import randint

from pygame.mixer import Sound      #para pegar valores randomicos

pygame.init()                   #inicializa a biblioteca

#print(pygame.font.get_fonts())     #Todas as fontes disponiveis

pygame.mixer.music.set_volume(0.15) #volume da musica de fundo
musica_de_fundo = pygame.mixer.music.load('./effects/BoxCat Games - CPU Talk.mp3')   #define musica de fundo
pygame.mixer.music.play(-1)     #poe a musica pra tocar; -1 pq ela vai se repetir quando acabar

colisao = pygame.mixer.Sound('./effects/smw_coin.wav')   #configura o som de colisao
colisao.set_volume(0.5)     #volume da moeda

perdeu = pygame.mixer.Sound('./effects/mixkit-retro-arcade-game-over-470.wav')   #configura som da derrota
perdeu.set_volume(0.5)

largura = 640       #variaveis para altura e largura
altura = 480

lista_cobra = []    #guarda as coordenadas por onde ja passou a cobra
comprimento_inicial = 25     

morreu = False

red = (255,0,0)
black = (0,0,0)
green = (0,165,0)
white = (255,255,255)

x = largura/2 - 25      #cobra
y = altura/2 - 25

velocidade = 3

x_controle = velocidade #controles de tamanho e movimentação
y_controle = 0

x1 = randint(0, 620)    #maca
y1 = randint(0, 460)

fonte = pygame.font.SysFont('arial', 20, True, True) #Crianção de fonte; tipo de fonte, tamanho, negrito, italico

pontos = 0

tela = pygame.display.set_mode((largura, altura))    #criar janela de acordo com as variaveis criadas
pygame.display.set_caption('My game')

relogio = pygame.time.Clock()       #clock do jogo; taxa de frames que o clock vai mater

#FUNÇÔES------------------------------------------------------------------------------

def aumenta_cobra(lista_cobra):
    for XeY in lista_cobra:
        #XeY = [x, y]
        #XeY[0] = x
        #XeY[1] = y

        pygame.draw.rect(tela, green, (XeY[0], XeY[1], 20, 20))

def reinicia_jogo():    #retorna as variaveis para reiniciar o jogo
    global pontos, comprimento_inicial, x, y, lista_cobra, lista_cabeca, x1, y1, morreu     #torna as variaveis globais para possibilitar reinicio
    pontos = 0
    comprimento_inicial = 25
    x = largura/2 - 25
    y =  altura/2 - 25
    lista_cobra = []
    lista_cabeca = []
    x1 = randint(0, 620)    
    y1 = randint(0, 460)
    morreu = False
    pygame.mixer.music.play(-1)


while True:     #loop principal
    relogio.tick(60)                #clock em 75 frames por segundo(fps)
    tela.fill(white)                        #A cada atualização do loop ele pinta a tela de preto

    mensagem = 'Pontos: {}'.format(pontos)

    texto_formatado = fonte.render(mensagem, True, black)   # texto, serrilhamento, cor de acordo com a fonte

    for event in pygame.event.get():        #checa os eventos que ocorrem na tela
        if event.type == QUIT:              #caso o evento seja sair
            pygame.quit()
            exit()

        if event.type == KEYDOWN:   #se a tecla for pressionada; limitar movimentação somente pra cima e para baixo; automatizar o movimento
            if event.key == K_a or event.key == K_LEFT:     #'a' ou seta pra esquerda
                #bloaqueia movimentação para a esquera se a tecla direita for apertada
                if x_controle == velocidade:
                    pass        #bloqueia a acao
                else:
                    x_controle = -velocidade
                    y_controle = 0
            if event.key == K_d or event.key == K_RIGHT:    #'d' ou seta pra direita
                if x_controle == -velocidade:
                    pass
                else:
                    x_controle = velocidade
                    y_controle = 0
            if event.key == K_w or event.key == K_UP:       #'w' ou seta pra cima
                if y_controle == velocidade:
                    pass
                else:
                    x_controle = 0
                    y_controle = -velocidade
            if event.key == K_s or event.key == K_DOWN:     #'s' ou seta pra baixo
                if y_controle == -velocidade:
                    pass
                else:
                    x_controle = 0
                    y_controle = velocidade
    
    #faz combra se mexer sozinha
    x += x_controle
    y += y_controle

    #interação de lados da janela com a movimentação da cobra
    if x > largura:
        x = x - largura
    if x < 0:
        x = largura + x
    if y > altura:
        y = y - altura
    if y < 0:
        y = altura + y

    cobra = pygame.draw.rect(tela, green, (x, y, 20, 20)) #(pos x, pos y, 50 = largura, 50 = altura); O eixo y incrementa para baixo
    maca = pygame.draw.rect(tela, red, (x1, y1, 20, 20))

    if cobra.colliderect(maca):      #metodo que checa se houve colição entre os retangulos
        x1 = randint(40, 600)
        y1 = randint(40, 400)

        pontos += 1
        comprimento_inicial += 1

        colisao.play()

    lista_cabeca = []       #lista pra guardar os valores das cordenadas da cabeça
    lista_cabeca.append(x)  #guarda x cabeca
    lista_cabeca.append(y)  #guarda y cabeca

    lista_cobra.append(lista_cabeca)    #guarda os pares ordenados por onde ja passou a cabeca

    #logica para combra morrer ao tocar no seu corpo
    if lista_cobra.count(lista_cabeca) > 1:     #se tiver mais de uma lista cabeça (coordenada da cabeca) em lista cobra = encostou
        
        fonte2 = pygame.font.SysFont('arial', 20, bold=True, italic=True)
        mensagem2 = 'Game Over! Pressione ESPAÇO para jogar novamente'
        texto_formatado2 = fonte2.render(mensagem2, True, black)
        ret_texto = texto_formatado2.get_rect()

        perdeu.play()

        morreu = True
        while morreu:
            tela.fill(white)
            pygame.mixer.music.stop()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        reinicia_jogo()

            ret_texto.center =  (largura//2, altura//2)
            tela.blit(texto_formatado2, ret_texto)
            pygame.display.update()


    if len(lista_cobra) > comprimento_inicial:
        del lista_cobra[0]

    aumenta_cobra(lista_cobra)

    tela.blit(texto_formatado, (500, 20))   #posicionando texto
    pygame.display.update()