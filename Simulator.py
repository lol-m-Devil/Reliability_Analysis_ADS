import math
import pygame
import sys
import random
import math

# # Parameters
# n_s = 5
# n_d = 10
# v_d = 2 # m/sec
# R_min = 10  # m
# R_c = 200  # m
# R_det = 300  # m
# r = 3
# l = 2
# m_f = 0

# Optional Parameters


# alpha = 6
# S = 10  # sec
# C = 240  # sec

# Drawing Parameters
adsSize = 5
droneSize = 5
health_bar_width = 20
health_bar_height = 6

# Pygame initialization
pygame.init()

# Set up the screen
screen_width = 1000
screen_height = 600
right_screen_width = 380
center_x_ADS = (screen_width + right_screen_width) // 2
center_y_ADS = screen_height // 2
screen = pygame.display.set_mode((screen_width, screen_height))
pause_button_rect = pygame.Rect(20, screen_height - 180, 80, 40)
play_button_rect = pygame.Rect(115, screen_height - 180, 100, 40)
middle_button_text = "Play"
reset_button_rect = pygame.Rect(235, screen_height - 180, 80, 40)

static_rect = pygame.Rect(right_screen_width, 0, screen_width - right_screen_width, screen_height)
captured_static_rect = screen.subsurface(static_rect).copy() 

pause = False

pygame.display.set_caption("Simulation")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LIGHT_RED = (255, 153, 153)
GREEN = (0, 255, 0)
LIGHT_GREEN = (150, 249, 124)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)

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

# Parameters
parameters = {
    "Number of ADS": "2",
    "Number of Drones": "5",
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

# def draw_text_input(x, y, label, value, active):
#     text_surface = font.render(label, True, BLACK)
#     screen.blit(text_surface, (x, y))
#     rect = pygame.Rect(x + 480, y, 100, 32)  # Reduced height to 40 pixels
#     if active:
#         pygame.draw.rect(screen, RED, rect, 2)
#     else:
#         pygame.draw.rect(screen, GRAY, rect, 2)
#     input_text = font.render(value, True, BLACK)
#     screen.blit(input_text, (x + 490, y+5))

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
                # return (flag == 0)

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

# Function to generate random points on a circle
def generate_points_on_circle(radius, num_points):
    points = []
    for _ in range(num_points):
        angle = random.uniform(0, 2 * math.pi)
        x = center_x_ADS + radius * math.cos(angle)
        y = center_y_ADS + radius * math.sin(angle)
        points.append((int(x), int(y)))
    return points

def draw_ui2():
    global middle_button_text
    screen.fill(WHITE)
    # screen.blit(captured_static_rect, (right_screen_width, 0))
    # pygame.draw.rect(screen, WHITE, (right_screen_width, 0, right_screen_width, screen_height))

    # font = pygame.font.SysFont(None, 24)  # Choose your font and size
    # text = "Press Play to start the simulation."
    # text_lines = text.split('\n')
    # text_rendered = font.render(text, True, BLACK)
    # rect = pygame.Rect(right_screen_width, 0, right_screen_width, screen_height)
    # pygame.draw.rect(screen, BLACK, (0, 0, right_screen_width, screen_height))
    # pygame.draw.rect(screen, WHITE, rect)

    # # Calculate text position for center alignment
    # text_width, text_height = font.size(text)
    # text_x = right_screen_width + rect.centerx - text_width // 2
    # text_y = rect.centery - text_height // 2
    # screen.blit(text_rendered, (text_x, text_y))

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

# Draw concentric circles and the square box at the center
def draw_environment():
    global middle_button_text
    screen.fill((135, 206, 250))
    pygame.draw.circle(screen, (144, 238, 144), (center_x_ADS, center_y_ADS), R_det, 0)
    pygame.draw.circle(screen, (255, 195, 77), (center_x_ADS, center_y_ADS), R_c, 0)
    pygame.draw.circle(screen, (255, 160, 0), (center_x_ADS, center_y_ADS), R_min, 0)
    pygame.draw.rect(screen, RED, (center_x_ADS - ( adsSize//2 ), center_y_ADS - ( adsSize//2 ), adsSize, adsSize))

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

        # print(key, value, key_x, key_y, value_x, value_y, box_x, box_y, box_width, box_height)
        
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

# Draw squares at the random points on the outermost circle
def draw_random_points(points, R):
    for point in points:
        pygame.draw.rect(screen, RED, (point[0] - (droneSize//2), point[1] - (droneSize//2), droneSize, droneSize))
        health_bar_x = point[0] - (health_bar_width//2)
        health_bar_y = point[1] - (droneSize//2) - health_bar_height
        
        pygame.draw.rect(screen, BLACK, (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
        health_bar_width_remaining = int(health_bar_width * R[points.index(point)] / r)
        pygame.draw.rect(screen, GREEN, (health_bar_x, health_bar_y, health_bar_width_remaining, health_bar_height))
        
def update_points_position(points):
    for i in range(len(points)):
        point_x, point_y = points[i]
        distance = math.sqrt((center_x_ADS - point_x) ** 2 + (center_y_ADS - point_y) ** 2)
        if distance == 0:
            continue
        dx = (center_x_ADS - point_x) * v_d / distance
        dy = (center_y_ADS - point_y) * v_d / distance
        points[i] = (point_x + dx, point_y + dy)

    return points

def draw_assignment_lines(points, assignment):
    for i in range(len(assignment)):
        drone_index = assignment[i]
        if drone_index < len(points):
            pygame.draw.line(screen, RED, (center_x_ADS, center_y_ADS), points[drone_index], 2)

def f(num_strikes_till_now, param = 0.005, a = 999):
    return 1/(1+a*math.exp(-param*num_strikes_till_now))

def iteration(L, R, t0, m_f, assignment):
    L_new = []
    for num_lasers in L:
        num_failures = sum([1 if random.random() < f(t0) else 0 for _ in range(num_lasers)])
        L_new.append(num_lasers - num_failures)
    
    print(L_new)    
    countLasers = [0 for _ in range(len(R))]
    for i in range(len(assignment)):
        countLasers[assignment[i]] += L[i]
    R_new = []
    sum_failures = 0
    for i in range(len(R)):
        num_failures = sum([1 if random.random() < m_f else 0 for _ in range(countLasers[i])] )
        num_strikes = countLasers[i] - num_failures
        R_new.append(max(0, R[i] - num_strikes))
        sum_failures = sum_failures + num_failures
    
    print(sum_failures)    
    print(R_new)
    return [L_new, R_new]

def main_loop():
    global captured_static_rect
    global pause

    if n_d == 0:
        return 0
    # Initialize the environment    
    points_on_outer_circle = generate_points_on_circle( R_det, n_d)
    L = [l for _ in range(n_s)]
    R = [r for _ in range(n_d)]
    assignment = list(random.randint(0, len(R)-1) for _ in range(len(L)))
    
    # Main game loop
    running = True
    t = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if Pause or Play buttons are clicked
                if pause_button_rect.collidepoint(event.pos):
                    pause = True
                elif play_button_rect.collidepoint(event.pos):
                    pause = False
                elif reset_button_rect.collidepoint(event.pos):
                    return -1

        if not pause:
            draw_environment()
            draw_random_points(points_on_outer_circle, R)

            distance = min(math.sqrt((center_x_ADS - point_x) ** 2 + (center_y_ADS - point_y) ** 2) for point_x, point_y in points_on_outer_circle)

            tq = t % (alpha*S + C)
            if ( tq <= alpha*S and distance <= R_c):
                draw_assignment_lines(points_on_outer_circle, assignment)
                if ( tq % S == 0 ):
                    
                    t0 = alpha*math.floor(t/(S*alpha + C)) + min(math.floor(t%(S*alpha + C)/S), alpha)
                    [L, R] = iteration(L, R, t0, m_f, assignment)
                    
                    R_new = [index for index in range(len(R)) if R[index] > 0]
                    if len(R_new) == 0:
                        running = False
                        continue
                    assignment = list(random.choice(R_new) for _ in range(len(L)))
                

            new_points_on_outer_circle = []
            for i in range(len(R)):
                if ( R[i] > 0 ):
                    new_points_on_outer_circle.append(points_on_outer_circle[i])
                else:
                    new_points_on_outer_circle.append((2*screen_width, 2*screen_height))
            points_on_outer_circle = new_points_on_outer_circle
            points_on_outer_circle = update_points_position(points_on_outer_circle)
            distance = min(math.sqrt((center_x_ADS - point_x) ** 2 + (center_y_ADS - point_y) ** 2) for point_x, point_y in points_on_outer_circle)
            
            if ( distance <= R_c):
                t = t + 1

            if( distance <= R_min):
                running = False
            
            pygame.display.flip()
            pygame.time.Clock().tick(5)
        
    return len([r for r in R if r > 0])   

def success_screen():
    global middle_button_text
    success_rect = pygame.Rect(right_screen_width, 0, screen_width - right_screen_width, screen_height)
    pygame.draw.rect(screen, GREEN, success_rect)
    
    font = pygame.font.Font(None, 36)
    text = font.render("Objective completed successfully", True, BLACK)
    text_rect = text.get_rect(center=success_rect.center)
    screen.blit(text, text_rect)

    middle_button_text = "Restart"
    pygame.display.flip()
    pygame.time.wait(2000)

    # flag = True
    # while flag:
    #     flag = not handle_events_new()

def failure_screen():
    global middle_button_text
    success_rect = pygame.Rect(right_screen_width, 0, screen_width - right_screen_width, screen_height)
    pygame.draw.rect(screen, LIGHT_RED, success_rect)
    
    font = pygame.font.Font(None, 36)
    text = font.render("Objective failed", True, BLACK)
    text_rect = text.get_rect(center=success_rect.center)
    screen.blit(text, text_rect)

    middle_button_text = "Restart"
    pygame.display.flip()
    pygame.time.wait(2000)
    
# Main function
def main():
    # welcome_screen()
    
    # wrong_input = True
    # while wrong_input:
    #     wrong_input = not handle_events()
    #     draw_ui()
    #     pygame.display.flip()

    run = True
    final_result = -1
    while run:
        update_variables()
        if final_result == 0:
            success_screen()
            final_result = -1
        elif final_result > 0:
            failure_screen()
            final_result = -1

        if final_result == -1:
            start = True
            while start:
                start = not handle_events_new()
                draw_ui2()
                pygame.display.flip()

        final_result = main_loop()

if __name__ == "__main__":
    main()

