import pygame
import random

# Pygame Settings
pygame.init()
WIDTH, HEIGHT = 800, 400  # Screen dimensions
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Thompson Sampling Hockey Game")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)

# Font Settings
font = pygame.font.Font(None, 36)

# Ball and Player Settings
ball = {"x": WIDTH // 2, "y": HEIGHT // 2, "dx": 8, "dy": 8, "radius": 10}  # Ball properties
player1 = {"x": 50, "y": HEIGHT // 2, "speed": 20, "width": 20, "height": 80}  # Player 1 properties
player2 = {"x": WIDTH - 70, "y": HEIGHT // 2, "speed": 20, "width": 20, "height": 80}  # Player 2 properties

# Strategy Settings
strategies = 3  # Number of strategies
rewards_1 = [0] * strategies  # Success rewards for each strategy
rewards_0 = [0] * strategies  # Failure rewards for each strategy

# Scores
score_p1 = 0  # Player 1's score
score_p2 = 0  # Player 2's score

def thompson_sampling():
    """
    Selects a strategy using the Thompson Sampling algorithm.
    Returns the chosen strategy.
    """
    max_random = 0
    chosen_strategy = 0
    for strategy in range(strategies):
        random_beta = random.betavariate(rewards_1[strategy] + 1, rewards_0[strategy] + 1)
        if random_beta > max_random:
            max_random = random_beta
            chosen_strategy = strategy
    return chosen_strategy

def simulate_defense(strategy, ball_y, player_y):
    """
    Adjusts player movement based on the selected strategy.
    - Strategy 0: Move directly to the ball's position.
    - Strategy 1: Predict the ball's future position with some randomness.
    - Strategy 2: Move randomly.
    """
    if strategy == 0:
        return ball_y
    elif strategy == 1:
        return ball_y + random.randint(-30, 30)
    elif strategy == 2:
        return player_y + random.choice([-10, 10])

# Game Loop
running = True
while running:
    screen.fill(LIGHT_BLUE)  # Set background color
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Ball Movement
    ball["x"] += ball["dx"]
    ball["y"] += ball["dy"]
    if ball["y"] - ball["radius"] < 0 or ball["y"] + ball["radius"] > HEIGHT:
        ball["dy"] *= -1  # Bounce off walls
    
    # Strategy Selection
    chosen_strategy_p1 = thompson_sampling()
    chosen_strategy_p2 = thompson_sampling()

    # Player Movement
    player1["y"] = simulate_defense(chosen_strategy_p1, ball["y"], player1["y"])
    player2["y"] = simulate_defense(chosen_strategy_p2, ball["y"], player2["y"])

    # Boundary Check
    player1["y"] = max(0, min(HEIGHT - player1["height"], player1["y"]))
    player2["y"] = max(0, min(HEIGHT - player2["height"], player2["y"]))

    # Goal Check
    if ball["x"] - ball["radius"] < player1["x"] + player1["width"]:
        if player1["y"] <= ball["y"] <= player1["y"] + player1["height"]:
            ball["dx"] *= -1  # Collision
        else:
            score_p2 += 1
            ball["x"], ball["y"] = WIDTH // 2, HEIGHT // 2  # Reset position
    elif ball["x"] + ball["radius"] > player2["x"]:
        if player2["y"] <= ball["y"] <= player2["y"] + player2["height"]:
            ball["dx"] *= -1  # Collision
        else:
            score_p1 += 1
            ball["x"], ball["y"] = WIDTH // 2, HEIGHT // 2  # Reset position

    # Drawing
    pygame.draw.circle(screen, RED, (ball["x"], ball["y"]), ball["radius"])
    pygame.draw.rect(screen, BLUE, (player1["x"], player1["y"], player1["width"], player1["height"]))
    pygame.draw.rect(screen, BLACK, (player2["x"], player2["y"], player2["width"], player2["height"]))

    # Display Scores
    score_text = font.render(f"P1: {score_p1} - P2: {score_p2}", True, BLACK)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
