import pygame

pygame.init()

clock = pygame.time.Clock()
fps = 60

#Game window
bottom_panel = 150
screen_width = 800
screen_hight = 400 + bottom_panel

screen = pygame.display.set_mode((screen_width, screen_hight))
pygame.display.set_caption("Game name")

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
            self.frame_index = 0



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


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()