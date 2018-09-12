import pygame

pygame.init()
print ('Joysticks: ', pygame.joystick.get_count())
my_joystick = pygame.joystick.Joystick(0)
my_joystick.init()
#Print number of axis and buttons
print('Name of joystick is:', my_joystick.get_name())
print('Number of axis:', my_joystick.get_numaxes())
print('Number of buttons:', my_joystick.get_numbuttons())

clock = pygame.time.Clock()

while 1:
    for event in pygame.event.get():
        print(my_joystick.get_axis(0), my_joystick.get_axis(1))
        if event.type == pygame.JOYBUTTONDOWN:
            print("Button Pressed")
            if my_joystick.get_button(0):
                print("Button 0 pressed")
            elif my_joystick.get_button(1):
                print("Button 1 pressed")
            elif my_joystick.get_button(2):
                print("Button 2 pressed")
            elif my_joystick.get_button(3):
                print("Button 3 pressed")
            elif my_joystick.get_button(4):
                print("Button 4 pressed")
            elif my_joystick.get_button(5):
                print("Button 5 pressed")
            elif my_joystick.get_button(6):
                print("Button 6 pressed")
            elif my_joystick.get_button(7):
                print("Button 7 pressed")
            elif my_joystick.get_button(8):
                print("Button 8 pressed")
            else:
                print("Unknown button pressed")

        clock.tick(40)



pygame.quit()
