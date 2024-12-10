##PLEASE CHANGE THE WORKING DIRECTORY AS PER FOLDER LOCATION##
import pygame
import time
import os
import subprocess  # To execute another Python script

# Change working directory
os.chdir(r"INPUT_WORKING__DIR")

# Initialize Pygame
pygame.init()



# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("8-Bit Game Intro")

# Load images for text
title_image = pygame.image.load("data/source/title.png")  # Image for "SPACE-O-RAMA!"
title_image = pygame.transform.scale(title_image, (400, 100))  # Resize if needed

start_image = pygame.image.load("data/source/enter.png")  # Image for "Press Enter to Start"
start_image = pygame.transform.scale(start_image, (400, 50))  # Resize if needed

# Main game intro loop
def intro_screen():
    running = True
    while running:

        # Draw title and start prompt images
        screen.blit(title_image, (width // 2 - title_image.get_width() // 2, height // 2 - 100))
        screen.blit(start_image, (width // 2 - start_image.get_width() // 2, height // 2 + 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False

        pygame.display.flip()  # Update display
        time.sleep(0.01)

# Run the intro screen
intro_screen()

# Close current script and run main.py
script_path = "data/earth_final.py"  # Replace with the name of your main script
if os.path.exists(script_path):
    pygame.quit()  # Ensure Pygame closes before running the next script
    subprocess.run(["python", script_path])
else:
    print(f"Script '{script_path}' not found! Ensure it exists in the directory.")
    pygame.quit()
