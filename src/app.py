import pygame as pg
import pymunk as pm
import pymunk.pygame_util
from pymunk.pygame_util import DrawOptions
pymunk.pygame_util.positive_y_is_up = False
import random


WIDTH, HEIGHT = 800,600
BALL_RADIUS = 6
FPS = 60
FRICTION = 1

def create_ball(space: pm.Space, position):
    ball_mass = 1000
    ball_radius = BALL_RADIUS
    ball_moment = pm.moment_for_circle(ball_mass, 0, ball_radius)
    ball_body = pm.Body(ball_mass, ball_moment)
    ball_body.position = position
    ball_shape = pm.Circle(ball_body, ball_radius)
    ball_shape.friction = FRICTION
    space.add(ball_body, ball_shape)

def main():
    # pygame setup
    pg.init()
    window = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption('Normal Distribution')
    clock = pg.time.Clock()


    # space setup
    space = pm.Space()
    space.gravity = (0,1000)
    draw_options = DrawOptions(window)


    # boundary walls
    boundary_width = 5
    left_wall_body = pm.Body(body_type=pm.Body.STATIC)
    left_wall_seg = pm.Segment(left_wall_body, (0,0), (0,HEIGHT), boundary_width)
    right_wall_body = pm.Body(body_type=pm.Body.STATIC)
    right_wall_seg = pm.Segment(right_wall_body, (WIDTH,0), (WIDTH,HEIGHT), boundary_width)
    bottom_wall_body = pm.Body(body_type=pm.Body.STATIC)
    bottom_wall_seg = pm.Segment(bottom_wall_body, (0,HEIGHT), (WIDTH,HEIGHT), boundary_width)
    top_wall_body = pm.Body(body_type=pm.Body.STATIC)
    top_wall_seg = pm.Segment(top_wall_body, (0,0), (WIDTH,0), boundary_width)
    space.add(left_wall_body, left_wall_seg, right_wall_body, right_wall_seg, bottom_wall_body, bottom_wall_seg, top_wall_body, top_wall_seg)

    # ball directors
    ## left
    ball_director_width = 5
    left_director_start = (0, 20)
    left_director_end = (380, 80)
    left_director_leg_end = (left_director_end[0], 120)
    left_director_body = pm.Body(body_type=pm.Body.STATIC)
    left_director_seg = pm.Segment(left_director_body, left_director_start, left_director_end, ball_director_width)
    left_director_seg.friction = FRICTION
    left_director_leg_seg = pm.Segment(left_director_body, left_director_end, left_director_leg_end, ball_director_width)
    left_director_leg_seg.friction = FRICTION

    ## right
    right_director_start = (800, 20)
    right_director_end = (420, 80)
    right_director_leg_end = (right_director_end[0], 120)
    right_director_body = pm.Body(body_type=pm.Body.STATIC)
    right_director_seg = pm.Segment(right_director_body, right_director_start, right_director_end, ball_director_width)
    right_director_seg.friction = FRICTION
    right_director_leg_seg = pm.Segment(right_director_body, right_director_end, right_director_leg_end, ball_director_width)
    right_director_leg_seg.friction = FRICTION
    space.add(left_director_body, left_director_seg, left_director_leg_seg, right_director_body, right_director_seg, right_director_leg_seg)


    # blocks
    idx = 0
    block_step = 30
    block_radius = 4
    for y in range(180,int(HEIGHT*0.7),block_step):
        if idx%2!=0:
            for x in range(0,WIDTH,block_step):
                block_body = pm.Body(body_type=pm.Body.STATIC)
                block_body.position = (x, y)
                block_shape = pm.Circle(block_body, block_radius)
                block_shape.friction = FRICTION
                space.add(block_body, block_shape)
        else:
            for x in range(block_step//2,WIDTH,block_step):
                block_body = pm.Body(body_type=pm.Body.STATIC)
                block_body.position = (x, y)
                block_shape = pm.Circle(block_body, block_radius)
                block_shape.friction = FRICTION
                space.add(block_body, block_shape)
        idx += 1

    # bar rods
    store_size = 50
    for x in range(10,WIDTH,store_size):
        rod_width = 2
        rod_body = pm.Body(body_type=pm.Body.STATIC)
        rod_seg = pm.Segment(rod_body, (x, 450), (x, HEIGHT), rod_width)
        space.add(rod_body, rod_seg)

    ball_creation_rate = 10 # per fps
    ticks = FPS
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return
            elif event.type == pg.MOUSEBUTTONDOWN:
                click_pos = pg.mouse.get_pos()
                create_ball(space, click_pos)

        ticks -= 1
        if ticks == 0:
            for _ in range(ball_creation_rate):
                #y = random.uniform(10, 40)
                #x = random.uniform(1, WIDTH-1)
                y = random.uniform(10, left_director_start[1])
                x = random.uniform(1, WIDTH-1)
                create_ball(space, (x,y))
            ticks = FPS

        window.fill((255, 255, 255))
        space.debug_draw(draw_options)
        pg.display.flip()
        space.step(1/FPS)
        clock.tick(FPS)
        

if __name__ == "__main__":
    main()
