import pygame, numpy, random, math, datetime

# initalise game
pygame.init()
screen = pygame.display.set_mode((1280, 720))
screen.fill("black")

# physical scalars
NUM_BODIES=128
G = -1
dt, time_step = 0, 0

class body:
    def __init__(self, id, mass, position, velocity=[0,0], acceleration=[0, 0]):
        self.id = id
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        
# equations of motion
def squared(x):
    return x*x

def cubed(x):
    return x*x*x

def distance(body_0, body_1):
    x = squared(body_0.position[0] - body_1.position[0])
    y = squared(body_0.position[1] - body_1.position[1])
    return math.sqrt(x + y)

def acceleration(m_0, body_0, body_1):
    denom = squared(distance(body_0, body_1))
    if denom == 0:
        return 1e-7
    else:
        return G * m_0 / denom
    
def direction(body_0, body_1):
    x = (body_0.position[0] - body_1.position[0]) / distance(body_0, body_1)
    y = (body_0.position[1] - body_1.position[1]) / distance(body_0, body_1)
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

def velocity_step(inital_velocity, time_step, acceleration):
    velocity_x = inital_velocity[0] + acceleration[0] * time_step
    velocity_y = inital_velocity[1] + acceleration[1] * time_step
    return [velocity_x, velocity_y]

def postion_step(inital_position, initial_velocity, time_step, acceleration):
    postion_x = inital_position[0] + initial_velocity[0] * time_step + 0.5 * acceleration[0] * squared(time_step)
    postion_y = inital_position[1] + initial_velocity[1] * time_step + 0.5 * acceleration[1] * squared(time_step)
    return [postion_x, postion_y]

# time step calculations
def step(body, initial_velocity, initial_position, initial_acceleration, system):
    body.acceleration = acceleration_step(body, system)
    body.velocity = velocity_step(initial_velocity, time_step, initial_acceleration)
    body.position = postion_step(initial_position, initial_velocity, time_step, initial_acceleration)

def total_step(system):
    for body in system:
        step(body, body.velocity, body.position, body.acceleration, system)

# draw function
def random_position():
    return (random.randrange(screen.get_width()), random.randrange(screen.get_width()))

def draw(position, screen, color):
    screen.fill("black")
    position = pygame.Vector2(position[0], position[1])
    pygame.draw.circle(screen, color, position, 10)
        
def sim(time_step, screen):
    timea = []
    clock = pygame.time.Clock()
    system = [body(id=i, position=random_position(), mass=1) for i in range(NUM_BODIES)]
    counter = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return pygame.quit()
        times = datetime.datetime.now()
        total_step(system)
        timee = datetime.datetime.now()
        timea.append((timee - times).microseconds)
        pygame.display.flip()
        dt = clock.tick(60) / 1000
        time_step += dt
        counter+=1
        if counter == 100:
            print("Average step time in microseconds: ", numpy.average(timea))
            break

sim(time_step=time_step, screen=screen)