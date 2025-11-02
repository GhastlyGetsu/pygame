import pygame

pygame.init()
screen = pygame.display.set_mode((720, 720))
pygame.display.set_caption("Tic Tac Toe")
clock = pygame.time.Clock()

grid_size = 500
grid = pygame.Rect(0, 0, grid_size, grid_size)
grid.center = screen.get_rect().center
cell_size = grid.width // 3

grid_state = [["" for _ in range(3)] for _ in range(3)]
current_player = "X"
winner = None

def check_winner(grid):
    # Check rows 
    for row in grid:
        if row[0] == row[1] == row[2] != "":
            return row[0]
    # Check columns
    for col in range(3):
        if grid[0][col] == grid[1][col] == grid[2][col] != "":
            return grid[0][col]    
    # Check diagonals
    if grid[0][0] == grid[1][1] == grid[2][2] != "":
        return grid[0][0]
    if grid[0][2] == grid[1][1] == grid[2][0] != "":
        return grid[0][2]
    
    return None


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # Logics for grid
        # Mouse position relative to the cells
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if winner: 
                grid_state = [["" for _ in range(3)] for _ in range(3)]
                current_player = "X"
                winner = None
                continue

            mx, my = pygame.mouse.get_pos()
            if grid.collidepoint(mx, my):
                col = (mx - grid.left) // cell_size
                row = (my - grid.top) // cell_size
            # Marking grid with X and O
            if grid_state[row][col] == "" and not winner:
                grid_state[row][col] = current_player
                winner = check_winner(grid_state)
            if winner is None:
                # Check for filled cells for draw/tie
                tie = all(cell != "" for row in grid_state for cell in row)
                if tie:
                   winner = "Draw"
            current_player = "O" if current_player == "X" else "X"


    screen.fill("#25A244")

    # Drawing grid
    pygame.draw.rect(screen, "#4AD66D", grid, 0, 45)
    for i in range(1, 3):
        x = grid.left + i * cell_size
        pygame.draw.line(screen, "#25A244", (x, grid.top), (x, grid.bottom), 3)
    for i in range(1, 3):
        y = grid.top + i * cell_size
        pygame.draw.line(screen, "#25A244", (grid.left, y), (grid.right, y), 3)
    pygame.draw.rect(screen, "#4AD66D", grid, 20, 45)
    
    # Drawing symbols
    font = pygame.font.Font(None, 175)
    for row in range(3):
        for col in range(3):
            symbol = grid_state[row][col]
            if symbol != "":
                # Finding center of cell
                x = grid.left + col * cell_size + cell_size // 2
                y = grid.top + row * cell_size + cell_size // 2 

                # Rendering symbols
                text_surface = font.render(symbol, True, "#1A7431")
                text_rect = text_surface.get_rect(center=(x, y))
                screen.blit(text_surface, text_rect)
    
    # Winner announcement
    if winner:
        win_font = pygame.font.Font(None, 80)
        win_text = win_font.render(f"{winner} wins!" if winner != "Draw" else "Draw!", True, "#155D27")
        win_rect = win_text.get_rect(center=(screen.get_width() // 2, 50))
        screen.blit(win_text, win_rect)
    
    # Restart text
    if winner:
        restart_font = pygame.font.Font(None, 50)
        restart_text = restart_font.render("Click anywhere to restart", True, "#155D27")
        restart_rect = restart_text.get_rect(center=(screen.get_width() // 2, screen.get_height() - 50))
        screen.blit(restart_text, restart_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

