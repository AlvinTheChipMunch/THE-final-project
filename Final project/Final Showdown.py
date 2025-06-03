from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

targets = []
bullets= []
target = []
# Make a platform
counter = 0
app = Ursina()

platform = Entity(model="plane", scale=(100,1,100), color=color.white, texture="white_cube", texture_scale=(100, 100), collider="box")

player = FirstPersonController(model="cube", y=0, origin_y=0.5, speed=20)


# Make a bot that follow you
for _ in range(11):
    x = random.randrange(-50, 50)
    z = random.randrange(-50, 50)
    y = 1.5
    target = Entity(model="cube", texture="real.jpg", color=color.white, scale=(0.01,4,4), dx=0.05, position=(x,y,z), collider="box", rotation=(90,0,90))
    target.collider = BoxCollider(target, size=(3,3,3))
    targets.append(target)

# Player get a gun, click to shoot

gun = Entity(parent=camera, texture="th.jpg", origin_y=-0.5, scale=(0.1,0.1,0.1), position = (2,-0.5,3), collider='box', rotation=(0,-90,0))
gun2 = Entity(parent=camera, model="cube", texture="th.jpg", origin_y=-0.5, scale=(1,1,0.001), position = (2,-1.1,3), collider='box', rotation=(0,-280,0))
player.gun = gun

def input(key):
    global bullets,counter
    if key == "left mouse down" and player.gun:
        bullet = Entity(parent=gun, model='sphere', scale=(2, 2, 2), position=(0.8, 2.5,0), speed=5, color=color.black, collider='box', rotation_y=90)
        bullets.append(bullet)
        gun.blink(color.black)
        bullet.world_parent = scene
        counter += 1
        if counter >= 20:
            message = Text(text="You used all your bullet!", scale = 1.5, origin=(0,0), background=True, color=color.blue)
            application.pause()

def update():
    if held_keys["escape"]:
        application.quit()

    for target in targets:
        target.position += (player.position - target.position) * time.dt * 0.5
        target.look_at(player, axis='down')

    global bullets
    if len(bullets) > 0:
        for bullet in bullets:
            bullet.position += bullet.forward * 8

# if the bullet collide with the bot, it die
            hit_info = bullet.intersects()
            if hit_info.hit:
                if hit_info.entity in targets:
                    targets.remove(hit_info.entity)
                    destroy(hit_info.entity)
                    destroy(bullet)
                    bullets.remove(bullet)
            death_info = player.intersects()
            if death_info.hit:
                if death_info.entity in targets:
                    message = Text(text="You Lose!", scale = 1.5, origin=(0,0), background=True, color=color.red)
                    
# After killing a wave of bot, player win
                    if len(targets) == 0:
# Win screen
                        message = Text(text="You Won!", scale = 1.5, origin=(0,0), background=True, color=color.blue)
# Player are able to place block
if __name__ == "__main__":
    app.run()