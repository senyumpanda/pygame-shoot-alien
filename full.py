import pygame
from pygame.locals import *

pygame.init()

SCREEN = pygame.display.set_mode((1280, 800))
pygame.display.set_caption('Shoot Alien')
CLOCK = pygame.time.Clock()
FPS = 60

BG_BUTTON = (35, 232, 232)
BG_MENU = (35, 107, 232)
BG_START = pygame.image.load('img/bg.jpg')
BG_PAUSE = (3, 252, 136)

def get_font(size):
    return pygame.font.Font('font/font.ttf', size)

def is_collision(x1, y1, x2, y2):
    coor_x = (x1 - x2) ** 2
    coor_y = (y1 - y2) ** 2
    distance = (coor_x + coor_y) ** 0.5
    if distance < 60:
        return True
    return False

def is_fall(x1, y1, x2, y2):
    coor_x = (x1 - x2) ** 2
    coor_y = (y1 - y2) ** 2
    distance = (coor_x + coor_y) ** 0.5
    if distance < 60:
        return True
    return False

class Button:
    def __init__(self, pos, font, text_input, base_color, hovering_color):
        self.x = pos[0]
        self.y = pos[1]
        self.font = font
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, base_color)
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text_rect = self.text.get_rect(center=(self.x, self.y))
        
    def update(self):
        SCREEN.blit(self.text, self.text_rect)
        
    def click_button(self, posisi_mouse):
        if posisi_mouse[0] in range(self.x-120, self.x+120) and posisi_mouse[1] in range(self.y-60, self.y+60):
            return True
        return False
            
    def hover_button(self, posisi_mouse):
        if posisi_mouse[0] in range(self.x-120, self.x+120) and posisi_mouse[1] in range(self.y-60, self.y+60) and self.hovering_color is not None:
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

class Player:
    def __init__(self):
        self.player_image = pygame.image.load('img/spaceship.png')
        self.bullet_image = pygame.image.load('img/bullet.png')
        self.bullet_image = pygame.transform.rotate(self.bullet_image, 90)
        self.player_rect = self.player_image.get_rect(center=(650, 720))
        self.bullet_rect = self.player_image.get_rect(center=(672, 750))
        self.bullet_status = "ready"
        self.player_x = 0
        self.bullet_x = 0
        self.bullet_y = 5
        self.score = 0
        
    def shoot(self):
        self.bullet_status = 'fire'
        SCREEN.blit(self.bullet_image, (self.bullet_rect.x, self.bullet_rect.y))
        
class Enemy:
    def __init__(self):
        self.enemy_image = pygame.image.load('img/monster.png')
        self.enemy_image = pygame.transform.scale(self.enemy_image, (72, 72))
        self.enemy_rect = self.enemy_image.get_rect(center=(40, 90))
        self.posisi_kanan = False
        self.posisi_kiri = True
        self.pindah_bawah = False
        self.enemy_x = 4
        self.enemy_y = 30
        
    def gerak_x(self, posisi_x):
        if posisi_x <= 0 or posisi_x >= 1200:
            return True
        return False

def main_menu():
    while True:
        SCREEN.fill(BG_MENU)
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        TITLE_TEXT = Button(pos=(650, 150), 
                              font=get_font(84), 
                              text_input='SPACE SHOOTER', 
                              base_color='White', 
                              hovering_color=None)
        START_BUTTON = Button(pos=(650, 425), 
                              font=get_font(60), 
                              text_input='START', 
                              base_color='White', 
                              hovering_color='#23e83a')
        QUIT_BUTTON = Button(pos=(650, 525), 
                             font=get_font(60), 
                             text_input='QUIT', 
                             base_color='White', 
                             hovering_color='#fc2003')
                
        for button in [TITLE_TEXT, START_BUTTON, QUIT_BUTTON]:
            button.hover_button(MENU_MOUSE_POS)
            button.update()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
            if event.type == MOUSEBUTTONDOWN:
                if START_BUTTON.click_button(MENU_MOUSE_POS):
                    start()
                if QUIT_BUTTON.click_button(MENU_MOUSE_POS):
                    pygame.quit()
        
        pygame.display.update()

def start():
    while True:
        SCREEN.blit(BG_START, (0,0))
        
        TEXT_SCORE = Button(pos=(70,25), 
                            font=get_font(15), 
                            text_input=f'Skor : {player.score}', 
                            base_color='White', 
                            hovering_color=None)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit() 

            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    player.player_x = -10
                if event.key == K_RIGHT:
                    player.player_x = 10
                if event.key == K_SPACE:
                    if player.bullet_status is 'ready':
                        player.bullet_rect.x = player.player_rect.x + 32
                        player.shoot()
            if event.type == KEYUP:
                if event.key == K_LEFT or event.key == K_RIGHT:
                    player.player_x = 0

        player.player_rect.x += player.player_x

        # RESTRICT PLAYER MOVEMENT
        if player.player_rect.x <= -15:
            player.player_rect.x = -15
        elif player.player_rect.x >= 1200:
            player.player_rect.x = 1200 

        # ENEMY MOVEMENET
        if enemy.posisi_kiri == True:
            # RESTRICT ENEMY MOVEMENT
            if enemy.pindah_bawah == False and enemy.gerak_x(enemy.enemy_rect.x):
                enemy.posisi_kiri = False
                enemy.posisi_kanan = True
                enemy.enemy_rect.y += enemy.enemy_y
                enemy.pindah_bawah = True
            else:
                enemy.pindah_bawah = False
                enemy.enemy_rect.x += enemy.enemy_x
        if enemy.posisi_kanan == True:
            # RESTRICT ENEMY MOVEMENT
            if enemy.pindah_bawah == False and enemy.gerak_x(enemy.enemy_rect.x): 
                enemy.posisi_kiri = True
                enemy.posisi_kanan = False
                enemy.enemy_rect.y += enemy.enemy_y
                enemy.pindah_bawah = True
            else:
                enemy.pindah_bawah = False
                enemy.enemy_rect.x -= enemy.enemy_x

        # COLLISION BETWEEN PLAYER AND ENEMY
        if is_fall(player.player_rect.x, player.player_rect.y, enemy.enemy_rect.x, enemy.enemy_rect.y):
            pause()

        # COLLISION BETWEEN BULLET AND ENEMY
        if is_collision(player.bullet_rect.x, player.bullet_rect.y, enemy.enemy_rect.x, enemy.enemy_rect.y):
            player.bullet_rect.y = 750
            player.bullet_status = 'ready'
            player.score += 1
                
        # RESTRICT BULLET MOVEMENT
        if player.bullet_rect.y <= 0:
            player.bullet_rect.y = 720 - (48 - 12)
            player.bullet_status = 'ready'
        
        # BULLET MOVEMENT
        if player.bullet_status is 'fire':
            player.shoot()
            player.bullet_rect.y -= player.bullet_y
        
        TEXT_SCORE.update()
        SCREEN.blit(enemy.enemy_image, enemy.enemy_rect)
        SCREEN.blit(player.player_image, player.player_rect)
        
        pygame.display.update()
        CLOCK.tick(FPS)
               
def pause():
    while True:
        SCREEN.fill(BG_PAUSE)
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        
        TITLE_TEXT = Button(pos=(650, 150), 
                              font=get_font(60), 
                              text_input='PERMAINAN SELESAI !', 
                              base_color='White', 
                              hovering_color=None)
        SCORE_TEXT = Button(pos=(650, 250), 
                             font=get_font(30), 
                             text_input=f'Skor : {player.score}', 
                             base_color='White', 
                             hovering_color=None)
        PLAY_AGAIN_BUTTON = Button(pos=(650, 425), 
                              font=get_font(60), 
                              text_input='PLAY AGAIN', 
                              base_color='White', 
                              hovering_color='#fcfc03')
        QUIT_BUTTON = Button(pos=(650, 525), 
                             font=get_font(60), 
                             text_input='QUIT', 
                             base_color='White', 
                             hovering_color='#fc2003')
        
        for button in [TITLE_TEXT, SCORE_TEXT, PLAY_AGAIN_BUTTON, QUIT_BUTTON]:
            button.hover_button(MENU_MOUSE_POS)
            button.update()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == MOUSEBUTTONDOWN:
                if PLAY_AGAIN_BUTTON.click_button(MENU_MOUSE_POS):
                    start()
                if QUIT_BUTTON.click_button(MENU_MOUSE_POS):
                    pygame.quit()
                    
        pygame.display.update()

player = Player()
enemy = Enemy()
main_menu()