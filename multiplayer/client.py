import pygame, socket, threading, json, time

# ---------- Pygame Setup ----------
pygame.init()
W, H = 1280, 720
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Multiplayer")
clock = pygame.time.Clock()
frame_dt = 0

MENU = "menu"
GAME = "game"
state = MENU
running = True

# ---------- Player ----------
player_pos = pygame.Vector2(W // 2, H // 2)
velocity = pygame.Vector2(0, 0)
PLAYER_SPEED = 750
GRAVITY = 2700
JUMP_FORCE = -1000
on_ground = False

player_name = ""
player_id = None
player_color = (255, 255, 255)

# Use a dict to store interpolation states for other players
other_players = {}  # pid -> {current, target, prev, name, color}

# ---------- Socket Setup ----------
HOST = "127.0.0.1"  # server IP
PORT = 5555
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
player_id = str(client.getsockname())

# ---------- Receive Thread ----------
def receive_data():
    global other_players, client
    buffer = ""
    while True:
        try:
            data = client.recv(4096)
            if not data:
                print("Server closed connection")
                break
            buffer += data.decode()
            while "\n" in buffer:
                message, buffer = buffer.split("\n", 1)
                if not message.strip():
                    continue
                try:
                    players = json.loads(message)
                    for pid, pdata in players.items():
                        if pid == player_id:
                            continue
                        # initialize new player
                        if pid not in other_players:
                            other_players[pid] = {
                                "prev": pygame.Vector2(pdata["x"], pdata["y"]),
                                "target": pygame.Vector2(pdata["x"], pdata["y"]),
                                "current": pygame.Vector2(pdata["x"], pdata["y"]),
                                "name": pdata.get("name", "???"),
                                "color": tuple(pdata.get("color", [255, 0, 0])),
                            }
                        else:
                            # update target for interpolation
                            other_players[pid]["prev"] = other_players[pid]["current"].copy()
                            other_players[pid]["target"] = pygame.Vector2(pdata["x"], pdata["y"])
                            other_players[pid]["name"] = pdata.get("name", "???")
                            other_players[pid]["color"] = tuple(pdata.get("color", [255,0,0]))
                except json.JSONDecodeError:
                    continue
        except Exception as e:
            print("Error in receive thread:", e)
            break

threading.Thread(target=receive_data, daemon=True).start()

# ---------- Input & Prediction ----------
def move(pos, dt):
    global on_ground, velocity
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and on_ground:
        velocity.y = JUMP_FORCE
        on_ground = False
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        pos.x -= PLAYER_SPEED * dt
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        pos.x += PLAYER_SPEED * dt

# ---------- Physics ----------
def player_physics(dt):
    global on_ground, velocity, player_pos
    # smoother gravity
    if velocity.y > 0:
        velocity.y += GRAVITY * 1.2 * dt
    else:
        velocity.y += GRAVITY * 0.8 * dt

    player_pos.y += velocity.y * dt
    if player_pos.y >= H - 50:
        player_pos.y = H - 50
        velocity.y = 0
        on_ground = True
    else:
        on_ground = False
    player_pos.x = max(0, min(W - 50, player_pos.x))

# ---------- Drawing with Interpolation ----------
def draw(screen):
    screen.fill("#000000")
    font = pygame.font.Font(None, 36)

    # Local player
    pygame.draw.rect(screen, player_color, (*player_pos, 50, 50))
    if player_name:
        name_text = font.render(player_name, True, "#FFFFFF")
        screen.blit(name_text, (player_pos.x + 5, player_pos.y - 30))

    # Other players: interpolation
    LERP_SPEED = 10.0  # adjust for smoother or faster movement
    for pdata in other_players.values():
        pdata["current"] += (pdata["target"] - pdata["current"]) * LERP_SPEED * frame_dt
        pygame.draw.rect(screen, pdata["color"], (pdata["current"].x, pdata["current"].y, 50, 50))
        text = font.render(pdata["name"], True, (255, 255, 255))
        screen.blit(text, (pdata["current"].x, pdata["current"].y - 30))

    pygame.display.flip()

# ---------- Menu ----------
def menu_loop():
    global state, running, player_name, player_color
    colors = [(255,179,186), (255,223,186), (255,255,186), (186,255,201), (186,225,255)]
    color_index = 0
    input_text = ""
    font = pygame.font.Font(None, 64)

    while state == MENU and running:
        global frame_dt
        frame_dt = clock.tick(60)/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and input_text.strip() != "":
                    player_name = input_text.strip()
                    player_color = colors[color_index]
                    state = GAME
                    return
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_LEFT:
                    color_index = (color_index - 1) % len(colors)
                elif event.key == pygame.K_RIGHT:
                    color_index = (color_index + 1) % len(colors)
                else:
                    if len(input_text) < 12 and event.unicode.isprintable():
                        input_text += event.unicode

        # Draw menu
        screen.fill("#000000")
        name_preview = font.render(f"Name: {input_text}", True, "#FFFFFF")
        screen.blit(name_preview, (W // 2 - name_preview.get_width() // 2, H // 2 - 150))
        for i, c in enumerate(colors):
            rect = pygame.Rect(W // 2 - 200 + i*100, H // 2 - 40, 80, 80)
            pygame.draw.rect(screen, c, rect)
            if i == color_index:
                pygame.draw.rect(screen, (255,255,255), rect, 4)
        info = font.render("ENTER to start, Arrow keys to change color", True, (150,150,150))
        screen.blit(info, (W // 2 - info.get_width() // 2, H // 2 + 80))
        pygame.display.flip()

# ---------- Game Loop ----------
def game_loop():
    global frame_dt, running, client
    while state == GAME and running:
        frame_dt = clock.tick(60)/1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        move(player_pos, frame_dt)
        player_physics(frame_dt)

        # Send local player data
        if client:
            try:
                msg_obj = {
                    "x": float(player_pos.x),
                    "y": float(player_pos.y),
                    "name": player_name,
                    "color": player_color
                }
                client.sendall((json.dumps(msg_obj) + "\n").encode())
            except:
                client = None

        draw(screen)

# ---------- Main ----------
def main():
    while running:
        if state == MENU:
            menu_loop()
        elif state == GAME:
            game_loop()
        else:
            break
    pygame.quit()

if __name__ == "__main__":
    main()
