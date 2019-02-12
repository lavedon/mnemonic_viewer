import pdb
import logging

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

                self.palaces = ["History", "Sales", "Coding"]

        def on_init(self):
                pygame.init()
                logging.info('pygame initialized')
                self.display_surf = pygame.display.set_mode((2000, 1200), HWSURFACE | DOUBLEBUF | RESIZABLE)
                self.display_caption = pygame.display.set_caption('Space is the Place')
                self._running = True
                self.clock = pygame.time.Clock()

        def on_event(self, event):
                if event.type == pygame.QUIT:
                        self._running = False
                     # Joystick Input
                if event.type == pygame.KEYDOWN:
                        logging.info('a controller button was pressed')
                        if event.key == pygame.K_a:
                            logging.info('Controller button 0 pressed')
                            self.text_surface1_flag = not self.text_surface1_flag
                        elif event.key == pygame.K_s:
                            logging.info('Controller button 1 pressed')
                            self.text_surface2_flag = not self.text_surface2_flag
                        elif event.key == pygame.K_d:
                            logging.info('Controller button 2 pressed' )
                            self.text_surface3_flag = not self.text_surface3_flag
                        elif event.key == pygame.K_f:
                            logging.info('Controller button 3 pressed')
                            self.image_flag = not self.image_flag
                        elif event.key == pygame.K_h:
                            logging.info('Controller button 4 pressed')
                            self.image_count -= 1 
                        elif event.key == pygame.K_l:
                            logging.info('Controller button 5 pressed.')
                            self.image_count += 1
                        elif event.key == pygame.K_SPACE:
                            logging.info('Controller button 6 pressed.')
                            # Besides start-up zero is never reached.
                            # Select Menu closes.  Reset to 0. theData.select_which = 0.  
                            # See line 80
                            # When select button pressed , 1 is added instantly
                            # Before the menu can even display.
                            # Skipping the first menu item before the menu opens.
                            theData.select_which += 1
                            # Always open the select menu when select is pressed
                            if theData.select_menu_open == False:
                                theData.select_menu_open = True
                            if theData.select_which >= len(theData.sheet_list):
                                theData.select_which = 0 
                                logging.debug("Start On? %s", theData.start_up)
                                logging.debug("select_which is %s", theData.select_which)
                                theData.select_menu_open = False
                        elif event.key == pygame.K_RETURN:
                            logging.info('Controller button 7 pressed.')
                            if theData.select_menu_open:
                                theData.select_menu_open = False
                                logging.debug("Call get from palace()")
                                theData.get_from_palace() 
                                logging.debug("Turn off Start_up %", theData.start_up)
                                theData.start_up = False
                                logging.debug("Call get_images")
                                theData.get_images()

        def on_render(self):
                black = 0, 0, 0

                self.display_surf.fill(black)

                if theData.start_up:
                    self.display_surf.blit(theData.select_menu(), (250, 250))
                else:
                    if self.image_flag:
                        self.display_surf.blit(theData.image_list_surf[self.image_count], (0, 0))
                    if self.text_surface1_flag:
                        self.display_surf.blit(theData.loci_list_surf[self.image_count], (50, 40))
                    if self.text_surface2_flag:
                        self.display_surf.blit(theData.facts_list_surf[self.image_count], (50, 120))
                    if self.text_surface3_flag:
                        self.display_surf.blit(theData.mnemonics_list_surf[self.image_count], (50, 250))
                    if theData.select_menu_open:
                        self.display_surf.blit(theData.select_menu(), (250, 250))

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


                self.start_up = True
                self.select_which = 0
                self.select_menu_open = False

                self.sheet_list = []
                #  the local location of folders with various palace images
                self.folder_locations = [
                        'C:\\Users\\Luke\\Documents\\Memory Palace\\Palaces\\Dredd',
                        'C:\\Users\\Luke\\Documents\\Memory Palace\\Palaces\\MATRIX',
                        'C:\\Users\\Luke\\Documents\\Memory Palace\\Palaces\\Computer\\Star Trek 25th Anniversary', 
                        'C:\\Users\\Luke\\Documents\\Memory Palace\\Palaces\\Sandman',
                        'C:\\Users\\Luke\\Documents\\Memory Palace\\Palaces\\RegEx']

               

                pygame.init()
                self.font_1 = pygame.font.Font(None, 72)
                self.font_2 = pygame.font.Font(None, 52)
                self.get_from_palace()
                if self.start_up:
                    self.select_menu()
                else:
                    self.get_images()


        def select_menu(self):

            self.select_menu_open = True 
            surface = pygame.Surface((1000, 800))
            surface.fill((255, 255, 255))

            # Render all the possible sheets in a box
            line_position = 10
            # Highlight currently select menu red
            for count, line in enumerate(self.sheet_list): 
                if count == self.select_which:
                    rendered_palace = self.font_1.render(line.title, False, (255, 0, 0))
                else:
                    rendered_palace = self.font_1.render(line.title, False, (0, 0, 0))
                surface.blit(rendered_palace, (10, line_position))
                line_position += rendered_palace.get_height() + 10
            return surface

        def get_from_palace(self):
                currentPalace = get_palace.Memory_Palace(self.select_which)
                self.sheet_list = currentPalace.sheets
                self.loci_list = currentPalace.loci
                self.facts_list = currentPalace.facts
                self.mnemonics_list = currentPalace.mnemonics
                self.image_files_list = currentPalace.image_files

        def get_images(self):
            if self.start_up:
                pass
            else:
                logging.debug("Loading Rendered Loci for sheet # %s", theData.select_which)
                for loci in self.loci_list:
                    self.loci_list_surf.append(self.font_1.render(loci, False, (0, 255, 0)))
                logging.debug("Loading Rendered images for sheet # %s", theData.select_which)
                for image in self.image_files_list:
                    filename = os.path.join(self.folder_locations[self.select_which], image)
                    self.image_list_surf.append(pygame.image.load(filename))
                logging.debug("Loading rendered facts list for sheet # %s", theData.select_which)
                for fact in self.facts_list:
                    self.image_rect = self.image_list_surf[0].get_rect()
                    self.image_rect.width = self.image_rect.width - 200
                    self.image_rect.height = self.image_rect.height - 400
                    self.facts_list_surf.append(textrect.render_textrect(fact, self.font_2, self.image_rect, (255, 255, 255), (0, 0, 0), 1))

                logging.debug("Loading rendered mnemonics list for sheet # %s", theData.select_which)
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
