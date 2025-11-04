import pygame, random

pygame.init()
screen = pygame.display.set_mode((720, 720))
pygame.display.set_caption("Tic Tac Toe")
clock = pygame.time.Clock()

game_state = "menu"

grid_size = 500
grid = pygame.Rect(0, 0, grid_size, grid_size)
grid.center = screen.get_rect().center
cell_size = grid.width // 3

grid_state = [["" for _ in range(3)] for _ in range(3)]
ai_symbol = "O"
player_symbol = "X"
current_player = player_symbol
winner = None


def check_winner(grid):
    # Rows
    for row in grid:
        if row[0] == row[1] == row[2] != "":
            return row[0]
    # Columns
    for col in range(3):
        if grid[0][col] == grid[1][col] == grid[2][col] != "":
            return grid[0][col]
    # Diagonals
    if grid[0][0] == grid[1][1] == grid[2][2] != "":
        return grid[0][0]
    if grid[0][2] == grid[1][1] == grid[2][0] != "":
        return grid[0][2]
    return None


def get_ai_move(board, ai_symbol, player_symbol):
    """AI Move Logic"""
    def find_winning_move(b, s):
        # Rows
        for r in range(3):
            if b[r][0] == b[r][1] == s and b[r][2] == "":
                return (r, 2)
            if b[r][0] == b[r][2] == s and b[r][1] == "":
                return (r, 1)
            if b[r][1] == b[r][2] == s and b[r][0] == "":
                return (r, 0)
        # Columns
        for c in range(3):
            if b[0][c] == b[1][c] == s and b[2][c] == "":
                return (2, c)
            if b[0][c] == b[2][c] == s and b[1][c] == "":
                return (1, c)
            if b[1][c] == b[2][c] == s and b[0][c] == "":
                return (0, c)
        # Diagonals
        if b[0][0] == b[1][1] == s and b[2][2] == "":
            return (2, 2)
        if b[0][0] == b[2][2] == s and b[1][1] == "":
            return (1, 1)
        if b[1][1] == b[2][2] == s and b[0][0] == "":
            return (0, 0)
        if b[0][2] == b[1][1] == s and b[2][0] == "":
            return (2, 0)
        if b[0][2] == b[2][0] == s and b[1][1] == "":
            return (1, 1)
        if b[2][0] == b[1][1] == s and b[0][2] == "":
            return (0, 2)
        return None

    # Try to win
    m = find_winning_move(board, ai_symbol)
    if m:
        return m
    # Block player
    m = find_winning_move(board, player_symbol)
    if m:
        return m
    # Center
    if board[1][1] == "":
        return (1, 1)
    # Corners
    corners = [(0,0), (0,2), (2,0), (2,2)]
    free_corners = [c for c in corners if board[c[0]][c[1]] == ""]
    if free_corners:
        return random.choice(free_corners)
    # Sides
    sides = [(0,1), (1,0), (1,2), (2,1)]
    free_sides = [s for s in sides if board[s[0]][s[1]] == ""]
    if free_sides:
        return random.choice(free_sides)
    return None


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Player click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if game_state == "menu":
                mx, my = pygame.mouse.get_pos()
                if button_rect.collidepoint(mx, my):
                    game_state = "playing"
                    continue
            if winner:
                grid_state = [["" for _ in range(3)] for _ in range(3)]
                current_player = player_symbol
                winner = None
                continue

            if current_player == player_symbol and not winner:
                mx, my = pygame.mouse.get_pos()
                if grid.collidepoint(mx, my):
                    col = (mx - grid.left) // cell_size
                    row = (my - grid.top) // cell_size
                    if grid_state[row][col] == "":
                        grid_state[row][col] = player_symbol
                        winner = check_winner(grid_state)
                        if not winner:
                            tie = all(cell != "" for row in grid_state for cell in row)
                            if tie:
                                winner = "Draw"
                                game_state = "game_over"
                        current_player = ai_symbol  # Switch to AI

    # --- Drawing phase ---
    # Menu
    if game_state == "menu":
        screen.fill("#25A244")
        title_font = pygame.font.Font(None, 120)
        title = title_font.render("Tic Tac Toe", True, "#155D27")
        title_rect = title.get_rect(center=(screen.get_width() // 2, 200))
        screen.blit(title, title_rect)

        # Buttons
        button_rect = pygame.Rect(0, 0, 250, 80)
        button_rect.center = (screen.get_width() // 2, 450)
        pygame.draw.rect(screen, "#4AD66D", button_rect, border_radius=20)
        button_font = pygame.font.Font(None, 60)
        button_text = button_font.render("Play", True, "#155D27")
        button_text_rect = button_text.get_rect(center=button_rect.center)
        screen.blit(button_text, button_text_rect)

    # Gameplay
    elif game_state == "playing":
        screen.fill("#25A244")
        # Grid background
        pygame.draw.rect(screen, "#4AD66D", grid, 0, 45)
        for i in range(1, 3):
            x = grid.left + i * cell_size
            pygame.draw.line(screen, "#25A244", (x, grid.top), (x, grid.bottom), 3)
        for i in range(1, 3):
            y = grid.top + i * cell_size
            pygame.draw.line(screen, "#25A244", (grid.left, y), (grid.right, y), 3)
        pygame.draw.rect(screen, "#4AD66D", grid, 20, 45)

        # Symbols
        font = pygame.font.Font(None, 175)
        for row in range(3):
            for col in range(3):
                symbol = grid_state[row][col]
                if symbol != "":
                    x = grid.left + col * cell_size + cell_size // 2
                    y = grid.top + row * cell_size + cell_size // 2
                    text_surface = font.render(symbol, True, "#1A7431")
                    text_rect = text_surface.get_rect(center=(x, y))
                    screen.blit(text_surface, text_rect)

            # Winner display
            if winner:
                win_font = pygame.font.Font(None, 80)
                win_text = win_font.render(f"{winner} wins!" if winner != "Draw" else "Draw!", True, "#155D27")
                win_rect = win_text.get_rect(center=(screen.get_width() // 2, 50))
                screen.blit(win_text, win_rect)

                restart_font = pygame.font.Font(None, 50)
                restart_text = restart_font.render("Click anywhere to restart", True, "#155D27")
                restart_rect = restart_text.get_rect(center=(screen.get_width() // 2, screen.get_height() - 50))
                screen.blit(restart_text, restart_rect)

    # Game over screen
    elif game_state == "game_over":
        screen.fill("#25A244")
        
        go_font = pygame.font.Font(None, 120)
        go = go_font.render("Game Over!", True, "#155D27")
        go_rect = go.get_rect(center=(screen.get_width() // 2, 50))
        screen.blit(go, go_rect)

        pa_rect = pygame.Rect(0, 0, 250, 80)
        pa_rect.center = (screen.get_width() // 2, 200)
        pa_font = pygame.font.Font(None, 60)
        pygame.draw.rect(screen, "#4AD66D", pa_rect, border_radius=20)
        pa_text = pa_font.render("Play Again", True, "#155D27")
        pa_text_rect = pa_text.get_rect(center=(pa_rect.center))
        screen.blit(pa_text, pa_text_rect)

        qm_rect = pygame.Rect(0, 0, 250, 80)
        qm_rect.center = (screen.get_width() // 2, 300)
        qm_font = pygame.font.Font(None, 60)
        pygame.draw.rect(screen, "#4AD66D", qm_rect, border_radius=20)
        qm_text = pa_font.render("Quit to Menu", True, "#155D27")
        qm_text_rect = qm_text.get_rect(center=(qm_rect.center))
        screen.blit(qm_text, qm_text_rect)

    pygame.display.flip()


    # --- AI Turn ---
    if current_player == ai_symbol and not winner:
        pygame.time.wait(500)  # Wait AFTER screen updates
        ai_move = get_ai_move(grid_state, ai_symbol, player_symbol)
        if ai_move:
            r, c = ai_move
            grid_state[r][c] = ai_symbol
            winner = check_winner(grid_state)
            if not winner:
                tie = all(cell != "" for row in grid_state for cell in row)
                if tie:
                    winner = "Draw"
            current_player = player_symbol  # Back to player

    clock.tick(60)

pygame.quit()
