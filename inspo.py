import numpy as np
import pygame as pg
import sys

num=0
WIDTH=700
HEIGHT=700
radii=2
gravitational_acc = 0.1

screen=pg.display.set_mode((WIDTH, HEIGHT))
screen.fill((255,255,255))
pg.display.set_caption("Ball Collision")
CLOCK=pg.time.Clock()
FPS=120
delta=1
getting_pressed=False


class Ball:
    def __init__(self,num_balls, width, height, radius, gravity):
        self.WIDTH=width
        self.HEIGHT=height
        self.number=num_balls
        self.radius=radius
        self.gravity=gravity
        self.pos=np.zeros((self.number,2))
        self.vel=np.zeros((self.number,2))
        self.acc=np.array([0, gravity])
        self.pos[:, 0]=np.random.uniform(50, self.WIDTH-50, self.number)
    def update(self, dt):
        self.vel += self.acc * dt
        self.pos += self.vel * dt

        hit_floor = self.pos[:, 1] + self.radius >= self.HEIGHT

        self.pos[hit_floor, 1] = self.HEIGHT-self.radius
        self.vel[hit_floor, 1] *= -0.8
        self.vel[hit_floor, 0] *= 0.994

        hit_left = (self.pos[:, 0] - self.radius <= 0)
        hit_right= (self.pos[:, 0] + self.radius >= self.WIDTH)

        self.pos[hit_left, 0] = self.radius
        self.pos[hit_right, 0] = self.WIDTH - self.radius
        self.vel[hit_left | hit_right, 0] *= -0.9


    def add_ball(self, x, y, vel_x, vel_y):

        new_pos = np.array([[x, y]])
        new_vel = np.array([[vel_x, vel_y]])


        self.pos = np.vstack([self.pos, new_pos])
        self.vel = np.vstack([self.vel, new_vel])
        self.number += 1

    def handle_collisions(self):
        if self.number < 2:
            return

        diff = self.pos[:, np.newaxis, :] - self.pos[np.newaxis, :, :]
        dist_sq = np.sum(diff ** 2, axis=2)

        collision_mask = (dist_sq < (2 * self.radius) ** 2) & (dist_sq > 0)
        collision_mask = np.triu(collision_mask)

        idx1, idx2 = np.where(collision_mask)

        if len(idx1) == 0:
            return

        dists = np.sqrt(dist_sq[idx1, idx2])
        normals = diff[idx1, idx2] / dists[:, np.newaxis]

        rel_vel = self.vel[idx1] - self.vel[idx2]
        vel_along_normal = np.sum(rel_vel * normals, axis=1)

        approaching = vel_along_normal < 0
        if not np.any(approaching):
            return

        idx1, idx2 = idx1[approaching], idx2[approaching]
        normals = normals[approaching]
        vel_along_normal = vel_along_normal[approaching]
        dists = dists[approaching]

        restitution = 0.9
        impulse = -(1 + restitution) * vel_along_normal
        impulse_vec = (impulse[:, np.newaxis] / 2) * normals

        self.vel[idx1] += impulse_vec
        self.vel[idx2] -= impulse_vec

        overlap = (2 * self.radius) - dists
        correction = (overlap[:, np.newaxis] / 2) * normals
        self.pos[idx1] += correction
        self.pos[idx2] -= correction

    def draw(self, surface):
        for i in range(self.number):
            pg.draw.circle(surface, (0, 100, 250), (int(self.pos[i, 0]), int(self.pos[i, 1])), self.radius)


engine=Ball(num, WIDTH, HEIGHT, radii, gravitational_acc)
running=True
while running:
    mouse_pos=pg.mouse.get_pos()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running=False
        if event.type == pg.MOUSEBUTTONDOWN:
            getting_pressed=True
            init_x, init_y = event.pos
        if event.type == pg.MOUSEBUTTONUP:
            if getting_pressed:
                dx = init_x - event.pos[0]
                dy = init_y - event.pos[1]
                stretch=np.hypot(dx, dy)
                power_limit=150
                if stretch>power_limit:
                    scale=power_limit/stretch
                    dx *= scale
                    dy *= scale
                sensitivity = 0.15
                engine.add_ball(init_x, init_y, dx * sensitivity, dy * sensitivity)
                getting_pressed = False
    screen.fill((255,255,255))
    if getting_pressed:
        pg.draw.circle(screen, (0, 100, 250), (init_x, init_y), radii)
        pg.draw.line(screen, (255, 0, 0), (init_x, init_y), mouse_pos, 2)

    engine.update(delta)
    engine.handle_collisions()
    engine.draw(screen)
    pg.display.flip()
    CLOCK.tick(FPS)

pg.quit()
sys.exit()