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
blue = (26,144,235)
white = (255,255,255)

#Set game variables IMP!!!
current_character = 1
total_characters = 3
action_cooldown = 0 
action_wait_time = 130
attack = False 
health_potion = False 
clicked = False

#just setting the title of the window
pygame.display.set_caption('Final x Journey')

#load background image
bg_img = pygame.image.load('Img/Background/1.png').convert_alpha()

#load bottom panel bar
panel_img = pygame.image.load('Img/GUI/panel.png').convert_alpha()

#load mouse sword icon image 
mouse_sword_icon = pygame.image.load('Img/Icon/mouse_sword_icon.png').convert_alpha()

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
    draw_text(f'{knight.name} Mana:{knight.mana}', font, blue, 100, screen_height - bottom_panel + 70 )
    #display skeleton stats
    gap_between_lines = 0
    for count, i in enumerate(skeleton_list):        
        draw_text(f'{i.name} {count+1} HP:{i.hp}', font, red, 500, screen_height - bottom_panel + 10 + gap_between_lines)
        gap_between_lines +=60

#To get the number of images involved in the animation
#CAN MAKE THIS A DICTIONARY OF A DICTIONARY???
def number_of_images_in_animation(name, action):    
    if action == "Idle":
        if name == "Knight":
            return 10
        elif name == "Skeleton":
            return 11
    elif action == "Attack":
        if name == "Knight":
            return 6
        elif name == "Skeleton":
            return 18
    elif action == "Dead":
        if name == "Knight":
            return 10
        elif name == "Skeleton":
            return 15
    return 0

#Common function for animating actions
#store the images that is required for the animation in a 2D list 
#self.animation_list[self.action][self.frame], here the below function returns a list temp_list which
# is a list of all images required for a particular action, that list is then appeneded in the animation list
def animation_images_list(name, action):
    number_of_images = number_of_images_in_animation(name,action)
    temp_list = []
    #for different actions we have different animations so we need to store them 
    #here the range index is the number of images in the sprite/ the animation folder for each actions
    for i in range(number_of_images): #loop through 10 images in our animation 
            image = pygame.image.load(f'Img/Characters/{name}/Animation/{action}/{i+1}.png')
            image = pygame.transform.scale(image, (image.get_width() *4, image.get_height() *4))
            temp_list.append(image)
    return temp_list

class character():
    def __init__(self, x, y, name, max_hp, strength, health_potions, max_mana = 0):
        self.x = x #storing x coordinate of where the character image will be drawn
        self.y = y #storing y coordinate of where the character image will be drawn
        self.name = name     
        self.max_hp = max_hp   
        self.hp = max_hp
        self.max_mana = max_mana   
        self.mana = max_mana
        self.strength = strength
        self.start_health_potions = health_potions
        self.health_potions = health_potions
        self.alive = True

        #This section is for animation
        self.animation_list = [] 
        self.frame = 0        
        self.action = 0 #action 0:Idle 1:Attack 2:Dead 3:Hit_taken
        self.update_time = pygame.time.get_ticks()

        #Store the idle animation images into the 2D nested animation_list
        self.animation_list.append(animation_images_list(self.name, "Idle"))
        self.animation_list.append(animation_images_list(self.name, "Attack"))
        self.animation_list.append(animation_images_list(self.name, "Dead"))

        self.image = self.animation_list[self.action][self.frame] #inital image [0][0]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)     
           

    def draw(self):
        screen.blit(self.image, self.rect)

    #if the time exceeds 85ms then the frame is updated by a new image using this update function
    def update_animation(self):      
        animation_cooldown = 85 #this is 100ms
        self.image = self.animation_list[self.action][self.frame]
        self.rect = self.image.get_rect()
        if self.name != "Knight" and self.action==1:
            self.rect.center = (220,380)  
        else:
            self.rect.center = (self.x,self.y)
        
        if (pygame.time.get_ticks() - self.update_time > animation_cooldown):
            self.update_time = pygame.time.get_ticks()
            self.frame +=1 
        #This determines what happens when we run out of frames for animation
        if (self.frame >= len(self.animation_list[self.action])):                       
            if self.alive == False:
                self.frame = len(self.animation_list[2]) - 1               
            else:
                self.idle()

    def idle(self):
        #set idle animation
        self.action = 0
        self.frame = 0
        self.update_time = pygame.time.get_ticks()

    def dead(self):
        #set death animation
        self.action = 2
        self.frame = 0
        self.update_time = pygame.time.get_ticks()
    
    def attack(self, target):
        #how much damage to deal?
        damage = self.strength
        target.hp -= damage

        #set attack animation
        self.action = 1
        self.frame = 0
        self.update_time = pygame.time.get_ticks()

        #check if target is dead 
        if target.hp <1:
            target.hp = 0
            target.alive = False
            target.dead()

#Class for the health bar
class health_bar: 
    def __init__(self, x, y, hp, max_hp, mana = 0 , max_mana = 0):
        self.x = x
        self.y = y
        self.hp = hp   #current hp
        self.max_hp = max_hp
        self.mana = mana   #current MANA
        self.max_mana = max_mana
        self.health_bar_length = 200
        self.health_ratio = self.max_hp/self.health_bar_length
        self.mana_ratio = self.max_mana/self.health_bar_length
        self.health_change_speed = 5

    def draw(self,hp):
        self.hp = hp        
        # pygame.draw.rect(screen, red, (self.x,self.y, self.hp/self.health_ratio, 20))
        pygame.draw.rect(screen, green, (self.x,self.y, self.hp/self.health_ratio, 20))
        pygame.draw.rect(screen, white, (self.x,self.y, self.health_bar_length, 20),4)   #here 4 is the width of the border   

    def draw_mana_bar(self,mana):
        pygame.draw.rect(screen, blue, (self.x,self.y, self.mana/self.mana_ratio, 20))
        pygame.draw.rect(screen, white, (self.x,self.y, self.health_bar_length, 20),4)   #here 4 is the width of the border   

knight = character(200,300,'Knight',30,5,3,20)
skeleton1 = character(500,400,'Skeleton',10,20,1)
skeleton2 = character(600,400,'Skeleton',10,2,1)

#make a list to store the skeletons/villains
skeleton_list = []
skeleton_list.append(skeleton1)
skeleton_list.append(skeleton2)

# skeleton1.hp = 1 #test to see if the health is decreasing in the health bar

#health bar instances
knight_health_bar = health_bar(100, screen_height - bottom_panel + 40, knight.hp, knight.max_hp)
#used the same health bar class to store the mana details as well but made the mana values optional
knight_mana_bar = health_bar(100, screen_height - bottom_panel + 100, 0,0,knight.mana, knight.max_mana)
skeleton1_health_bar = health_bar(500, screen_height - bottom_panel + 40, skeleton1.hp, skeleton1.max_hp)
skeleton2_health_bar = health_bar(500, screen_height - bottom_panel + 100, skeleton2.hp, skeleton2.max_hp)


#have to set run as true so pygame can use a while to loop through it 
#MAIN GAME LOOOOP!!!
run = True
while run:
    
    #fix constant fps 
    clock.tick(fps)  #equivalent to pygame.time.Clock().tick(60)   

    #draw the background 
    draw_bg()

    #Draw the bottom panels and the health bars in them
    draw_panel() #draw panel contains draw texts which displays the texts
    knight_health_bar.draw(knight.hp)
    knight_mana_bar.draw_mana_bar(knight.hp)
    skeleton1_health_bar.draw(skeleton1.hp)
    skeleton2_health_bar.draw(skeleton2.hp)

    #draw our hero knight and other characters (skeleton used as the other character for now)
    knight.update_animation()
    knight.draw()
    for villain in skeleton_list:
        villain.update_animation()
        villain.draw()

#Player action section 
    #RESET ACTION VARIABLES 
    attack = False 
    health_potion = False 
    target = None

    #Change mouse pointer icon to a sword when hovering over an enemy
    #make mouse pointer visible 
    pygame.mouse.set_visible(True)
    mouse_pos = pygame.mouse.get_pos()
    for count, skeleton in enumerate(skeleton_list):
        if skeleton.rect.collidepoint(mouse_pos):
            if skeleton.alive == True:
                #hide the mouse and display our sword mouse icon
                pygame.mouse.set_visible(False)
                screen.blit(mouse_sword_icon, mouse_pos)
                if clicked == True:
                    attack = True 
                    target = skeleton_list[count]

    #KNIGHT ACTION / PLAYER ACTION  
    if knight.alive == True:
        if current_character == 1:
            action_cooldown +=1
            if action_cooldown >= action_wait_time:
                #Do some player action 
                #Do attack action 
                if attack == True and target != None:
                    knight.attack(target)
                    current_character +=1
                    action_cooldown = 0 

    #SKELETON ACTION / ENEMY ACTION 
    if knight.alive == True:
        for count, skeleton in enumerate(skeleton_list):
            if current_character == (2+count):
                if skeleton.alive == True:            
                        action_cooldown +=1
                        if action_cooldown >= action_wait_time:
                            #Do some enemy action 
                            #Do attack action for skeleton
                            skeleton.attack(knight)                                               
                            current_character +=1
                            action_cooldown = 0 
                else:                
                    current_character +=1

    #if all fighters have had a turn then reset
    if current_character > total_characters:
        current_character = 1
            
    #pygame event listner 
    for event in pygame.event.get():
        #checks whether the program window has been closed or not
        if event.type == pygame.QUIT:
            run = False

        #check when mouse is clicked 
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        else: 
            clicked = False

    pygame.display.update()

#closing pygame 
pygame.quit()
