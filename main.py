import pygame

#initializing pygame
pygame.init()

#setting up the clock and the fps so that the while loop doesnt mess our animations
clock = pygame.time.Clock()
fps = 60 #can be anything

#setup screen size and display screen
#Maybe get new panel designs
bottom_panel = 150
screen_width = 800
screen_height = 512 + bottom_panel
screen = pygame.display.set_mode((screen_width, screen_height))

font = pygame.font.SysFont('Time New Roman', 35)
red = (255,0,0)
green = (0,255,0)
white = (255,255,255)

#just setting the title of the window
pygame.display.set_caption('Final x Journey')

#load background image
bg_img = pygame.image.load('Img/Background/1.png').convert_alpha()

#load bottom panel bar
panel_img = pygame.image.load('Img/GUI/panel.png').convert_alpha()

#function to draw the background in game window
def draw_bg():
    screen.blit(bg_img, (0,0))

#function to display text in the game window
def draw_text(text, font, text_col, x, y):
    image = font.render(text, True, text_col)
    screen.blit(image, (x,y))

#function to draw the bottom panel bar in game window
def draw_panel():
    #display the panel box
    screen.blit(panel_img, (0,screen_height - bottom_panel))
    #display knight stats
    draw_text(f'{knight.name} HP:{knight.hp}', font, red, 100, screen_height - bottom_panel + 10 )
    gap_between_lines = 0
    for count, i in enumerate(skeleton_list):        
        draw_text(f'{i.name} {count+1} HP:{i.hp}', font, red, 500, screen_height - bottom_panel + 10 + gap_between_lines)
        gap_between_lines +=60


#Classes TODO: maybe add child classes to solve the animation cutting in half due to variable number of images for each character and their actions
class character():
    def __init__(self, x, y, name, max_hp, strength, health_potions):
        self.name = name     
        self.max_hp = max_hp   
        self.hp = max_hp
        self.strength = strength
        self.start_health_potions = health_potions
        self.health_potions = health_potions
        self.alive = True
        #This section is for animation
        self.animation_list = [] 
        self.frame = 0
        self.update_time = pygame.time.get_ticks()
        self.action = 1 #action 0:Idle 1:Attack 2:Hit taken 3:Dead

        #for different actions we have different animations so we need to store them 
        #here the range index is the number of images in the sprite/ the animation folder for each actions

        #Store the idle animation images 
        temp_list = []
        number_of_images = 0     #Doing this as there is different number of images for knight and skeleton for animation
        if self.name == "Knight":
            number_of_images = 10
        if self.name == "Skeleton":
            number_of_images = 11
        for i in range(number_of_images): #loop through 10 images in our animation 
            image = pygame.image.load(f'Img/Characters/{self.name}/Animation/Idle/{i+1}.png')
            image = pygame.transform.scale(image, (image.get_width() *4, image.get_height() *4))
            temp_list.append(image)
        self.animation_list.append(temp_list)

        #Store the attack animation images 
        temp_list = []
        number_of_images = 0 
        if self.name == "Knight":
            number_of_images = 6
        if self.name == "Skeleton":
            number_of_images = 18
        for i in range(number_of_images): #loop through 10 images in our animation 
            image = pygame.image.load(f'Img/Characters/{self.name}/Animation/Attack/{i+1}.png')
            image = pygame.transform.scale(image, (image.get_width() *4, image.get_height() *4))
            temp_list.append(image)
        self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def draw(self):
        screen.blit(self.image, self.rect)

    #if the time exceeds 85ms then the frame is updated by a new image using this update function
    def update_animation(self):
        animation_cooldown = 85 #this is 100ms
        self.image = self.animation_list[self.action][self.frame]

        if (pygame.time.get_ticks() - self.update_time > animation_cooldown):
            self.update_time = pygame.time.get_ticks()
            self.frame +=1 
        if (self.frame >= len(self.animation_list[self.action])):
            self.frame = 0

#Class for the health bar
class health_bar: 
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp   #current hp
        self.max_hp = max_hp
        self.health_bar_length = 200
        self.health_ratio = self.max_hp/self.health_bar_length
        self.health_change_speed = 5

    def draw(self,hp):
        pygame.draw.rect(screen, red, (self.x,self.y, self.hp/self.health_ratio, 20))
        pygame.draw.rect(screen, white, (self.x,self.y, self.health_bar_length, 20),4)   #here 4 is the width of the border   

#create objects from the classes here
knight = character(200,300,'Knight',30,5,3)
skeleton1 = character(500,400,'Skeleton',10,2,1)
skeleton2 = character(600,400,'Skeleton',10,2,1)

#make a list to store the skeletons/villains
skeleton_list = []
skeleton_list.append(skeleton1)
skeleton_list.append(skeleton2)

# skeleton1.hp = 1 #test to see if the health is decreasing in the health bar

#health bar instances
knight_health_bar = health_bar(100, screen_height - bottom_panel + 40, knight.hp, knight.max_hp)
skeleton1_health_bar = health_bar(500, screen_height - bottom_panel + 40, skeleton1.hp, skeleton1.max_hp)
skeleton2_health_bar = health_bar(500, screen_height - bottom_panel + 100, skeleton2.hp, skeleton2.max_hp)


#have to set run as true so pygame can use a while to loop through it 
run = True
while run:
    
    #fix constant fps 
    clock.tick(fps)  #equivalent to pygame.time.Clock().tick(60)   

    #draw the background 
    draw_bg()

    #Draw the bottom panels and the health bars in them
    draw_panel() #draw panel contains draw texts which displays the texts
    knight_health_bar.draw(knight.hp)
    skeleton1_health_bar.draw(skeleton1.hp)
    skeleton2_health_bar.draw(skeleton2.hp)

    #draw our hero knight and other characters (skeleton used as the other character for now)
    knight.update_animation()
    knight.draw()
    for villain in skeleton_list:
        villain.update_animation()
        villain.draw()

    #pygame event listner 
    for event in pygame.event.get():
        #checks whether the program window has been closed or not
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

#closing pygame 
pygame.quit()
