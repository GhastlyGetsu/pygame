import pygame
pygame.init()

W, H = 640, 640
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Birdie
bird_x = W // 4
bird_y = H // 2
bird_w, bird_h = 34, 34
velocity = 0.0
GRAVITY = 0.75
JUMP_STRENGTH = -11

game_state = "playing"
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            velocity = JUMP_STRENGTH
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            velocity = JUMP_STRENGTH

    # Physics
    velocity += GRAVITY
    bird_y += velocity
    # Boundary
    if bird_y < 0:
        bird_y = 0
        velocity = 0

    if bird_y > H - bird_h:
        bird_y = H - bird_h
        velocity = 0

    screen.fill("#000000")

    pygame.draw.rect(screen, "#FFFFFF", (bird_x, int(bird_y), bird_w, bird_h))
    
    pygame.display.flip()
    dt = clock.tick(60) / 1000
