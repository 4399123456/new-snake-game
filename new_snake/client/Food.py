import sys,random
import pygame
from setting import Setting

setting = Setting()

class Food(pygame.sprite.Sprite):
    def __init__(self,screen):
        super().__init__()
        self.screen = screen
        self.food_size = setting.food_size
        self.food_color = setting.food_color
        self.food_pos_x = list(range(20,780,20))
        self.food_pos_y = list(range(20,580,20))
        self.food_pos = setting.food_pos

    def draw(self):
        pygame.draw.rect(self.screen,self.food_color,(self.food_pos[0],self.food_pos[1],self.food_size,self.food_size))

    def generate(self,snake):
        while True:
            x = random.choice(self.food_pos_x)
            y = random.choice(self.food_pos_y)
            is_repeat = False
            for body in snake.body_pos:
                if body[0] == x and body[1] == y:
                    is_repeat = True
            if not is_repeat:
                self.food_pos = [x,y]
                break
            else:
                continue
