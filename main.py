#!/usr/bin/env python3

# Import necessary libraries and classes
import pvp
import easyAI
import mediumAI
import hardAI
import pygame
import sys

# Define some colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 100, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
WINDOW_SIZE = (910, 950)
WIDTH, HEIGHT = WINDOW_SIZE

# Create the Pygame window
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Connect4")

# Define fonts
title_font = pygame.font.SysFont(None, 120, bold=True, italic=True)
font = pygame.font.SysFont("Arial", 60, bold=True, italic=False)

# Define the available game options with their corresponding text and game object
menu_options = [
    {"text": "PVP", "game": pvp},
    {"text": "Easy", "game": easyAI},
    {"text": "Medium", "game": mediumAI},
    {"text": "Hard", "game": hardAI},
    {"text": "Quit Game", "game": None},
]

def draw_text(text, font, colour, x, y):
    pygame.font.init()

    # Draws text on the screen
    text_surface = font.render(text, True, colour)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def draw_menu():
    # Define colours for menu options
    colour_options = [GREEN, YELLOW, ORANGE, RED, WHITE]

    # Define border colour and width
    border_colour = BLACK
    border_width = 2

    # Draws the title "Connect4" on the screen
    draw_text("Connect4", title_font, WHITE, WIDTH/2, HEIGHT/4)
    # Creates an empty list to store the option rectangles
    option_rects = []
    # Loops through the menu options and creates a text surface and rectangle for each option
    for index, option in enumerate(menu_options):
        # Renders the option text
        option_text = font.render(option["text"], True, BLACK)

        # Centers the option rectangle vertically and horizontally
        option_rect = option_text.get_rect(center=(WIDTH/2, HEIGHT/2.5 + index * 90))

        # Adds the option rectangle to the list of option rectangles
        option_rects.append(option_rect)

        # Defines the rectangle with border
        option_colour = colour_options[index % len(colour_options)]
        rect_with_border = pygame.Rect(option_rect.left - border_width, option_rect.top - border_width,
                                    option_rect.width + 2 * border_width, option_rect.height + 2 * border_width)

        # Draws the rectangle with border
        pygame.draw.rect(screen, border_colour, rect_with_border, 0, border_radius=10)
        pygame.draw.rect(screen, option_colour, option_rect, 0, border_radius=10)

        # Draws the option text
        screen.blit(option_text, option_rect)
        
    # Returns the list of option rectangles
    return option_rects

def menu():
    # Draws the menu on the screen and gets the rectangles for each option
    option_rects = draw_menu()
    # Updates the display to show the menu
    pygame.display.flip()
    # Sets the initial choice to None
    choice = None
    # Waits for the player to make a choice
    while choice is None:
        # Gets all the events in the event queue
        for event in pygame.event.get():
            # If the player has clicked the close button on the window, exit the game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # If the player has clicked the mouse button, check if they clicked on an option
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Left mouse click
                # Gets the position of the mouse click
                mouse_pos = event.pos
                # Iterates over all the option rectangles and checks if the mouse is inside one of them
                for index, option_rect in enumerate(option_rects):
                    if option_rect.collidepoint(mouse_pos):
                        # If the mouse is inside an option rectangle, get the corresponding game
                        choice = menu_options[index]["game"]
                        # If the player has chosen to quit the game, exit the game
                        if choice is None:
                            pygame.quit()
                            sys.exit()
    # Return the chosen game
    return choice

def main():
    # Runs the game
    while True:
        # Displays the menu and gets the player's choice
        choice = menu()
        # If the player has chosen to quit the game, exit the game loop
        if choice is None:
            break
        # Otherwise, start the chosen game
        choice.play()

if __name__ == '__main__':
    main()