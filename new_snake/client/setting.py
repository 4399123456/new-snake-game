import pygame
import random

class Setting():
    def __init__(self):
        self.window_info()
        self.snake_info()
        self.food_info()
        self.start_info()
        self.font_info()
        self.pause_info()
        self.game_over_info()
        self.client_info()

    def client_info(self):
        self.server_ip = '127.0.0.1'
        self.server_port = 8796
        self.recv_max_bytes = 4096 * 10

    def window_info(self):
        self.window_size = (800,600)
        self.window_title = 'Snake'
        self.bg_color = (255,255,255)
        self.FPS = 15

    def snake_info(self):
        self.block_size = 20
        self.head_color = (237,233,9)
        self.body_color = (34,235,23)

    def food_info(self):
        self.food_size = 20
        self.food_color = (255,0,0)
        self.food_pos = [300,300]

    def font_info(self):
        self.font_type = None

    def start_info(self):
        self.start_text_1 = "Snake Game"
        self.start_text_2 = "Click the screen or press space to start!"

    def pause_info(self):
        self.pause_text_1 = "Pause"
        self.pause_text_2 = "Press Esc or space or click the screen to start!"

    def game_over_info(self):
        self.game_over_text_1 = "Game Over!"
        self.game_over_text_2 = "Press Esc or click the screen to restart!"



