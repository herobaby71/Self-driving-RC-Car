import pygame
import pygame.font
import numpy as np
import cv2
import sys
import time
from control import simpleControl


#Useful constants
BLACK = (0,0,0)
WHITE = (255,255,255)
SIZE = (640,480)

def CV2PYGAME(image):
    #image = cv2.cvtColor(image,cv2.COLOR_GRAY2RGB)
    image = np.rot90(cv2.cvtColor(image,cv2.COLOR_BGR2RGB))
    return pygame.surfarray.make_surface(image)

class RCControl:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Control The RC Car w/ Arrows :)")
        self.size = SIZE
        self.screen = pygame.display.set_mode(self.size)
        self.QUIT = False

        #key commands:
        self.keys = {0:"forward", 1:"forward_left", 2:"forward_right", 3:"reverse",
            4:"reverse_left", 5:"reverse_right", 6:"idle", 7:"right", 8:"left"}
        
        #Update the background 
        self.updateBackground('Use arrows to move')
        
        #control arrows False: not pressed/ True: pressed
        self.UP = False
        self.DOWN = False
        self.LEFT = False
        self.RIGHT = False
    #Key '0' is for pausing
    def P(self):
        #p: pause, r:start taking data points
        p = False
        s = False
        n = False
        keys = pygame.key.get_pressed()
        if(keys[pygame.K_p]):
            p = True
        if(keys[pygame.K_n]):
            n = True
        if(keys[pygame.K_s]):
            s = True
        return (p,s,n)
    def getKeys(self):
        #change if they pressed keys are changed. update if there are changes and return True
        changed = False
        up = down = left = right = False
        keys = pygame.key.get_pressed()            
        if keys[pygame.K_UP]:
            up = True
        if keys[pygame.K_DOWN]:
            down = True
        if keys[pygame.K_LEFT]:
            left = True
        if keys[pygame.K_RIGHT]:
            right = True
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                self.QUIT = True
                self.quit()
        if (self.UP,self.DOWN,self.LEFT,self.RIGHT) != (up,down,left,right):
            self.UP,self.DOWN,self.LEFT,self.RIGHT = up,down,left,right
            changed = True
        return changed
    #update the background with recent commands
    def updateBackground(self, txt):
        big_font = pygame.font.Font(None, 40)
        text = big_font.render(txt, 1, WHITE)
        text_position = text.get_rect(centerx=self.size[0] / 2)
        background = pygame.Surface(self.screen.get_size())
        background.blit(text, text_position)
        self.setScreen(background)

    #get the commands
    def getCommand(self):             
        command_key = 6
        if(self.UP):
            command_key = 0
            if(self.LEFT):
                command_key=1
            elif(self.RIGHT):
                command_key=2
        elif(self.DOWN):
            command_key = 3
            if(self.LEFT):
                command_key=4
            elif(self.RIGHT):
                command_key=5
        elif(self.RIGHT):
            command_key = 7
        elif(self.LEFT):
            command_key = 8
        return command_key

    #Send commands through Control simpleCommand
    def simpleControl(self, com):
        simpleControl(com)
        
    def start(self):
        clock = pygame.time.Clock()

        while(not self.QUIT):
            if(self.getKeys()):                
                command_key = self.getCommand()
                #send commands to server
                self.simpleControl(command_key)
                self.updateBackground(self.keys[command_key])

            #limit 20 frames per sec
            clock.tick(60)
            
       
    def setScreen(self,image):
        self.screen.blit(image,(0,0))
        pygame.display.update()
        pygame.display.flip()
    def quit(self):
        self.QUIT = True
        pygame.quit()
    
def main():
    a = RCControl()
    a.start()

if __name__ == "__main__":
    main ()
