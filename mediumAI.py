# Import necessary libraries
import numpy
import random
import pygame
import math
import sys

# Define the main function to play the game
def play():

    # Define number of rows and columns in the game board
    ROW_COUNT = 6
    COLUMN_COUNT = 7

    # Function to create the game board using the number of rows and columns defined
    def generate_board():
        board = numpy.zeros((ROW_COUNT, COLUMN_COUNT))
        return board

    # Function to print out the current game board to the console
    def print_board(board):
        print(board)

    # Assign integer constants to represent empty cells, player discs and AI discs respectively
    EMPTY = 0
    PLAYER_DISC = 1
    AI_DISC = 2

    # Evaluate a group of 4 discs in a row
    def check_win(group, disc):
        score = 0
        ai_disc = PLAYER_DISC

        # Determine the AI's disc based on the current player's disc
        if disc == PLAYER_DISC:
            ai_disc = AI_DISC

        # Assign a score based on how many discs of the current player's type are in the window
        if group.count(disc) == 4:
            score += 100
        elif group.count(disc) == 3 and group.count(EMPTY) == 1:
            score += 5
        elif group.count(disc) == 2 and group.count(EMPTY) == 2:
            score += 2

        # Subtract points if the opponent has 3 discs in a row with an empty space next to them
        if group.count(ai_disc) == 3 and group.count(EMPTY) == 1:
            score -= 4

        # Subtract points if the opponent has 3 discs in a row horizontally or vertically
        if group.count(ai_disc) == 3 and group.count(EMPTY) == 1:
            if (EMPTY in group[:3] and ai_disc == group[3]) or (EMPTY in group[1:] and ai_disc == group[0]):
                score -= 50

        return score

    # Function to check if there is a winning move on the game board for a given disc (i.e. if there are four discs in a row, column, or diagonal)
    def winning_move(board, disc):
        # Check for horizontal win
        for row in range(ROW_COUNT):
            for col in range(COLUMN_COUNT - 3):
                if board[row][col] == disc and board[row][col + 1] == disc and board[row][col + 2] == disc and board[row][col + 3] == disc:
                    return True

        # Check for vertical win
        for row in range(ROW_COUNT - 3):
            for col in range(COLUMN_COUNT):
                if board[row][col] == disc and board[row + 1][col] == disc and board[row + 2][col] == disc and board[row + 3][col] == disc:
                    return True

        # Check for diagonal win (going up)
        for row in range(ROW_COUNT - 3):
            for col in range(COLUMN_COUNT - 3):
                if board[row][col] == disc and board[row + 1][col + 1] == disc and board[row + 2][col + 2] == disc and board[row + 3][col + 3] == disc:
                    return True

        # Check for diagonal win (going down)
        for row in range(3, ROW_COUNT):
            for col in range(COLUMN_COUNT - 3):
                if board[row][col] == disc and board[row - 1][col + 1] == disc and board[row - 2][col + 2] == disc and board[row - 3][col + 3] == disc:
                    return True

        return False

    # Set the length of the window or line needed to win the game
    WIN_LENGTH = 4

    def score_position(board, disc):
        score = 0

        # Score center column
        center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])] # Get the values of the center column
        center_count = center_array.count(disc) # Count the number of times the AI's disc appears in the center column
        score += center_count * 4 # Add 4 points for each disc in the center column

        # Score Horizontal
        for row in range(ROW_COUNT):
            row_array = [int(i) for i in list(board[row,:])] # Get the values of the current row
            for col in range(COLUMN_COUNT-3):
                group = row_array[col:col+WIN_LENGTH] # Create a group of 4 values from the row
                score += check_win(group, disc) # Check the group and add the score to the total score

        # Score Vertical
        for col in range(COLUMN_COUNT):
            col_array = [int(i) for i in list(board[:,col])] # Get the values of the current column
            for row in range(ROW_COUNT-3):
                group = col_array[row:row+WIN_LENGTH] # Create a group of 4 values from the column
                score += check_win(group, disc) # Check the group and add the score to the total score

        # Score diagonal (going up)
        for row in range(ROW_COUNT-3):
            for col in range(COLUMN_COUNT-3):
                group = [board[row+i][col+i] for i in range(WIN_LENGTH)] # Create a group of 4 values from the diagonal
                score += check_win(group, disc) # Check the group and add the score to the total score

        # Score diagonal (going down)
        for row in range(ROW_COUNT-3):
            for col in range(COLUMN_COUNT-3):
                group = [board[row+3-i][col+i] for i in range(WIN_LENGTH)] # Create a group of 4 values from the diagonal
                score += check_win(group, disc) # Check the group and add the score to the total score

        return score

    # Function to drop a game disc (i.e. a piece or chip) into the specified column and row on the game board
    def drop_disc(board, row, col, disc):
        board[row][col] = disc

    # Function to find the next open row in a column                
    def get_row(board, col):
        return next((row for row, row_values in enumerate(board) if row_values[col] == 0), None)

    # Pick the best move for the AI given the current board state
    def best_move(board, piece):

        valid_locations = get_valid_locations(board)
        best_score = -1000000
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_row(board, col)
            temp_board = board.copy()
            drop_disc(temp_board, row, col, piece)
            score = score_position(temp_board, piece)
            if score > best_score:
                best_score = score
                best_col = col

        return best_col

    # Function to check if a location is valid (i.e. if a disc can be placed there)
    def valid_location(board, col):
        return any(row[col] == 0 for row in board)

    # Get a list of all the valid locations for a new disc to be dropped in
    def get_valid_locations(board):
        valid_locations = []
        for col in range(COLUMN_COUNT):
            if valid_location(board, col):
                valid_locations.append(col)
        return valid_locations

    # Define grid and background colours
    WHITE = (240, 255, 255)
    BLACK = (0, 0, 0)

    # Define player colours
    PURPLE = (104, 34, 139)
    GREEN = (0, 100, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    BLUE = (0, 0, 255)
    ORANGE = (255, 128, 0)
    PINK = (255, 100, 255)
    GREY = (54, 69, 79)
    AQUA = (0, 255, 255)

    # Draw the game board grid, using a nested loop to draw each square and circle
    def draw_board(board):
        for row in range(len(board)):
            for col in range(len(board[0])):
                x, y = col * WINDOW, (ROW_COUNT - row - 1) * WINDOW
                # Draw black squares
                pygame.draw.rect(screen, BLACK, (x, y + WINDOW, WINDOW, WINDOW))
                # Draw white circles
                pygame.draw.circle(screen, WHITE, (x + WINDOW//2, y + 3*WINDOW//2), CIRCLE_RADIUS)
                if board[row][col] == 1:
                    # Draw purple circles for player 1's discs
                    pygame.draw.circle(screen, p1_colour, (x + WINDOW//2, y + 3*WINDOW//2), CIRCLE_RADIUS)
                elif board[row][col] == 2:
                    # Draw green circles for player 2's discs 
                    pygame.draw.circle(screen, ai_colour, (x + WINDOW//2, y + 3*WINDOW//2), CIRCLE_RADIUS)
        # Update the display to show the new board
        pygame.display.update()

    # Generate the game board using the generate_board() function
    board = generate_board()

    # Print the current game board to the console for debugging purposes
    print_board(board)

    # Set game_over flag to False as the game has not yet ended
    game_over = False

    # Set the initial turn to 0, this will be used to keep track of which player's turn it is
    turn = 0

    # Set up the game window by initializing pygame module
    pygame.init()

    # Define size of each square in the game board, which will determine the size of the window
    WINDOW = 130

    # Calculate the radius of the circles that will be used to represent the discs
    CIRCLE_RADIUS = int(WINDOW/2 - 5)

    # Account for counter bar
    BAR_HEIGHT = 40

    # Calculate the width and height of the game window based on the number of columns and rows in the game board
    width = COLUMN_COUNT * WINDOW
    height = ((ROW_COUNT+1) * WINDOW) + BAR_HEIGHT
    size = (width, height)

    # Create the game window using the size calculated above
    screen = pygame.display.set_mode(size)

    # Re-initialize pygame module
    pygame.init()

    # Create the game window using the size calculated above
    screen = pygame.display.set_mode((width, height))

    # Function to return to main menu options
    def navigate_to_main_menu():
        # Fill the screen with black to clear the PvP menu
        screen.fill(BLACK)
        # Call the "main" function from main.py
        from main import main
        main()

    # Define function to display the menu screen for players to choose disc colours
    def display_menu(screen):
        pygame.font.init()
        font = pygame.font.SysFont("Arial", 30, bold=True, italic=False)
        # Define the available colour options and their corresponding names
        colour_options = [PURPLE, GREEN, RED, YELLOW, BLUE, ORANGE, PINK, GREY, AQUA]
        colour_names = ["Purple", "Green", "Red", "Yellow", "Blue", "Orange", "Pink", "Grey", "Aqua"]
        rect_size = 150
        rect_margin = 20
        rect_x = (screen.get_width() - (rect_size*3 + rect_margin*2)) // 2  # center the rectangles horizontally
        rect_y = (screen.get_height() - (rect_size*3 + rect_margin*2)) // 2  # center the rectangles vertically

        # Fill the screen with black background
        screen.fill(BLACK)

        # Render and display the game title
        title_text = font.render("You Selected Medium Mode!", True, WHITE)
        screen.blit(title_text, (50, 50))

        # Render and display the prompt for player 1 to select a colour
        choice_text = font.render("Please choose a colour:", True, WHITE)
        screen.blit(choice_text, (50, 100))

        # Draw the colour options as rectangles with their corresponding colour and names
        for i, colour_name in enumerate(colour_names):
            x = rect_x + (i % 3) * (rect_size + rect_margin)
            y = rect_y + (i // 3) * (rect_size + rect_margin)
            rect = pygame.Rect(x, y, rect_size, rect_size)
            pygame.draw.rect(screen, colour_options[i], rect)
            colour_option_text = font.render(colour_name, True, BLACK)
            screen.blit(colour_option_text, (rect.centerx - colour_option_text.get_width()//2, rect.centery - colour_option_text.get_height()//2))

        # Draw the "Back" option at the bottom of the screen
        back_text = font.render("Back to Main Menu", True, (0, 0, 0), (255, 255, 255))
        back_rect = back_text.get_rect(center=(screen.get_width()//2, screen.get_height()-50))
        pygame.draw.rect(screen, (255, 255, 255), back_rect, border_radius=10)
        screen.blit(back_text, back_rect)

        # Update the display to show the new menu screen
        pygame.display.update()
  
        p1_choice = None
        # Loop until player 1 selects a colour or quits the game using the ESC key
        while not p1_choice:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if the mouse click is within one of the colour option rectangles
                    mouse_pos = pygame.mouse.get_pos()
                    if back_rect.collidepoint(mouse_pos):
                        navigate_to_main_menu()
                    for i, colour_name in enumerate(colour_names):
                        rect = pygame.Rect(rect_x + (i % 3) * (rect_size + rect_margin), rect_y + (i // 3) * (rect_size + rect_margin), rect_size, rect_size)
                        if rect.collidepoint(mouse_pos):
                            # Set player 1's colour choice based on the index of the selected colour option
                            p1_choice = colour_options[i]

        # If player 1 has already made their choice, remove the "Player 1: Choose a colour:" message from the screen
        if p1_choice is not None:
            pygame.draw.rect(screen, BLACK, (50, 100, 400, 40))

        # Create a list of AI colour choices
        ai_choices = [colour for colour in colour_options if colour != p1_choice]
        # Select a random colour from the AI colour choices
        ai_choice = random.choice(ai_choices)

        pygame.display.update()

        # Fill the screen with black background
        screen.fill(BLACK)

        # Draw the game board on the screen
        draw_board(board)

        # Return the player's colour choice and the AI's colour choice
        return p1_choice, ai_choice

    # Call the display_menu function and assign the returned colour choices to p1_colour and ai_colour variables to be used elsewhere
    p1_colour, ai_colour = display_menu(screen)

    # Draw the initial game board
    draw_board(board)
    pygame.display.update()
    pygame. display. set_caption("Connect4")

    # Set up the font for the game over message
    font = pygame.font.SysFont("Lucida Sans Unicode", 65, bold=True, italic=False)
    count_font = pygame.font.SysFont(None, 30)

    # Initialize the counters for each player
    p1_total_discs = 21
    ai_total_discs = 21

    # Define player numbers
    PLAYER = 0
    AI = 1

    # Randomly choose which player goes first
    turn = random.randint(PLAYER, AI)

    # Set up timer
    start_time = 0
    elapsed_time = 0

    # Run the game loop
    while not game_over:
        # Check for events (mouse movement or button press)
        for event in pygame.event.get():
            # If the user closes the window, exit the game
            if event.type == pygame.QUIT:
                sys.exit()

            # If the user moves the mouse, show a preview of where the player's disc will go
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0,0, width, WINDOW))
                posx = event.pos[0]
                if turn == PLAYER:
                    pygame.draw.circle(screen, p1_colour, (posx, int(WINDOW/2)), CIRCLE_RADIUS)

                # Draw the player 1's disc counter at the bottom left of the screen
                p1_text = count_font.render("Player: " + str(p1_total_discs) + " discs", True, p1_colour)
                pygame.draw.rect(screen, BLACK, (0, height-40, p1_text.get_width()+20, 60))
                screen.blit(p1_text, (10, height - 32))

                # Draw the player 2's disc counter at the bottom right of the screen
                ai_text = count_font.render("AI: " + str(ai_total_discs) + " discs", True, ai_colour)
                pygame.draw.rect(screen, BLACK, (width-ai_text.get_width()-20, height-40, ai_text.get_width()+20, 60))
                screen.blit(ai_text, (width - ai_text.get_width() - 10, height - 32))

                # Draw the "Back" option at the bottom of the screen
                back_text = count_font.render("Back to Main Menu", True, (0, 0, 0), (255, 255, 255))
                back_rect = back_text.get_rect(center=(screen.get_width()//2, screen.get_height()-20))
                pygame.draw.rect(screen, (255, 255, 255), back_rect, border_radius=10)
                screen.blit(back_text, back_rect)

            # Update the display to show the new disc preview
            pygame.display.update()

            # If the user clicks the mouse, drop a disc on the board
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0,0, width, WINDOW))
                
                # If it's the player's turn, drop a disc where the user clicked
                if turn == PLAYER:
                    posx = event.pos[0]
                    col = int(math.floor(posx/WINDOW))

                    if valid_location(board, col):
                        row = get_row(board, col)
                        drop_disc(board, row, col, 1)
                        p1_total_discs -= 1

                        # Set the start time if it's the first move
                        if start_time == 0:
                            start_time = pygame.time.get_ticks()

                        # Check if the player has won the game
                        if winning_move(board, PLAYER_DISC):
                            elapsed_time = (pygame.time.get_ticks() - start_time)
                            seconds = elapsed_time // 1000
                            milliseconds = (elapsed_time % 1000) // 10  # Extract milliseconds
                            label = font.render("YOU WIN!! Time: {}.{} seconds".format(seconds, milliseconds), 1, p1_colour)
                            text_rect = label.get_rect(center=(width/2, WINDOW/2))
                            screen.blit(label, text_rect)
                            game_over = True

                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            # Check if the mouse click is within one of the colour option rectangles
                            mouse_pos = pygame.mouse.get_pos()
                            if back_rect.collidepoint(mouse_pos):
                                navigate_to_main_menu()

                        # Switches turn from player to AI
                        turn += 1
                        turn = turn % 2

                        # Print the current state of the board to the console and display it on the screen
                        print_board(board)
                        draw_board(board)

                # If the game is over, wait for user to click "back to main menu" before closing the game window
                if game_over:
                    while True:
                        for event in pygame.event.get():
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                # get current mouse position
                                mouse_pos = pygame.mouse.get_pos()
                                # check if user clicked on "back to main menu" button
                                if back_rect.collidepoint(mouse_pos):
                                    navigate_to_main_menu()
                                    # exit the loop and close the game window
                                    break
                            elif event.type == pygame.QUIT:
                                # handle quit event
                                pygame.quit()
                                sys.exit()
                        else:
                            # continue waiting for user input
                            continue
                        # if the loop was exited, break out of the main game loop and close the game window
                        break

        # AI's turn
        if turn == AI and not game_over:				

            # Choose the best move for the AI player
            col = best_move(board, AI_DISC)

            # If the chosen move is valid, drop the AI player's disc in that column
            if valid_location(board, col):
                pygame.time.wait(500)
                row = get_row(board, col)
                drop_disc(board, row, col, AI_DISC)
                ai_total_discs -= 1

                # Checks for a winning move then ends the game with a message
                if winning_move(board, AI_DISC):
                    elapsed_time = (pygame.time.get_ticks() - start_time)
                    seconds = elapsed_time // 1000
                    milliseconds = (elapsed_time % 1000) // 10  # Extract milliseconds
                    label = font.render("YOU LOSE :( Time: {}.{} seconds".format(seconds, milliseconds), 1, ai_colour)
                    text_rect = label.get_rect(center=(width/2, WINDOW/2))
                    screen.blit(label, text_rect)
                    game_over = True

                # Print and draw the updated game board
                print_board(board)
                draw_board(board)

                # Switch to the other player's turn
                turn += 1
                turn = turn % 2

                # If the game is over, wait for user to click "back to main menu" before closing the game window
                if game_over:
                    while True:
                        for event in pygame.event.get():
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                # get current mouse position
                                mouse_pos = pygame.mouse.get_pos()
                                # check if user clicked on "back to main menu" button
                                if back_rect.collidepoint(mouse_pos):
                                    navigate_to_main_menu()
                                    # exit the loop and close the game window
                                    break
                            elif event.type == pygame.QUIT:
                                # handle quit event
                                pygame.quit()
                                sys.exit()
                        else:
                            # continue waiting for user input
                            continue
                        # if the loop was exited, break out of the main game loop and close the game window
                        break

    # Game is finished, draw black background
    pygame.draw.rect(screen, BLACK, (0, 0, width, height))
    pygame.display.update()