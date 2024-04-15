from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

# grass_texture = load_texture("assests/grass.png")

app = Ursina()


WALKING_SPEED = 5
RUNNING_SPEED = WALKING_SPEED * 1.5
MIN_HEIGHT = -60
MAX_HEIGHT = 60

floor_set = set()

punch_sound = Audio("assets/punch.wav", autoplay=False, loop=False)

def update():
    if held_keys["control"]:
        player.speed = RUNNING_SPEED
    else:
        player.speed = WALKING_SPEED

    if player.y < MIN_HEIGHT:
        generate_floor()
        player.y = MAX_HEIGHT
        
class Voxel(Button):
    def __init__(self, position):
        super().__init__(
            parent=scene,
            position=position,
            model="cube",
            texture="white_cube",
            origin_y=0.5,
            color=color.color(0,0, random.uniform(0.9,1)),
            scale=1
        )
    

def generate_floor():
    for x in range(-16,16):
        for z in range(-16, 16):
            if (x, z) not in floor_set:
                floor_set.add((x,z))
                Voxel(position=(x,0,z))

def input(key):
    if key == "left mouse down":
        punch_sound.play()
        if mouse.hovered_entity is not None:
            x = mouse.hovered_entity.position.x
            z = mouse.hovered_entity.position.z
            floor_set.remove((x,z))
            destroy(mouse.hovered_entity)

    if key == "right mouse down":
        hitinfo = raycast(camera.world_position, camera.forward, distance=100)

        if hitinfo.hit:
            Voxel(position=hitinfo.entity.position + hitinfo.normal)


generate_floor()
player = FirstPersonController()
# Voxel(position=(0,0,0))

player.mouse_sensitivity = Vec2(100,100)
player.speed = 5



if __name__ == "__main__":
    app.run()