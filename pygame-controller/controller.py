import os
import pprint
import pygame
import socket
from time import sleep

class JoyStickController(object):
    controller = None
    axis_data = None
    button_data = None
    hat_data = None
    
    def init(self):
        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()

    def listen(self, socket):
        
        if not self.axis_data:
            self.axis_data = {}
            for i in range(3):
                if i > 1:
                    self.axis_data[i] = 1.0
                else:
                    self.axis_data[i] = 0.0                    

        if not self.button_data:
            self.button_data = {}
            for i in range(self.controller.get_numbuttons()):
                self.button_data[i] = False

        if not self.hat_data:
            self.hat_data = {}
            for i in range(self.controller.get_numhats()):
                self.hat_data[i] = (0, 0)

        while True:
            
            for event in pygame.event.get():
                
                if event.type == pygame.JOYAXISMOTION:
                    self.axis_data[event.axis] = round(event.value, 4)
                elif event.type == pygame.JOYBUTTONDOWN:
                    self.button_data[event.button] = True
                elif event.type == pygame.JOYBUTTONUP:
                    self.button_data[event.button] = False
                elif event.type == pygame.JOYHATMOTION:
                    self.hat_data[event.hat] = event.value 

            msg = str(self.axis_data) + ' ' + str(self.button_data) + '\n'
            sock.send(msg.encode('ascii'))
            sleep (10.0 / 1000.0);

if __name__ == "__main__":    

    HOST = 'localhost'
    PORT = 60000

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    joy = JoyStickController()
    joy.init()
    joy.listen(sock)
