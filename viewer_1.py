import logging
import pdb

logging.basicConfig(filename='viewer.log', filemode='w', format='%(levelname)s:%(asctime)s %(message)s', level=logging.DEBUG)

import pygame
from pygame.locals import *
import os
import fnmatch
import get_palace 


class App:
        def __init__(self):
                logging.debug('class App called')
                self._running = True
                self._display_surf = None
                self._display_caption = None
                self.size = self.weight, self.height = 1400, 600
                self.image_count = 0
                self.clock = None

                self.text_surface1_flag = False 
                self.text_surface1 = None
                self.text_surface2_flag = False
                self.text_surface2 = None
                self.text_surface3_flag = False
                self.text_surface3 = None
                
                self.select_which = 0
                self.select_menu = None
                self.palaces = ["Sales", "History", "Coding"]

        def on_init(self):
                pygame.init()
                self.joystick = pygame.joystick.Joystick(0)
                self.joystick.init()
                logging.info('joystick initialized')
                logging.info('pygame initialized')
                self._display_surf = pygame.display.set_mode((self.size), HWSURFACE | DOUBLEBUF | RESIZABLE)
                self._display_caption = pygame.display.set_caption('Space is the Place')
                self._running = True
                logging.info('theViewer created.')
                logging.info('%s ', theViewer)
                self.clock = pygame.time.Clock()


# Add button 5 Joystick left 
# add button 6 Joystick right
        def on_event(self, event):
                if event.type == pygame.QUIT:
                        self._running = False
                # Keyboard Input
                keys = pygame.key.get_pressed()

                if keys[pygame.K_LEFT]:
                        logging.info('Left key pressed.')
                        theViewer.prev_image()
                elif keys[pygame.K_RIGHT]:
                        logging.info('Right key pressed.')
                        theViewer.next_image()

                # Joystick Input
                if event.type == pygame.JOYBUTTONDOWN:
                        logging.info('a controller button was pressed')
                        if self.joystick.get_button(0):
                            logging.info('Controller button 0 pressed')
                            self.text_surface1 = theData.font.render('Controller button 0 pressed', False, (0, 0, 255))
                            self.text_surface1_flag = not self.text_surface1_flag
                        elif self.joystick.get_button(1):
                            logging.info('Controller button 1 pressed')
                            self.text_surface2 = theData.font.render('Controller button 1 pressed', False, (255, 0, 0))
                            self.text_surface2_flag = not self.text_surface2_flag
                        elif self.joystick.get_button(2):
                            logging.info('Controller button 2 pressed' )
                            self.text_surface3 = theData.font.render('Controller button 2 pressed', False, (0, 255, 0))
                            self.text_surface3_flag = not self.text_surface3_flag
                        elif self.joystick.get_button(3):
                            logging.info('Controller button 3 pressed')
                        elif self.joystick.get_button(4):
                            logging.info('Controller button 4 pressed')
                            theViewer.prev_image() 
                        elif self.joystick.get_button(5):
                            logging.info('Controller button 5 pressed.')
                            theViewer.next_image()
                        elif self.joystick.get_button(6):
                            logging.info('Controller button 6 pressed.')
                            if self.select_which < 3: 
                                self.select_menu = theData.font.render(self.palaces[self.select_which], False, (0, 0, 0), (255, 255, 255)) 
                                self.select_which += 1
                                logging.info('Select screen set to %s', self.select_which)
                            else:
                                self.select_which = 0
                                logging.info('Select screen set to %s', self.select_which)

                        elif self.joystick.get_button(7):
                            logging.info('Controller button 7 pressed.')
                            theData.browse_folder()
                            theData.get_images()

        def on_loop(self):
                pass
        def on_render(self):
                black = 0, 0, 0

                self._display_surf.fill(black)
                self._display_surf.blit(theViewer.image, (theViewer.x, theViewer.y))
                if self.text_surface1_flag == True:
                    self._display_surf.blit(self.text_surface1, (50, 40))
                if self.text_surface2_flag == True:
                    self._display_surf.blit(self.text_surface2, (50, 70))
                if self.text_surface3_flag == True:
                    self._display_surf.blit(self.text_surface3, (50, 110))
                if self.select_which > 0:
                    self._display_surf.blit(self.select_menu, (250, 250))

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
                        self.on_loop()
                        self.on_render()
                self.on_cleanup()

class Data:
        def __init__(self):
                logging.debug('class Data called.')
                self.folder = None 
                self.image_list = None
                self.loci_list = None
                self.facts_list = None
                self.mnemonics_list = None
                self.image_files_list = None


                pygame.font.init()
                self.font = pygame.font.Font(None, 72)
                self.get_from_palace()


        def get_from_palace(self):
                dreddPalace = get_palace.Memory_Palace(0)
                pdb.set_trace()
                self.loci_list = dreddPalace.loci
                self.facts_list = dreddPalace.facts
                self.mnemonics_list = dreddPalace.mnemonics
                self.image_files_list = dreddPalace.image_files


        def sort_filenames(self, l):
                """ Sorts the given iterable in the way that is expected.

                Required arguments:
                l -- The iterable to be sorted.

                """
                convert = lambda text: int(text) if text.isdigit() else text
                alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
                return sorted(l, key = alphanum_key)

        def browse_folder(self):
                # Allow user to select folder
                root = Tk()
                self.folder = filedialog.askdirectory()
                logging.info('%s folder selected', self.folder)
                root.destroy()

                
                    
class Viewer:
        def __init__(self):
                self.x = 10 
                self.y = 10 
                self.text_x = 20
                self.text_y = 40
                self.width = 64
                self.height = 64
                self.change_image = theData.image_list 
                self.image = self.change_image[0]
                logging.info('new Viewer class created.  Image list is: %s', self.change_image)
            
        def prev_image(self):
                if theApp.image_count > 0:
                        theApp.image_count -=1
                self.image = self.change_image[theApp.image_count]

        def next_image(self):
                logging.debug('image count now set to %s.  There are %s total images', theApp.image_count, len(theData.image_list))
                if theApp.image_count < len(theData.image_list) - 1:
                        theApp.image_count += 1
                else:
                        logging.info('Reached the final image.')
                theViewer.image = theViewer.change_image[theApp.image_count]    

if __name__ == "__main__" :
        theData = Data()
        theViewer = Viewer()
        theApp= App()
        theApp.on_execute()
