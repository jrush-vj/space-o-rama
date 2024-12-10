import random
import pygame
import os

os.chdir(r"C:\Jerush\Coding_Programming\Side-Projects\pyjam")
# Initialize Pygame
pygame.init()

pygame.mixer.init()

# Load and play background music
pygame.mixer.music.load("data/source/intro_music.mp3")  # Replace with the correct path
pygame.mixer.music.set_volume(0.5)  # Set volume (0.0 to 1.0)
pygame.mixer.music.play(-1)  # Play music on loop (-1 for infinite looping)

# Set up the display
screen_width = 576
screen_height = 324          
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Parallax Background and Character Animation")

# Clock for controlling FPS
clock = pygame.time.Clock()

# Function to extract frames from a spritesheet
def extract_frames(spritesheet_path, frame_width, frame_height):
    try:
        spritesheet = pygame.image.load(spritesheet_path).convert_alpha()
    except pygame.error as e:
        print(f"Error loading spritesheet: {e}")
        return []  # Return an empty list if loading fails
    
    sheet_width, sheet_height = spritesheet.get_size()
    frames = []
    for i in range(sheet_width // frame_width):  # Assuming frames are horizontal
        frame = spritesheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
        frames.append(frame)
    return frames

# Load animations from each spritesheet
animations = {
    "Idle": extract_frames("C:\\Jerush\\Coding_Programming\\Side-Projects\\pyjam\\data\\anims\\Fighter\\Idle.png", 128, 128),
    "Run_right": extract_frames("C:\\Jerush\\Coding_Programming\\Side-Projects\\pyjam\\data\\anims\\Fighter\\Run_right.png", 128, 128),
    "Run_left": extract_frames("C:\\Jerush\\Coding_Programming\\Side-Projects\\pyjam\\data\\anims\\Fighter\\Run_left.png", 128, 128),
    "Jetpack": extract_frames("C:\\Jerush\\Coding_Programming\\Side-Projects\\pyjam\\data\\anims\\Fighter\\Jetpack.png", 128, 128),  # Jetpack animation
}

# Load the images with transparency preserved
background_far = pygame.image.load("C:/Jerush/Coding_Programming/Side-Projects/pyjam/data/source/earth/background_far.png").convert_alpha()
background_mid = pygame.image.load("C:/Jerush/Coding_Programming/Side-Projects/pyjam/data/source/earth/background_mid.png").convert_alpha()
background_front = pygame.image.load("C:/Jerush/Coding_Programming/Side-Projects/pyjam/data/source/earth/background_front.png").convert_alpha()
ground = pygame.image.load("C:/Jerush/Coding_Programming/Side-Projects/pyjam/data/source/earth/ground.png").convert_alpha()

# Define the speeds at which each background moves (parallax effect)
far_speed = 0.8
mid_speed = 2.0
front_speed = 3.0
ground_speed = 4.0

# Player variables
player_width = 128
player_height = 128
player_x = screen_width // 2 - player_width // 2
player_y = screen_height - player_height - 50
player_speed = 12
player_state = "Idle"
previous_state = player_state
frame_index = 0            
animation_speed = 0.2
frame_timer = 0
is_jetpacking = False  # Replace is_jumping with is_jetpacking
jetpack_fuel = 100# Fuel percentage (out of 100)
jetpack_fuel_consumption = 0.5  # Rate of fuel consumption when jetpacking
fuel_recovery_rate = 0.5  # Fuel recovery rate when not jetpacking
horizontal_movement = 0

# Background repeat variables
num_repeats = 30  # Number of repetitions for the ground
repeat_count = 0
loop_ended = False

# Set initial background positions
bg_far_x = 0
bg_mid_x = 0
bg_front_x = 0
ground_x = 0

# Font for displaying counter and text
font = pygame.font.SysFont("Arial", 24, bold=True)
large_font = pygame.font.SysFont("Arial", 48, bold=True)

# Transition flag
level_transition = False
transition_timer = 0
transition_duration = 3  # Duration of the level transition (in seconds)

# Gravity and jetpack thrust
gravity = 0.5 
jetpack_thrust = 1  # Upward force when jetpacking
falling_gravity = 10  # Increased gravity when fuel is empty

# Player animation frame update control
frame_update_delay = 0.2       # Delay in seconds between frame updates
frame_timer += animation_speed  # Use the global animation speed for frame timing


# Main game loop
running = True
while running:
    screen.fill((0, 0, 0))  # Clear the screen with black color
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the keys currently being pressed
    keys = pygame.key.get_pressed()

    if not loop_ended:
        # Move the player and backgrounds based on input
        if keys[pygame.K_a]:  # Move left
            player_state = "Run_left"
            player_x -= player_speed  # Move player left
            bg_far_x += far_speed
            bg_mid_x += mid_speed
            bg_front_x += front_speed
            ground_x += ground_speed

        elif keys[pygame.K_d]:  # Move right
            player_state = "Run_right"
            player_x += player_speed  # Move player right
            bg_far_x -= far_speed
            bg_mid_x -= mid_speed
            bg_front_x -= front_speed
            ground_x -= ground_speed

        elif keys[pygame.K_LCTRL]:  # Shielding
            player_state = "Shield"

        elif keys[pygame.K_LSHIFT]:  # Attacking
            player_state = "Attack"

        else:
            player_state = "Idle"  # Switch to idle animation when no keys are pressed


# Check for jetpack activation or deactivation
    # Check for jetpack activation or deactivation
    if keys[pygame.K_SPACE] and jetpack_fuel > 0:
        # While spacebar is pressed, jetpack is active
        is_jetpacking = True
        player_state = "Jetpack"
        player_y -= jetpack_thrust  # Move the player upwards
        jetpack_fuel -= jetpack_fuel_consumption  # Consume fuel while jetpacking
    else:
        # When spacebar is released and the player is in the air
        if player_y < screen_height - player_height - 50:  # Player is still in the air
            is_jetpacking = False
            gravity = falling_gravity  # Apply stronger gravity when in the air after space is released
            player_y += gravity  # Apply gravity to the player
    
            # Ensure the player doesn't fall below the ground
            if player_y >= screen_height - player_height - 50:
                player_y = screen_height - player_height - 50  # Keep player on the ground
                gravity = 0.5  # Reset gravity back to normal when grounded

        else:
            # If player is on the ground, reset gravity and other states
            player_y = screen_height - player_height - 50  # Ensure player is grounded
            gravity = 0.5  # Reset gravity to normal when grounded
            is_jetpacking = False  # Stop jetpacking if player is on the ground
        if not is_jetpacking and jetpack_fuel < 100:
            jetpack_fuel += fuel_recovery_rate  # Gradually recover fuel
            jetpack_fuel = min(jetpack_fuel, 100)  # Ensure fuel doesn't exceed 100

    # Check for ground repetition and loop  end
    if not loop_ended:
        if ground_x <= -ground.get_width():
            ground_x = 0
            repeat_count += 1
            if repeat_count >= num_repeats:
                loop_ended = True
                level_transition = True  # Trigger level transition

    # Draw the backgrounds with the updated positions
    screen.blit(background_far, (bg_far_x, 0))
    screen.blit(background_far, (bg_far_x + background_far.get_width(), 0))  # Draw the background again to create the looping effect

    screen.blit(background_mid, (bg_mid_x, 0))
    screen.blit(background_mid, (bg_mid_x + background_mid.get_width(), 0))

    screen.blit(background_front, (bg_front_x, 0))
    screen.blit(background_front, (bg_front_x + background_front.get_width(), 0))

    # Draw the ground (scrolling with the player)
    screen.blit(ground, (ground_x, screen_height - ground.get_height()))
    screen.blit(ground, (ground_x + ground.get_width(), screen_height - ground.get_height()))  # Draw the ground again for looping effect
        # In the main game loop, inside the event checking

# Fuel logic for falling down
    if jetpack_fuel <= 0:  # If fuel is empty, start falling
        player_state = "Idle"  # Ensure the state is "Idle" when falling down
        is_jetpacking = False  # Stop any jetpack-related actions
        
# Handle falling due to gravity after fuel is empty
    if jetpack_fuel <= 0 and player_y < screen_height - player_height - 50:
        # Apply gravity effect
        player_y += 10  # Adjust gravity value as per your needs
        if player_y >= screen_height - player_height - 50:
            player_y = screen_height - player_height - 50  # Ensure player doesn't go below the ground level
            # After landing on the ground, stop the fall (reset fuel or trigger a new event as needed)
            is_jetpacking = False

    # Animate the player character
    current_animation = animations.get(player_state, animations["Idle"])

    if frame_timer >= frame_update_delay:
        frame_timer = 0
        # Safely update the frame index, ensuring it stays within the bounds
        frame_index = (frame_index + 1) % len(current_animation)


    # Check if there are frames available in the current animation
    if current_animation and len(current_animation) > 0:
        # Draw the current frame of the player's animation
        screen.blit(current_animation[frame_index], (screen_width // 2 - player_width // 2, player_y))
    else:
        # Fallback: Draw the idle animation's first frame if no frames are found
        fallback_frame = animations["Idle"][0] if animations["Idle"] else None
        if fallback_frame:
            screen.blit(fallback_frame, (screen_width // 2 - player_width // 2, player_y))

# Make sure we have frames to display
    if current_animation and len(current_animation) > 0:
        frame_timer += animation_speed
        if frame_timer >= 1:
            frame_timer = 0
            frame_index = (frame_index + 1) % len(current_animation)  # Prevent index out of range

        # Draw the current frame of the player's animation (idle in the case of falling)
        screen.blit(current_animation[frame_index], (screen_width // 2 - player_width // 2, player_y))
    else:
        # Fallback: Draw the idle animation's first frame if no frames are found
        fallback_frame = animations["Idle"][0] if animations["Idle"] else None
        if fallback_frame:
            screen.blit(fallback_frame, (screen_width // 2 - player_width // 2, player_y))

# Optionally, display the fuel bar and other UI elements

    # Display the repeat counter
    counter_text = font.render(f"Ground Loops: {repeat_count}/{num_repeats}", True, (255, 255, 255))
    screen.blit(counter_text, (10, 10))

    # Display the fuel bar in the top-right corner
    fuel_bar_width = 200
    fuel_bar_height = 20
    fuel_color = (0, 255, 0) if jetpack_fuel > 50 else (255, 255, 0) if jetpack_fuel > 20 else (255, 0, 0)
    pygame.draw.rect(screen, (255, 255, 255), (screen_width - fuel_bar_width - 10, 10, fuel_bar_width, fuel_bar_height))
    pygame.draw.rect(screen, fuel_color, (screen_width - fuel_bar_width - 10, 10, jetpack_fuel * 2, fuel_bar_height))

    # Show "Level Cleared" when the loop ends
    if loop_ended:
        level_cleared_text = large_font.render("Level Cleared!", True, (255, 255, 0))
        screen.blit(level_cleared_text, (screen_width // 2 - level_cleared_text.get_width() // 2, screen_height // 2 - level_cleared_text.get_height() // 2))
        
        # Handle level transition logic
        if level_transition:
            transition_timer += 1
            if transition_timer > transition_duration * 60:  # Convert seconds to frames (assuming 60 FPS)
                # Here you can reload the level or transition to a new scene
                print("Transitioning to next level...")
                pygame.time.delay(1000)  # Small delay before transitioning

                # Reset everything and load the new level (e.g., reset player position, backgrounds, etc.)
                level_transition = False
                repeat_count = 0  # Reset ground loops
                loop_ended = False
                bg_far_x = 0
                bg_mid_x = 0
                bg_front_x = 0
                ground_x = 0
                player_x = screen_width // 2 - player_width // 2
                player_y = screen_height - player_height - 50
                player_state = "Idle"  # Reset player state

    # Update the screen
    pygame.display.flip()

    # Set the frame rate
    clock.tick(45)
# Quit Pygame
pygame.quit()
