# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5

key_dict = {simplegui.KEY_MAP['left'] : "my_ship_left",
            simplegui.KEY_MAP['right'] : "my_ship_right",
            simplegui.KEY_MAP['up'] : "my_ship_thrust",
            simplegui.KEY_MAP['down'] : "my_ship_off",
            simplegui.KEY_MAP['space'] : "my_ship_shot"
           }

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 80)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 10, 100)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 60)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.thruster = False
        
    def draw(self,canvas):
        if self.thruster:
            canvas.draw_image(self.image, (self.image_center[0]+self.image_size[0], self.image_center[1]),
                              self.image_size, self.pos, (self.radius,self.radius), self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, (self.radius,self.radius), self.angle)

    def update(self):
        self.angle += self.angle_vel
        if self.thruster:
            self.vel[0] += 0.3*angle_to_vector(self.angle)[0]
            self.vel[1] += 0.3*angle_to_vector(self.angle)[1]
        self.vel[0] -= 0.02*self.vel[0]
        self.vel[1] -= 0.02*self.vel[1]
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.pos[0] = self.pos[0] % WIDTH
        self.pos[1] = self.pos[1] % HEIGHT
        
        
    def change_angle_vel(self, amount):
        self.angle_vel += amount
        
    def change_thrust(self, state):
        self.thruster = state
        if self.thruster:
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.rewind()
    def shoot(self):
        global a_missile
        dx = self.radius/2*angle_to_vector(self.angle)[0]
        dy = self.radius/2*angle_to_vector(self.angle)[1]
        a_missile = Sprite([self.pos[0]+dx,self.pos[1]+dy] ,
                           [self.vel[0] + 5*angle_to_vector(self.angle)[0], self.vel[1] + 5*angle_to_vector(self.angle)[1]] ,
                           0, 0, missile_image, missile_info, missile_sound)
        
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, (self.radius,self.radius), self.angle)
    
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]  
        self.angle += self.angle_vel
        self.pos[0] = self.pos[0] % WIDTH
        self.pos[1] = self.pos[1] % HEIGHT
           
def draw(canvas):
    global time
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    canvas.draw_text('Score', [30, 30], 20, 'White')
    canvas.draw_text(str(score), [50, 50], 20, 'White')
    canvas.draw_text('Lives', [WIDTH-70, 30], 20, 'White')
    canvas.draw_text(str(lives), [WIDTH-50, 50], 20, 'White')
    
    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    a_rock.update()
    a_missile.update()
            
# timer handler that spawns a rock    
def rock_spawner():
    global a_rock
    width = random.randint(0, WIDTH)
    height = random.randint(0, HEIGHT)
    while dist([width, height], a_rock.pos)<WIDTH/3:
        width = random.randint(0, WIDTH)
        height = random.randint(0, HEIGHT)
    a_rock = Sprite([width, height], [random.random()*6-3, random.random()*6-3], 0, random.random()*0.2-0.1, asteroid_image, asteroid_info)

def keydown_handler(key):
    for k in key_dict.keys():
        if key == k:
            if key_dict[key] == "my_ship_left":
                my_ship.change_angle_vel(-0.1)
            elif key_dict[key] == "my_ship_right":
                my_ship.change_angle_vel(0.1)
            elif key_dict[key] == "my_ship_thrust":
                my_ship.change_thrust(True)
            elif key_dict[key] == "my_ship_shot":
                my_ship.shoot()
                
def keyup_handler(key):
    for k in key_dict.keys():
        if key == k:
            if key_dict[key] == "my_ship_left":
                my_ship.change_angle_vel(0.1)
            elif key_dict[key] == "my_ship_right":
                my_ship.change_angle_vel(-0.1)
            elif key_dict[key] == "my_ship_thrust":
                my_ship.change_thrust(False)

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0.01, asteroid_image, asteroid_info)
a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown_handler)
frame.set_keyup_handler(keyup_handler)
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
