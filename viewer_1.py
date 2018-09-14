import logging
import pdb

logging.basicConfig(filename='viewer.log', filemode='w', format='%(levelname)s:%(asctime)s %(message)s', level=logging.DEBUG)

import pygame
from pygame.locals import *
from tkinter import filedialog
from tkinter import *
import os
import fnmatch


class App:
        def __init__(self):
                logging.debug('class App called')
                self._running = True
                self._display_surf = None
                self._display_caption = None
                self.size = self.weight, self.height = 1400, 600
                self.image_count = 0
                self.clock = None

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
                        logging.info('Controller button 5 pressed')
                        if self.joystick.get_button(4):
                                theViewer.prev_image() 
                        elif self.joystick.get_button(5):
                                logging.info('Controller button 6 pressed.')
                                theViewer.next_image()
                        elif self.joystick.get_button(6):
                                logging.info('Controller select button')
                                theData.browse_folder()
                                theData.get_images()

        def on_loop(self):
                pass
        def on_render(self):
                black = 0, 0, 0
                self._display_surf.fill(black)
                self._display_surf.blit(theViewer.image, (theViewer.x, theViewer.y))
                pygame.display.flip()

        def on_cleanup(self):
                pygame.quit()

        def on_execute(self):
                
                if self.on_init() == False:
                        logging.info('App.on_execute if self.on_init() == False RUNNING')
                        self._running = False

                while( self._running ):
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
                self.image_list = []
                self.browse_folder()
                self.get_images()

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

        def get_images(self):
                for f in self.sort_filenames(os.listdir(self.folder)):
                        if fnmatch.fnmatch(f, '*.png'):
                                self.image_list.append(pygame.image.load(self.folder + '/' + f))
                                logging.info('adding %s to self.image_list', self.folder + '/' + f)
                logging.warning('image list is: %s', self.image_list)

class Viewer:
        def __init__(self):
                self.x = 10 
                self.y = 10 
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
