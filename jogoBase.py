# by SLMM  2026
# versao 0.1.1

import pygame
import random

from pygame.locals import ( 
  K_UP,
  K_DOWN,
  K_LEFT,
  K_RIGHT,
  KEYDOWN,
  QUIT,
  K_ESCAPE,
  K_SPACE,
  K_x
)

pygame.init()

# define clock para FPS do jogo
clock = pygame.time.Clock()

SC_WIDTH = 800
SC_HEIGHT = 600

class Player(pygame.sprite.Sprite):
  def __init__(self):
    super(Player, self).__init__()
    # cria superfice e coloca cor azul
    self.surf = pygame.Surface((75,25))
    self.surf.fill((0,0,255))
    self.rect = self.surf.get_rect()

  def update(self, pressed_key):
    if pressed_key[K_UP]:
      self.rect.move_ip(0, -5)
    if pressed_key[K_DOWN]:
      self.rect.move_ip(0, 5)
    if pressed_key[K_LEFT]:
      self.rect.move_ip(-5, 0)
    if pressed_key[K_RIGHT]:
      self.rect.move_ip(5, 0)
      
    # testa para ver se não saiu da tela  
    if self.rect.right > SC_WIDTH:
      self.rect.right = SC_WIDTH
    if self.rect.left < 0:
      self.rect.left = 0
    if self.rect.top <= 0:
      self.rect.top = 0
    if self.rect.bottom >= SC_HEIGHT:
      self.rect.bottom = SC_HEIGHT     

 # criar aqui classe do inimigo
 #      

class Enemy(pygame.sprite.Sprite):
  def __init__(self):
    super(Enemy, self).__init__()
    self.surf = pygame.Surface((25,25))
    self.surf.fill((235,15,25)) # branco
    self.rect = self.surf.get_rect(
      center = (
        random.randint(SC_WIDTH+20, SC_WIDTH+ 100),
        random.randint(40,SC_HEIGHT)
      )
    )
    self.speed = random.randint(5, 20)

  def update(self):
    self.rect.move_ip(-self.speed, 0)  
    if self.rect.right < 0:
      self.kill()
 
# definicao para escrever texto na tela
fonte = pygame.font.SysFont('Arial',30)
vidas = 4
texto = fonte.render(f'Vidas : {vidas}', True, (255,0,128))

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 500)


 # definir condições iniciais do jogo
screen = pygame.display.set_mode([SC_WIDTH, SC_HEIGHT])
pygame.display.set_caption("Jogo Base")

running = True
jogador = Player()
# criar os grupos de sprites
inimigos = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(jogador)
posicao = jogador.rect 


while running:
  posicao = jogador.rect
  for event in pygame.event.get():
    if event.type == KEYDOWN:
      if event.key == K_ESCAPE or \
         event.key == K_x:
         running = False
    elif event.type == QUIT:
      running = False
    elif event.type == ADDENEMY:
      novo = Enemy()
      inimigos.add(novo)
      all_sprites.add(novo)  

  teclas = pygame.key.get_pressed()
  jogador.update(teclas)
  inimigos.update()

  # antes de atulizar a tela testar a colisao 
  colidiu = pygame.sprite.spritecollide(jogador, inimigos, True)
  if colidiu:
    vidas -= 1
    texto = fonte.render(f'Vidas : {vidas}', True, (255,0,128))
    if vidas == 0:
      jogador.kill()
      running = False


  screen.fill((255,255,255))
  for entidade in all_sprites:
    screen.blit(entidade.surf, entidade.rect)
  screen.blit(texto, (SC_WIDTH-150,0))  

  pygame.display.flip()
  clock.tick(30) # define 30 fps para o jogo


screen.fill((255,255,255))
texto = fonte.render(f'Acabou o jogo', True, (255,0,128))
posi = texto.get_rect()
screen.blit(texto, ((SC_WIDTH/2)-posi.centerx,\
                    (SC_HEIGHT/2)-posi.centery ))

img = pygame.image.load("niquel.jpg")
img_rect = img.get_rect()
img_rect.topleft = (100, 50)
screen.blit(img, img_rect)

pygame.display.flip()
pygame.time.wait(3000)

pygame.quit()

