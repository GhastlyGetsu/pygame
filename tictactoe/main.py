import pygame

pygame.init()
screen = pygame.display.set_mode((720, 720))
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    grid_size = 500
    grid = pygame.Rect(0, 0, grid_size, grid_size)
    grid.center = screen.get_rect().center
    cell_size = grid.width // 3
    screen.fill("#25A244")
    
    pygame.draw.rect(screen, "#4AD66D", grid)

    for i in range(1, 3):
        x = grid.left + i * cell_size
        pygame.draw.line(screen, "#25A244", (x, grid.top), (x, grid.bottom), 3)
    for i in range(1, 3):
        y = grid.top + i * cell_size
        pygame.draw.line(screen, "#25A244", (grid.left, y), (grid.right, y), 3)
    pygame.draw.rect(screen, "#4AD66D", grid, 15)


    pygame.display.flip()
    clock.tick(60)

pygame.quit()

