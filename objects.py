from utils import *
import random as rand
import copy

class Milestone():
    def __init__(self, time_until, active):
        self.time_until = time_until
        self.passed = False
        self.active = active
        if active:
            self.start_time = pygame.time.get_ticks()
    def start(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()
    def reset(self):
        self.active = False
        self.passed = False

#All time in milliseconds
class Timer():
    def __init__(self):
        self.milestones = {}
    def add_milestone(self, milestone_name, time_until, active = False):
        milestone = Milestone(time_until, active)
        self.milestones[milestone_name] = milestone
    def start_milestone(self, milestone_name):
        self.milestones[milestone_name].start()
    def reset_milestone(self, milestone_name):
        self.milestones[milestone_name].reset()
    def update_milestones(self):
        for key in self.milestones:
            if self.milestones[key].active and pygame.time.get_ticks() >= self.milestones[key].start_time + self.milestones[key].time_until:
                self.milestones[key].passed = True
    def delete_milestone(self, milestone_name):
        self.milestones.pop(milestone_name)

class Object():
    def __init__(self, x, y, tag = None):
        self.x = x
        self.y = y
        self.tag = tag
        self.dead = False
    def update(self):
        pass

class Rect(Object):
    def __init__(self, x, y, w, h, color = None, image = None, tag = None):
        Object.__init__(self, x, y, tag)
        self.w = w
        self.h = h
        self.color = color
        self.image = image
    def update(self):
        pass
    def render(self):
        if (self.color is None) and (self.image is None):
            render_rect(self.x, self.y, self.w, self.h)
        elif self.image is not None:
            render_image(self.x,self.y, self.w, self.h, self.image)
        else:
            render_rect(self.x, self.y, self.w, self.h, self.color)

class Circle(Object):
    def __init__(self, x, y, r, color = None, image = None, tag = None):
        Object.__init__(self, x, y, tag)
        self.r = r
        self.color = color
        self.image = image
    def render(self):
        if (self.color is None) and (self.image is None):
            render_circle(self.x + self.r, self.y + self.r, self.r)
        elif self.image is not None:
            render_image(self.x, self.y, self.r * 2, self.r * 2, self.image)
        else:
            render_circle(self.x + self.r, self.y + self.r, self.r, self.color)
    def update(self):
        pass
class Moveable(Object):
    def __init__(self, x, y, dx = 0, dy = 0, tag = None):
        Object.__init__(self, x, y, tag)
        self.dx = dx
        self.dy = dy
    def update(self):
        self.x += self.dx
        self.y += self.dy
class Moveable_Rect(Moveable, Rect):
    def __init__(self, x, y, w, h, dx = 0, dy = 0, color = None, image = None, tag = None):
        Moveable.__init__(self, x, y, dx, dy, tag)
        Rect.__init__(self, x, y, w, h, color, image, tag)
    def update(self):
        Moveable.update(self)

class Moveable_Circle(Moveable, Circle):
    def __init__(self, x, y, r, dx = 0, dy = 0, color = None, image = None, tag = None):
        Moveable.__init__(self, x, y, dx, dy, tag)
        Circle.__init__(self, x, y, r, color, image, tag)
    def update(self):
        Moveable.update(self)
class Tile(Rect):
    def __init__(self, x, y, type, tag = None):
        Rect.__init__(self, x, y, TILE_WIDTH, TILE_HEIGHT, tag)
        self.type = type
        self.setup_tile()
        self.tag = "tile"
    def setup_tile(self):
        if self.type == 1:
            self.health = 1
            self.max_health = 1
            self.color = RED
        elif self.type == 2:
            self.health = 2
            self.max_health = 2
            self.color = BLUE
        elif self.type == 3:
            self.health = 3
            self.max_health = 3
            self.color = GREEN

    def render(self):
        pygame.draw.rect(Game.screen, BLACK, pygame.Rect(self.x, self.y, self.w, self.h))
        pygame.draw.rect(Game.screen, pygame.Color(self.color), pygame.Rect(self.x + TILE_WIDTH_RENDER_OFFSET, self.y + TILE_HEIGHT_RENDER_OFFSET, self.w - TILE_WIDTH_RENDER_OFFSET * 2, self.h - TILE_HEIGHT_RENDER_OFFSET * 2))

    def take_damage(self):
        self.health -= 1
        self.color = (self.color[0] * 0.7, self.color[1] * 0.7, self.color[2] * 0.7)
        if self.health == 0:
            self.dead = True
        else:
            pygame.mixer.Sound('Audio/pong.wav').play()

class Paddle(Moveable_Rect):
    def __init__(self, x, y, w, h):
        Moveable_Rect.__init__(self, x, y, w, h)
        self.arrow_angle = math.pi / 2
        self.tag = "paddle"
    def paddle():
        return Paddle(SCREEN_WIDTH / 2 - PADDLE_WIDTH / 2, 0.9 * SCREEN_HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT)
    def render_paddle_at(self, x_pos):
        pygame.draw.rect(Game.screen, NAVY, pygame.Rect(x_pos, self.y, self.w, self.h), border_radius = int(self.w / 2), width = 2)
        if Game.rest_state:
            start_pt = (x_pos + self.w / 2 - 2, self.y - BALL_RADIUS * 3)
            end_pt = (start_pt[0] + ARROW_LENGTH * -math.cos(self.arrow_angle), start_pt[1] + ARROW_LENGTH * -math.sin(self.arrow_angle))
            self.arrow_angle += Game.arrow_change
            if self.arrow_angle < math.pi * 0.1:
                self.arrow_angle = math.pi * 0.1
            elif self.arrow_angle > math.pi * 0.9:
                self.arrow_angle = math.pi * 0.9
            render_arrow(start_pt, end_pt, self.arrow_angle)
        else:
            self.arrow_angle = math.pi / 2
    def render(self):
        self.render_paddle_at(self.x)
        if (self.x + self.w > SCREEN_WIDTH):
            self.render_paddle_at(self.x - SCREEN_WIDTH)
        elif (self.x < 0):
            self.render_paddle_at(self.x + SCREEN_WIDTH)
    def wraparound(self):
        if (self.x >= SCREEN_WIDTH):
            self.x = self.x - SCREEN_WIDTH
        elif (self.x <= -self.w):
            self.x = SCREEN_WIDTH + self.x
    def update(self):
        self.dx = Game.paddle_dx
        Moveable_Rect.update(self)
        self.wraparound()

class Ball(Moveable_Circle):
    def __init__(self, x, y, r, dx = 0, dy = 0, color = WHITE, image = None):
        Moveable_Circle.__init__(self, x, y, r, dx, dy, color, image)
        self.tag = "ball"
    def render(self):
        pygame.draw.circle(Game.screen, NAVY, (self.x + self.r, self.y + self.r), self.r, width = 2)
    def bounce(self, x_bounce = False, y_bounce = False):
        if x_bounce:
            self.dx = -self.dx
        if y_bounce:
            self.dy = -self.dy
        pygame.mixer.Sound('Audio/pong.wav').play()

    def collide_tiles(self):
        overlapping_tiles = []
        for tile in Game.current_level:
            if rect_overlapping_circle(tile, self):
                overlapping_tiles.append(tile)
                tile.take_damage()
        if len(overlapping_tiles) == 1:
            overlap_width, overlap_height = get_overlapping_rect(pygame.Rect(self.x, self.y, self.r*2, self.r*2), overlapping_tiles[0])
            if overlap_width > overlap_height:
                self.bounce(False, True)
            else:
                self.bounce(True)
        elif len(overlapping_tiles) == 2:
            if overlapping_tiles[0].y == overlapping_tiles[1].y:
                self.bounce(False, True)
            elif overlapping_tiles[0].x == overlapping_tiles[1].x:
                self.bounce(True)
            else:
                self.bounce(True, True)
        elif len(overlapping_tiles) > 2:
            self.bounce(True, True)


    def collide_paddle(self):
        hit = False

        if rect_overlapping_circle(Game.paddle, self):
            hit = True
            xDiff = self.x + self.r - Game.paddle.x
        elif Game.paddle.x <= 0:
            phantom_paddle = Rect(SCREEN_WIDTH + Game.paddle.x, Game.paddle.y, -Game.paddle.x, Game.paddle.h)
            if rect_overlapping_circle(phantom_paddle, self):
                hit = True
                xDiff = self.x + self.r - SCREEN_WIDTH - Game.paddle.x
        elif Game.paddle.x + Game.paddle.w >= SCREEN_WIDTH:
            phantom_paddle = Rect(0, Game.paddle.y, SCREEN_WIDTH - Game.paddle.x, Game.paddle.h)
            if rect_overlapping_circle(phantom_paddle, self):
                hit = True
                xDiff = self.x + self.r + SCREEN_WIDTH - Game.paddle.x
        if hit:
            self.bounce()
            if xDiff < Game.paddle.w * 0.2:
                xDiff = Game.paddle.w * 0.2
            elif xDiff > Game.paddle.w * 0.8:
                xDiff = Game.paddle.w * 0.8

            rand_multiplier = 1 + (rand.randint(-5, 5) / 100)
            xDiff *= rand_multiplier

            self.dy = -BALL_SPEED * math.sin((xDiff / Game.paddle.w) * math.pi)
            self.dx = -BALL_SPEED * math.cos((xDiff / Game.paddle.w) * math.pi)
    def collide_walls(self):
        if self.x <= 0:
            self.x = 0
            self.bounce(True)
        elif self.x + self.r * 2 >= SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.r * 2
            self.bounce(True)
        if self.y <= 0:
            self.y = 0
            self.bounce(False, True)
    def collide_bottom(self):
        if self.y + self.r * 2 >= SCREEN_HEIGHT:
            self.ball_death()
    def ball_death(self):
        Game.objects.append(Explosion(self.x + self.r, self.y + self.r))
        self.dead = True
        pygame.mixer.Sound('Audio/ding.wav').play()

    def update(self):
        Moveable_Circle.update(self)
        self.collide_tiles()
        self.collide_paddle()
        self.collide_walls()
        self.collide_bottom()
    #def render(self):
    #    Moveable_Circle.render(self)

class Explosion(Circle):
    def __init__(self, x, y, r = 1, color = RED, grow_rate = 5, duration = 1000):
        Circle.__init__(self, x, y, r, color)
        self.grow_rate = grow_rate
        self.color = color
        self.timer = Timer()
        self.timer.add_milestone('done_growing', duration / 2, active = True)
        self.timer.add_milestone('done_shrinking', duration / 2, active = False)
    def update(self):
        self.timer.update_milestones()
        if (self.timer.milestones['done_growing'] is not None) and self.timer.milestones['done_growing'].passed:
            self.timer.reset_milestone('done_growing')
            self.timer.start_milestone('done_shrinking')
            self.grow_rate = -self.grow_rate
        self.r += self.grow_rate
        self.x -= self.grow_rate
        self.y -= self.grow_rate
        if self.r <= 0:
            self.r = 1
        if (self.timer.milestones['done_shrinking'] is not None) and self.timer.milestones['done_shrinking'].passed:
            self.dead = True
class Powerup(Moveable_Rect):
    def __init__(self, x, y, w, h, dx = 0, dy = 5, color = None, image = None, tag = "powerup"):
        Moveable_Rect.__init__(self, x, y, w, h, dx, dy, color, image, tag)
    def update(self):
        Moveable_Rect.update(self)
        if rect_overlapping_rect(self, Game.paddle):
            self.collected()
    def collected(self):
        self.dead = True
        pygame.mixer.Sound('Audio/powerup.wav').play()


class Multiball_Powerup(Powerup):
    def __init__(self, x, y, w, h, dx = 0, dy = 5, color = None, image = None, tag = "powerup"):
        Powerup.__init__(self, x, y, w, h, dx, dy, color)
    def collected(self):
        Powerup.collected(self)
        new_balls = []
        new_balls.append(Ball(Game.paddle.x + Game.paddle.w / 2 - BALL_RADIUS, Game.paddle.y - BALL_RADIUS * 2, BALL_RADIUS, BALL_SPEED * math.cos(math.pi + math.pi / 2 + 0.2), BALL_SPEED * math.sin(math.pi + math.pi / 2 + 0.2), color = WHITE))
        new_balls.append(Ball(Game.paddle.x + Game.paddle.w / 2 - BALL_RADIUS, Game.paddle.y - BALL_RADIUS * 2, BALL_RADIUS, BALL_SPEED * math.cos(math.pi + math.pi / 2 - 0.2), BALL_SPEED * math.sin(math.pi + math.pi / 2 - 0.2), color = WHITE))
        #new_balls.append(Ball(Game.paddle.x + Game.paddle.w / 2 - BALL_RADIUS, Game.paddle.y - BALL_RADIUS * 2, BALL_RADIUS, BALL_SPEED * math.cos(math.pi + math.pi / 2), BALL_SPEED * math.sin(math.pi + 0.2), color = WHITE))
        Game.objects.extend(new_balls)
    def multiball(x, y):
        return Multiball_Powerup(x, y, 20, 20, dx = 0, dy = 5)
    def render(self):
        pygame.draw.circle(Game.screen, BLUE, (self.x, self.y), BALL_RADIUS)
        pygame.draw.circle(Game.screen, BLUE, (self.x - BALL_RADIUS * 1.5, self.y + BALL_RADIUS * 3), BALL_RADIUS)
        pygame.draw.circle(Game.screen, BLUE, (self.x + BALL_RADIUS * 1.5, self.y + BALL_RADIUS * 3), BALL_RADIUS)

class Long_Powerup(Powerup):
    def __init__(self, x, y, w, h, dx = 0, dy = 5, color = None, image = None, tag = "powerup"):
        Powerup.__init__(self, x, y, w, h, dx, dy, color)
    def collected(self):
        Powerup.collected(self)
        if Game.paddle.w == PADDLE_WIDTH:
            Game.paddle.w *= 1.5
        else:
            Game.paddle.w *= 1.15
    def long(x, y):
        return Long_Powerup(x, y, 20, 20, dx = 0, dy = 5)
    def render(self):
        self.image = pygame.image.load("Images/long.png")
        Powerup.render(self)
