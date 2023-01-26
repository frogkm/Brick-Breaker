from globals import *


def get_level_maps():
    #[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    #[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    #[2, 2, 2, 2, 2, 2, 2, 2, 2, 2]

    maps = [
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    ],
    [
        [],[],[],[],[],[],
        [0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
        [],[],[],
        [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
        [],[],[],
        [3, 2, 2, 3, 2, 2, 3, 2, 2, 3]
    ],
    [
        [0, 3, 0, 3, 0, 3, 0, 3, 0, 0],
        [3, 0, 3, 0, 3, 0, 3, 0, 3, 0],
        [0, 3, 0, 3, 0, 3, 0, 3, 0, 3],
        [3, 0, 3, 0, 3, 0, 3, 0, 3, 0],
        [0, 3, 0, 3, 0, 3, 0, 3, 0, 3]
    ],
    [
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
    ]

    ]
    return maps

def make_level_maps():
    full_maps = []
    for map in get_level_maps():
        full_maps.append(lists_to_level_map(map))
    return full_maps

def render_arrow(start_pt, end_pt, arrow_angle, color = WHITE, shaft_thickness = 3, head_length = 15, head_thickness = 3, head_angle = 0.6):
    pygame.draw.line(Game.screen, WHITE, start_pt, end_pt, shaft_thickness)
    new_end_pt = (end_pt[0] + head_length * math.cos(arrow_angle - head_angle), end_pt[1] + head_length * math.sin(arrow_angle - math.pi * 0.2))
    pygame.draw.line(Game.screen, WHITE, end_pt, new_end_pt, head_thickness)
    other_end_pt = (end_pt[0] + head_length * math.cos(arrow_angle + head_angle), end_pt[1] + head_length * math.sin(arrow_angle + math.pi * 0.2))
    pygame.draw.line(Game.screen, WHITE, end_pt, other_end_pt, head_thickness)
def rect_overlapping_rect(rect1, rect2):
    if rect1.x + rect1.w >= rect2.x and rect1.x <= rect2.x + rect2.w and rect1.y + rect1.h >= rect2.y and rect1.y <= rect2.y + rect2.h:
        return True
    return False
def rect_overlapping_circle(rect, circ):
    if rect.x + rect.w >= circ.x and rect.x <= circ.x + circ.r * 2 and rect.y + rect.h >= circ.y and rect.y <= circ.y + circ.r * 2:
        return True
    return False
def render_rect(x, y, w, h, color = WHITE):
    pygame.draw.rect(Game.screen, color, pygame.Rect(x, y, w, h))
def render_circle(center_x, center_y, r, color = WHITE):
    pygame.draw.circle(Game.screen, color, (center_x, center_y), r)
def render_image(x, y, w, h, image):
    image = pygame.transform.scale(image, (w, h))
    Game.screen.blit(image, (x, y))
def render_centered_text(cent_x, cent_y, text, font, color = WHITE):
    test_surf = font.render(text, True, color)
    w = test_surf.get_width()
    h = test_surf.get_height()
    x = cent_x - w / 2
    y = cent_y - h / 2
    Game.screen.blit(test_surf, (x, y))
def render_level_num(cent_x, cent_y):
    render_centered_text(cent_x, cent_y, 'Level', Game.font, WHITE)
    render_centered_text(cent_x, cent_y + 50, str(Game.level_idx + 1), Game.large_font, WHITE)
def render_controls(cent_x, cent_y):
    render_centered_text(cent_x, cent_y, 'Move Paddle', Game.font, WHITE)
    render_centered_text(cent_x, cent_y + 30, '|A| |D|', Game.font, NAVY)
    #Game.screen.blit(pygame.image.load('Images/paddle.png'), (cent_x,cent_y))

    render_centered_text(cent_x, cent_y + 70, 'Initial Angle', Game.font, WHITE)
    render_centered_text(cent_x, cent_y + 100, '|<-| |->|', Game.font, NAVY)

    render_centered_text(cent_x, cent_y + 140, 'Release Ball', Game.font, WHITE)
    render_centered_text(cent_x, cent_y + 170, '|SPACE|', Game.font, NAVY)

def center_rect_in_rect(rect, big_rect, x_center = True, y_center = False):
    if(x_center):
        rect.x = big_rect.x + big_rect.w / 2 - rect.w / 2
    if(y_center):
        rect.y = big_rect.y + big_rect.h / 2 - rect.h / 2


#Returns first object found with given tag
def get_object(tag):
    for object in Game.objects:
        if object.tag == tag:
            return object
    return None
#Returns list of all objects with tag
def get_objects(tag):
    tagged = []
    for object in Game.objects:
        if object.tag == tag:
            tagged.append(object)
    return tagged
def get_overlapping_rect(first, other):
    start_pt_width = first.x
    if first.x < other.x:
        start_pt_width = other.x
    end_pt_width = first.x + first.w
    if first.x + first.w > other.x + other.w:
        end_pt_width = other.x + other.w
    overlap_width = end_pt_width - start_pt_width
    start_pt_height = first.y
    if first.y < other.y:
        start_pt_height = other.y
    end_pt_height = first.y + first.h
    if first.y + first.h > other.y + other.h:
        end_pt_height = other.y + other.h
    overlap_height = end_pt_height - end_pt_height
    return overlap_width, overlap_height
