import pgzrun
TILE_SIZE = 64
# map with 13x13 grid
WIDTH = HEIGHT = TILE_SIZE * 13

tiles = ['straight', 'tree3', 'tree2', 'fairy']
maze = [
    [1,1,1,0,1,1,1,1,1,1,1,1,1],
    [1,1,1,0,1,1,0,0,0,0,0,1,1],
    [1,1,1,0,0,0,0,1,0,1,0,1,1],
    [1,1,1,1,1,1,1,1,0,1,0,1,1],
    [1,3,1,1,0,0,0,0,0,1,0,3,1],
    [1,0,1,1,0,1,1,1,0,1,1,1,1],
    [1,0,1,1,0,1,3,1,0,1,1,1,1],
    [1,0,0,0,0,1,0,1,0,1,1,1,1],
    [1,1,0,1,1,1,0,1,0,1,1,1,1],
    [1,1,0,0,0,0,0,0,0,1,1,1,1],
    [1,1,1,1,1,1,1,1,0,1,1,1,1],
    [1,1,1,1,1,1,1,0,0,1,1,1,1],
    [1,1,1,1,1,1,1,2,1,1,1,1,1]
]
#To Do: have enemies chase player, change keys, possibly change images)
player = Actor('girl', topleft = (3*TILE_SIZE,1*TILE_SIZE))
enemy1 = Actor('guy', topleft = (2* TILE_SIZE, 7* TILE_SIZE))
enemy2 = Actor('boy1', topleft = (8* TILE_SIZE, 1* TILE_SIZE))

#enemy2 = #To Do (I tried adding and another enemy and program said invalid syntax for line 27/28)
moveForward = True
move_enemy2_Forward = True
player_dead = False
unlock = 0
msg = ""

def draw():
    screen.clear()
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            img = tiles[maze[row][col]]
            screen.blit(img, (x,y))
    player.draw()
    enemy1.draw()
    enemy2.draw()
    screen.draw.text(msg, (10,10), color = 'cyan', fontsize = 50)

def on_key_down(key):
    global unlock
    global msg
    row = int(player.y//TILE_SIZE)
    col = int(player.x//TILE_SIZE)
    if key == keys.UP:
        row -= 1
    if key == keys.DOWN:
        row += 1
    if key == keys.LEFT:
        col -= 1
    if key == keys.RIGHT:
        col += 1
        print(row,col)
    tile = tiles[maze[row][col]]
    if tile == 'straight' and not player_dead:
        move_player(row,col)
    if tile == 'fairy':
        unlock += 1 
        maze[row][col] = 0
        move_player(row,col)
    if tile == 'tree2' and unlock == 3:
        msg = 'Helena has escaped, but has she truly won?'
        move_player(row,col)
        sounds.collision.play()

def move_player(row,col):
    x = col*TILE_SIZE
    y = row*TILE_SIZE
    animate(player,topleft = (x,y), duration=.2)

def move_enemy1():
    global moveForward
    global msg
    
    
    row = int(enemy1.y//TILE_SIZE)
    col = int(enemy1.x//TILE_SIZE)
    tile = tiles[maze[row][col]]
    if moveForward:
        col += 1
    else:
        col -= 1
    tile = tiles[maze[row][col]]
        
    if not tile == 'tree3':
        x = col*TILE_SIZE
        y = row * TILE_SIZE
        animate(enemy1,topleft = (x,y), duration = 1)
        print(row, col, tile, x,y)

    else:
        moveForward = not moveForward
    if enemy1.colliderect(player):
        msg = "CHASE OVER"
        clock.schedule_unique(gameover,.1)

def move_enemy2():
    global move_enemy2_Forward
    global msg
    
    row = int(enemy2.y//TILE_SIZE)
    col = int(enemy2.x//TILE_SIZE)
    tile = tiles[maze[row][col]]
    if move_enemy2_Forward:
        row += 2
    else:
        row -= 2
    tile = tiles[maze[row][col]]
        
    if not tile == 'tree3':
        x = col*TILE_SIZE
        y = row * TILE_SIZE
        animate(enemy2,topleft = (x,y), duration = 1)
        print(row, col, tile, x,y)

    else:
        move_enemy2_Forward = not move_enemy2_Forward
    if enemy2.colliderect(player) or enemy1.colliderect(player):
        msg = "CHASE OVER"
        clock.schedule_unique(gameover,.1)

def update():
    move_enemy1()
    move_enemy2()


def gameover():
    global player_dead
    player.image = 'girl'
    player_dead = True

    

pgzrun.go()