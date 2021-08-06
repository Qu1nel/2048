import copy
import json
import sys
import os
import pygame
from database import get_best, insert_result
from random import shuffle, randint
from logics import *



def render_screen(scr: int, delta: int = 0) -> None:
    """ Does 3 actions

    1 - Insert 2 random numbers into the matrix, if possible
    
    2 - Renders the screen

    3 - Refreshes the screen

    :param scr: score
    :param delta: delta
    :return: None
    """
    insert_in_mas()
    draw_interface(scr, delta)
    pygame.display.update()


def insert_in_mas() -> None:
    """ Inserts randomly 2 or 4 into the game matrix DURING the game process.

    :return: None
    """
    global mas, is_mas_move
    if is_mas_move and is_zero_in_mas(mas):
        is_mas_move = False
        empty = get_empty_list(mas)  # List of empty cells
        shuffle(empty)  # List gets in the way
        random_num = empty.pop()  # Selects a random item
        x, y = get_index_from_number(random_num)
        mas = insert_2_or_4(mas, x, y)


def init_vars() -> None:
    """ Initializes the main game variables m and score.

    :return: None
    """
    global mas, score
    score = 0
    mas = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
    # Fill two cells with random numbers
    FIRST_SLOT = randint(1, 16)
    SECOND_SLOT = randint(1, 16)
    while FIRST_SLOT == SECOND_SLOT:  # In case the random cells are the same
        FIRST_SLOT = randint(1, 16)
        SECOND_SLOT = randint(1, 16)
    mas = insert_2_or_4(mas, *get_index_from_number(FIRST_SLOT))
    mas = insert_2_or_4(mas, *get_index_from_number(SECOND_SLOT))


def load_game() -> None:
    """ Loads save from data.txt file if it exists.

    :return: None
    """
    global mas, score, USERNAME
    path = os.getcwd()
    if 'data.txt' in os.listdir(path):
        with open('data.txt') as file:
            data = json.load(file)
            mas = data['mas']
            score = data['score']
            USERNAME = data['user']
        full_path = os.path.join(path, 'data.txt')
        os.remove(full_path)
    else:
        init_vars()


def save_game() -> None:
    """ Saves the game when exiting the menu or exiting the game.

    Creates a data.txt file with a json dictionary inside,
    to use all the basic constants at the time of saving

    :return: None
    """
    data = {
        'user': USERNAME,
        'score': score,
        'mas': mas
    }
    with open('data.txt', 'w') as outfile:
        json.dump(data, outfile)


def around_arrow() -> None:
    """ Draws the screen when the encapsulated arrow is clicked.

    In the future, it makes it possible to choose what to do: 1-restart the game, 2-cancel

    :return: None
    """
    cancel_box = pygame.Rect(145, 415, 150, 70)
    repeat_box = pygame.Rect(305, 415, 150, 70)

    blur = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    blur.fill((0, 0, 0, 140))
    screen.blit(blur, (0, 0))

    screen.blit(get_font(53, GEN_FONT).render('Reset game?', True, COLORS['WHITE']), (60, 200))
    font_H3 = pygame.font.Font(GEN_FONT, 32)
    screen.blit(font_H3.render('Are you sure you wish to', True, COLORS['WHITE']), (60, 300))
    screen.blit(font_H3.render('reset the game?', True, COLORS['WHITE']), (60, 340))

    pygame.draw.rect(screen, (110, 110, 110), cancel_box, border_radius=12)
    screen.blit(font_H3.render('Cancel', True, COLORS['WHITE']), (174, 413))

    pygame.draw.rect(screen, (110, 110, 110), repeat_box, border_radius=12)
    screen.blit(font_H3.render('Reset', True, COLORS['WHITE']), (341, 413))
    pygame.display.update()

    make_decision = False
    while not make_decision:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE:  # cancel
                    render_screen(score)
                    make_decision = True
                elif event.key == pygame.K_RETURN:  # reset
                    init_vars()
                    render_screen(score)
                    make_decision = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if cancel_box.collidepoint(event.pos):  # cancel
                    render_screen(score)
                    make_decision = True
                elif repeat_box.collidepoint(event.pos):  # reset
                    init_vars()
                    render_screen(score)
                    make_decision = True


def back_arrow(old_scr: int) -> None:
    """ Loads the last action before the button is clicked.

    :param old_scr: old score counter
    :return: None
    """
    global mas, score
    if copy_mas is not None and copy_mas != mas:
        mas = copy.deepcopy(copy_mas)
        score = old_scr
        draw_interface(score)
        pygame.display.update()


def draw_top_gamers() -> None:
    """ Draws the screen with players

    :return: None
    """
    menu_box = pygame.Rect(225, 532, 75, 75)
    ALL_PLAYERS = get_best()

    backGround_with_crown = "images\\BG\\rating.jpg"
    backGround_without_crown = "images\\BG\\rating_nothing.jpg"
    path_bg = backGround_with_crown if get_best(1)['name'] is not None else backGround_without_crown
    rating_bg = pygame.image.load(path_bg)
    menu = pygame.image.load("images\\elements\\home.png")
    screen.blit(rating_bg, (0, 0))
    screen.blit(pygame.transform.scale(menu, [50, 50]), (236, 543))

    screen.blit(get_font(120, GEN_FONT).render('Rating', True, COLORS['WHITE']), (86, -50))

    for id, player in ALL_PLAYERS.items():
        if player['name'] is None:
            screen.blit(get_font(45, GEN_FONT).render('Nothing', True, COLORS['WHITE']), (180, 115 + 100 * id))
        else:
            name = get_font(40, GEN_FONT).render(player['name'] + ':', True, COLORS['WHITE'])
            if name.get_width() > 154:
                S = player['name'] + ':'
                screen.blit(get_font(28, GEN_FONT).render(S, True, COLORS['WHITE']), (117, 135 + 100 * id))
                size_font = 35
                score_txt = get_font(size_font, GEN_FONT).render(str(player['score']), True, COLORS['WHITE'])
                while 289 - name.get_width() + 20 + score_txt.get_width() - 117 > 309:  # ширина
                    score_txt = get_font(size_font, GEN_FONT).render(str(player['score']), True, COLORS['WHITE'])
                    size_font -= 2
                y = 128 if size_font == 35 else 133
                x = get_font(28, GEN_FONT).render(player['name'] + ':', True, COLORS['WHITE']).get_width() + 127
                direct_x = (406 - x) // 2 - score_txt.get_width() // 2
            else:
                screen.blit(name, (117, 124 + 100 * id))
                size_font = 35
                score_txt = get_font(size_font, GEN_FONT).render(str(player['score']), True, COLORS['WHITE'])
                while 289 - name.get_width() + 20 + score_txt.get_width() - 117 > 309:  # ширина
                    score_txt = get_font(size_font, GEN_FONT).render(str(player['score']), True, COLORS['WHITE'])
                    size_font -= 2
                y = 128 if size_font == 35 else 133
                x = name.get_width() + 127
                direct_x = (406 - x) // 2 - score_txt.get_width() // 2

            screen.blit(score_txt, (x + direct_x, y + 100 * id))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_BACKSPACE:
                    draw_menu()
                    return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if menu_box.collidepoint(event.pos):
                    draw_menu()
                    return None


def put_name() -> None:
    """ Draws a screen with a name entry.
    There are length restrictions

    :return: None
    """

    def render() -> None:
        name_bg = pygame.image.load("images\\BG\\input_username.jpg")
        menu = pygame.image.load("images\\elements\\home.png")
        screen.blit(name_bg, (0, 0))
        screen.blit(pygame.transform.scale(menu, [50, 50]), (236, 494))
        screen.blit(get_font(120, GEN_FONT).render('2048', True, COLORS['WHITE']), (108, 60))
        screen.blit(get_font(45, GEN_FONT).render('OK', True, COLORS['WHITE']), (229, 371))

    global USERNAME

    active_colour = '#013df2'
    inactive_colour = '#33346b'
    ok_box = pygame.Rect(118, 383, 289, 80)
    input_box = pygame.Rect(118, 283, 289, 80)
    menu_box = pygame.Rect(225, 483, 75, 75)

    render()
    font_input = get_font(48, GEN_FONT)
    pygame.draw.rect(screen, color := inactive_colour, input_box, 1, border_radius=15)
    pygame.display.update()

    name = ''
    active = False
    input_name = False
    while not input_name:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                active = True if input_box.collidepoint(event.pos) else False
                if ok_box.collidepoint(event.pos):
                    if len(name) >= 3:
                        USERNAME = name
                        input_name = True
                elif menu_box.collidepoint(event.pos):
                    draw_menu()
                    return None
                color = active_colour if active else inactive_colour
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if active:
                    if event.key == pygame.K_RETURN:
                        if len(name) >= 3:
                            USERNAME = name
                            input_name = True
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        if font_input.render(name, True, COLORS['WHITE']).get_width() < 261:
                            name += event.unicode
        render()
        if name == '' and color == inactive_colour:
            screen.blit(font_input.render('Username', True, COLORS['GRAY']), (155, 267))
        txt = font_input.render(name, True, COLORS['WHITE'])
        pygame.draw.rect(screen, color, input_box, 1, border_radius=15)
        screen.blit(txt, (input_box.w - txt.get_width() // 2 - 26, 267))
        pygame.display.update()


def draw_menu() -> None:
    """ Draws the main menu.

    :return: None
    """
    play_box = pygame.Rect(118, 283, 289, 80)
    rating_box = pygame.Rect(118, 383, 289, 80)

    start_bg = pygame.image.load("images\\BG\\menu.jpg")
    screen.blit(start_bg, (0, 0))

    font = get_font(45, GEN_FONT)
    screen.blit(get_font(120, GEN_FONT).render('2048', True, COLORS['WHITE']), (108, 60))
    screen.blit(font.render('PLAY', True, COLORS['WHITE']), (210, 270))
    screen.blit(font.render('RATING', True, COLORS['WHITE']), (186, 370))

    pygame.display.update()

    pressed_button = False
    while not pressed_button:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN:
                    put_name()
                    pressed_button = True
                elif event.key == 114:
                    draw_top_gamers()
                    pressed_button = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_box.collidepoint(event.pos):
                    put_name()
                    pressed_button = True
                elif rating_box.collidepoint(event.pos):
                    draw_top_gamers()
                    pressed_button = True


def draw_game_over() -> None:
    """ Draws the screen after losing

    :return: None
    """
    global USERNAME
    repeat_box = pygame.Rect(447, 153, 58, 58)

    blur = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    blur.fill((0, 0, 0, 60))
    screen.blit(blur, (0, 0))

    screen.blit(get_font(60, GEN_FONT).render('Game Over!', True, COLORS['WHITE']), (100, 290))
    pygame.draw.rect(screen, '#8d8d8d', repeat_box, border_radius=8)
    round_arrow = pygame.image.load("images\\elements\\around_arrow.png")
    screen.blit(pygame.transform.scale(round_arrow, [43, 43]), (453, 159))
    pygame.display.update()

    insert_result(USERNAME, score)
    make_decision = False
    while not make_decision:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Clicked on the cross
                USERNAME = None
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    USERNAME = None
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN:
                    USERNAME = None
                    make_decision = True
                elif event.key == pygame.K_BACKSPACE:
                    make_decision = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if repeat_box.collidepoint(event.pos):
                    make_decision = True


def draw_victory() -> None:
    """ Checks for the presence of 2048 in the matrix, and, if necessary, draws the victory screen ONLY 1 TIME

    :return: None
    """
    start_draw = False
    for i in range(4):
        if 2048 in mas[i]:
            start_draw = True
            break

    if start_draw:
        if not hasattr(draw_victory, 'count'):
            draw_victory.count = 0
        else:
            draw_victory.count += 1
        if draw_victory.count >= 1:
            return None

        blur = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        blur.fill((0, 0, 0, 85))
        screen.blit(blur, (0, 0))

        font_H1 = pygame.font.Font(GEN_FONT, 90)
        text_H1 = font_H1.render('You Win!', True, COLORS['WHITE'])
        screen.blit(text_H1, (WIDTH // 2 - text_H1.get_size()[0] // 2, 330))
        font_H3 = pygame.font.Font(GEN_FONT, 35)
        text_H3 = font_H3.render('Click any button to Continue', True, COLORS['WHITE'])
        screen.blit(text_H3, (WIDTH // 2 - text_H3.get_size()[0] // 2, 455))

        pygame.display.update()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    render_screen(score)
                    running = False
                if event.type == pygame.KEYDOWN:
                    render_screen(score)
                    running = False


def game_loop() -> bool:
    """ Main game loop.

    :return: boolean value. True - if the menu button was pressed, False otherwise
    """
    global score, mas, is_mas_move, copy_mas, old_score, USERNAME

    repeat_box = pygame.Rect(447, 153, 58, 58)
    menu_box = pygame.Rect(305, 153, 58, 58)
    back_arrow_box = pygame.Rect(376, 153, 58, 58)
    play_ground = pygame.Rect(15, 225, 488, 488)

    draw_interface(score)
    pygame.display.update()
    is_mas_move = False
    move_mouse = False
    while is_zero_in_mas(mas) or can_move(mas):
        for event in pygame.event.get():  # Event handler
            if event.type == pygame.QUIT:  # Clicked on the cross
                save_game()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Clicked on the mouse button
                if menu_box.collidepoint(event.pos):  # Menu
                    insert_result(USERNAME, score)
                    USERNAME = None
                    return True
                elif back_arrow_box.collidepoint(event.pos):  # Back arrow
                    back_arrow(old_score)
                elif repeat_box.collidepoint(event.pos):  # Encapsulated arrow
                    around_arrow()
                elif play_ground.collidepoint(event.pos):  # Swipe mouse part 1
                    move_mouse = True
                    position = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:  # Released the mouse button
                if move_mouse:  # Swipe mouse part 2
                    move_mouse = False
                    if position != event.pos:
                        source_swipe = get_side(position, event.pos)
                        if source_swipe[1] > 30:
                            command_side = {'UP': move_up, 'DOWN': move_down,
                                            'LEFT': move_left, 'RIGHT': move_right}
                            copy_mas = copy.deepcopy(mas)
                            mas, delta, is_mas_move = command_side[source_swipe[0]](mas)
                            score += delta
                            render_screen(score, delta)
                            draw_victory()
            elif event.type == pygame.KEYDOWN:  # Pressed the key
                delta = 0
                if event.key == pygame.K_ESCAPE:
                    save_game()
                    pygame.quit()
                    sys.exit()
                elif event.key == 104:  # Menu
                    insert_result(USERNAME, score)
                    USERNAME = None
                    return True
                elif event.key == 98:  # Back arrow
                    back_arrow(old_score)
                elif event.key == 114:  # Encapsulated arrow
                    around_arrow()
                elif event.key == pygame.K_LEFT or event.key == 97:  # Left
                    copy_mas = copy.deepcopy(mas)
                    mas, delta, is_mas_move = move_left(mas)
                elif event.key == pygame.K_RIGHT or event.key == 100:  # Right
                    copy_mas = copy.deepcopy(mas)
                    mas, delta, is_mas_move = move_right(mas)
                elif event.key == pygame.K_UP or event.key == 119:  # Up
                    copy_mas = copy.deepcopy(mas)
                    mas, delta, is_mas_move = move_up(mas)
                elif event.key == pygame.K_DOWN or event.key == 115:  # Down
                    copy_mas = copy.deepcopy(mas)
                    mas, delta, is_mas_move = move_down(mas)
                old_score = score
                score += delta
                render_screen(score, delta)
                draw_victory()
    return False


def draw_interface(scr: int, delta: int = 0) -> None:
    """ Draws the main interface

    :param scr: score
    :param delta: delta for score
    :return: None
    """
    back_ground = pygame.image.load("images\\BG\\BackGround.jpg")  # BackGround
    round_arrow = pygame.image.load("images\\elements\\around_arrow.png")  # Encapsulated arrow
    arrow = pygame.image.load("images\\elements\\arrow.png")  # Back arrow
    menu = pygame.image.load("images\\elements\\home.png")  # Menu

    screen.blit(pygame.transform.scale(back_ground, [WIDTH, HEIGHT + 2]), (0, 0))
    screen.blit(pygame.transform.scale(round_arrow, [43, 43]), (453, 159))
    screen.blit(pygame.transform.scale(arrow, [58, 58]), (374, 154))
    screen.blit(pygame.transform.scale(menu, [38, 38]), (314, 162))

    var = lambda x, y: is_what_rank_numbers(y) * 8 if x == 25 else is_what_rank_numbers(y) * 7

    best_score = get_best(1)['score']
    high_score = 0 if best_score == -1 else best_score  # Best result
    size_score, size_high_score = get_size_font(scr, high_score)  # Variable size of the font
    screen.blit(get_font(18, GEN_FONT).render('SCORE', True, COLORS['GRAY']), (300, 55))  # Text score
    screen.blit(get_font(17, GEN_FONT).render('HIGH SCORE', True, COLORS['GRAY']), (402, 55))  # Text high score
    screen.blit(get_font(86, GEN_FONT).render('2048', True, COLORS['WHITE']), (30, 2))  # Text for 2048

    result = var(size_score, scr)  # substitution for number score
    screen.blit(get_font(size_score, GEN_FONT).render(f'{scr}', True, COLORS['WHITE']), (317 - result, 77))

    result = var(size_high_score, high_score)  # substitution for number high score
    screen.blit(get_font(size_high_score, GEN_FONT).render(f'{high_score}', True, COLORS['WHITE']), (440 - result, 77))
    if delta > 0:
        var = is_what_rank_numbers(delta) * 14  # substitution for number delta
        screen.blit(get_font(34, GEN_FONT).render(f'+{delta}', True, COLORS['WHITE']), (115 - var, 160))

    pretty_print(mas)
    for row in range(BLOCKS):  # Building cells
        for column in range(BLOCKS):
            value, font = get_const_4_cell(mas[row][column], GEN_FONT)
            text = font.render(f'{value}', True, get_colour(value))
            w = column * SIZE_BLOCK + (column - 1) * MARGIN + 30
            h = row * SIZE_BLOCK + (row - 1) * MARGIN + 240
            if value != 0:  # Placing numbers on cells
                pygame.draw.rect(screen, COLORS[value], (w, h, SIZE_BLOCK + 2, SIZE_BLOCK + 2), border_radius=7)
                font_w, font_h = text.get_size()
                text_x = w + (SIZE_BLOCK - font_w) / 2
                text_y = h + (SIZE_BLOCK - font_h) / 2 - 6
                screen.blit(text, (text_x, text_y))


# WINDOW CONSTANTS
BLOCKS = 4
SIZE_BLOCK = 112
MARGIN = 9
WIDTH = 520
HEIGHT = 725

is_mas_move = None
mas = None
copy_mas = None
score = old_score = None
USERNAME = None
GEN_FONT = 'vag-world-bold.ttf'  # The main font of the game

COLORS = {
    0: "#545c8a",
    2: '#e4f2fd',
    4: '#badffa',
    8: '#6cb8f4',
    16: '#319eef',
    32: '#2a79d8',
    64: '#275ce6',
    128: '#7420e8',
    256: '#9025c0',
    512: '#b32885',
    1024: '#990066',
    2048: '#bb165b',
    4096: '#1A0553',
    8192: '#02334D',
    16384: '#004949',
    32768: '#1F142F',
    65536: '#000000',
    131072: '#000000',
    262144: '#000000',
    524288: '#000000',
    'WTF?!': '#ffffff',
    'WHITE': '#ebeeff',
    'GRAY': '#aebad0'
}
if __name__ == '__main__':
    # Create a window
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('2048')
    pygame.display.set_icon(pygame.image.load('2048_icon.png'))

    while True:  # Game loop
        load_game()
        if USERNAME is None:
            draw_menu()
        if game_loop():
            continue
        draw_game_over()
