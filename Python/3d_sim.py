import pygame, numpy, random, math, datetime
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


# initalise game
pygame.init()
display = (800, 600)
screen = pygame.display.set_mode((800, 600), pygame.DOUBLEBUF | pygame.OPENGL)
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, 0.0)

# physical scalars
NUM_BODIES = 128
G = -1
MAX_VELOCITY = 1


# OpenGL Lighting parameters
def set_lighting():
    # Enable Lighting
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    # Set lighting intensity and color
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.5, 0.5, 0.5, 1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1])

    # Set the light position
    glLightfv(GL_LIGHT0, GL_POSITION, [1.0, 1.0, 1.0, 0.0])

    # Enable material properties
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)


class body:
    def __init__(
        self,
        id,
        mass,
        position,
        velocity=[0, 0, 0],
        acceleration=[0, 0, 0],
        color="white",
        is_black_hole=False,
    ):
        self.id = id
        self.mass = mass
        self.position = position
        self.velocity = velocity  # if velocity else self.random_velocity()
        self.acceleration = acceleration
        self.color = self.random_color()
        self.is_black_hole = is_black_hole
        self.previous_positions = []

    def random_velocity(self):
        distance_to_center = math.sqrt(sum([coord**2 for coord in self.position]))
        speed = math.sqrt(G * 10 / distance_to_center)

        # Create a unit vector pointing in the direction of velocity
        velocity_direction = [-self.position[1], self.position[0], 0]
        velocity_direction = [
            coord / math.sqrt(sum([coord**2 for coord in velocity_direction]))
            for coord in velocity_direction
        ]

        return [coord * speed for coord in velocity_direction]

    def random_color(self):
        r = random.randint(0, 255)
        b = random.randint(0, 255)
        g = random.randint(0, 255)
        a = 255
        return [r, g, b, a]

    def update_position(self, new_position):
        self.previous_positions.append(self.position)
        self.position = new_position
        if len(self.previous_positions) > 20:  # limit the length of the trail
            self.previous_positions.pop(0)


# equations of motion
def squared(x):
    return x * x


def random_position():
    y = random.uniform(-1.0, 1.0) * display[0] * 4 / display[1]
    x = random.uniform(-1.0, 1.0) * display[0] * 4 / display[1]
    z = random.uniform(-10.0, -40.0)
    return [x, y, z]


def distance(body_0, body_1):
    x = squared(body_0.position[0] - body_1.position[0])
    y = squared(body_0.position[1] - body_1.position[1])
    z = squared(body_0.position[2] - body_1.position[2])
    return math.sqrt(x + y + z)


def distance_pos(pos_0, pos_1):
    x = squared(pos_0[0] - pos_1[0])
    y = squared(pos_0[1] - pos_1[1])
    z = squared(pos_0[2] - pos_1[2])
    return math.sqrt(x + y + z)


def distance_2d(pos_0, pos_1):
    x = squared(pos_0[0] - pos_1[0])
    y = squared(pos_0[1] - pos_1[1])
    return math.sqrt(x + y)


def acceleration(m_0, body_0, body_1):
    softening = 0.01
    dist = distance(body_0, body_1)
    denom = dist**2 + softening**2
    return G * m_0 / denom


def direction(body_0, body_1):
    dist = distance(body_0, body_1)
    if dist < 0.1:
        dist = 0.1
    x = (body_0.position[0] - body_1.position[0]) / dist
    y = (body_0.position[1] - body_1.position[1]) / dist
    z = (body_0.position[2] - body_1.position[2]) / dist
    return [x, y, z]


# Same as above but with position lists instead of bodies
def direction_pos(pos_0, pos_1):
    dist = distance_pos(pos_0, pos_1)
    if dist < 0.1:
        dist = 0.1
    x = (pos_0[0] - pos_1[0]) / dist
    y = (pos_0[1] - pos_1[1]) / dist
    z = (pos_0[2] - pos_1[2]) / dist
    return [x, y, z]


def total_acceleration(body, system):
    total_accel = [0, 0, 0]
    for body_ in system:
        if body_.id != body.id:
            accel = acceleration(body_.mass, body, body_)
            dir = direction(body, body_)
            total_accel[0] += dir[0] * accel
            total_accel[1] += dir[1] * accel
            total_accel[2] += dir[2] * accel
    return total_accel


def acceleration_step(body, system):
    total_accel = total_acceleration(body, system)
    damping_factor = 0.1  # You can adjust this value as needed
    body.velocity = [v * (1 - damping_factor) for v in body.velocity]
    return total_accel


def velocity_condition(velocity_x, velocity_y, velocity_z):
    if velocity_x < -1 * MAX_VELOCITY:
        velocity_x = -1 * MAX_VELOCITY
    if velocity_y < -1 * MAX_VELOCITY:
        velocity_y = -1 * MAX_VELOCITY
    if velocity_z < -1 * MAX_VELOCITY:
        velocity_z = -1 * MAX_VELOCITY
    if velocity_x > MAX_VELOCITY:
        velocity_x = MAX_VELOCITY
    if velocity_y > MAX_VELOCITY:
        velocity_y = MAX_VELOCITY
    if velocity_z > MAX_VELOCITY:
        velocity_z = MAX_VELOCITY
    return [velocity_x, velocity_y, velocity_z]


def velocity_step(inital_velocity, time_step, acceleration):
    velocity_x = inital_velocity[0] + acceleration[0] * time_step
    velocity_y = inital_velocity[1] + acceleration[1] * time_step
    velocity_z = inital_velocity[2] + acceleration[2] * time_step
    return velocity_condition(velocity_x, velocity_y, velocity_z)


def postion_step(inital_position, initial_velocity, time_step, acceleration):
    postion_x = (
        inital_position[0]
        + initial_velocity[0] * time_step
        + 0.5 * acceleration[0] * squared(time_step)
    )
    postion_y = (
        inital_position[1]
        + initial_velocity[1] * time_step
        + 0.5 * acceleration[1] * squared(time_step)
    )
    postion_z = (
        inital_position[2]
        + initial_velocity[2] * time_step
        + 0.5 * acceleration[2] * squared(time_step)
    )
    return [postion_x, postion_y, postion_z]


# time step calculations
def step(
    body,
    initial_velocity,
    initial_position,
    initial_acceleration,
    system,
    time_step,
):
    body.acceleration = acceleration_step(body, system)
    body.velocity = velocity_step(initial_velocity, time_step, initial_acceleration)
    body.update_position(
        postion_step(
            initial_position, initial_velocity, time_step, initial_acceleration
        )
    )


def dot_product(v1, v2):
    return sum((a * b) for a, b in zip(v1, v2))


def total_step(system, time_step, black_hole_position, black_hole_mass):
    for body in system:
        step(
            body,
            body.velocity,
            body.position,
            body.acceleration,
            system,
            time_step,
        )
        # Apply black hole gravity
        if black_hole_position is not None:
            direction_to_black_hole = direction_pos(body.position, black_hole_position)
            distance_to_black_hole = distance_pos(body.position, black_hole_position)
            # Calculate velocity towards the black hole
            velocity_towards_black_hole = dot_product(
                body.velocity, direction_to_black_hole
            )

            damping_factor = 1
            # To prevent the bodies from shooting out of the screen when being attracted from very close
            # But only the body is approaching the black hole (not when it is moving away)
            if distance_to_black_hole < 0.1 and velocity_towards_black_hole > 0:
                damping_factor = 1

            # Calculate force magnitude and direction (normalized)
            force_magnitude = (
                G
                * body.mass
                * damping_factor
                * black_hole_mass
                / (distance_to_black_hole**2 + 0.01**2)
            )
            force_direction = [
                force / distance_to_black_hole for force in direction_to_black_hole
            ]

            # Apply the force to the body (F = ma, so a = F/m)
            body.acceleration[0] += force_direction[0] * force_magnitude / body.mass
            body.acceleration[1] += force_direction[1] * force_magnitude / body.mass
            body.acceleration[2] += force_direction[2] * force_magnitude / body.mass


def draw(body):
    glPushMatrix()
    glColor3f(body.color[0] / 255.0, body.color[1] / 255.0, body.color[2] / 255.0)
    glTranslate(body.position[0], body.position[1], body.position[2])
    gluSphere(gluNewQuadric(), body.mass / 50, 32, 32)

    # draw the trail
    glBegin(GL_POINTS)
    for i, pos in enumerate(reversed(body.previous_positions)):
        glVertex3f(pos[0], pos[1], pos[2])
    glEnd()

    glPopMatrix()


def draw_all(system, black_hole_position):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # rotate the camera around the center of the system, which is at (0,0,0)
    # glRotatef(0.1, 0, 1, 0)
    for body in system:
        draw(body)
    if black_hole_position is not None:
        glPushMatrix()
        glColor3f(1.0, 1.0, 1.0)
        glTranslate(
            black_hole_position[0], black_hole_position[1], black_hole_position[2]
        )
        gluSphere(gluNewQuadric(), 0.1, 32, 32)
        glPopMatrix()
    pygame.display.flip()


# Convert 2D screen coordinates to 3D world coordinates
def screen_to_world_coordinates(screen_x, screen_y, depth_z):
    world_x = screen_x / display[0] * 2 - 1  # convert from [0, display[0]] to [-1, 1]
    world_y = 1 - screen_y / display[1] * 2  # convert from [0, display[1]] to [1, -1]

    # Apply the same scaling as in random_position
    world_x *= display[0] * 4 / display[1]
    world_y *= display[0] * 4 / display[1]

    return [world_x, world_y, depth_z]


if __name__ == "__main__":
    set_lighting()
    time_average, counter = [], 0
    time_step = 0
    system = [
        body(id=i, position=random_position(), mass=random.randint(1, 10))
        for i in range(NUM_BODIES)
    ]
    is_running = True

    # We create a "black" hole on user mouse clicks. RMB to repel, LMB to attract
    black_hole_position = None  # Initialize black hole position
    black_hole_mass = 100000  # Set black hole mass
    attracting = True

    while is_running:
        time_start = datetime.datetime.now()
        total_step(
            system,
            time_step,
            black_hole_position,
            (black_hole_mass if attracting else -black_hole_mass),
        )
        time_end = datetime.datetime.now()
        time_average.append((time_end - time_start).microseconds)
        draw_all(system, black_hole_position)
        time_step += 0.0001
        counter += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                is_running = False
                break

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Set black hole position when mouse button is pressed
                if event.button == 1:
                    attracting = True
                elif event.button == 3:
                    attracting = False
                black_hole_position = screen_to_world_coordinates(
                    *pygame.mouse.get_pos(), -20
                )
            elif event.type == pygame.MOUSEMOTION and black_hole_position is not None:
                # Update black hole position when mouse is moved while button is pressed
                black_hole_position = screen_to_world_coordinates(
                    *pygame.mouse.get_pos(), -20
                )
            elif event.type == pygame.MOUSEBUTTONUP:
                # Remove black hole when mouse button is released
                black_hole_position = None
        if counter == 8080:
            print("Average step time in microseconds: ", numpy.average(time_average))
            break
    print("")
    print("C++ output: ")
