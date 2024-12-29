import sys,time
import pygame
from Food import Food
from setting import Setting


setting = Setting()

direct = 'r'
disable_left = False
disable_right = False
disable_up = False
disable_down = False

eat_food = False
eat_time_delay = None

score = 0

def control_board(event,main_info,client,best_score,username):
    global direct,disable_up,disable_down,disable_left,disable_right
    if event.type == pygame.KEYDOWN:
        if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and not disable_right:
            direct = 'r'
            disable_left = True
            disable_right = True
            disable_up = False
            disable_down = False

        elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and not disable_left:
            direct = 'l'
            disable_left = True
            disable_right = True
            disable_up = False
            disable_down = False

        elif (event.key == pygame.K_UP or event.key == pygame.K_w) and not disable_up:
            direct = 'u'
            disable_left = False
            disable_right = False
            disable_up = True
            disable_down = True

        elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and not disable_down:
            direct = 'd'
            disable_left = False
            disable_right = False
            disable_up = True
            disable_down = True
        elif event.key == pygame.K_ESCAPE:
            main_info.is_pause = True
            main_info.pause_game(client,best_score,username)

def check_eat_food(snake,food):
    global eat_time_delay,eat_food,score
    if snake.body_pos[0][0] == food.food_pos[0] and snake.body_pos[0][1] == food.food_pos[1]:
        eat_food = True
        eat_time_delay = time.time()
        snake.eat()
        score += 10

    if eat_food:
        if time.time() - eat_time_delay >= 0.1:
            food.generate(snake)
            eat_food = False

def check_dead(snake,main_info,food,client,best_score,username):
    head = snake.body_pos[0]
    if head[0] >= setting.window_size[0] or head[0] < 0:
        main_info.is_over = True
        main_info.game_over(client,best_score,username,snake,food)
        if score > best_score:
            client.send(('score ' + str(score) + ' ' + username).encode())
        else:
            client.send(('score ' + str(best_score) + ' ' + username).encode())
        #reset_game(snake,food)


    elif head[1] >= setting.window_size[1] or head[1] < 0:
        main_info.is_over = True
        main_info.game_over(client,best_score,username,snake,food)
        if score > best_score:
            client.send(('score ' + str(score) + ' ' + username).encode())
        else:
            client.send(('score ' + str(best_score) + ' ' + username).encode())
        #reset_game(snake,food)

    for body in snake.body_pos[1:]:
        if body[0] == head[0] and body[1] == head[1]:
            main_info.is_over = True
            main_info.game_over(client,best_score,username,snake,food)
            if score > best_score:
                client.send(('score ' + str(score) + ' ' + username).encode())
            else:
                client.send(('score ' + str(best_score) + ' ' + username).encode())
            #reset_game(snake, food)
            break

def reset_game(snake,food):
    global direct,disable_up,disable_down,disable_left,disable_right,eat_food,score
    snake.body_pos = [[100,40],[80,40],[60,40],[40,40],[20,40]]
    food.food_pos = setting.food_pos
    direct = 'r'
    disable_left = False
    disable_right = False
    disable_up = False
    disable_down = False
    eat_food = False
    score = 0

def execute(screen,snake,food,main_info,client,best_score,username):
    snake.draw()
    if not eat_food:
        food.draw()
    snake.move(direct)
    main_info.render_text(f"score:{score}",(158,156,155),30,10,10)
    main_info.render_text(f"best score:{best_score}",(158,156,155),30,setting.window_size[0] / 2 - 50,10)
    check_eat_food(snake,food)
    check_dead(snake,main_info,food,client,best_score,username)

