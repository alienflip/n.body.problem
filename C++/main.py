import pygame, numpy, random, math, datetime

# initalise game
pygame.init()
screen = pygame.display.set_mode((1280, 720))
screen.fill("black")

# physical scalars
NUM_BODIES = 128
G = -1
MAX_VELOCITY = 1

def random_color():
    r = random.randint(0, 255)
    b = random.randint(0, 255)
    g = random.randint(0, 255)
    a = 255
    return [r, g, b ,a]

# equations of motion
def squared(x):
    return x*x

def distance(pos_0_x, pos_0_y, pos_1_x, pos_1_y):
    x = squared(pos_0_x - pos_1_x)
    y = squared(pos_0_y - pos_1_y)
    return math.sqrt(x + y)

def acceleration(m_0, pos_0_x, pos_0_y, pos_1_x, pos_1_y):
    denom = squared(distance(pos_0_x, pos_0_y, pos_1_x, pos_1_y))
    if denom < 0.1:
        return 0.1
    else:
        return G * m_0 / denom
    
def direction(pos_0_x, pos_0_y, pos_1_x, pos_1_y):
    dist = distance(pos_0_x, pos_0_y, pos_1_x, pos_1_y)
    if dist < 0.1:
        dist = 0.1
    x = (pos_0_x - pos_1_x) / dist
    y = (pos_0_y - pos_1_y) / dist
    return [x, y]

def acceleration_step(current_body, system):
    total_accel = [0, 0]
    pos_0_x = system[current_body+2]
    pos_0_y = system[current_body+3]
    for i in range(len(system)):
        if i % 8 == 0:
            id = system[i]
            if current_body != id:
                mass = system[i+1]
                pos_1_x = system[i+2]
                pos_1_y = system[i+3]
                accel = acceleration(mass, pos_0_x, pos_0_y, pos_1_x, pos_1_y)
                dir = direction(pos_0_x, pos_0_y, pos_1_x, pos_1_y)
                total_accel[0] += dir[0] * accel
                total_accel[1] += dir[1] * accel
    return total_accel

def velocity_condition(velocity_x, velocity_y):
    if velocity_x < -1 * MAX_VELOCITY:
        velocity_x = -1 * MAX_VELOCITY
    if velocity_y < -1 * MAX_VELOCITY:
        velocity_y = -1 * MAX_VELOCITY
    if velocity_x > MAX_VELOCITY:
        velocity_x =  MAX_VELOCITY
    if velocity_y > MAX_VELOCITY:
        velocity_y = MAX_VELOCITY
    return [velocity_x, velocity_y]

def velocity_step(inital_velocity, time_step, acceleration):
    velocity_x = inital_velocity[0] + acceleration[0] * time_step
    velocity_y = inital_velocity[1] + acceleration[1] * time_step
    return velocity_condition(velocity_x, velocity_y)

def postion_step(inital_position, initial_velocity, time_step, acceleration):
    postion_x = inital_position[0] + initial_velocity[0] * time_step + 0.5 * acceleration[0] * squared(time_step)
    postion_y = inital_position[1] + initial_velocity[1] * time_step + 0.5 * acceleration[1] * squared(time_step)
    return [postion_x, postion_y]

# assuming a universe with a toral topology
def boundary_condition(pos, dimensions):
    if pos[0] < 0:
        pos[0] = dimensions[0]
    if pos[1] < 0:
        pos[1] = dimensions[1]
    if pos[0] > dimensions[0]:
        pos[0] = 0
    if pos[1] > dimensions[1]:
        pos[1] = 0

# time step calculations
def step(current_body, initial_velocity, initial_position, initial_acceleration, system, time_step, dimensions):
    if current_body == 0:
        pass#print(initial_acceleration)
    acceleration = acceleration_step(current_body, system)
    if current_body == 0:
        pass#print(acceleration)
    boundary_condition(initial_position, dimensions)
    velocity = velocity_step(initial_velocity, time_step, initial_acceleration)
    position = postion_step(initial_position, initial_velocity, time_step, initial_acceleration)
    return [position, velocity, acceleration]

def total_step(system, time_step, dimensions):
    output = []
    for i in range(len(system)):
        if i % 8 == 0:
            pos_x = system[i+2]
            pos_y = system[i+3]
            vel_x = system[i+4]
            vel_y = system[i+5]
            accel_x = system[i+6]
            accel_y = system[i+7]
            out_i = step(i, [vel_x, vel_y], [pos_x, pos_y], [accel_x, accel_y], system, time_step, dimensions)
            output.append(system[i])
            output.append(system[i+1])
            output.append(out_i[0][0])
            output.append(out_i[0][1])
            output.append(out_i[1][0])
            output.append(out_i[1][1])
            output.append(out_i[2][0])
            output.append(out_i[2][1])
    return output

# draw function
def random_position():
    return (random.randrange(screen.get_width()), random.randrange(screen.get_height()))

def draw(position_x, position_y, screen, color):
    position = pygame.Vector2(position_x, position_y)
    if position[0] < 0 or position[1] < 0:
        return
    if position[0] > screen.get_width() or position[1] > screen.get_width():
        return
    else:
        pygame.draw.circle(screen, color, position, 10)

def draw_all(system, screen, id_color_map):
    screen.fill("black")
    for i in range(len(system)):
        if i % 8 == 0:
            draw(system[i+2], system[i+3], screen, id_color_map[int(i/8)])
    pygame.display.flip()

if __name__ == '__main__':
    dimensions = [screen.get_width(), screen.get_height()]
    id_color_map = [random_color() for i in range(NUM_BODIES)]
    time_average, counter, time_step = [], 0, 0
    input_system = [] 
    #input_system = [0, 2, 78, 261, 0, 0, 0, 0, 1, 1, 861, 534, 0, 0, 0, 0, 2, 0, 187, 372, 0, 0, 0, 0, 3, 2, 1120, 0, 0, 0, 0, 0, 4, 2, 411, 579, 0, 0, 0, 0, 5, 0, 788, 444, 0, 0, 0, 0, 6, 2, 1086, 52, 0, 0, 0, 0, 7, 7, 828, 305, 0, 0, 0, 0, 8, 7, 199, 562, 0, 0, 0, 0, 9, 5, 191, 456, 0, 0, 0, 0, 10, 4, 1124, 684, 0, 0, 0, 0, 11, 8, 1149, 292, 0, 0, 0, 0, 12, 0, 929, 164, 0, 0, 0, 0, 13, 4, 730, 319, 0, 0, 0, 0, 14, 5, 406, 481, 0, 0, 0, 0, 15, 9, 626, 282, 0, 0, 0, 0, 16, 1, 690, 595, 0, 0, 0, 0, 17, 6, 616, 566, 0, 0, 0, 0, 18, 5, 543, 439, 0, 0, 0, 0, 19, 2, 1021, 151, 0, 0, 0, 0, 20, 5, 1167, 88, 0, 0, 0, 0, 21, 6, 1273, 570, 0, 0, 0, 0, 22, 3, 1153, 37, 0, 0, 0, 0, 23, 2, 1022, 433, 0, 0, 0, 0, 24, 8, 171, 295, 0, 0, 0, 0, 25, 1, 1042, 258, 0, 0, 0, 0, 26, 9, 163, 671, 0, 0, 0, 0, 27, 7, 570, 183, 0, 0, 0, 0, 28, 5, 150, 637, 0, 0, 0, 0, 29, 7, 326, 339, 0, 0, 0, 0, 30, 0, 455, 237, 0, 0, 0, 0, 31, 1, 1154, 516, 0, 0, 0, 0, 32, 8, 1268, 116, 0, 0, 0, 0, 33, 1, 1052, 3, 0, 0, 0, 0, 34, 1, 1128, 327, 0, 0, 0, 0, 35, 5, 557, 81, 0, 0, 0, 0, 36, 5, 20, 544, 0, 0, 0, 0, 37, 1, 216, 713, 0, 0, 0, 0, 38, 9, 418, 175, 0, 0, 0, 0, 39, 9, 1119, 518, 0, 0, 0, 0, 40, 7, 276, 427, 0, 0, 0, 0, 41, 2, 949, 182, 0, 0, 0, 0, 42, 2, 549, 65, 0, 0, 0, 0, 43, 0, 820, 387, 0, 0, 0, 0, 44, 10, 1021, 584, 0, 0, 0, 0, 45, 1, 1061, 519, 0, 0, 0, 0, 46, 9, 148, 90, 0, 0, 0, 0, 47, 3, 888, 470, 0, 0, 0, 0, 48, 10, 292, 208, 0, 0, 0, 0, 49, 5, 81, 649, 0, 0, 0, 0, 50, 0, 1274, 158, 0, 0, 0, 0, 51, 8, 48, 501, 0, 0, 0, 0, 52, 8, 1145, 401, 0, 0, 0, 0, 53, 3, 1191, 89, 0, 0, 0, 0, 54, 7, 340, 397, 0, 0, 0, 0, 55, 6, 437, 100, 0, 0, 0, 0, 56, 9, 475, 352, 0, 0, 0, 0, 57, 6, 1188, 344, 0, 0, 0, 0, 58, 9, 212, 635, 0, 0, 0, 0, 59, 3, 1084, 49, 0, 0, 0, 0, 60, 7, 1, 655, 0, 0, 0, 0, 61, 1, 407, 522, 0, 0, 0, 0, 62, 9, 413, 632, 0, 0, 0, 0, 63, 4, 102, 553, 0, 0, 0, 0, 64, 6, 479, 654, 0, 0, 0, 0, 65, 0, 834, 71, 0, 0, 0, 0, 66, 4, 1140, 612, 0, 0, 0, 0, 67, 10, 21, 518, 0, 0, 0, 0, 68, 10, 93, 79, 0, 0, 0, 0, 69, 3, 327, 633, 0, 0, 0, 0, 70, 7, 417, 621, 0, 0, 0, 0, 71, 8, 551, 345, 0, 0, 0, 0, 72, 8, 346, 167, 0, 0, 0, 0, 73, 6, 542, 56, 0, 0, 0, 0, 74, 0, 585, 698, 0, 0, 0, 0, 75, 4, 965, 540, 0, 0, 0, 0, 76, 3, 1174, 401, 0, 0, 0, 0, 77, 3, 989, 389, 0, 0, 0, 0, 78, 4, 1051, 155, 0, 0, 0, 0, 79, 10, 1242, 41, 0, 0, 0, 0, 80, 4, 1024, 19, 0, 0, 0, 0, 81, 3, 678, 477, 0, 0, 0, 0, 82, 5, 128, 617, 0, 0, 0, 0, 83, 9, 231, 584, 0, 0, 0, 0, 84, 10, 153, 673, 0, 0, 0, 0, 85, 5, 480, 427, 0, 0, 0, 0, 86, 7, 1247, 402, 0, 0, 0, 0, 87, 5, 1024, 320, 0, 0, 0, 0, 88, 10, 843, 18, 0, 0, 0, 0, 89, 7, 482, 490, 0, 0, 0, 0, 90, 8, 490, 348, 0, 0, 0, 0, 91, 4, 810, 109, 0, 0, 0, 0, 92, 5, 837, 463, 0, 0, 0, 0, 93, 1, 1234, 395, 0, 0, 0, 0, 94, 5, 320, 592, 0, 0, 0, 0, 95, 2, 604, 48, 0, 0, 0, 0, 96, 7, 1144, 505, 0, 0, 0, 0, 97, 7, 481, 486, 0, 0, 0, 0, 98, 1, 1096, 302, 0, 0, 0, 0, 99, 9, 1088, 637, 0, 0, 0, 0, 100, 10, 1172, 411, 0, 0, 0, 0, 101, 4, 4, 689, 0, 0, 0, 0, 102, 0, 1247, 336, 0, 0, 0, 0, 103, 7, 435, 23, 0, 0, 0, 0, 104, 2, 822, 701, 0, 0, 0, 0, 105, 4, 72, 182, 0, 0, 0, 0, 106, 6, 1226, 304, 0, 0, 0, 0, 107, 10, 769, 55, 0, 0, 0, 0, 108, 0, 306, 40, 0, 0, 0, 0, 109, 1, 324, 671, 0, 0, 0, 0, 110, 5, 197, 534, 0, 0, 0, 0, 111, 5, 100, 123, 0, 0, 0, 0, 112, 0, 605, 485, 0, 0, 0, 0, 113, 3, 718, 450, 0, 0, 0, 0, 114, 8, 407, 401, 0, 0, 0, 0, 115, 7, 937, 688, 0, 0, 0, 0, 116, 3, 513, 482, 0, 0, 0, 0, 117, 3, 477, 707, 0, 0, 0, 0, 118, 8, 959, 231, 0, 0, 0, 0, 119, 6, 1082, 124, 0, 0, 0, 0, 120, 8, 707, 467, 0, 0, 0, 0, 121, 9, 928, 690, 0, 0, 0, 0, 122, 0, 606, 708, 0, 0, 0, 0, 123, 9, 754, 41, 0, 0, 0, 0, 124, 7, 892, 669, 0, 0, 0, 0, 125, 0, 1203, 539, 0, 0, 0, 0, 126, 0, 912, 416, 0, 0, 0, 0, 127, 0, 255, 11, 0, 0, 0, 0]
    for i in range(NUM_BODIES):
        position = random_position()
        velocity = [0, 0]
        accel = [0, 0]
        input_system.append(i)
        input_system.append(random.randint(0, 10))
        input_system.append(position[0])
        input_system.append(position[1])
        input_system.append(velocity[0])
        input_system.append(velocity[1])
        input_system.append(accel[0])
        input_system.append(accel[1])
    is_running = True
    while is_running:
        time_start = datetime.datetime.now()
        input_system = total_step(input_system, time_step, dimensions)
        #print(input_system)
        time_end = datetime.datetime.now()
        time_average.append((time_end - time_start).microseconds)
        draw_all(input_system, screen, id_color_map)
        time_step += 0.001
        #break
        counter+=1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                is_running = False
                print("Average step time in microseconds: ", numpy.average(time_average))
                break
        if counter == 808:
            print("Average step time in microseconds: ", numpy.average(time_average))
            break