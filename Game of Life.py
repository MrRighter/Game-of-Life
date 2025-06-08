import sys
import random
from copy import deepcopy
import base64
import io

import pygame

from Class_GoL_Button import PicGoLButton
from button_str_codes import *
from font_str_code import *

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('Game of Life')
clock = pygame.time.Clock()

RES_DISPLAY = WIDTH, HEIGHT = pygame.display.get_surface().get_size()
TILE = 12
W, H = WIDTH // TILE, HEIGHT // TILE

next_field = [[0 for i in range(W)] for j in range(H)]
current_field = [[random.randint(0, 1) for _ in range(W)] for _ in range(H)]

start_stop_button = PicGoLButton(115, 20, 104, 64, start_stop1, start_stop2, start_stop3)
options_button = PicGoLButton(20, 20, 64, 64, options1, options2, options3)

decoded_font_data = base64.b64decode(pixel_font_code)
font_stream = io.BytesIO(decoded_font_data)
my_pixel_font = pygame.font.Font(font_stream, 40)

game_paused = False
options_open = False
start_stop_active = True
options_active = True

current_pattern_index = 0


def patterns_filling():
    global current_pattern_index
    current_patterns_fields = [
        [[1 if i == W // 2 or j == H // 2 else 0 for i in range(W)] for j in range(H)],
        [[1 if not i % 9 else 0 for i in range(W)] for _ in range(H)],
        [[1 if not (2 * i + j) % 4 else 0 for i in range(W)] for j in range(H)],
        [[1 if not (i * j) % 22 else 0 for i in range(W)] for j in range(H)]
    ]
    current_pattern_field = current_patterns_fields[current_pattern_index]
    current_pattern_index = (current_pattern_index + 1) % len(current_patterns_fields)
    return current_pattern_field


def text_gol_button(screen, x, y, width, height, text, font_color, bg_color, hover_color, active_color):
    mouse_pos = pygame.mouse.get_pos()
    if x < mouse_pos[0] < x + width and y < mouse_pos[1] < y + height:
        if pygame.mouse.get_pressed()[0]:
            pygame.draw.rect(screen, active_color, pygame.Rect(x, y, width, height))
        else:
            pygame.draw.rect(screen, hover_color, pygame.Rect(x, y, width, height))
    else:
        pygame.draw.rect(screen, bg_color, pygame.Rect(x, y, width, height))

    text_refers = my_pixel_font.render(text, True, font_color)
    button_rect = text_refers.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_refers, button_rect)


def check_cell(current_field, x, y):
    if game_paused:
        return current_field[y][x]
    count = 0
    for j in range(y - 1, y + 2):
        for i in range(x - 1, x + 2):
            if current_field[j][i]:
                count += 1

    if current_field[y][x]:
        count -= 1
        if count == 2 or count == 3:
            return 1
        return 0
    else:
        if count == 3:
            return 1
        return 0


def count_living_cells(field):
    count = 0
    for row in field:
        count += sum(row)
    return count


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_stop_button.collidepoint(event.pos) and start_stop_active:
                game_paused = not game_paused
                options_active = not options_active
            if options_button.collidepoint(event.pos) and options_active:
                options_open = not options_open
                start_stop_active = not start_stop_active
            if game_paused:
                x, y = pygame.mouse.get_pos()
                x, y = x // TILE, y // TILE
                if event.button == 1:
                    current_field[y][x] = 1
                elif event.button == 3:
                    current_field[y][x] = 0
        elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0] and game_paused:
            x, y = pygame.mouse.get_pos()
            x, y = x // TILE, y // TILE
            current_field[y][x] = 1
        elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[2] and game_paused:
            x, y = pygame.mouse.get_pos()
            x, y = x // TILE, y // TILE
            current_field[y][x] = 0

    if options_open:
        number_of_buttons = 4
        button_width = 430
        button_height = 70
        button_margin = 40
        total_height = number_of_buttons * button_height + (number_of_buttons - 1) * button_margin
        start_y = (HEIGHT - total_height) // 2
        button_texts = ["Random Filling", "Patterns Filling", "Remove Cells", "Close Game"]

        back_field_width2, back_field_height2 = button_width + 35, total_height + 35
        back_field_x2, back_field_y2 = (WIDTH - back_field_width2) // 2, (HEIGHT - back_field_height2) // 2

        back_field_width1, back_field_height1 = back_field_width2 + 70, back_field_height2 + 110
        back_field_x1, back_field_y1 = (WIDTH - back_field_width1) // 2, (HEIGHT - back_field_height1) // 2

        back_field1 = pygame.draw.rect(screen, "#e4e4e4",
                                       pygame.Rect(back_field_x1, back_field_y1, back_field_width1, back_field_height1))
        back_field2 = pygame.draw.rect(screen, "#c4c4c4",
                                       pygame.Rect(back_field_x2, back_field_y2, back_field_width2, back_field_height2))

        for i, text in enumerate(button_texts, start=1):
            button_y = start_y + (i - 1) * (button_height + button_margin)
            button_x = (WIDTH - button_width) // 2
            text_gol_button(screen, button_x, button_y, button_width, button_height, text,
                                     "#0a0a0a", "#949494", "#a4a4a4", "#848484")

            mouse_pos = pygame.mouse.get_pos()
            if button_x < mouse_pos[0] < button_x + button_width and button_y < mouse_pos[1] < button_y + button_height:
                if pygame.mouse.get_pressed()[0]:
                    if text == "Close Game":
                        sys.exit()
                    elif text == "Random Filling":
                        current_field = [[random.randint(0, 1) for i in range(W)] for j in range(H)]
                        options_open = not options_open
                        start_stop_active = not start_stop_active
                    elif text == "Patterns Filling":
                        current_field = patterns_filling()
                        options_open = not options_open
                        start_stop_active = not start_stop_active
                    elif text == "Remove Cells":
                        current_field = [[0 for i in range(W)] for j in range(H)]
                        options_open = not options_open
                        start_stop_active = not start_stop_active
                        game_paused = not game_paused
                        options_active = not options_active
    else:
        screen.fill("#0c0c0c")
        [pygame.draw.line(screen, (4, 4, 4), (x, 0), (x, HEIGHT)) for x in range(0, WIDTH, TILE)]
        [pygame.draw.line(screen, (4, 4, 4), (0, y), (WIDTH, y)) for y in range(0, HEIGHT, TILE)]

        for x in range(1, W - 1):
            for y in range(1, H - 1):
                if current_field[y][x]:
                    pygame.draw.rect(screen, pygame.Color('#792bff'), (x * TILE + 2, y * TILE + 2, TILE - 2, TILE - 2))
                next_field[y][x] = check_cell(current_field, x, y)
        current_field = deepcopy(next_field)

        living_cells = count_living_cells(current_field)
        population = my_pixel_font.render(f"Population: {str(living_cells)}", True, "#e4e4e4")
        screen.blit(population, (245, 35))

    start_stop_button.handle_event(event)
    start_stop_button.check_hover(pygame.mouse.get_pos())
    start_stop_button.draw(screen)

    options_button.handle_event(event)
    options_button.check_hover(pygame.mouse.get_pos())
    options_button.draw(screen)

    clock.tick(12)
    pygame.display.flip()
