import os,sys,time
import pygame
from setting import Setting
import game_logitic as gl
from Snake import Snake
from Food import Food
from main_info import Main_info

setting = Setting()
clock = pygame.time.Clock()


def run_game(client,window,best_score,username):
    screen = pygame.display.set_mode(setting.window_size)
    pygame.display.set_caption(setting.window_title)
    snake = Snake(screen)
    food = Food(screen)
    main_info = Main_info(screen)
    screen.fill(setting.bg_color)
    main_info.start_game(gl.execute,snake,food,clock,main_info,client,best_score,username)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if gl.score > best_score:
                    client.send(('score ' + str(gl.score) + ' ' + username).encode())
                else:
                    client.send(('score ' + str(best_score) + ' ' + username).encode())
                sys.exit()
            gl.control_board(event,main_info,client,best_score,username)

        screen.fill(setting.bg_color)
        gl.execute(screen,snake,food,main_info,client,best_score,username)

        clock.tick(setting.FPS)
        pygame.display.flip()


