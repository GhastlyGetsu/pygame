import pygame, random
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

# Pipes
PIPE_MIN = 150
PIPE_MAX = H - 150
PIPE_WIDTH = 80
PIPE_GAP = 200
PIPE_SPEED = 5
pipe_x = W
pipe_y = random.randint(PIPE_MIN, PIPE_MAX)

# Score
score = 0
pipe_scored = False
score_scale = 1.0
score_scale_target = 1.0
score_y = 50
SCORE_POP = 1.5
SCORE_ANIM_SPEED = 6.0


game_state = "playing"

def update_bird():
    global bird_y, velocity
    # Birdie logic
    velocity += GRAVITY
    bird_y += velocity

    if bird_y < 0:
        bird_y = 0
        velocity = 0
    if bird_y > H - bird_h:
        bird_y = H - bird_h
        velocity = 0

def update_pipe():
    global pipe_x, pipe_y, PIPE_WIDTH, PIPE_SPEED, pipe_scored, score, score_scale, score_scale_target
    # Pipe logic
    pipe_x -= PIPE_SPEED
    if pipe_x + PIPE_WIDTH < bird_x and not pipe_scored:
        score += 1
        pipe_scored = True
        score_scale = SCORE_POP
        score_scale_target = 1.0
    if pipe_x < - PIPE_WIDTH:
        pipe_x = W
        pipe_y = random.randint(PIPE_MIN, PIPE_MAX)
        pipe_scored = False

def detect_collision(bird_rect, pipe_top_rect, pipe_bottom_rect):
   return bird_rect.colliderect(pipe_top_rect) or bird_rect.colliderect(pipe_bottom_rect)

font_cache = {}
def get_font(size):
    if size not in font_cache:
        font_cache[size] = pygame.font.Font("dev/pygame/fonts/Minecraft.ttf", size)
    return font_cache[size]

def draw_game():
    screen.fill("#000000")
    # Pipes
    pygame.draw.rect(screen, "#FFFFFF", (pipe_x, 0, PIPE_WIDTH, pipe_y - PIPE_GAP // 2))
    pygame.draw.rect(screen, "#FFFFFF", (pipe_x, pipe_y + PIPE_GAP // 2, PIPE_WIDTH, H - (pipe_y + PIPE_GAP // 2)))
    # Birdie
    pygame.draw.rect(screen, "#FFFFFF", (bird_x, int(bird_y), bird_w, bird_h))
    # Score
    score_y = 50 - (score_scale - 1.0) * 20
    font = get_font(int(50 * score_scale))
    text = font.render(str(score), True, "#FFFFFF")
    text_rect = text.get_rect(center=(W // 2, score_y))
    screen.blit(text, text_rect)

    if game_state == "game_over":
        pygame.draw.rect(screen, "#FF0000", (0, 0, W, H), 5)
 
    pygame.display.flip()

running = True
while running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            velocity = JUMP_STRENGTH
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            velocity = JUMP_STRENGTH
    if game_state == "playing":
        update_bird()
        update_pipe()
    elif game_state == "game_over":
        velocity = 0

    bird_rect = pygame.Rect(bird_x, bird_y, bird_w, bird_h)
    pipe_top_rect = pygame.Rect(pipe_x, 0, PIPE_WIDTH, pipe_y - PIPE_GAP // 2)
    pipe_bottom_rect = pygame.Rect(pipe_x, pipe_y + PIPE_GAP // 2, PIPE_WIDTH, H - (pipe_y + PIPE_GAP // 2))
    if detect_collision( bird_rect, pipe_top_rect, pipe_bottom_rect):
        game_state = "game_over"

    score_scale += (score_scale_target - score_scale) * SCORE_ANIM_SPEED * dt
    draw_game()
