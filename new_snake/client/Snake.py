import sys
import pygame
from setting import Setting

setting = Setting()

class Snake(pygame.sprite.Sprite):
    def __init__(self,screen):
        super().__init__()
        self.screen = screen
        self.block_size = setting.block_size
        self.head_pos = [100,40]
        self.body_pos = [self.head_pos,[80,40],[60,40],[40,40],[20,40]]
        self.head_color = setting.head_color
        self.body_color = setting.body_color

    def draw(self):
        pygame.draw.rect(self.screen,self.head_color,(self.body_pos[0][0],self.body_pos[0][1],self.block_size,self.block_size))
        for i in range(1,len(self.body_pos)):
            pygame.draw.rect(self.screen,self.body_color,(self.body_pos[i][0],self.body_pos[i][1],self.block_size,self.block_size))

    def move(self,direct='r'):
        head = self.body_pos[0]
        if direct == 'r':
            self.body_pos.pop()
            new_item = [head[0] + 20,head[1]]
            self.body_pos.insert(0,new_item)
        elif direct == 'l':
            self.body_pos.pop()
            new_item = [head[0] - 20,head[1]]
            self.body_pos.insert(0,new_item)
        elif direct == 'u':
            self.body_pos.pop()
            new_item = [head[0],head[1] - 20]
            self.body_pos.insert(0,new_item)
        elif direct == 'd':
            self.body_pos.pop()
            new_item = [head[0],head[1] + 20]
            self.body_pos.insert(0,new_item)

    def eat(self,direct='r'):
        last = [self.body_pos[-1][0],self.body_pos[-1][1]]
        if direct == 'r':
            last[0] -= 20
        elif direct == 'l':
            last[0] += 20
        elif direct == 'u':
            last[1] += 20
        elif direct == 'd':
            last[1] -= 20
        self.body_pos.append(last)

