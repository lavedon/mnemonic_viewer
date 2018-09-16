import logging
import pdb

logging.basicConfig(filename='viewer.log', filemode='w', format='%(levelname)s:%(asctime)s %(message)s', level=logging.DEBUG)

import pygame
from pygame.locals import *
import os
import fnmatch
import get_palace 
import textrect


class App:
        def __init__(self):
                logging.debug('class App called')
                self._running = True
                self.image_count = 0
                self.clock = None

                self.text_surface1_flag = False 
                self.text_surface2_flag = False
                self.text_surface3_flag = False
                self.image_flag = True 

                self.select_which = 0
                self.select_menu = None
                self.palaces = ["Sales", "History", "Coding"]

        def on_init(self):
                pygame.init()
                self.joystick = pygame.joystick.Joystick(0)
                self.joystick.init()
                logging.info('joystick initialized')
                logging.info('pygame initialized')
                self.display_surf = pygame.display.set_mode((1800, 800), HWSURFACE | DOUBLEBUF | RESIZABLE)
                self.display_caption = pygame.display.set_caption('Space is the Place')
                self._running = True
                self.clock = pygame.time.Clock()

        def on_event(self, event):
                if event.type == pygame.QUIT:
                        self._running = False
                     # Joystick Input
                if event.type == pygame.JOYBUTTONDOWN:
                        logging.info('a controller button was pressed')
                        if self.joystick.get_button(0):
                            logging.info('Controller button 0 pressed')
                            self.text_surface1_flag = not self.text_surface1_flag
                        elif self.joystick.get_button(1):
                            logging.info('Controller button 1 pressed')
                            self.text_surface2_flag = not self.text_surface2_flag
                        elif self.joystick.get_button(2):
                            logging.info('Controller button 2 pressed' )
                            self.text_surface3_flag = not self.text_surface3_flag
                        elif self.joystick.get_button(3):
                            logging.info('Controller button 3 pressed')
                            self.image_flag = not self.image_flag
                        elif self.joystick.get_button(4):
                            logging.info('Controller button 4 pressed')
                            self.image_count -= 1 
                        elif self.joystick.get_button(5):
                            logging.info('Controller button 5 pressed.')
                            self.image_count += 1
                        elif self.joystick.get_button(6):
                            logging.info('Controller button 6 pressed.')
                        elif self.joystick.get_button(7):
                            logging.info('Controller button 7 pressed.')

        def on_render(self):
                black = 0, 0, 0

                self.display_surf.fill(black)
                if self.image_flag == True:
                    self.display_surf.blit(theData.image_list_surf[self.image_count], (0, 0))
                if self.text_surface1_flag == True:
                    self.display_surf.blit(theData.loci_list_surf[self.image_count], (50, 40))
                if self.text_surface2_flag == True:
                    self.display_surf.blit(theData.facts_list_surf[self.image_count], (50, 120))
                if self.text_surface3_flag == True:
                    self.display_surf.blit(theData.mnemonics_list_surf[self.image_count], (50, 250))
                if self.select_which > 0:
                    self.display_surf.blit(self.select_menu, (250, 250))

                pygame.display.flip()

        def on_cleanup(self):
                pygame.quit()

        def on_execute(self):
                
                if self.on_init() == False:
                        logging.info('App.on_execute if self.on_init() == False RUNNING')
                        self._running = False

                while (self._running):
                        self.clock.tick(27)
                        for event in pygame.event.get():
                                self.on_event(event)
                        self.on_render()
                self.on_cleanup()
        

class Data:
        def __init__(self):
                logging.debug('class Data called.')
                self.folder = None 
                self.image_list = [] 
                self.image_list_surf = [] 
                self.loci_list = [] 
                self.loci_list_surf = [] 
                self.facts_list = [] 
                self.facts_list_surf = []
                self.mnemonics_list = [] 
                self.mnemonics_list_surf = [] 
                self.image_files_list = [] 
                self.image_rect = None


                pygame.init()
                self.font_1 = pygame.font.Font(None, 72)
                self.font_2 = pygame.font.Font(None, 52)
                self.get_from_palace()
                self.get_images()

        def get_from_palace(self):
                dreddPalace = get_palace.Memory_Palace(0)
                self.loci_list = dreddPalace.loci
                self.facts_list = dreddPalace.facts
                self.mnemonics_list = dreddPalace.mnemonics
                self.image_files_list = dreddPalace.image_files

        def get_images(self):
            for loci in self.loci_list:
                self.loci_list_surf.append(self.font_1.render(loci, False, (0, 255, 0)))
            for image in self.image_files_list:
                filename = os.path.join('C:\\Users\\Luke\\Desktop\\Memory Palace\\Palaces\\Dredd', image)
                self.image_list_surf.append(pygame.image.load(filename))
            for fact in self.facts_list:
                self.image_rect = self.image_list_surf[0].get_rect()
                self.image_rect.width = self.image_rect.width - 200
                self.image_rect.height = self.image_rect.height - 400
                self.facts_list_surf.append(textrect.render_textrect(fact, self.font_2, self.image_rect, (255, 255, 255), (0, 0, 0), 1))

            for mnemonic in self.mnemonics_list:
                # self.mnemonics_list_surf.append(self.font_2.render(mnemonic, False, (139, 0, 139))) 
                self.mnemonics_list_surf.append(textrect.render_textrect(mnemonic, self.font_2, self.image_rect, (255, 255, 255), (0, 0, 0), 0))
      
class Viewer:
    def __init__(self):
        self.caption = "Memory Palace 3000"
        


if __name__ == "__main__" :
    theData = Data()
    theApp= App()
    theApp.on_execute()
