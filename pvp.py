# Import necessary libraries
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
        board = [[0 for i in range(COLUMN_COUNT)] for j in range(ROW_COUNT)]
        return board

    # Function to print out the current game board to the console
    def print_board(board):
        print(board)

    # Define grid and background colours
    BLACK = (0, 0, 0)
    WHITE = (240, 255, 255)

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
                    # Draw circles for player 1's discs with chosen colour
                    pygame.draw.circle(screen, p1_colour, (x + WINDOW//2, y + 3*WINDOW//2), CIRCLE_RADIUS)
                elif board[row][col] == 2:
                    # Draw circles for player 2's discs with chosen colour
                    pygame.draw.circle(screen, p2_colour, (x + WINDOW//2, y + 3*WINDOW//2), CIRCLE_RADIUS)
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
        title_text = font.render("You Selected PVP Mode!", True, WHITE)
        screen.blit(title_text, (50, 50))

        # Render and display the prompt for player 1 to select a colour
        choice_text = font.render("Player 1, Please choose a colour:", True, WHITE)
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
                            # Grey out the selected color square
                            pygame.draw.rect(screen, GREY, rect)
                            pygame.draw.line(screen, RED, (rect.left + 10, rect.top + 10), (rect.right - 10, rect.bottom - 10), 5)
                            pygame.draw.line(screen, RED, (rect.left + 10, rect.bottom - 10), (rect.right - 10, rect.top + 10), 5)
                            colour_option_text = font.render(colour_name, True, BLACK)
                            screen.blit(colour_option_text, (rect.centerx - colour_option_text.get_width()//2, rect.centery - colour_option_text.get_height()//2))

        # If player 1 has already made their choice, remove the "Player 1: Choose a colour:" message from the screen
        if p1_choice is not None:
            pygame.draw.rect(screen, BLACK, (50, 100, 400, 40))

        # Display "Player 2: Choose a colour:" message on the screen
        choice_text = font.render("Player 2, Please choose a colour:", True, WHITE)
        screen.blit(choice_text, (50, 100))
        pygame.display.update()

        p2_choice = None
        while not p2_choice:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if back_rect.collidepoint(mouse_pos):
                        navigate_to_main_menu()
                    for i, colour_name in enumerate(colour_names):
                        rect = pygame.Rect(rect_x + (i % 3) * (rect_size + rect_margin), rect_y + (i // 3) * (rect_size + rect_margin), rect_size, rect_size)
                        # If a color option is clicked and it's different from the color chosen by player 1,
                        # assign it to player 2's choice
                        if rect.collidepoint(mouse_pos) and colour_options[i] != p1_choice:
                            p2_choice = colour_options[i]
            # Close the menu as soon as p2_choice is selected
            if p2_choice:
                break

        # Fill the screen with black color
        screen.fill(BLACK)
        # Draw the game board
        draw_board(board)

        # Return both players' color choices
        return p1_choice, p2_choice

    # Call the function and assign the returned values to variables p1_colour and p2_colour so they can be used elsewhere
    p1_colour, p2_colour = display_menu(screen)

    # Draw the initial game board
    draw_board(board)
    pygame.display.update()
    pygame.display.set_caption("Connect4")

    # Function to drop a game disc (i.e. a piece or chip) into the specified column and row on the game board
    def drop_disc(board, row, col, disc):
        board[row][col] = disc

    # Function to check if a location is valid (i.e. if a disc can be placed there)
    def valid_location(board, col):
        return any(row[col] == 0 for row in board)

    # Function to find the next open row in a column                
    def get_row(board, col):
        return next((row for row, row_values in enumerate(board) if row_values[col] == 0), None)

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

    # Set up the font for the game over message
    font = pygame.font.SysFont("Lucida Sans Unicode", 75, bold=True, italic=False)
    count_font = pygame.font.SysFont(None, 30)

    # Initialize the counters for each player
    p1_total_discs = 21
    p2_total_discs = 21

    # Run the game loop
    while not game_over:
        # Check for events (mouse movement or button press)
        for event in pygame.event.get():
            # If the user closes the window, exit the game
            if event.type == pygame.QUIT:
                sys.exit()

            # Check if the event type is a mouse motion
            if event.type == pygame.MOUSEMOTION:
                # Fill a rectangle with a black color to remove any previous previews
                pygame.draw.rect(screen, BLACK, (0, 0, width, WINDOW))
                # Get the x-coordinate of the mouse position
                posx = event.pos[0]
                # If it's player 1's turn, draw a circle with the player 1's color on the screen where the mouse is
                if turn == 0:
                    pygame.draw.circle(screen, p1_colour, (posx, int(WINDOW/2)), CIRCLE_RADIUS)
                # Otherwise, draw a circle with the player 2's color
                else: 
                    pygame.draw.circle(screen, p2_colour, (posx, int(WINDOW/2)), CIRCLE_RADIUS)

                # Draw the player 1's disc counter at the bottom left of the screen
                p1_text = count_font.render("Player 1 Discs: " + str(p1_total_discs) + " discs", True, p1_colour)
                pygame.draw.rect(screen, BLACK, (0, height-40, p1_text.get_width()+20, 60))
                screen.blit(p1_text, (10, height - 32))

                # Draw the player 2's disc counter at the bottom right of the screen
                p2_text = count_font.render("Player 2: " + str(p2_total_discs) + " discs", True, p2_colour)
                pygame.draw.rect(screen, BLACK, (width-p2_text.get_width()-20, height-40, p2_text.get_width()+20, 60))
                screen.blit(p2_text, (width - p2_text.get_width() - 10, height - 32))

                # Draw the "Back" option at the bottom of the screen
                back_text = count_font.render("Back to Main Menu", True, (0, 0, 0), (255, 255, 255))
                back_rect = back_text.get_rect(center=(screen.get_width()//2, screen.get_height()-20))
                pygame.draw.rect(screen, (255, 255, 255), back_rect, border_radius=10)
                screen.blit(back_text, back_rect)

            # Update the display to show the new disc preview and counters
            pygame.display.update()

            # If the user clicks the mouse, drop a disc on the board
            # Check if the event type is a mouse button down
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Fill a rectangle with a black color to remove any previous previews
                pygame.draw.rect(screen, BLACK, (0, 0, width, WINDOW))
            
                # If it's player 1's turn, drop a disc where the user clicked
                if turn == 0:
                    # Get the x-coordinate of the mouse position
                    posx = event.pos[0]
                    # Determine the column where the disc should be dropped
                    col = int(math.floor(posx/WINDOW))

                    # If the location is valid, drop the disc on the board
                    if valid_location(board, col):
                        row = get_row(board, col)
                        drop_disc(board, row, col, 1)
                        p1_total_discs -= 1

                        # Check if the player won, and if so, end the game with a win message
                        if winning_move(board, 1):
                            label = font.render("Player 1 Wins!!", 1, p1_colour)
                            text_rect = label.get_rect(center=(width/2, WINDOW/2))
                            screen.blit(label, text_rect)
                            game_over = True

                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            # Check if the mouse click is within one of the colour option rectangles
                            mouse_pos = pygame.mouse.get_pos()
                            if back_rect.collidepoint(mouse_pos):
                                navigate_to_main_menu()

                # Player 2's turn
                else:	
                    # Get the x-coordinate of the mouse position
                    posx = event.pos[0]
                    # Determine the column where the disc should be dropped
                    col = int(math.floor(posx/WINDOW))

                    # If the selected column is a valid location, drop the disc
                    if valid_location(board, col):
                        row = get_row(board, col)
                        drop_disc(board, row, col, 2)
                        p2_total_discs -= 1

                        # Check if the player won, and if so, end the game with a win message
                        if winning_move(board, 2):
                            label = font.render("Player 2 Wins!!", 1, p2_colour)
                            text_rect = label.get_rect(center=(width/2, WINDOW/2))
                            screen.blit(label, text_rect)
                            game_over = True

                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            # Check if the mouse click is within one of the colour option rectangles
                            mouse_pos = pygame.mouse.get_pos()
                            if back_rect.collidepoint(mouse_pos):
                                navigate_to_main_menu()

                # Print the current state of the board to the console and display it on the screen
                print_board(board)
                draw_board(board)

                # Switches turn from player to player
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