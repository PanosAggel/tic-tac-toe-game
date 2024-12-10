import pygame,random
from pygame.locals import *

pygame.init()

screen_width = 300
screen_height = 300

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('TicTacToe')


# Define variables
line_width = 6
markers = []
clicked = False
pos = []
player = 1
winner = 0
start_game = False
game_over = False
player_vs_ai = False

# Define colors
blue = (0, 0, 255)
yellow = (255, 255, 0)
purple = (128, 0, 128)

# Define font
font = pygame.font.SysFont(None, 40)

# Create rectangles
again_rect = Rect(70, 150, 160, 50)
option1_rect = Rect(40, 90, 225, 50)
option2_rect = Rect(70, 150, 170, 50)
settings_icon_hitbox = Rect(260, 5, 35, 35)

# Settings icon png
settings_icon = pygame.image.load("TicTacToe/assets/settings_cogwheel.png").convert()
settings_icon = pygame.transform.scale(settings_icon, (35, 35))

# Game logic:
# Board creation
def create_board():
    for x in range(3):
        row = [0] * 3
        markers.append(row)

create_board()

# Checking for win or draw
def check_winner():

    global winner
    global game_over

    y_pos = 0
    for x in markers:
        # Check columns
        if sum(x) == 3:
            winner = 1
            game_over = True
        if sum(x) == -3:
            winner = 2
            game_over = True

        # Check rows
        if markers[0][y_pos] + markers[1][y_pos] + markers[2][y_pos] == 3:
            winner = 1
            game_over = True            
        if markers[0][y_pos] + markers[1][y_pos] + markers[2][y_pos] == -3:
            winner = 2
            game_over = True            
        y_pos += 1

    # Check cross
    if markers[0][0] + markers[1][1] + markers[2][2] == 3 or  markers[2][0] + markers[1][1] + markers[0][2] == 3:
        winner = 1
        game_over = True
    if markers[0][0] + markers[1][1] + markers[2][2] == -3 or  markers[2][0] + markers[1][1] + markers[0][2] == -3:
        winner = 2
        game_over = True

    # Check draw
    if all(y != 0 for x in markers for y in x):
        game_over = True


# This will check whether the AI has any winning opportunities at hand or any threats that it needs to block.
# If a row, column or diagonal is equal to the target sum, then the empty cell 
# within the corrsepdonding pattern will be filled with a marker.
def check_for_win_or_threat(target_sum, player_marker):
    # Check horizontal patterns
    for x in range(3):
        if sum(markers[x]) == target_sum:
            for y in range(3):
                if markers[x][y] == 0:
                    markers[x][y] = player_marker
                    return True

    # Check vertical patterns
    for y in range(3):
        if markers[0][y] + markers[1][y] + markers[2][y] == target_sum:
            for x in range(3):
                if markers[x][y] == 0:
                    markers[x][y] = player_marker
                    return True

    # Check diagonal patterns (Top-left to bottom-right)
    if markers[0][0] + markers[1][1] + markers[2][2] == target_sum:
        for x in range(3):
            if markers[x][x] == 0:
                markers[x][x] = player_marker
                return True

    # Check diagonal patterns (Top-right to bottom-left)
    if markers[0][2] + markers[1][1] + markers[2][0] == target_sum:
        for x in range(3):
            if markers[x][2 - x] == 0:
                markers[x][2 - x] = player_marker
                return True

    # No move found
    return False


# AI plays as second player
def ai_play():
    global markers

    empty_cells = []  # List of empty cells on the board
    for x in range(3):
        for y in range(3):
            if markers[x][y] == 0:
                empty_cells.append((x, y))

    # Prioritize winning moves
    if check_for_win_or_threat(-2, -1):  # Look for two O's to win (player2 = -1, so -1 + -1 = -2 as the target sum)
        return

    # Block player threats
    if check_for_win_or_threat(2, -1):  # Look for two X's to block (player1 = 1, so 1 + 1 = 2 as the target sum)
        return
        
    # If no winning moves are made or no threats are to be blocked, the AI draws a circle in a random empty cell
    if empty_cells:
        random_cell = random.choice(empty_cells)
        markers[random_cell[0]][random_cell[1]] = -1
      

def reset_game():
    global start_game, markers, player, winner, game_over, pos

    markers = []
    pos = []
    player = 1
    winner = 0
    game_over = False
    create_board()


# Drawing the game:
# Color of any button when unpressed
def unpressed_button(text, rect, coords):
    img = font.render(text, True, blue)
    pygame.draw.rect(screen, yellow, rect)
    pygame.draw.rect(screen, blue, rect, 2)
    screen.blit(img, coords)

# Color of any button when pressed
def pressed_button(text, rect, coords):
    img = font.render(text, True, yellow)
    pygame.draw.rect(screen, blue, rect)
    pygame.draw.rect(screen, blue, rect, 2)
    screen.blit(img, coords) 


# Draw main menu
def draw_main_menu():
    global start_game

    # Detecting mouse position and left mouse button state
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()[0]

    # The user chooses 'Player vs Player'
    if option1_rect.collidepoint(mouse_pos) and mouse_pressed:
        pressed_button('Player vs Player', option1_rect, (45, 101))
    else:
        unpressed_button('Player vs Player', option1_rect, (45, 101))

    # The user chooses 'Player vs AI'
    if option2_rect.collidepoint(mouse_pos) and mouse_pressed:
        pressed_button('Player vs AI', option2_rect, (73, 162))
    else:
        unpressed_button('Player vs AI', option2_rect, (73, 162))


def draw_grid():
    bg = (25, 15, 25)
    grid = (50, 50, 50)
    screen.fill(bg)
    for x in range(1,3):
        pygame.draw.line(screen, grid, (0, x * 100), (screen_width, x * 100), line_width)
        pygame.draw.line(screen, grid, (x * 100, 0), (x * 100, screen_height), line_width)


def draw_markers():
    x_pos = 0
    for x in markers:
        y_pos = 0
        for y in x:
            if y == 1:
                pygame.draw.line(screen, blue, (x_pos * 100 + 15, y_pos * 100 + 15), (x_pos * 100 + 85, y_pos * 100 + 85), line_width)
                pygame.draw.line(screen, blue, (x_pos * 100 + 15, y_pos * 100 + 85), (x_pos * 100 + 85, y_pos * 100 + 15), line_width)
            if y == -1:
                pygame.draw.circle(screen, purple, (x_pos * 100 + 50, y_pos * 100 + 50), 38, line_width)
            y_pos += 1
        x_pos += 1
                

# Draw 'Winner/Draw' and 'Play again' buttons on the screen
def draw_winner(winner):
    if winner != 0:
        win_text = 'Player ' + str(winner) + ' wins!'
        win_img = font.render(win_text, True, blue)
        pygame.draw.rect(screen, yellow, (50, 90, 200, 50))
        pygame.draw.rect(screen, blue, (50, 90, 200, 50), 2)
        screen.blit(win_img, (55, 102))
    else:
        win_text = 'Draw!'
        win_img = font.render(win_text, True, blue)
        pygame.draw.rect(screen, yellow, (101, 90, 100, 50))
        pygame.draw.rect(screen, blue, (101, 90, 100, 50), 2)
        screen.blit(win_img, (112, 102))

    # Display settings icon on the top right
    screen.blit(settings_icon, (260, 5))

    # Change 'Play again' button color when pressed
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()[0]
    if again_rect.collidepoint(mouse_pos) and mouse_pressed:
        pressed_button('Play again?', again_rect, (73, 162))
    else:
        unpressed_button('Play again?', again_rect, (73, 162))


# Main loop
# Initialize clock and frame rate
clock = pygame.time.Clock()
FPS = 60

run = True
while run:

    draw_grid()
    draw_markers()

    if start_game == False:
        draw_main_menu()

    # Event handlers
    for event in pygame.event.get():
        # Quitting the game
        if event.type == pygame.QUIT:
            run = False 
        # Detecting mouse clicks from user
        if game_over == False:
            if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
                clicked = True
            if event.type == pygame.MOUSEBUTTONUP and clicked == True:
                clicked = False         
                pos = pygame.mouse.get_pos()
                cell_x = pos[0]
                cell_y = pos[1]
                # If the game has started then make the mouse clicks have functionality
                if markers[cell_x // 100][cell_y // 100] == 0 and start_game:
                    markers[cell_x // 100][cell_y // 100] = player
                    # Changing to player 2 by having them be represented by -1 
                    player *= -1
                    check_winner()
                    # AI makes the moves of player 2
                    if player_vs_ai and game_over == False:
                        ai_play()
                        player *= -1
                        check_winner()
                # If the game hasn't started, check whether any button is pressed to start, as well as the preferred gamemode
                elif start_game == False:
                    pos = pygame.mouse.get_pos()
                    # 'Player vs Player' button is pressed
                    if option1_rect.collidepoint(pos): 
                        start_game = True
                        player_vs_ai = False
                    # 'Player vs AI' button is pressed
                    elif option2_rect.collidepoint(pos):
                        start_game = True
                        player_vs_ai = True
    if game_over:
        draw_winner(winner)
        
        # Clicking the settings icon
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if settings_icon_hitbox.collidepoint(pos):
                start_game = False
                reset_game()

            # Reset game if "Play Again" button is clicked and then released
            elif again_rect.collidepoint(pos):
                clicked = True  

        if event.type == pygame.MOUSEBUTTONUP and clicked:
            pos = pygame.mouse.get_pos()
            if again_rect.collidepoint(pos):               
                #Reset variables and clear board
                reset_game()
            clicked = False

    pygame.display.update()

    # Limit frame rate
    clock.tick(FPS)


pygame.quit()