import pygame

#initializing pygame
pygame.init()

#setting up the clock and the fps so that the while loop doesnt mess our animations
clock = pygame.time.Clock()
fps = 60 #can be anything

#setup screen size and display screen
bottom_panel = 150
screen_width = 800
screen_height = 512 + bottom_panel
screen = pygame.display.set_mode((screen_width, screen_height))

#just setting the title of the window
pygame.display.set_caption('Final x Journey')

#load background image
bg_img = pygame.image.load('Img/Background/1.png').convert_alpha()

#load bottom panel bar
panel_img = pygame.image.load('Img/GUI/panel.png').convert_alpha()

#function to draw the background in game window
def draw_bg():
    screen.blit(bg_img, (0,0))

#function to draw the bottom panel bar in game window
def draw_panel():
    screen.blit(panel_img, (0,screen_height - bottom_panel))


#Classes 
class character():
    def __init__(self, x, y, name, max_hp, strength, health_potions):
        self.name = name     
        self.max_hp = max_hp   



#have to set run as true so pygame can use a while to loop through it 
run = True
while run:
    
    #fix constant fps 
    clock.tick(fps)  #equivalent to pygame.time.Clock().tick(60)   

    #draw the background and panel
    draw_bg()
    draw_panel()

    #pygame event listner 
    for event in pygame.event.get():
        #checks whether the program window has been closed or not
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

#closing pygame 
pygame.quit()
