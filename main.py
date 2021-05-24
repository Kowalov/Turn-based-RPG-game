import pygame
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

#Game window
bottom_panel = 150
screen_width = 800
screen_hight = 400 + bottom_panel

screen = pygame.display.set_mode((screen_width, screen_hight))
pygame.display.set_caption("Game name")


#Game variables
current_fighter = 1
total_fighters = 3
action_cooldown = 0
action_wait_time = 90
attack = False
potions = False
clicked = False


#Def fonts
font = pygame.font.SysFont('Times New Roman', 26)

#define colours
red = (255,0,0)
green = (0,255,0)

#Load images
#Background image
background_img = pygame.image.load('img/background/background.png').convert_alpha()
#Bottom panel
panel_img = pygame.image.load('img/icons/panel.png').convert_alpha()
#sword image
sword_img = pygame.image.load('img/icons/sword.png').convert_alpha( )

#Drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#Drawing background function
def draw_bg():
    screen.blit(background_img, (0,0))
#Drawing panel function
def draw_pn():
    #draw panel
    screen.blit(panel_img, (0,screen_hight - bottom_panel))
    #show knight stats
    draw_text(f'{knight.name} HP: {knight.hp}', font, red, 100, screen_hight - bottom_panel + 10)
    for count, i in enumerate(bandit_list):
        #show name and health
        draw_text(f'{i.name} HP: {i.hp}', font, red, 550, (screen_hight - bottom_panel + 10) + count * 60)

#Fighter class
class Fighter():
    def __init__(self, x, y, name, max_hp, strength, potions):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.potions = potions
        self.start_potions = potions
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0  #0:idle, 1:attack, 2:hurt, 3:dead
        self.update_time = pygame.time.get_ticks()

        #load idle images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'img/{self.name}/Idle/{i}.png')
            img = pygame.transform.scale(img, (img.get_width()*3, img.get_height()*3))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # load attack images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'img/{self.name}/Attack/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


    def draw(self):
        screen.blit(self.image, self.rect)


    def update(self):
        animation_cooldown = 100
        #handle animation
        #update image
        self.image = self.animation_list[self.action][self.frame_index]

        #check how much time passed since last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        #reset animation back to the start
        if self.frame_index >=  len(self.animation_list[self.action]):
            self.idle()

    #Resets animation to idle
    def idle(self):
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()


    def attack(self, target):
        #deal damage
        rand = random.randint(-5, 5)
        damage = self.strength + rand
        target.hp -= damage

        #check if dead
        if target.hp < 1:
            target.hp = 0
            target.alive = False

        #set animation to attack
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()



class Healthbar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, hp):
        #new health updating
        self.hp = hp
        #health ratio
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))


knight = Fighter(200,260,'Knight',30,10,3)
bandit1 = Fighter(550,270,'Bandit',20,6,1)
bandit2 = Fighter(700,270,'Bandit',20,6,1)

bandit_list = []
bandit_list.append(bandit1)
bandit_list.append(bandit2)

knight_health_bar = Healthbar(100, screen_hight - bottom_panel + 40, knight.hp, knight.max_hp)
bandit1_health_bar = Healthbar(550, screen_hight - bottom_panel + 40, bandit1.hp, bandit1.max_hp)
bandit2_health_bar = Healthbar(550, screen_hight - bottom_panel + 100, bandit2.hp, bandit2.max_hp)

run = True
while run:

    clock.tick(fps)

    #draw background
    draw_bg()
    #draw panel
    draw_pn()
    knight_health_bar.draw(knight.hp)
    bandit1_health_bar.draw(bandit1.hp)
    bandit2_health_bar.draw(bandit2.hp)

    #draw fighters
    knight.update()
    knight.draw()
    for bandit in bandit_list:
        bandit.update()
        bandit.draw()

    #control player action
    #reset action variables
    attack = False
    potions = False
    target = None
    #make sure mouse if visible
    pygame.mouse.set_visible(True)
    pos = pygame.mouse.get_pos()
    for count, bandit in enumerate(bandit_list):
        if bandit.rect.collidepoint(pos):
            pygame.mouse.set_visible(False)
            #show short in place of mouse
            screen.blit(sword_img, pos)



    #player action
    if knight.alive == True:
        if current_fighter == 1:
            action_cooldown += 1
            if action_cooldown >= action_wait_time:
                #look for player action
                #attack
                knight.attack(bandit1)
                current_fighter += 1
                action_cooldown = 0


    #enemy action
    for count, bandit in enumerate(bandit_list):
        if current_fighter == 2 + count:
            if bandit.alive == True:
                action_cooldown += 1
                if action_cooldown >= action_wait_time:
                    bandit.attack(knight)
                    current_fighter += 1
                    action_cooldown = 0
            else:
                current_fighter += 1

    #reset back to the begining after all moves
    if current_fighter > total_fighters:
        current_fighter = 1


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()