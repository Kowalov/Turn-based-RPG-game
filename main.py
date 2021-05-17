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

#Load images
#Background image
background_img = pygame.image.load('img/background/background.png').convert_alpha()
#Bottom panel
panel_img = pygame.image.load('img/icons/panel.png').convert_alpha()

#Drawing background function
def draw_bg():
    screen.blit(background_img, (0,0))
#Drawing panel function
def draw_pn():
    screen.blit(panel_img, (0,screen_hight - bottom_panel))


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
        self.update_time = pygame.time.get_ticks()
        for i in range(8):
            img = pygame.image.load(f'img/{self.name}/Idle/{i}.png')
            img = pygame.transform.scale(img, (img.get_width()*3, img.get_height()*3))
            self.animation_list.append(img)
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        animation_cooldown = 100
        #handle animation
        #update image
        self.image = self.animation_list[self.frame_index]

        #check how much time passed since last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1


knight = Fighter(200,260,'Knight',30,10,3)
bandit1 = Fighter(550,270,'Bandit',20,5,1)
bandit2 = Fighter(700,270,'Bandit',20,5,1)

bandit_list = []
bandit_list.append(bandit1)
bandit_list.append(bandit2)


run = True
while run:

    clock.tick(fps)

    #draw background
    draw_bg()
    #draw panel
    draw_pn()
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