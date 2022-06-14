import pygame
from pygame.locals import *
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

verticies = ((-0.6, 1, 0),  # góra kapelusza
             (-0.3, 1, 0.5),
             (0.3, 1, 0.5),
             (0.6, 1, 0),
             (0.3, 1, -0.5),
             (-0.3, 1, -0.5),

             (-0.6, -0.8, 0),  # środek kapelusza
             (-0.3, -0.8, 0.5),
             (0.3, -0.8, 0.5),
             (0.6, -0.8, 0),
             (0.3, -0.8, -0.5),
             (-0.3, -0.8, -0.5),

             (-1, -1, 0),  # dół kapelusza
             (-0.5, -1, 0.866),
             (0.5, -1, 0.866),
             (1, -1, 0),
             (0.5, -1, -0.866),
             (-0.5, -1, -0.866),

             (-0.55, 0.95, 0),  # góra kapelusza wewnątrz
             (-0.275, 0.95, 0.48),
             (0.275, 0.95, 0.48),
             (0.55, 0.95, 0),
             (0.275, 0.95, -0.48),
             (-0.275, 0.95, -0.48),

             (-0.55, -0.8, 0),  # środek kapelusza wewnątrz
             (-0.275, -0.8, 0.48),
             (0.275, -0.8, 0.48),
             (0.55, -0.8, 0),
             (0.275, -0.8, -0.48),
             (-0.275, -0.8, -0.48),

             (-1, -1.05, 0),  # dół kapelusza wewnątrz
             (-0.5, -1.05, 0.866),
             (0.5, -1.05, 0.866),
             (1, -1.05, 0),
             (0.5, -1.05, -0.866),
             (-0.5, -1.05, -0.866))

edges = ((0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0),  # góra kapelusza
         # góra - środek
         (0, 6), (1, 7), (2, 8), (3, 9), (4, 10), (5, 11),
         # środek kapelusza
         (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 6),
         # środek - dół
         (6, 12), (7, 13), (8, 14), (9, 15), (10, 16), (11, 17),
         # dół kapelusza
         (12, 13), (13, 14), (14, 15), (15, 16), (16, 17), (17, 12),

         # wewnatrz - zewnatrz
         (12, 30), (13, 31), (14, 32), (15, 33), (16, 34), (17, 35),

         # góra wew
         (18, 19), (19, 20), (20, 21), (21, 22), (22, 23), (23, 18),
         # góra - środek wew
         (18, 24), (19, 25), (20, 26), (21, 27), (22, 28), (23, 29),
         # środek wew
         (24, 25), (25, 26), (26, 27), (27, 28), (28, 29), (29, 24),
         # środek - dół wew
         (24, 30), (25, 31), (26, 32), (27, 33), (28, 34), (29, 35),
         # dół wew
         (30, 31), (31, 32), (32, 33), (33, 34), (34, 35), (35, 30))

surfacesHex = ((0, 1, 2, 3, 4, 5), (23, 22, 21, 20, 19, 18))
# surfacesHex = ((0, 1, 2, 3, 4, 5), (18, 19, 20, 21, 22, 23))
surfaces = ((6, 7, 1, 0),  # gorne zewn
            (7, 8, 2, 1),
            (8, 9, 3, 2),
            (9, 10, 4, 3),
            (10, 11, 5, 4),
            (11, 6, 0, 5),
            # dolne zewn
            (12, 13, 7, 6),
            (13, 14, 8, 7),
            (14, 15, 9, 8),
            (15, 16, 10, 9),
            (16, 17, 11, 10),
            (17, 12, 6, 11),
            # zewn wewn
            (30, 31, 13, 12),
            (31, 32, 14, 13),
            (32, 33, 15, 14),
            (33, 34, 16, 15),
            (34, 35, 17, 16),
            (35, 30, 12, 17),
            # dolne wewn
            (24, 25, 31, 30), (25, 26, 32, 31), (26, 27, 33, 32), (27, 28, 34, 33), (28, 29, 35, 34), (29, 24, 30, 35),
            # gorne wewn
            (18, 19, 25, 24), (19, 20, 26, 25), (20, 21, 27, 26), (21, 22, 28, 27), (22, 23, 29, 28), (23, 18, 24, 29))

colors = [(0.066, 0.317, 0.450) for _ in range(32)]
# colors2 = ((0.019, 0.247, 0.368), (0.066, 0.317, 0.450), (0.019, 0.247, 0.368),  # gorne zewn
#           (0.007, 0.172, 0.262), (0.007, 0.101, 0.152), (0.007, 0.172, 0.262),
#           # dolne zewn
#           (0.066, 0.317, 0.450), (0.019, 0.247, 0.368), (0.007, 0.172, 0.262),
#           (0.066, 0.317, 0.450), (0.019, 0.247, 0.368), (0.007, 0.172, 0.262),
#           # zewn wewn
#           (0.019, 0.247, 0.368), (0.007, 0.172, 0.262), (0.066, 0.317, 0.450),
#           (0.019, 0.247, 0.368), (0.007, 0.172, 0.262), (0.066, 0.317, 0.450),
#           # dolne wewn
#           (0.019, 0.247, 0.368), (0.066, 0.317, 0.450), (0.019, 0.247, 0.368),
#           (0.007, 0.172, 0.262), (0.007, 0.101, 0.152), (0.007, 0.172, 0.262),
#           # gorne wewn
#           (0.066, 0.317, 0.450), (0.019, 0.247, 0.368), (0.007, 0.172, 0.262),
#           (0.066, 0.317, 0.450), (0.019, 0.247, 0.368), (0.007, 0.172, 0.262),
#           # hexagony
#           (0.019, 0.247, 0.368), (0.019, 0.247, 0.368),)


def getNormal(points):
    points = np.array(points)
    n = np.cross(points[1, :] - points[0, :], points[2, :] - points[0, :])
    norm = np.linalg.norm(n)
    if norm == 0:
        raise ValueError('zero norm')
    return tuple(n / norm)


def getNormals(planes):
    return [getNormal([verticies[vNr] for vNr in plane]) for plane in planes]


normals = getNormals(surfaces)
normalsHex = getNormals(surfacesHex)


def drawText(x, y, text, font):
    textSurface = font.render(text, True, (0.007, 0.172, 0.262, 255)).convert_alpha()
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glWindowPos2d(x, y)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)
    return


def drawObj():
    x = 0
    glBegin(GL_QUADS)
    for surface in surfaces:
        glNormal3fv(normals[x])
        for vertex in surface:
            glColor3fv(colors[x])
            glVertex3fv(verticies[vertex])
        x += 1
    glEnd()

    y = 0
    glBegin(GL_POLYGON)
    for surface in surfacesHex:
        glNormal3fv(normalsHex[y])
        for vertex in surface:
            glColor3fv(colors[x])
            glVertex3fv(verticies[vertex])
        x += 1
        y += 1
    glEnd()

    # glBegin(GL_LINES)
    # for edge in edges:
    #     for vertex in edge:
    #         glColor3fv((0, 0, 0))
    #         glVertex3fv(verticies[vertex])
    # glEnd()


def main():
    pygame.init()
    pygame.display.set_caption("Cylinder")
    font = pygame.font.SysFont('arial', 15)
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    glLoadIdentity()

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glMatrixMode(GL_MODELVIEW)
    glTranslatef(0, 0, -7)
    glClearColor(1, 0.843, 0, 0)  # kolor tła
    glCullFace(GL_BACK)
    glShadeModel(GL_SMOOTH)

    glLight(GL_LIGHT0, GL_POSITION,  (0, 0, 1, 0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0, 0, 0, 1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)  # to display txt
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # to display txt

    mx, my, mz = 0.0, 0.0, 0.0
    ra, rx, ry, rz = 0.0, 0.0, 0.0, 0.0
    speed = 3.0
    ml = 0.01
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_p:  # restart
                    glLoadIdentity()
                    glTranslatef(0, 0, -7)
                    continue
                elif event.key == pygame.K_1:  # ustawienie prędkości
                    speed = 1.0
                elif event.key == pygame.K_2:
                    speed = 2.0
                elif event.key == pygame.K_3:
                    speed = 3.0
                elif event.key == pygame.K_4:
                    speed = 4.0
                elif event.key == pygame.K_5:
                    speed = 5.0
                elif event.key == pygame.K_6:
                    speed = 6.0
                elif event.key == pygame.K_7:
                    speed = 7.0
                elif event.key == pygame.K_8:
                    speed = 8.0
                elif event.key == pygame.K_9:
                    speed = 9.0
                elif event.key == pygame.K_0:
                    speed = 0.0

                # sterowanie
            pressed = pygame.key.get_pressed()
            mx = (pressed[K_l] - pressed[K_j]) * ml * speed  # prawo, lewo
            my = (pressed[K_u] - pressed[K_o]) * ml * speed  # góra, dół
            mz = (pressed[K_i] - pressed[K_k]) * ml * speed  # przód, tył
            glTranslatef(mx, my, mz)
            # obracanie
            rx = (pressed[K_s] - pressed[K_w])  # dół, góra
            ry = (pressed[K_d] - pressed[K_a])  # prawo, lewo
            rz = (pressed[K_q] - pressed[K_e])  # przeciwnie, zgodnie (z ruchem zegara)
            if rx or ry or rz:
                ra = speed
            else:
                ra = 0.0  # jeśli kąt != 0 to przy wyzerowanych innych składowych obiekt się porusza
            glRotatef(ra, rx, ry, rz)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

        drawObj()
        drawText(10, 10, "Created by Katarzyna Sajchta", font)

        glDisable(GL_LIGHT0)
        glDisable(GL_LIGHTING)
        glDisable(GL_COLOR_MATERIAL)

        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == '__main__':
    main()
