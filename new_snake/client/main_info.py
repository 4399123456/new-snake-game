import sys
import pygame
from setting import Setting
import game_logitic as gl

setting = Setting()
pygame.font.init()

class Main_info():
    def __init__(self,screen):
        self.screen = screen
        self.is_start = True
        self.is_pause = False
        self.is_over = False

    def start_game(self,execute,snake,food,clock,main_info,client,best_score,username):
        execute(self.screen, snake, food,main_info,client,best_score,username)
        self.render_text(setting.start_text_1, (0, 0, 0), 35, setting.window_size[0] / 2 - 60,
                         setting.window_size[1] / 2 - 50)
        self.render_text(setting.start_text_2, (255, 0, 0), 40, setting.window_size[0] / 2 - 250,
                         setting.window_size[1] / 2 - 15)

        while self.is_start:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if gl.score > best_score:
                        client.send(('score ' + str(gl.score) + ' ' + username).encode())
                    else:
                        client.send(('score ' + str(best_score) + ' ' + username).encode())
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.is_start = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if mouse_pos[0] >= 0 and mouse_pos[0] <= setting.window_size[0]\
                            and mouse_pos[1] >= 0 and mouse_pos[1] <= setting.window_size[1]:
                        self.is_start = False
            # clock.tick(setting.FPS)
            pygame.display.update()

    def pause_game(self,client,best_score,username):
        self.render_text(setting.pause_text_1, (0, 0, 0), 35, setting.window_size[0] / 2 - 30,
                         setting.window_size[1] / 2 - 50)
        self.render_text(setting.pause_text_2, (255, 0, 0), 40, setting.window_size[0] / 2 - 300,
                         setting.window_size[1] / 2 - 15)
        while self.is_pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if gl.score > best_score:
                        client.send(('score ' + str(gl.score) + ' ' + username).encode())
                    else:
                        client.send(('score ' + str(best_score) + ' ' + username).encode())
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.is_pause = False
                    elif event.key == pygame.K_SPACE:
                        self.is_pause = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if mouse_pos[0] >= 0 and mouse_pos[0] <= setting.window_size[0]\
                            and mouse_pos[1] >= 0 and mouse_pos[1] <= setting.window_size[1]:
                        self.is_pause = False

            pygame.display.update()

    def game_over(self,client,best_score,username,snake,food):
        self.render_text(setting.game_over_text_1, (255, 0, 0), 40, setting.window_size[0] / 2 - 80,
                         setting.window_size[1] / 2 - 50)
        self.render_text(setting.game_over_text_2, (0, 255, 0), 45, setting.window_size[0] / 2 - 280,
                         setting.window_size[1] / 2  - 10)
        while self.is_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if gl.score > best_score:
                        client.send(('score ' + str(gl.score) + ' ' + username).encode())
                    else:
                        client.send(('score ' + str(best_score) + ' ' + username).encode())
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                        if gl.score > best_score:
                            client.send(('score ' + str(gl.score) + ' ' + username).encode())
                        else:
                            client.send(('score ' + str(best_score) + ' ' + username).encode())
                        gl.reset_game(snake,food)
                        self.is_over = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if mouse_pos[0] >= 0 and mouse_pos[0] <= setting.window_size[0] \
                            and mouse_pos[1] >= 0 and mouse_pos[1] <= setting.window_size[1]:
                        if gl.score > best_score:
                            client.send(('score ' + str(gl.score) + ' ' + username).encode())
                        else:
                            client.send(('score ' + str(best_score) + ' ' + username).encode())
                        gl.reset_game(snake,food)
                        self.is_over = False


            pygame.display.flip()


    def render_text(self,text:str,color:tuple,size,x,y):
        font = pygame.font.SysFont(setting.font_type,size)
        font_render = font.render(text,True,color)
        self.screen.blit(font_render,(x,y))



