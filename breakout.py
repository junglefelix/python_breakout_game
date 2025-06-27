import json
import pygame
import random

from ball import Ball #my
level = 1
load_next_level = True
lives= 5
powerup_visible = False
powerup_active = False 
pygame.init()

pygame.mixer.init()  # Initialize the mixer (add this after screen setup)
hit_sound = pygame.mixer.Sound(f"Glass.wav")  # Load the sound (add after ball setup)
paddle_sound = pygame.mixer.Sound(f"Swordswi.wav")  # Load the sound (add after ball setup)
fall_sound = pygame.mixer.Sound(f"Sweepdow.wav")
# Screen settings
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout Clone")

font = pygame.font.SysFont("Arial", 20)

COLOR_MAP = {
    "BLACK": (0, 0, 0),
    "GREY":(90,90,90),
    "WHITE": (255, 255, 255),
    "RED": (255, 0, 0),
    "Blue": (0, 150, 255),
    "BLUE": (0, 150, 255),
    "purpule": (150, 0, 255),
    "LIGHT_YELLOW": (255, 255, 150),
    "Light Yellow": (255, 255, 150),
    "LIGHT_GREEN": (150, 255, 150),
    "Light Green": (150, 255, 150),
    "LIGHT_PINK": (255, 200, 200),
    "Light Pink": (255, 200, 200),
    "LIGHT_CYAN": (200, 255, 255),
    "Light Cyan": (200, 255, 255),
}


# Paddle settings
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
paddle_x = WIDTH // 2 - PADDLE_WIDTH // 2
paddle_y = HEIGHT - 40
paddle_speed = 5
paddle_color = COLOR_MAP.get("Blue")  # Initial paddle color

# Ball settings
BALL_SIZE = 10
balls = [
    Ball(WIDTH // 2, HEIGHT // 1.2, 4, -4, BALL_SIZE, COLOR_MAP.get("WHITE"))
]

# Brick settings
BRICK_WIDTH = 80
BRICK_HEIGHT = 30
BRICK_ROWS = 5
BRICK_COLS = WIDTH // BRICK_WIDTH
bricks = []

# powerup settings
powerup_shrink_width = 60
powerup_shrink_height = 20
# List of possible powerups
powerups = [
    {"type": "add_life", "description": "Add 1 life", "color": COLOR_MAP.get("LIGHT_GREEN")},
    {"type": "expand_paddle", "description": "Expand paddle size", "color": COLOR_MAP.get("LIGHT_PINK")},
    {"type": "shrink_paddle", "description": "Shrink paddle size", "color": COLOR_MAP.get("LIGHT_PINK")},
    {"type": "increase_ball_speed", "description": "Increase ball speed", "color": COLOR_MAP.get("BLUE")},
    {"type": "decrease_ball_speed", "description": "Decrease ball speed", "color": COLOR_MAP.get("BLUE")},
    {"type": "multi_ball", "description": "Spawn multiple balls", "color": COLOR_MAP.get("LIGHT_CYAN")},
    {"type": "slow_paddle", "description": "Slow down paddle movement", "color": COLOR_MAP.get("WHITE")},
    {"type": "fast_paddle", "description": "Speed up paddle movement", "color": COLOR_MAP.get("WHITE")},
    {"type": "brick_piercing", "description": "Ball pierces through bricks", "color": COLOR_MAP.get("LIGHT_GREEN")},
    {"type": "reverse_controls", "description": "Reverse paddle controls", "color": COLOR_MAP.get("purpule")},
    {"type": "extra_points", "description": "Gain extra points", "color": COLOR_MAP.get("LIGHT_YELLOW")},
    {"type": "reduce_brick_hits", "description": "Reduce hits required for all bricks", "color": COLOR_MAP.get("LIGHT_CYAN")},
    {"type": "random_color_paddle", "description": "Change paddle to a random color", "color": COLOR_MAP.get("RED")},
    {"type": "random_color_ball", "description": "Change ball to a random color", "color": COLOR_MAP.get("RED")},
    {"type": "freeze_bricks", "description": "Freeze bricks for a short time", "color": COLOR_MAP.get("WHITE")},
]


def load_bricks_from_file(level_file, BRICK_WIDTH, BRICK_HEIGHT):
    bricks = []
    with open(level_file, "r") as file:
        brick_data = json.load(file)
    for data in brick_data:
        x = data["x"]
        y = data["y"]
        color_name = data.get("color", "RED")  # Default to RED if color not specified
        color = COLOR_MAP.get(color_name, COLOR_MAP.get("RED"))  # Default to RED if color not found
        hits = data.get("hits", 1)

        brick = {
            "rect": pygame.Rect(x, y, BRICK_WIDTH - 3, BRICK_HEIGHT - 3),
            "color": color,  
            "hidden": False,
            "hits": hits  
        }
        bricks.append(brick)
    return bricks

clock = pygame.time.Clock()

# Game loop
running = True

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_x < WIDTH - PADDLE_WIDTH:
        paddle_x += paddle_speed

    # Ball movement
    # ball_x += ball_dx
    # ball_y += ball_dy
    for ball in balls:
        ball.move()

    # powerup movement
    if powerup_visible:
        powerup_y += 3
        if powerup_y > HEIGHT:
            powerup_visible = False
            powerup_y = 0
            powerup_active = False
    
    # Check for powerup collision with paddle
    if powerup_visible and paddle.colliderect(powerup_rect):
        powerup_visible = False  # Hide the powerup after collecting it
        powerup_active = False
        # Apply powerup effect (e.g., increase paddle size)
        if powerup_type["type"] == "add_life":
            lives = lives +1
            print(f"Powerup collected: {powerup_type['description']}")
            print(f"Lives: {lives}")
        elif powerup_type["type"] == "expand_paddle":
            paddle_width_increase = 20
            PADDLE_WIDTH = PADDLE_WIDTH + paddle_width_increase

            paddle_x = max(0, paddle_x - paddle_width_increase // 2)  # Center the paddle
            PADDLE_WIDTH = min(PADDLE_WIDTH, WIDTH - paddle_x)  # Ensure it doesn't go off screen
            #paddle_color = COLOR_MAP.get("LIGHT_GREEN")  # Change paddle color on powerup
            powerup_visible = False  # Hide the powerup after collecting it
            #owerup_y = 0  # Reset powerup position
        elif powerup_type["type"] == "shrink_paddle":
            paddle_width_decrease = 20
            PADDLE_WIDTH = max(20, PADDLE_WIDTH - paddle_width_decrease)
            print(f"Powerup collected: {powerup_type['description']}")
            print(f"Paddle Width: {PADDLE_WIDTH}")
        elif powerup_type["type"] == "increase_ball_speed":
            for ball in balls:
                ball.dx *= 1.2
                ball.dy *= 1.2
            print(f"Powerup collected: {powerup_type['description']}")

        elif powerup_type["type"] == "decrease_ball_speed":
            for ball in balls:
                ball.dx *= 0.8
                ball.dy *= 0.8
            print(f"Powerup collected: {powerup_type['description']}")

        elif powerup_type["type"] == "multi_ball":
            # Logic to spawn multiple balls
            new_balls = []
            for ball in balls:
                # Create two new balls at the same position as the current ball
                new_balls.append(Ball(ball.x, ball.y, -abs(ball.dx)/2, -abs(ball.dy), ball.size, ball.color))  # Up-left
                #print(f"added ball1 x: {ball.x}, y: {ball.y} , dx: {-abs(ball.dx)/2}, dy: {-abs(ball.dy)}")
                new_balls.append(Ball(ball.x, ball.y, abs(ball.dx)/2, -abs(ball.dy), ball.size, ball.color))   # Up-right
                #print(f"added ball2 x: {ball.x}, y: {ball.y} , dx: {abs(ball.dx)/2}, dy: {-abs(ball.dy)}")
            balls.extend(new_balls)  # Add the new balls to the existing list
            print(f"Powerup collected: {powerup_type['description']}")
            print(f"Number of balls: {len(balls)}")
        elif powerup_type["type"] == "slow_paddle":
            paddle_speed *= 0.5
            print(f"Powerup collected: {powerup_type['description']}")
            print(f"Paddle Speed: {paddle_speed}")
        elif powerup_type["type"] == "fast_paddle":
            paddle_speed *= 1.5
            print(f"Powerup collected: {powerup_type['description']}")
            print(f"Paddle Speed: {paddle_speed}")
        elif powerup_type["type"] == "brick_piercing":
            # Logic to make the ball pierce through bricks (not implemented in this example)
            print(f"Powerup collected: {powerup_type['description']}")
        elif powerup_type["type"] == "reverse_controls":
            # Logic to reverse paddle controls (not implemented in this example)
            print(f"Powerup collected: {powerup_type['description']}")
        elif powerup_type["type"] == "extra_points":
            # Logic to gain extra points (not implemented in this example)
            print(f"Powerup collected: {powerup_type['description']}")
        elif powerup_type["type"] == "reduce_brick_hits":
            # Logic to reduce hits required for all bricks (not implemented in this example)
            print(f"Powerup collected: {powerup_type['description']}")
        elif powerup_type["type"] == "random_color_paddle":
            paddle_color = random.choice([color for name, color in COLOR_MAP.items() if name != "BLACK"])
            print(f"Powerup collected: {powerup_type['description']}")
            print(f"Paddle Color: {paddle_color}")
        elif powerup_type["type"] == "random_color_ball":
            ball_color = random.choice([color for name, color in COLOR_MAP.items() if name != "BLACK"])
            print(f"Powerup collected: {powerup_type['description']}")
            print(f"Ball Color: {ball_color}")
        elif powerup_type["type"] == "freeze_bricks":
            # Logic to freeze bricks for a short time (not implemented in this example)
            print(f"Powerup collected: {powerup_type['description']}")      

        #paddle_x = max(0, paddle_x - paddle_width_increase // 2)  # Center the paddle
        #PADDLE_WIDTH = min(PADDLE_WIDTH, WIDTH - paddle_x)  # Ensure it doesn't go off screen
        #paddle_color = COLOR_MAP.get("LIGHT_GREEN")  # Change paddle color on powerup
        #powerup_visible = False  # Hide the powerup after collecting it
        #owerup_y = 0  # Reset powerup position              

    # Ball collision with walls
    for ball in balls[:]:  # Iterate over a copy of the list to allow removal
        if ball.x <= 0 or ball.x >= WIDTH - ball.size:
            ball.bounce_horizontal()
        if ball.y <= 0:
            ball.bounce_vertical()
        if ball.y >= HEIGHT:  # Ball falls off screen
            balls.remove(ball)  # Remove the ball from the list
            if not balls:  # Check if all balls are gone
                fall_sound.play()
                pygame.time.delay(2000)
                lives -= 1
                if lives == 0:
                    running = False
                else:
                    # Reset the game state with one new ball
                    balls.append(Ball(WIDTH // 2, HEIGHT // 1.2, 4, -4, BALL_SIZE, COLOR_MAP.get("WHITE")))

    # Ball collision with paddle
    paddle = pygame.Rect(paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT)
    for ball in balls:
        ball_rect = pygame.Rect(ball.x, ball.y, ball.size, ball.size)
        if paddle.colliderect(ball_rect):
            ball.bounce_vertical()  # Reverse the ball's vertical direction
            #print(f"Ball {ball} bounced off the paddle")

            # Adjust ball direction based on where it hits the paddle
            hit_pos = (ball.x + ball.size // 2) - paddle_x
            #print(f"hit_pos: {hit_pos}")
            ball.dx = (hit_pos - PADDLE_WIDTH // 2) / (PADDLE_WIDTH // 2) * 4
            #print(f"ball.dx: {ball.dx}")
            paddle_sound.play()


    # Load next level if needed
    if load_next_level:
        # Display level message
        screen.fill(COLOR_MAP.get("BLACK"))
        large_font = pygame.font.SysFont("Arial", 40)  # Create a larger font
        level_text = large_font.render(f"Level {level}", True, COLOR_MAP.get("LIGHT_YELLOW"))
        level_text_rect = level_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(level_text, level_text_rect)
        pygame.display.flip()

        # Pause for 3 seconds
        pygame.time.delay(3000)

        # Load new bricks and reset ball/paddle
        bricks = load_bricks_from_file(f"level{level}.json", BRICK_WIDTH, BRICK_HEIGHT)
        print(f"level: {level}")

        # Reset the balls list with one new ball
        balls = [
            Ball(WIDTH // 2, HEIGHT // 1.2, 4, -4, BALL_SIZE, COLOR_MAP.get("WHITE"))
        ]

        level += 1
        load_next_level = False
        powerup_active = False 

    # Ball collision with bricks
    for ball in balls:
        ball_rect = pygame.Rect(ball.x, ball.y, ball.size, ball.size)
        for brick in bricks[:]:  # Copy list to avoid modification issues
            if brick["rect"].colliderect(ball_rect):
                hits = brick["hits"]
                #print(f"brick hits: {hits}")
                #print(f"Brick coordinates: {brick['rect'].x}, {brick['rect'].y}")
                #print(f"ball coordinates: {ball_rect.x}, {ball_rect.y}")

                # Chance to spawn a powerup
                if powerup_active == False:
                    if random.random() < 0.9:  # 10% chance to spawn a powerup
                        print("Powerup occurred!")
                        powerup_x = brick["rect"].x + (BRICK_WIDTH - powerup_shrink_width) // 2
                        powerup_y = brick["rect"].y + (BRICK_HEIGHT - powerup_shrink_height) // 2
                        powerup_rect = pygame.Rect(powerup_x, powerup_y, powerup_shrink_width, powerup_shrink_height)
                        powerup_visible = True
                        powerup_type = random.choice(powerups)
                        powerup_active = True
                       # powerup_type = next((p for p in powerups if p["type"] == "multi_ball"), None)

                # Calculate overlap on each side
                brick_rect = brick["rect"]
                top_overlap = ball_rect.bottom - brick_rect.top
                bottom_overlap = brick_rect.bottom - ball_rect.top
                left_overlap = ball_rect.right - brick_rect.left
                right_overlap = brick_rect.right - ball_rect.left

                # Find the smallest overlap to determine the collision side
                min_overlap = min(top_overlap, bottom_overlap, left_overlap, right_overlap)

                # Check direction of ball movement and overlap to confirm collision side
                if min_overlap == top_overlap and ball.dy > 0:
                    ball.bounce_vertical()
                elif min_overlap == bottom_overlap and ball.dy < 0:
                    ball.bounce_vertical()
                elif min_overlap == left_overlap and ball.dx > 0:
                    ball.bounce_horizontal()
                elif min_overlap == right_overlap and ball.dx < 0:
                    ball.bounce_horizontal()
           

                # Reduce brick hits and remove if destroyed
                hits -= 1
                brick["hits"] = hits
                if hits == 0:
                    bricks.remove(brick)

                hit_sound.play()

                # Check if all bricks are destroyed
                if len([brick for brick in bricks if brick["hits"] > 0]) == 0:
                    load_next_level = True
                break

    # Clear screen
    screen.fill(COLOR_MAP.get("BLACK"))

    # Draw paddle
    pygame.draw.rect(screen, paddle_color, (paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))

    # Draw ball
    #pygame.draw.ellipse(screen, ball_color, (ball_x, ball_y, BALL_SIZE, BALL_SIZE))
    for ball in balls:
        ball.draw(screen)

    # Draw powerup (if any)
    if powerup_visible:
        powerup_rect = pygame.Rect(powerup_x, powerup_y, powerup_shrink_width, powerup_shrink_height)
        # Draw the powerup rectangle
        pygame.draw.rect(screen, powerup_type["color"], powerup_rect)

    # Draw bricks
    for brick in bricks:
        pygame.draw.rect(screen, brick["color"], brick["rect"])


    text = font.render(f"lives:{lives}",True,COLOR_MAP.get("LIGHT_PINK"))  # Text, antialiasing, color
    text_r = text.get_rect(center=(30, 20))  # Center the text
    screen.blit(text, text_r)

    # Update display
    pygame.display.flip()

    # Control frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()