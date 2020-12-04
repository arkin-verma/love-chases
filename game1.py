import pgzrun
TILE_SIZE = 64
# map with 10x10 grid
WIDTH = HEIGHT = TILE_SIZE * 10

tiles = ['straight', 'tree3', 'tree1', 'fairy']
maze = [
    [1,1,1,1,1,1,1,1,1,1],
    [1,0,1,0,0,0,0,0,0,1],
    [1,0,1,0,1,0,1,1,1,1],
    [1,0,0,0,1,0,1,1,1,1],
    [1,1,1,1,1,0,1,0,3,1],
    [1,1,0,0,0,0,0,0,1,1],
    [1,1,0,1,1,1,1,1,1,1],
    [1,1,0,1,0,0,0,0,0,1],
    [1,1,0,0,0,1,0,1,1,1],
    [1,1,1,1,1,1,2,1,1,1],
]

player = Actor('boy2', topleft = (1*TILE_SIZE,1*TILE_SIZE))
enemy1 = Actor('girl', topleft = (2* TILE_SIZE, 5* TILE_SIZE))
moveForward = True
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
    try:
        tile = tiles[maze[row][col]]
        if tile == 'straight' and not player_dead:
            move_player(row,col)
        if tile == 'fairy':
            unlock += 1 
            maze[row][col] = 0
            move_player(row,col)
        if tile == 'tree1' and unlock > 0:
            msg = 'Demetrius has escaped...for now.'
            move_player(row,col)
            sounds.collision.play()
    except:
        pass

def move_player(row,col):
    x = col*TILE_SIZE
    y = row*TILE_SIZE
    animate(player,topleft = (x,y), duration=.2)

def update():
    global moveForward
    global msg
    row = int(enemy1.y//TILE_SIZE)
    col = int(enemy1.x//TILE_SIZE)
    if moveForward:
        col += 1
    else:
        col -= 1
    tile = tiles[maze[row][col]]
    if not tile == 'tree3':
        x = col*TILE_SIZE
        y = row * TILE_SIZE
        animate(enemy1,topleft = (x,y), duration = .3)
    else:
        moveForward = not moveForward
    if enemy1.colliderect(player):
        msg = "CHASE OVER"
        clock.schedule_unique(gameover,.1)

def gameover():
    global player_dead
    player.image = 'boy2'
    player_dead = True

    

pgzrun.go()

# pyinstaller --windowed --onefile game1.spec
# WAP to make game to get all fruit, avoid two enemies, and get to the goal