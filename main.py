from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from height_map import HillGrid


app = Ursina()

WALKING_SPEED = 5
RUNNING_SPEED = WALKING_SPEED * 1.5
MIN_HEIGHT = -60 
MAX_HEIGHT = 60
grass_texture = load_texture("assets/grass.png")
dirt_texture = load_texture("assets/dirt.png")


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
    def __init__(self, position,texture):
        super().__init__(
            parent=scene,
            position=position,
            model="assets/block",
            texture=texture,
            origin_y=0.5,
            color=color.color(0,0, random.uniform(0.9,1)),
            scale=0.5
        )


def generate_floor():
    h = HillGrid(ITER=50, SIZE=20)
    for x in range(16):
        for z in range( 16):
            for y in range(-1, h[x][z]):
                Voxel(position=(x,y,z), texture=dirt_texture)
            Voxel(position=(x, h[x][z] ,z), texture=grass_texture)

def input(key):
    if key == "left mouse down":
        punch_sound.play()
        if mouse.hovered_entity is not None:
            x = mouse.hovered_entity.position.x
            z = mouse.hovered_entity.position.z
            destroy(mouse.hovered_entity)

    if key == "right mouse down":
        hitinfo = raycast(camera.world_position, camera.forward, distance=100)

        if hitinfo.hit:
            Voxel(position=hitinfo.entity.position + hitinfo.normal, texture=grass_texture)

generate_floor()
player = FirstPersonController()
player.mouse_sensitivity = Vec2(100, 100)
player.speed = 5


if __name__=="__main__":
    app.run()
