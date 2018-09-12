import pygame

pygame.init()

j = pygame.joystick.Joystick(0)
j.init()

running = True
try:
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.JOYBUTTONDOWN:
                print("Button Pressed")
                if j.get_button(0):
                    print("Button #1 Pressed")
                elif j.get_button(1):
                    print("Button #2 Pressed")
                elif j.get_button(2):
                    print("Button #3 Pressed")
                elif j.get_button(3):
                    print("Button #4 Pressed")
                elif j.get_button(4):
                    print("Button #5 Pressed")
                elif j.get_button(5):
                    print("Button #6 Pressed")
                elif j.get_button(6):
                    print("Button #7 Pressed")
                elif j.get_button(7):
                    print("Button #8 Pressed")
            elif event.type == pygame.JOYBUTTONUP:
                print("Button Released")
            elif event.type == pygame.QUIT:
                running = False

except KeyboardInterrupt:
    print("EXITING NOW")
    j.quit()
