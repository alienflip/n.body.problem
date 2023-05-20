import pygame, numpy, random, math, datetime

# initalise game
pygame.init()
screen = pygame.display.set_mode((1280, 720))
screen.fill("black")

# physical scalars
NUM_BODIES = 128
G = -1
MAX_VELOCITY = 1


class body:
    def __init__(
        self, id, mass, position, velocity=[0, 0], acceleration=[0, 0], color="white"
    ):
        self.id = id
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.color = self.random_color()

    def random_color(self):
        r = random.randint(0, 255)
        b = random.randint(0, 255)
        g = random.randint(0, 255)
        a = 255
        return [r, g, b, a]


# equations of motion
def squared(x):
    return x * x


def distance(body_0, body_1):
    x = squared(body_0.position[0] - body_1.position[0])
    y = squared(body_0.position[1] - body_1.position[1])
    return math.sqrt(x + y)


def acceleration(m_0, body_0, body_1):
    denom = squared(distance(body_0, body_1))
    if denom < 0.1:
        return 0.1
    else:
        return G * m_0 / denom


def direction(body_0, body_1):
    dist = distance(body_0, body_1)
    if dist < 0.1:
        dist = 0.1
    x = (body_0.position[0] - body_1.position[0]) / dist
    y = (body_0.position[1] - body_1.position[1]) / dist
    return [x, y]


def total_acceleration(body, system):
    total_accel = [0, 0]
    for body_ in system:
        if body_.id != body.id:
            accel = acceleration(body_.mass, body, body_)
            dir = direction(body, body_)
            total_accel[0] += dir[0] * accel
            total_accel[1] += dir[1] * accel
    return total_accel


def acceleration_step(body, system):
    return total_acceleration(body, system)


def velocity_condition(velocity_x, velocity_y):
    if velocity_x < -1 * MAX_VELOCITY:
        velocity_x = -1 * MAX_VELOCITY
    if velocity_y < -1 * MAX_VELOCITY:
        velocity_y = -1 * MAX_VELOCITY
    if velocity_x > MAX_VELOCITY:
        velocity_x = MAX_VELOCITY
    if velocity_y > MAX_VELOCITY:
        velocity_y = MAX_VELOCITY
    return [velocity_x, velocity_y]


def velocity_step(inital_velocity, time_step, acceleration):
    velocity_x = inital_velocity[0] + acceleration[0] * time_step
    velocity_y = inital_velocity[1] + acceleration[1] * time_step
    return velocity_condition(velocity_x, velocity_y)


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
    return [postion_x, postion_y]


# assuming a universe with a toral topology
def boundary_condition(body, dimensions):
    if body.position[0] < 0:
        body.position[0] = dimensions[0]
    if body.position[1] < 0:
        body.position[1] = dimensions[1]
    if body.position[0] > dimensions[0]:
        body.position[0] = 0
    if body.position[1] > dimensions[1]:
        body.position[1] = 0


# time step calculations
def step(
    body,
    initial_velocity,
    initial_position,
    initial_acceleration,
    system,
    time_step,
    dimensions,
):
    body.acceleration = acceleration_step(body, system)
    boundary_condition(body, dimensions)
    body.velocity = velocity_step(initial_velocity, time_step, initial_acceleration)
    body.position = postion_step(
        initial_position, initial_velocity, time_step, initial_acceleration
    )


def total_step(system, time_step, dimensions):
    for body in system:
        step(
            body,
            body.velocity,
            body.position,
            body.acceleration,
            system,
            time_step,
            dimensions,
        )


# draw function
def random_position():
    return (random.randrange(screen.get_width()), random.randrange(screen.get_height()))


def draw(position, screen, color):
    position = pygame.Vector2(position[0], position[1])
    if position[0] < 0 or position[1] < 0:
        return
    if position[0] > screen.get_width() or position[1] > screen.get_width():
        return
    else:
        pygame.draw.circle(screen, color, position, 10)


def draw_all(system, screen):
    screen.fill("black")
    for body in system:
        draw(body.position, screen, body.color)
    pygame.display.flip()


if __name__ == "__main__":
    time_average, counter = [], 0
    time_step = 0
    system = [
        body(id=i, position=random_position(), mass=random.randint(0, 10))
        for i in range(NUM_BODIES)
    ]
    dimensions = [screen.get_width(), screen.get_height()]
    is_running = True
    while is_running:
        time_start = datetime.datetime.now()
        total_step(system, time_step, dimensions)
        time_end = datetime.datetime.now()
        time_average.append((time_end - time_start).microseconds)
        draw_all(system, screen)
        time_step += 0.001
        counter += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                is_running = False
                break
        if counter == 808:
            print("Average step time in microseconds: ", numpy.average(time_average))
            break
    print("")
    print("C++ output: ")
