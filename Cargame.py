import pygame
import time
import random
import os
from random_image import random_image

# Initialize pygame
pygame.init()
pwd = os.getcwd()
score = 0

# Define colors here
gray = (119, 118, 110)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 200, 0)
blue = (0, 0, 200)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)
bright_blue = (0, 0, 255)

# Display dimensions
display_width = 1200
display_height = 800

# Setup a game display
gamedisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.update()
pygame.display.set_caption("Traffic Model")
clock = pygame.time.Clock()

# Load assets
gameplay_background_image = pygame.image.load("./assets/background_image.jpg")
road_image = pygame.image.load("./assets/road_image.jpg")
car_image = pygame.image.load("./assets/Audi_Skinny_2.png")
crossing_image = pygame.image.load("./assets/crossing_image.png")
trafficlight_green_image = pygame.image.load("./assets/trafficlight_green.png")
trafficlight_yellow_image = pygame.image.load("./assets/trafficlight_yellow.png")
trafficlight_red_image = pygame.image.load("./assets/trafficlight_red.png")
intro_background_image = pygame.image.load("./assets/intro_background.jpg")
paused_background_image = pygame.image.load("./assets/pause_icon.png")

# Initialize pause state
paused = False

end_of_road = False

# Def Text Object
def text_objects(text, font):
    textsurface = font.render(text, True, black)
    return textsurface, textsurface.get_rect()

# Def Button Object
def button(button_text, x, y, width, height, inactive_color, active_color, action=None):
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse_pos[0] > x and y + height > mouse_pos[1] > y:
        pygame.draw.rect(gamedisplay, active_color, (x, y, width, height))

        if click[0] == 1 and action is not None:
            if action == "play":
                countdown()
            elif action == "quit":
                pygame.quit()
                quit()
                sys.exit()
            elif action == "menu":
                main_menu()
            elif action == "pause":
                pause()
            elif action == "unpause":
                unpause()
    else:
        pygame.draw.rect(gamedisplay, inactive_color, (x, y, width, height))

    smalltext = pygame.font.Font("freesansbold.ttf", 20)
    textsurf, textrect = text_objects(button_text, smalltext)
    textrect.center = ((x + (width / 2)), (y + (height / 2)))
    gamedisplay.blit(textsurf, textrect)

def pause():
    global paused

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                sys.exit()
        gamedisplay.blit(paused_background_image, (0, 0))
        largetext = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects("PAUSED", largetext)
        TextRect.center = ((display_width / 2), (display_height / 2))
        gamedisplay.blit(TextSurf, TextRect)

        button("Continue", 150, 450, 150, 50, green, bright_green, "unpause")
        button("Restart", 350, 450, 150, 50, blue, bright_blue, "play")
        button("Main Menu", 550, 450, 200, 50, red, bright_red, "menu")

        pygame.display.update()
        clock.tick(30)

def unpause():
    global paused
    paused = False

def show_sign(x_sign_start, y_sign_start, sign):
    font = pygame.font.Font("freesansbold.ttf", 60)
    prediction = font.render(f"Prediction: {sign}", True, black)

    # gamedisplay.blit(prediction, (x_sign_start, y_sign_start - 100))
    gamedisplay.blit(sign, (x_sign_start, y_sign_start))

def score_system(score):
    font = pygame.font.SysFont(None, 50)
    score = font.render(f"Score: {score}", True, black)
    gamedisplay.blit(score, (0, 50))

def gameover_display(text):
    largetext = pygame.font.Font("freesansbold.ttf", 80)
    textsurf, textrect = text_objects(text, largetext)
    textrect.center = ((display_width / 2), (display_height / 2))

    gamedisplay.blit(textsurf, textrect)
    pygame.display.update()
    time.sleep(0.5)
    game_loop()

def loop():
    gameover_display("Loading New Loop...")

def background():
    gamedisplay.blit(gameplay_background_image, (0, 0))
    gamedisplay.blit(road_image, (275, 0))

def car(x, y):
    gamedisplay.blit(car_image, (x, y))

def select_random_file():
    pwd = os.getcwd()
    sign_folder_list = os.listdir(fr"{pwd}\CNN_Road_Sign\road_signs_img")

    image_paths = []
    folder_choice = random.choice(['0 TrafficLight', '1 Stop', '2 speedlimit', '3 Crosswalk'])
    for folder in sign_folder_list:
        if folder == folder_choice:
            choice = random.choice(os.listdir(fr"{pwd}\CNN_Road_Sign\road_signs_img\{folder}"))
    return (fr"{pwd}\CNN_Road_Sign\road_signs_img\{folder_choice}\{choice}", folder_choice)

def main_menu():
    main_menu = True
    while main_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gamedisplay.blit(intro_background_image, (0, 0))
        largetext = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects("Traffic Model", largetext)
        TextRect.center = (400, 100)
        gamedisplay.blit(TextSurf, TextRect)

        button("Start", 150, 520, 100, 50, green, bright_green, "play")
        button("Quit", 550, 520, 100, 50, red, bright_red, "quit")

        pygame.display.update()
        clock.tick(50)

def set_scene():
    font = pygame.font.SysFont(None, 50)
    x = (display_width * 0.35)
    y = (display_height * 0.95)

    background()

    gamedisplay.blit(car_image, (x, y))

    score = font.render(f"Score: {0}", True, black)
    gamedisplay.blit(score, (0, 50))

    button("Pause", 650, 0, 150, 50, blue, bright_blue, "pause")

def countdown():
    countdown = True
    while countdown:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gamedisplay.fill(gray)
        set_scene()

        largetext = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects("GO!", largetext)
        TextRect.center = ((display_width / 2), (display_height / 2))
        gamedisplay.blit(TextSurf, TextRect)
        pygame.display.update()
        clock.tick(1)

        game_loop()

def game_loop():
    global paused, score
    x = (display_width * 0.35)
    y = (display_height * 0.95)
    x_change = 0
    obstacle_speed = 9
    y_change = -2
    scored = False

    result = random_image()
    sign = pygame.image.load(result[0])
    sign_prediction = result[1]

    gameover = False
    while not gameover:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        paused = True
        gamedisplay.fill(gray)

        background()

        show_sign(560, 200, sign)

        score_system(score)

        if sign_prediction == 'crosswalk':
            if not scored:
                score += 1
                scored = True
            gamedisplay.blit(crossing_image, (275, 400))
            y += y_change
            car(x, y)
            if y == 478:
                y_change = 0
                time.sleep(1)
                y_change = -4
        elif sign_prediction == 'speedlimit80':
            if not scored:
                score += 1
                scored = True
            y_change = -8
            y += y_change
            car(x, y)
        elif sign_prediction == 'stop':
            if not scored:
                score += 1
                scored = True
            y += y_change
            car(x, y)
            if y == 478:
                y_change = 0
                time.sleep(2)
                y_change = -4
        elif sign_prediction == 'trafficlight':
            if not scored:
                score += 1
                scored = True
            y += y_change
            car(x, y)

            if y > 550:
                gamedisplay.blit(trafficlight_yellow_image, (250, 400))

            if y > 478 and 550 > y:
                gamedisplay.blit(trafficlight_red_image, (250, 400))

            if y == 478:
                y_change = 0
                time.sleep(3)
                y += -1
                gamedisplay.blit(trafficlight_green_image, (250, 400))
                time.sleep(0.3)

            if y < 478:
                gamedisplay.blit(trafficlight_green_image, (250, 400))
                y_change = -4
        else:
            x += x_change
            y += -2
            car(x, y)

        if y < 0:
            scored = False
            game_loop()

        button("Pause", 650, 0, 150, 50, blue, bright_blue, "pause")
        pygame.display.update()
        clock.tick(60)

main_menu()
pygame.quit()
quit()
