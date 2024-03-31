import pygame
import sys
import random
from math import comb
from itertools import product
import numpy as np
import math
import theo_rel

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
screen_width = 800
screen_height = 600
trials = 1
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Real-time Simulation Graph")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Fonts
font = pygame.font.SysFont(None, 32)

# Variable names
n_s = None
n_d = None
v_d = None
R_min = None
R_c = None
r = None
l = None
m_f = None
alpha = None
S = None
C = None



# Parameters

parameters = {
    "Number of ADS": "2",
    "Number of Drones": "5",
    "Velocity of Drone": "3",
    "Min Allowed Proximity for Drone": "10",
    "Critical Region": "200",
    "Hits to kill a Drone": "3",
    "Lasers in one ADS": "2",
    "Failure Probability of a strike": "0.25",
    "Max Strikes before ADS requires Cool-down": "6",
    "Strike Time": "10",
    "Cooldown Time": "240"
}

# Input fields
input_fields = {}
active_field = ""

def draw_text_input(x, y, label, value, active):
    text_surface = font.render(label, True, BLACK)
    screen.blit(text_surface, (x, y))
    rect = pygame.Rect(x + 480, y, 100, 32)  # Reduced height to 40 pixels
    if active:
        pygame.draw.rect(screen, RED, rect, 2)
    else:
        pygame.draw.rect(screen, GRAY, rect, 2)
    input_text = font.render(value, True, BLACK)
    screen.blit(input_text, (x + 490, y+5))

def draw_ui():
    screen.fill(WHITE)
    y_offset = 30  # Reduced height to 40 pixels
    for key, value in parameters.items():
        active = key == active_field
        draw_text_input(50, y_offset, f"{key}:", value, active)
        y_offset += 40  # Reduced height to 40 pixels
    pygame.draw.rect(screen, BLACK, (screen_width//2 - 50, screen_height - 100, 100, 50))
    next_button_text = font.render("Next", True, WHITE)
    screen.blit(next_button_text, (screen_width//2 - 30, screen_height - 80))

def update_variables():
    global n_s, n_d, v_d, R_min, R_c, R_det, r, l, m_f, alpha, S, C
    flag = True
    try:
        n_s = int(parameters["Number of ADS"])
    except ValueError:
        flag = False
        print("Invalid input for Number of ADS. Please enter a valid numerical value.")
    try:
        n_d = int(parameters["Number of Drones"])
    except ValueError:
        flag = False
        print("Invalid input for Number of Drones. Please enter a valid numerical value.")
    try:
        v_d = float(parameters["Velocity of Drone"])
    except ValueError:
        flag = False
        print("Invalid input for Velocity of Drone. Please enter a valid numerical value.")
    try:
        R_min = int(parameters["Min Allowed Proximity for Drone"])
    except ValueError:
        flag = False
        print("Invalid input for Min Allowed Proximity for Drone. Please enter a valid numerical value.")
    try:
        R_c = int(parameters["Critical Region"])
    except ValueError:
        flag = False
        print("Invalid input for Critical Region. Please enter a valid numerical value.")
    try:
        r = int(parameters["Hits to kill a Drone"])
    except ValueError:
        flag = False
        print("Invalid input for Hits to kill a Drone. Please enter a valid numerical value.")
    try:
        l = int(parameters["Lasers in one ADS"])
    except ValueError:
        flag = False
        print("Invalid input for Lasers in one ADS. Please enter a valid numerical value.")
    try:
        m_f = float(parameters["Failure Probability of a strike"])
    except ValueError:
        flag = False
        print("Invalid input for Failure Probability of a strike. Please enter a valid numerical value.")
    try:
        alpha = int(parameters["Max Strikes before ADS requires Cool-down"])
    except ValueError:
        flag = False
        print("Invalid input for Max Strikes before ADS requires Cool-down. Please enter a valid numerical value.")
    try:
        S = int(parameters["Strike Time"])
    except ValueError:
        flag = False
        print("Invalid input for Strike Time. Please enter a valid numerical value.")
    try:
        C = int(parameters["Cooldown Time"])
    except ValueError:
        flag = False
        print("Invalid input for Cooldown Time. Please enter a valid numerical value.")
    return flag
    
def print_variables():
    print("n_s:", n_s)
    print("n_d:", n_d)
    print("v_d:", v_d)
    print("R_min:", R_min)
    print("R_c:", R_c)
    print("r:", r)
    print("l:", l)
    print("m_f:", m_f)
    print("alpha:", alpha)
    print("S:", S)
    print("C:", C)     

def handle_events():
    global active_field
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for key, value in parameters.items():
                rect = pygame.Rect(500, 30 + 40 * list(parameters.keys()).index(key), 100, 32)  # Reduced height to 40 pixels
                if rect.collidepoint(mouse_pos):
                    active_field = key
            if screen_width//2 - 50 < mouse_pos[0] < screen_width//2 + 50 and screen_height - 100 < mouse_pos[1] < screen_height - 50:
                flag = update_variables()
                print_variables()
                return flag
        if event.type == pygame.KEYDOWN:
            if active_field:
                if event.key == pygame.K_RETURN:
                    active_field = ""
                elif event.key == pygame.K_BACKSPACE:
                    parameters[active_field] = parameters[active_field][:-1]
                else:
                    parameters[active_field] += event.unicode


def welcome_screen():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 36)
    text = font.render("Welcome to the graph simulation", True, BLACK)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
    screen.blit(text, text_rect)

    continue_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2, 200, 50)
    pygame.draw.rect(screen, GREEN, continue_button)

    font = pygame.font.Font(None, 30)
    text = font.render("Continue", True, BLACK)
    text_rect = text.get_rect(center=continue_button.center)
    screen.blit(text, text_rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button.collidepoint(event.pos):
                    return





def f(num_strikes_till_now, param = 0.005, a = 999):
    return 1/(1+a*math.exp(-param*num_strikes_till_now))

def iteration(L, R, t, t0, m_f, assignment):
    L_new = []
    for num_lasers in L:
        num_failures = sum([1 if random.random() <= f(t0-t+1) else 0 for _ in range(num_lasers)])
        L_new.append(num_lasers - num_failures)

    countLasers = [0 for _ in range(len(R))]
    for i in range(len(assignment)):
        countLasers[assignment[i]] += L[i]
    R_new = []
    for i in range(len(R)):
        num_failures = sum([1 if random.random() <= m_f else 0 for _ in range(countLasers[i])] )
        num_strikes = countLasers[i] - num_failures
        if (R[i] - num_strikes > 0):
            R_new.append(R[i] - num_strikes)
    return [L_new, R_new]

def initializer(trials, n_s, n_d, l, r, m_f, t0):
    L = [l for _ in range(n_s)]
    R = [r for _ in range(n_d)]

    successCount = 0
    for _ in range(trials):
        if simulator(L, R, m_f, t0, t0):
            successCount += 1
    
    return successCount

def simulator(L, R, m_f, t, t0):
    if len(R) == 0:
        return True
    elif t == 0:   
        return False
    
    assignment = list(random.randint(0, len(R)-1) for _ in range(len(L)))
    [L, R] = iteration(L, R, t, t0, m_f, assignment)
    return simulator(L, R, m_f, t-1, t0)

def t0(S, alpha, C, v_d, R_min, R_c):
    tc = (R_c - R_min)/v_d
    return alpha*math.floor(tc/(S*alpha + C)) + min(math.floor(tc%(S*alpha + C)/S), alpha)
# Function generator
def generate_values():
    while True:
        yield initializer(trials, n_s, n_d, l, r, m_f, t0(S, alpha, C, v_d, R_min, R_c))  # Replace this with your own function to generate values

# Main function to draw the graph
def draw_graph(values, current_value, constant_value, horizontal_line_value):
    screen.fill(WHITE)  # Clear the screen

    # Draw box for the graph
    graph_box_height = HEIGHT * 2 // 3
    graph_box_rect = pygame.Rect(0, HEIGHT - graph_box_height, WIDTH, graph_box_height)
    pygame.draw.rect(screen, GRAY, graph_box_rect)

    # Draw X-axis
    pygame.draw.line(screen, BLACK, (0, HEIGHT*(9/10)), (WIDTH, HEIGHT *(9/10)), 2)
    # Draw Y-axis
    pygame.draw.line(screen, BLACK, (WIDTH*(1/10) + 40, HEIGHT * 1 // 3), (WIDTH *(1/10) + 40, HEIGHT), 2)

    # Draw the graph using the values
    for i in range(len(values) - 1):
        pygame.draw.line(screen, BLUE, (i+121, HEIGHT - values[i]), (i + 122, HEIGHT - values[i + 1]), 2)

    # Draw horizontal line with specific value
    pygame.draw.line(screen, RED, (WIDTH*(1/10) + 40, HEIGHT - horizontal_line_value), (WIDTH, HEIGHT - horizontal_line_value), 2)

    # Draw labels for axes
    font = pygame.font.SysFont("timesnewroman", 20)
    text = font.render("Time", True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT - 40))
    screen.blit(text, text_rect)
    text = font.render("Reliability", True, BLACK)
    text_rect = text.get_rect(center=(65, HEIGHT* 1//3 + 80))
    screen.blit(text, text_rect)

    # Draw boxes for current and constant values
    value_box_height = HEIGHT // 12
    current_value_rect = pygame.Rect(30, 10, 340, value_box_height)
    constant_value_rect = pygame.Rect(430, 10, 340, value_box_height)
    pygame.draw.rect(screen, GRAY, current_value_rect)
    pygame.draw.rect(screen, GRAY, constant_value_rect)

    # Draw text for current and constant values
    font = pygame.font.SysFont("timesnewroman", 22)
    text = font.render(f"Simulated Reliability: {current_value : .6f}", True, BLACK)
    text_rect = text.get_rect(center=(200, 10 + value_box_height // 2))
    screen.blit(text, text_rect)
    text = font.render(f"Theoretical Reliability: {constant_value : .6f}", True, BLACK)
    text_rect = text.get_rect(center=(600, 10 + value_box_height // 2))
    screen.blit(text, text_rect)

    pygame.display.flip()  # Update the display

# Main loop
def main():
    welcome_screen()
    run = True
    while run:
        run = not handle_events()
        draw_ui()
        pygame.display.flip()
    values_generator = generate_values()
    values = []  
    steps = 0 
    current_value = 0
    L = [l for _ in range(n_s)]
    R = [r for _ in range(n_d)]
    theo_rel.successdp.clear()
    theo_rel.prob_r_dp.clear()
    constant_value = theo_rel.successProbability(t0(S,alpha, C, v_d, R_min, R_c), t0(S,alpha, C, v_d, R_min, R_c),L, R ,m_f )  # Set your constant value here
    horizontal_line_value = 240*constant_value + 60  # Set your horizontal line value here
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Get the next value from the generator
        next_value = next(values_generator)
        print(next_value)
        current_value = (current_value*steps + next_value)/(steps+trials)
        steps += trials
        values.append(240*current_value + 60)
        if len(values) > WIDTH:
            values.pop(0)  # Remove the oldest value if the list is too long

        draw_graph(values, current_value, constant_value, horizontal_line_value)
        clock.tick(30)  # Adjust the FPS as needed

if __name__ == "__main__":
    main()
