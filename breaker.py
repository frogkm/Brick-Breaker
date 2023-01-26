from objects import *

def level_map_to_tile_map(level_map):
    tile_map = []
    for j in range(len(level_map)):
        for i in range(len(level_map[j])):
            if level_map[j][i] != 0:
                tile_map.append(Tile(i * TILE_WIDTH, j * TILE_HEIGHT, level_map[j][i]))
    return tile_map

def get_input():
    keys = pygame.key.get_pressed()
    Game.paddle_dx = 0
    if keys[pygame.K_a]:
        Game.paddle_dx -= PADDLE_SPEED
    if keys[pygame.K_d]:
        Game.paddle_dx += PADDLE_SPEED
    if Game.rest_state:
        Game.arrow_change = 0
        if keys[pygame.K_LEFT]:
            Game.arrow_change -= 0.1
        elif keys[pygame.K_RIGHT]:
            Game.arrow_change += 0.1
        if keys[pygame.K_SPACE]:
            shoot_ball_from_rest()

def shoot_ball(pos, angle):
    new_ball = Ball(pos[0], pos[1], BALL_RADIUS, BALL_SPEED * math.cos(angle), BALL_SPEED * math.sin(angle))
    Game.objects.append(new_ball)


def shoot_ball_from_rest():
    Game.num_lives -= 1
    Game.rest_state = False
    shoot_ball((Game.paddle.x + Game.paddle.w / 2 - BALL_RADIUS, Game.paddle.y - BALL_RADIUS * 2), math.pi + Game.paddle.arrow_angle)

def timed_events():
    if Game.timer.milestones["soft_reset"].passed:
        Game.timer.reset_milestone("soft_reset")
        soft_reset_level()
    if Game.timer.milestones["reset"].passed:
        Game.timer.reset_milestone("reset")
        reset_level()
    if Game.timer.milestones["level_completed"].passed:
        Game.timer.reset_milestone("level_completed")
        next_level()

def level_completed():
    pygame.mixer.Sound('Audio/win.wav').play()
    clear_powerups()
    for ball in get_objects("ball"):
        Game.objects.append(Explosion(ball.x + ball.r, ball.y + ball.r, grow_rate = 10, duration = 1000))
        pygame.mixer.Sound('Audio/ding.wav').play()
        Game.objects.remove(ball)
    Game.timer.start_milestone('level_completed')

def clear_powerups():
    for powerup in get_objects('powerup'):
        Game.objects.remove(powerup)

def last_ball_gone():
    if Game.num_lives == 0:
        start_level_reset()
    else:
        start_soft_reset()

def last_tile_gone():
    level_completed()

def spawn_rand_powerup(rect):
    total = MULTIBALL_FREQ + LONG_FREQ
    multi_range = range(0, MULTIBALL_FREQ)
    long_range = range(MULTIBALL_FREQ, MULTIBALL_FREQ + LONG_FREQ)

    num = rand.randint(0, total - 1)
    powerup = None
    if num in multi_range:
        powerup = Multiball_Powerup(0, 0, POWER_WIDTH, POWER_HEIGHT)
    elif num in long_range:
        powerup = Long_Powerup(0, 0, POWER_WIDTH, POWER_HEIGHT)
    center_rect_in_rect(powerup, rect, True, True)
    Game.objects.append(powerup)


def try_spawn_powerup(rect):
    if rand.randint(1, 100) / 100 < POWERUP_PERCENT:
        spawn_rand_powerup(rect)

def check_for_death(object):
    if object.dead:
        if object.tag == "ball" and len(get_objects("ball")) == 1:
            Game.objects.remove(object)
            last_ball_gone()
        elif object.tag == "tile":
            pygame.mixer.Sound('Audio/bounce.wav').play()
            try_spawn_powerup(object)
            Game.objects.remove(object)
            Game.current_level.remove(object)
            if len(get_objects("tile")) == 0:
                last_tile_gone()
        else:
            Game.objects.remove(object)

def soft_reset_level():
    Game.paddle.w = PADDLE_WIDTH
    center_rect_in_rect(Game.paddle, Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), x_center = True)
    Game.rest_state = True

def reset_level():
    soft_reset_level()
    Game.num_lives = NUM_LIVES
    Game.current_level = level_map_to_tile_map(Game.level_maps[Game.level_idx])
    Game.objects = []
    Game.objects.extend(Game.current_level)
    Game.objects.append(Game.paddle)

def next_level():
    if Game.level_idx + 1 <= len(Game.level_maps) - 1:
        Game.level_idx += 1
    reset_level()

def start_soft_reset():
    clear_powerups()
    Game.timer.start_milestone('soft_reset')
def start_level_reset():
    clear_powerups()
    pygame.mixer.Sound('Audio/crying.wav').play()
    Game.timer.start_milestone('reset')

def update():
    for object in Game.objects:
        object.update()
        check_for_death(object)
    Game.timer.update_milestones()
    timed_events()

def render_lives(cent_x, cent_y):
    render_centered_text(cent_x, cent_y, 'Lives', Game.font, WHITE)
    for i in range(Game.num_lives):
        new_ball = Ball(cent_x - BALL_RADIUS, cent_y + 35 + i * 50, int(BALL_RADIUS * 1.5),color=WHITE)
        new_ball.render()

def render_hud():
    pygame.draw.rect(Game.screen, WHITE, pygame.Rect(SCREEN_WIDTH , 0, SCREEN_WIDTH_EXTENSION, SCREEN_HEIGHT))
    render_rect(SCREEN_WIDTH , 0, SCREEN_WIDTH_EXTENSION, SCREEN_HEIGHT, BLUE)
    render_level_num(SCREEN_WIDTH + SCREEN_WIDTH_EXTENSION / 2, 40)
    render_controls(SCREEN_WIDTH + SCREEN_WIDTH_EXTENSION / 2, 150)
    render_lives(SCREEN_WIDTH + SCREEN_WIDTH_EXTENSION / 2, 380)
    pygame.draw.rect(Game.screen, WHITE, pygame.Rect(SCREEN_WIDTH , 0, SCREEN_WIDTH_EXTENSION, SCREEN_HEIGHT), border_radius = 50, width = 5)
    pygame.draw.rect(Game.screen, WHITE, pygame.Rect(SCREEN_WIDTH , 0, SCREEN_WIDTH_EXTENSION, SCREEN_HEIGHT), width = 5)

def render():
    Game.screen.fill(LIGHT_BLUE)
    for object in Game.objects:
        object.render()
    render_hud()
    pygame.display.flip()




def main():
    pygame.init()
    pygame.display.set_caption('Block-Buster')

    Game.screen = pygame.display.set_mode((SCREEN_WIDTH + SCREEN_WIDTH_EXTENSION, SCREEN_HEIGHT))
    Game.stop = False
    Game.clock = pygame.time.Clock()
    Game.timer = Timer()
    Game.paddle_dx = 0
    Game.level_maps = get_level_maps()
    Game.level_idx = 0
    Game.current_level = level_map_to_tile_map(Game.level_maps[Game.level_idx])
    Game.rest_state = True
    Game.arrow_change = 0
    Game.num_lives = NUM_LIVES
    Game.small_font = pygame.font.SysFont('Arial', 10, bold=True)
    Game.font = pygame.font.SysFont('Arial', 20, bold=True)
    Game.large_font = pygame.font.SysFont('Arial', 40, bold=True)

    Game.timer.add_milestone("soft_reset", 3000)
    Game.timer.add_milestone("reset", 5000)
    Game.timer.add_milestone("level_completed", 5000)

    Game.paddle = Paddle.paddle()
    Game.objects = []
    Game.objects.append(Game.paddle)
    Game.objects.extend(Game.current_level)

    #Powerup.setup()


    while not Game.stop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Game.stop = True
        get_input()
        update()
        render()

        Game.clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
