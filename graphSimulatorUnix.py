import pygame
import sys
import random
from math import comb
from itertools import product
import numpy as np
import math
import theoreticalReliabitlity
import os
import threading
from threading import Thread
import multiprocessing
from multiprocessing import Process, Manager, Value
import signal

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH = 1000
HEIGHT = 600
screen_width = 1000
screen_height = 600
right_screen_width = 380
screen = pygame.display.set_mode((screen_width, screen_height))
pause_button_rect = pygame.Rect(20, screen_height - 180, 80, 40)
play_button_rect = pygame.Rect(115, screen_height - 180, 100, 40)
middle_button_text = "Play"
reset_button_rect = pygame.Rect(235, screen_height - 180, 80, 40)


trials = 1

pygame.display.set_caption("Simulation Graph")


static_rect = pygame.Rect(right_screen_width, 0, screen_width - right_screen_width, screen_height)
captured_static_rect = screen.subsurface(static_rect).copy() 

pause = False

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHT_RED = (255, 153, 153)
LIGHT_GREEN = (150, 249, 124)

# Fonts
font = pygame.font.SysFont(None, 32)


# Variable names
n_s = None
n_d = None
v_d = None
R_min = None
R_c = None
R_det = None
r = None
l = None
m_f = None
alpha = None
S = None
C = None

computed_reliability = Value('d', -1)
steps = 0

# Parameters
parameters = {
    "Number of ADS": "1",
    "Number of Drones": "2",
    "Velocity of Drone (m/(10*sec))": "3",
    "Min Allowed Proximity for Drone": "10",
    "Critical Region (m/10)": "200",
    "Detection Region (m/10)": "300",
    "Successful Hits to kill a Drone": "3",
    "Lasers in one ADS": "2",
    "Failure Probability of a strike": "0.25",
    "Max Strikes before ADS requires Cool-down": "6",
    "Strike Time (sec)": "10",
    "Cooldown Time (sec)": "240"
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
    flag = 0
    try:
        C = int(parameters["Cooldown Time (sec)"])
        if C <= 0:
            raise ValueError("Cooldown Time must be a positive integer.")
    except ValueError:
        flag = -12
        print("Invalid input for Cooldown Time (sec). Please enter a valid numerical value.")

    try:
        S = int(parameters["Strike Time (sec)"])
        if S <= 0:
            raise ValueError("Strike Time must be a positive integer.")
    except ValueError:
        flag = -11
        print("Invalid input for Strike Time (sec). Please enter a valid numerical value.")

    try:
        alpha = int(parameters["Max Strikes before ADS requires Cool-down"])
        if alpha <= 0:
            raise ValueError("Max Strikes before ADS requires Cool-down must be a positive integer.")
    except ValueError:
        flag = -10
        print("Invalid input for Max Strikes before ADS requires Cool-down. Please enter a valid numerical value.")

    try:
        m_f = float(parameters["Failure Probability of a strike"])
        if m_f < 0 or m_f > 1:
            raise ValueError("Failure Probability of a strike must be a float between 0 and 1.")
    except ValueError:
        flag = -9
        print("Invalid input for Failure Probability of a strike. Please enter a valid numerical value.")

    try:
        l = int(parameters["Lasers in one ADS"])
        if l <= 0:
            raise ValueError("Lasers in one ADS must be a positive integer.")
    except ValueError:
        flag = -8
        print("Invalid input for Lasers in one ADS. Please enter a valid numerical value.")

    try:
        r = int(parameters["Successful Hits to kill a Drone"])
        if r <= 0:
            raise ValueError("Hits to kill a Drone must be a positive integer.")
    except ValueError:
        flag = -7
        print("Invalid input for Hits to kill a Drone. Please enter a valid numerical value.")

    try:
        R_det = float(parameters["Detection Region (m/10)"])
        if R_det < 0:
            raise ValueError("Detection Region must be a non-negative float.")
    except ValueError:
        flag = -6
        print("Invalid input for Detection Region (m/10). Please enter a valid numerical value.")

    try:
        R_c = float(parameters["Critical Region (m/10)"])
        if R_c < 0:
            raise ValueError("Critical Region must be a non-negative float.")
    except ValueError:
        flag = -5
        print("Invalid input for Critical Region (m/10). Please enter a valid numerical value.")

    try:
        R_min = float(parameters["Min Allowed Proximity for Drone"])
        if R_min < 0:
            raise ValueError("Min Allowed Proximity for Drone must be a non-negative float.")
    except ValueError:
        flag = -4
        print("Invalid input for Min Allowed Proximity for Drone. Please enter a valid numerical value.")

    try:
        v_d = float(parameters["Velocity of Drone (m/(10*sec))"])
        if v_d <= 0:
            raise ValueError("Velocity of Drone must be a positive float.")
    except ValueError:
        flag = -3
        print("Invalid input for Velocity of Drone (m/(10*sec)). Please enter a valid numerical value.")

    try:
        n_d = int(parameters["Number of Drones"])
        if n_d < 0:
            raise ValueError("Number of Drones must be a positive integer.")
    except ValueError:
        flag = -2
        print("Invalid input for Number of Drones. Please enter a valid numerical value.")

    try:
        n_s = int(parameters["Number of ADS"])
        if n_s <= 0:
            raise ValueError("Number of ADS must be a positive integer.")
    except ValueError:
        flag = -1
        print("Invalid input for Number of ADS. Please enter a valid numerical value.")

    return flag
    
def print_variables():
    print("n_s:", n_s)
    print("n_d:", n_d)
    print("v_d:", v_d)
    print("R_min:", R_min)
    print("R_c:", R_c)
    print("R_det:", R_det)
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

def handle_events_new():
    global active_field
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            print(mouse_pos)
            for key, value in parameters.items():
                rect = pygame.Rect(315, 15 + 33 * list(parameters.keys()).index(key), 50, 23)
                if rect.collidepoint(mouse_pos):
                    active_field = key
                    print("Activated = " + active_field)
            if play_button_rect.collidepoint(mouse_pos):
                flag = update_variables()
                print_variables()
                return errorHandle(flag)

        if event.type == pygame.KEYDOWN:
            if active_field:
                if event.key == pygame.K_RETURN:
                    active_field = ""
                elif event.key == pygame.K_BACKSPACE:
                    parameters[active_field] = parameters[active_field][:-1]
                    print("Params = " + parameters[active_field])
                else:
                    parameters[active_field] += event.unicode
                    print("Params = " + parameters[active_field])

def errorHandle(flag):
    if ( flag == 0 ):
        return True
    
    y_offset = 15
    font = pygame.font.Font(None, 20)
    err_button_text = font.render("Error in input format!", True, WHITE)

    add_offset = (flag+1)*-1 *34


    pygame.draw.rect(screen, LIGHT_RED, (390, y_offset+add_offset, 150, 23))
    screen.blit(err_button_text, (400, y_offset + add_offset+ 5))
    pygame.display.flip()
    pygame.time.wait(3000)

    return False

def draw_ui2():
    global middle_button_text
    screen.fill(WHITE)
    font = pygame.font.Font(None, 20)
    
    text_y = 20  # Initial y-coordinate
    for key, value in parameters.items():
        key_surface = font.render(f"{key}:", True, BLACK)
        value_surface = font.render(value, True, BLACK)
        
        key_width, key_height = key_surface.get_size()
        value_width, value_height = value_surface.get_size()
        
        key_x = 20
        key_y = text_y
        screen.blit(key_surface, (key_x, key_y))
        
        value_x = key_x + 300
        value_y = text_y
        screen.blit(value_surface, (value_x, value_y))
        
        # Calculate the position and size of the rectangular box around the value
        box_x = value_x - 5  # Adjust the left margin as needed
        box_y = value_y - 5
        box_width = 50  # Adjust the width padding as needed
        box_height = value_height + 10  # Adjust the height padding as needed
        
        # Draw the rectangular box with a white border
        pygame.draw.rect(screen, BLACK, (box_x, box_y, box_width, box_height), 2)
        if ( key == active_field ):
            pygame.draw.rect(screen, RED, (box_x, box_y, box_width, box_height), 2)
        
        # Increment y-coordinate for the next line
        text_y += max(key_height, value_height) + 20  # Adjust the vertical spacing as needed
    
    pygame.draw.rect(screen, WHITE, pause_button_rect)
    pygame.draw.rect(screen, BLACK, pause_button_rect, 2)
    pygame.draw.rect(screen, WHITE, play_button_rect)
    pygame.draw.rect(screen, BLACK, play_button_rect, 2)
    pygame.draw.rect(screen, WHITE, reset_button_rect)
    pygame.draw.rect(screen, BLACK, reset_button_rect, 2)

    font = pygame.font.Font(None, 30)
    pause_text = font.render("Pause", True, BLACK)
    screen.blit(pause_text, (30, screen_height - 170))
    play_text = font.render(middle_button_text, True, BLACK)
    screen.blit(play_text, (125, screen_height - 170))
    reset_text = font.render("Reset", True, BLACK)
    screen.blit(reset_text, (245, screen_height - 170))

def draw_environment():
    global middle_button_text
    # screen.fill((135, 206, 250))
    
    pygame.draw.rect(screen, WHITE, (0, 0, right_screen_width, screen_height))

    font = pygame.font.Font(None, 20)
    
    text_y = 20  # Initial y-coordinate
    for key, value in parameters.items():
        key_surface = font.render(f"{key}:", True, BLACK)
        value_surface = font.render(value, True, BLACK)
        
        key_width, key_height = key_surface.get_size()
        value_width, value_height = value_surface.get_size()
        
        key_x = 20
        key_y = text_y
        screen.blit(key_surface, (key_x, key_y))
        
        value_x = key_x + 300
        value_y = text_y
        screen.blit(value_surface, (value_x, value_y))
        
        # Calculate the position and size of the rectangular box around the value
        box_x = value_x - 5  # Adjust the left margin as needed
        box_y = value_y - 5
        box_width = 50  # Adjust the width padding as needed
        box_height = value_height + 10  # Adjust the height padding as needed
        
        # Draw the rectangular box with a white border
        pygame.draw.rect(screen, BLACK, (box_x, box_y, box_width, box_height), 2)
        
        # Increment y-coordinate for the next line
        text_y += max(key_height, value_height) + 20  # Adjust the vertical spacing as needed
    
    pygame.draw.rect(screen, WHITE, pause_button_rect)
    pygame.draw.rect(screen, BLACK, pause_button_rect, 2)
    pygame.draw.rect(screen, WHITE, play_button_rect)
    pygame.draw.rect(screen, BLACK, play_button_rect, 2)
    pygame.draw.rect(screen, WHITE, reset_button_rect)
    pygame.draw.rect(screen, BLACK, reset_button_rect, 2)

    middle_button_text = "Play"
    font = pygame.font.Font(None, 30)
    pause_text = font.render("Pause", True, BLACK)
    screen.blit(pause_text, (30, screen_height - 170))
    play_text = font.render(middle_button_text, True, BLACK)
    screen.blit(play_text, (125, screen_height - 170))
    reset_text = font.render("Reset", True, BLACK)
    screen.blit(reset_text, (245, screen_height - 170))

    pygame.display.flip()

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

def calculate_theoretical_reliability(computed_reliability):
    print("Calculating Theoretical Reliability")
    L = [l for _ in range(n_s)]
    R = [r for _ in range(n_d)]
    theoreticalReliabitlity.successdp.clear()
    theoreticalReliabitlity.prob_r_dp.clear()
    computed_reliability.value = theoreticalReliabitlity.successProbability(t0(S,alpha, C, v_d, R_min, R_c), t0(S,alpha, C, v_d, R_min, R_c),L, R ,m_f )  # Set your constant value here
    print("Theoretical Reliability:", computed_reliability.value)

def generate_values():
    while True:
        yield initializer(trials, n_s, n_d, l, r, m_f, t0(S, alpha, C, v_d, R_min, R_c))  # Replace this with your own function to generate values

def draw_graph(values, current_value):
    # Draw box for the graph
    graph_box_height = HEIGHT * 2 // 3
    graph_box_rect = pygame.Rect(right_screen_width, HEIGHT - graph_box_height, WIDTH - right_screen_width, graph_box_height)
    pygame.draw.rect(screen, GRAY, graph_box_rect)

    # Draw X-axis
    pygame.draw.line(screen, BLACK, (right_screen_width, HEIGHT*(9/10)), (WIDTH, HEIGHT *(9/10)), 2)
    # Draw Y-axis
    pygame.draw.line(screen, BLACK, (right_screen_width + 40, HEIGHT * 1 // 3), (right_screen_width + 40, HEIGHT), 2)

    # Draw the graph using the values
    for i in range(len(values) - 1):
        pygame.draw.line(screen, BLUE, (i+right_screen_width + 40, HEIGHT - values[i]), (i + right_screen_width + 40, HEIGHT - values[i + 1]), 2)

    # Draw labels for axes
    font = pygame.font.SysFont("timesnewroman", 20)
    text = font.render(f"Current Simulations: {steps}", True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2 +50, HEIGHT - 40))
    screen.blit(text, text_rect)
    text = font.render("Reliability", True, BLACK)
    text_rect = text.get_rect(center=(right_screen_width+100, HEIGHT* 1//3 + 20 ))
    screen.blit(text, text_rect)

    # Draw boxes for current and constant values
    value_box_height = HEIGHT // 12
    current_value_rect = pygame.Rect(430, HEIGHT * 1 // 3 - 40-value_box_height, 340, value_box_height)
    constant_value_rect = pygame.Rect(430, 40, 340, value_box_height)
    pygame.draw.rect(screen, GRAY, current_value_rect)
    pygame.draw.rect(screen, GRAY, constant_value_rect)



    # Draw text for current and constant values
    font = pygame.font.SysFont("timesnewroman", 22)
    text = font.render(f"Simulated Reliability: {current_value : .6f}", True, BLACK)
    screen.blit(text, (430 + 10, HEIGHT * 1 // 3 - 40- value_box_height +10))


    text = font.render("1", True, BLACK)
    screen.blit(text, (right_screen_width + 25, HEIGHT - 300-11))

    text = font.render("0.5", True, BLACK)
    screen.blit(text, (right_screen_width + 8, HEIGHT - 180-11))
    
    text = font.render("0", True, BLACK)
    screen.blit(text, (right_screen_width + 25, HEIGHT - 45-11))

    
    if computed_reliability.value >= 0:
        text = font.render(f"Theoretical Reliability: {computed_reliability.value : .6f}", True, BLACK)
        pygame.draw.line(screen, RED, (right_screen_width +40, HEIGHT -  240*computed_reliability.value - 60), (WIDTH, HEIGHT - 240*computed_reliability.value - 60), 1)
    else:
        text = font.render("Theoretical Reliability: Evaluating", True, BLACK)
        
    screen.blit(text, (430 + 10, 40 + 10))

    pygame.display.flip()  # Update the display

def main_loop():
    global captured_static_rect
    global pause
    global steps
    
    values = []  
    steps = 0 
    current_value = 0
    clock = pygame.time.Clock()
    
    # Main game loop
    running = True
    pid = os.fork()
    
    if(pid == 0):
        calculate_theoretical_reliability(computed_reliability)
        myPid = os.getpid()
        os.kill(myPid, signal.SIGKILL)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pause_button_rect.collidepoint(event.pos):
                    pause = True
                elif play_button_rect.collidepoint(event.pos):
                    pause = False
                elif reset_button_rect.collidepoint(event.pos):
                    try:
                        os.kill(pid, signal.SIGKILL)
                        print("Killed the child process")
                    except OSError as e:
                        print("Error killing the child process:", e)
                    return -1


        if not pause:
            draw_environment()
            values_generator = generate_values()
            
            # Get the next value from the generator
            next_value = next(values_generator)
            
            current_value = (current_value*steps + next_value)/(steps+trials)
            steps += trials
            values.append(240*current_value + 60)
            
            if len(values) > WIDTH-right_screen_width-40:
                values.pop(0)  # Remove the oldest value if the list is too long

            draw_graph(values, current_value)
            clock.tick(30)  # Adjust the FPS as needed
                
            pygame.display.flip()
                
def main():
    run = True
    final_result = -1
    while run:
        update_variables()
        print_variables()
        if final_result == -1:
            start = True
            while start:
                start = not handle_events_new()
                draw_ui2()
                pygame.display.flip()

        computed_reliability.value = -1
        final_result = main_loop()

if __name__ == "__main__":
    main()
