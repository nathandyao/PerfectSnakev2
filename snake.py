"""
Snake Eater
Made with PyGame
"""

import pygame, sys, time, random, copy

#############################################################################################################################
##########################################            NEW           #########################################################
#############################################################################################################################

#CREAT A TREE WITH THE GRID

def pathfinder():
    global incc
    global snake_body
    global auto_mode
    global fakebodys
    global timer
    colm,rowz = snake_pos
    pl = (rowz,colm)
    colm = int(colm/10)+1
    rowz = int(rowz/10)+1
    #print(f"col:{colm},row:{rowz}")
    temp = (leading[rowz,colm][0] - rowz,leading[rowz,colm][1] - colm)
    tailpos = (int(snake_body[-1][1]/10)+1,int(snake_body[-1][0]/10)+1)
    #print((f"head:{pl}"))
    #print(f"food:{food_pos}")
    tempbody = copy.deepcopy(snake_body)
    if score > int(rows*cols*4*0.4) and auto_mode != fakebodys:
      auto_mode = fakebodys
      for i in range(fakebodys):
        snake_body.pop()
      print("AUTOMODE")
    #print(timer)
    if timer == 0 and not incc and auto_mode !=1 and next_step(pl,snake_body,tailpos,direction,[]):
      '''print("FOUND")
      print((f"head:{pl}"))
      print(f"food:{food_pos}")
      print(true_sim_sol)'''
      timer = int(score+4)
      incc = True
    snake_body = tempbody
    #print(true_sim_sol)
    if incc:
      if len(true_sim_sol) !=0:
        #print(true_sim_sol)
        placehold = true_sim_sol.pop(0)
        '''print(placehold)
        print("PATH FOUND")'''
        return placehold
    if timer > 0:
      timer -= 1
    incc = False
    if temp == (0, 1):
      return('RIGHT')
    if temp == (1, 0):
        return('DOWN')
    if temp == (0, -1):
        return('LEFT')
    if temp ==  (-1, 0):
        return('UP')
        
    #print(leading[rowz,colm])
    
def next_step(sim_pos,sim_body,tailpos,directions,sim_sol):
  if sim_pos in sim_gone2:
    return False
  sim_gone2.add(sim_pos)
  rl_row = sim_pos[0]
  rl_col = sim_pos[1]
  #print(sim_pos)
  #print(food_pos)
  col = int(rl_col/10)+1
  row = int(rl_row/10)+1
  if sim_pos[0] == food_pos[1] and sim_pos[1] == food_pos[0]:
    for i in sim_body:
      deb_col = int(i[0]/10)+1
      dub_row = int(i[1]/10)+1
      #print(f"sim_body:{dub_row},{deb_col} | sim_weight: {order[dub_row,deb_col]}")
    for i in sim_sol:
      true_sim_sol.append(i)
    #print(len(true_sim_sol))
    return True
  lrsim_body = sim_body
  udsim_body = sim_body
  rcheck = False
  lcheck = False
  ucheck = False
  dcheck = False
  if food_pos[0] > rl_col and directions != 'LEFT' and [rl_col+10,rl_row] not in sim_body and col != cols*2:
      if notbetween(order[tailpos],order[(row,col)],order[(row,col+1)]):
          directions = "RIGHT"
          #print("RIGHT")
          sim_sol.append("RIGHT")
          
          lrsim_body.insert(0, [sim_pos[1],sim_pos[0]])
          lrsim_body.pop()
          sim_tailph = (int(lrsim_body[-1][1]/10)+1,int(lrsim_body[-1][0]/10)+1)
          
          rcheck = next_step((rl_row,rl_col+10),lrsim_body,sim_tailph,directions,sim_sol)
          sim_sol.pop()
          
  elif food_pos[0] < rl_col and directions != 'RIGHT' and [rl_col-10,rl_row]  not in sim_body and col!=1:
      if notbetween(order[tailpos],order[(row,col)],order[(row,col-1)]):
          directions = "LEFT"
          #print("LEFT")
          sim_sol.append("LEFT")
          
          lrsim_body.insert(0, [sim_pos[1],sim_pos[0]])
          lrsim_body.pop()
          sim_tailph = (int(lrsim_body[-1][1]/10)+1,int(lrsim_body[-1][0]/10)+1)
          
          lcheck = next_step((rl_row,rl_col-10),lrsim_body,sim_tailph,directions,sim_sol)
          sim_sol.pop()
  if rcheck or lcheck:
    return True
  if food_pos[1] < rl_row and directions != 'DOWN' and [rl_col,rl_row-10] not in sim_body and row!=1:
      if notbetween(order[tailpos],order[(row,col)],order[(row-1,col)]):
          directions = "UP"
          #print("UP")
          sim_sol.append("UP")
          
          udsim_body.insert(0, [sim_pos[1],sim_pos[0]])
          udsim_body.pop()
          sim_tailph = (int(udsim_body[-1][1]/10)+1,int(udsim_body[-1][0]/10)+1)
          
          ucheck = next_step((rl_row-10,rl_col),udsim_body,sim_tailph,directions,sim_sol)
          sim_sol.pop()
  elif food_pos[1] > rl_row and directions != 'UP' and [rl_col,rl_row+10]  not in sim_body and row!=rows*2:
      if notbetween(order[tailpos],order[(row,col)],order[(row+1,col)]):
          directions = "DOWN"
          #print("DOWN")
          sim_sol.append("DOWN")
          
          udsim_body.insert(0, [sim_pos[1],sim_pos[0]])
          udsim_body.pop()
          sim_tailph = (int(udsim_body[-1][1]/10)+1,int(udsim_body[-1][0]/10)+1)
          
          dcheck = next_step((rl_row+10,rl_col),udsim_body,sim_tailph,directions,sim_sol)
          sim_sol.pop()
          
  if ucheck or dcheck:
    return True
  return False

def notbetween(tail,head,number):
   #print(f"tail:{tail},head:{head},number:{number}")
    if head - tail > 1:
        return number < tail or number > head
    else: 
        if (number < tail and number > head):
            return True
        return False
        
def create ():
  visited = set()
  que = [(1, 1)]
  edges = {}
  for i in range(1,rows+1):
    for j in range(1,cols+1):
      edges[(i, j)] = []
  visited.add((1,1))
  #print(edges[(1,1)])
  while que:
      row, col = que.pop(0)
      #print(que)
      #print(visited)
      for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        new_row = row + dr
        new_col = col + dc
        if 1 <= new_row <= rows and 1 <= new_col <= cols:
          if (new_row, new_col) in visited:
            continue
          if (dr,dc) == (0,1):
            edges[(row,col)].append("R")
            edges[(new_row,new_col)].append("L")
          elif (dr,dc) == (0,-1):
            edges[(row,col)].append("L")
            edges[(new_row,new_col)].append("R")
          elif (dr,dc) == (1,0):
            edges[(row,col)].append("D")
            edges[(new_row,new_col)].append("U")
          elif (dr,dc) == (-1,0):
            edges[(row,col)].append("U")
            edges[(new_row,new_col)].append("D")
          visited.add((new_row,new_col))
          que.insert(random.randint(0, len(que)),(new_row,new_col))
          # random.randint(0, len(que))
  return edges

# DECODE
def botline(row1,col1):
  # draw line below
  maze[(row1,col1)].append((row1,col1-1))
  maze[(row1,col1)].append((row1,col1+1))
  maze[(row1,col1-1)].append((row1,col1))
  maze[(row1,col1-1)].append((row1,col1-2))
  
def topline(row1,col1):
  # draw line above
  maze[(row1-1,col1)].append((row1-1,col1-1))
  maze[(row1-1,col1)].append((row1-1,col1+1))
  maze[(row1-1,col1-1)].append((row1-1,col1))
  maze[(row1-1,col1-1)].append((row1-1,col1-2))

def rightline(row1, col1):
  # draw line right
  maze[(row1, col1)].append((row1 - 1, col1))
  maze[(row1, col1)].append((row1 + 1, col1))
  maze[(row1 - 1, col1)].append((row1, col1))
  maze[(row1 - 1, col1)].append((row1 - 2, col1))
  
def leftline(row1, col1):
  # draw line left
  maze[(row1, col1 - 1)].append((row1 - 1, col1- 1))
  maze[(row1, col1 - 1)].append((row1 + 1, col1 - 1))
  maze[(row1 - 1, col1 - 1)].append((row1, col1 - 1))
  maze[(row1 - 1, col1 - 1)].append((row1 - 2, col1 - 1))
  
def topleft(row1, col1):
  maze[(row1 - 1, col1 - 1)].append((row1 - 2, col1 - 1))
  maze[(row1 - 1, col1 - 1)].append((row1 - 1, col1 - 2))

def botright(row1, col1):
  maze[(row1, col1)].append((row1 + 1, col1))
  maze[(row1, col1)].append((row1, col1 + 1))

def topright(row1, col1):
  maze[(row1 - 1, col1)].append((row1 - 2, col1))
  maze[(row1 - 1, col1)].append((row1 - 1, col1 + 1))

def botleft(row1, col1):
  maze[(row1, col1 - 1)].append((row1, col1 - 2))
  maze[(row1, col1 - 1)].append((row1 + 1, col1-1))
  
def decode ():
  for row in range(1,rows+1):
    for col in range(1,cols+1):
      row1 = row*2
      col1 = col*2
      '''
      ul = (row*2-1,col*2-1)
      dl = (row*2,col*2-1)
      ur = (row*2-1,col*2)
      dr = (row*2,col*2)'''
      rn = edges[(row,col)]

      if "R" in rn and "L" in rn and "U" in rn and "D" in rn:
        topleft(row1,col1)
        botleft(row1,col1)
        topright(row1,col1)
        botright(row1,col1)
      #3s
      elif "R" in rn and "L" in rn and "U" in rn:
        topright(row1,col1)
        topleft(row1,col1)
        botline(row1,col1)
      elif "L" in rn and "U" in rn and "D" in rn:
        topleft(row1,col1)
        botleft(row1,col1)
        rightline(row1,col1)
      elif "R" in rn and "U" in rn and "D" in rn:
        leftline(row1,col1)
        topright(row1,col1)
        botright(row1,col1)
      elif "L" in rn and "R" in rn and "D" in rn:
        topline(row1,col1)
        botleft(row1,col1)
        botright(row1,col1)
      #2s
      elif "R" in rn and "L" in rn:
        botline(row1,col1)
        topline(row1,col1)
        
      elif "R" in rn and "U" in rn:
        #left L
        maze[(row1, col1 - 1)].append((row1 - 1, col1- 1))
        maze[(row1 - 1, col1 - 1)].append((row1, col1 - 1))
        maze[(row1 - 1, col1 - 1)].append((row1 - 2, col1 - 1))
        #bot L
        maze[(row1,col1)].append((row1,col1-1))
        maze[(row1,col1)].append((row1,col1+1))
        maze[(row1,col1-1)].append((row1,col1))
        
        topright(row1,col1)
      elif "R" in rn and "D" in rn:
        #left L
        maze[(row1, col1 - 1)].append((row1 - 1, col1- 1))
        maze[(row1, col1 - 1)].append((row1 + 1, col1 - 1))
        maze[(row1 - 1, col1 - 1)].append((row1, col1 - 1))
        #top L
        maze[(row1-1,col1)].append((row1-1,col1-1))
        maze[(row1-1,col1)].append((row1-1,col1+1))
        maze[(row1-1,col1-1)].append((row1-1,col1))
        botright(row1,col1)

      elif "L" in rn and "U" in rn:
        # bot L
        maze[(row1,col1)].append((row1,col1-1))
        maze[(row1,col1-1)].append((row1,col1))
        maze[(row1,col1-1)].append((row1,col1-2))
        # right L
        maze[(row1, col1)].append((row1 - 1, col1))
        maze[(row1 - 1, col1)].append((row1, col1))
        maze[(row1 - 1, col1)].append((row1 - 2, col1))
        topleft(row1,col1)
      elif "L" in rn and "D" in rn:
        # top L
        maze[(row1-1,col1)].append((row1-1,col1-1))
        maze[(row1-1,col1-1)].append((row1-1,col1))
        maze[(row1-1,col1-1)].append((row1-1,col1-2))

        # right L
        maze[(row1, col1)].append((row1 - 1, col1))
        maze[(row1, col1)].append((row1 + 1, col1))
        maze[(row1 - 1, col1)].append((row1, col1))
        botleft(row1,col1)
      elif "U" in rn and "D" in rn:
        leftline(row1,col1)
        rightline(row1,col1)
      #1s
      elif "R" in rn:
        #left L
        maze[(row1, col1 - 1)].append((row1 - 1, col1- 1))
        maze[(row1 - 1, col1 - 1)].append((row1, col1 - 1))
        #top L
        maze[(row1-1,col1)].append((row1-1,col1-1))
        maze[(row1-1,col1)].append((row1-1,col1+1))
        maze[(row1-1,col1-1)].append((row1-1,col1))
        #bot L
        maze[(row1,col1)].append((row1,col1-1))
        maze[(row1,col1)].append((row1,col1+1))
        maze[(row1,col1-1)].append((row1,col1))
      elif "L" in rn:
        # top L
        maze[(row1-1,col1)].append((row1-1,col1-1))
        maze[(row1-1,col1-1)].append((row1-1,col1))
        maze[(row1-1,col1-1)].append((row1-1,col1-2))
        # right L
        maze[(row1, col1)].append((row1 - 1, col1))
        maze[(row1 - 1, col1)].append((row1, col1))
        #bot L
        maze[(row1,col1)].append((row1,col1-1))
        maze[(row1,col1-1)].append((row1,col1))
        maze[(row1,col1-1)].append((row1,col1-2))
      elif "U" in rn:
        # bot L
        maze[(row1,col1)].append((row1,col1-1))
        maze[(row1,col1-1)].append((row1,col1))
        # right L
        maze[(row1, col1)].append((row1 - 1, col1))
        maze[(row1 - 1, col1)].append((row1, col1))
        maze[(row1 - 1, col1)].append((row1 - 2, col1))
        #left L
        maze[(row1, col1 - 1)].append((row1 - 1, col1- 1))
        maze[(row1 - 1, col1 - 1)].append((row1, col1 - 1))
        maze[(row1 - 1, col1 - 1)].append((row1 - 2, col1 - 1))
      elif "D" in rn:
        # top L
        maze[(row1-1,col1)].append((row1-1,col1-1))
        maze[(row1-1,col1-1)].append((row1-1,col1))

        # right L
        maze[(row1, col1)].append((row1 - 1, col1))
        maze[(row1, col1)].append((row1 + 1, col1))
        maze[(row1 - 1, col1)].append((row1, col1))
        
        #left L
        maze[(row1, col1 - 1)].append((row1 - 1, col1- 1))
        maze[(row1, col1 - 1)].append((row1 + 1, col1 - 1))
        maze[(row1 - 1, col1 - 1)].append((row1, col1 - 1))
      
      
def turn2path ():
  pather = []
  fakeque = [(1,1)]
  fakevisited = set()
  while fakeque:
    #print(fakeque)
    pl = fakeque.pop(0)
    if pl in fakevisited:
      continue
    fakevisited.add(pl)
    pather.append(pl)
    for i in maze[(pl)]:
      fakeque.insert(0,i)
  return pather


#############################################################################################################################
##########################################            NEW           #########################################################
#############################################################################################################################

# Difficulty settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120
difficulty = 4800
#WOOT WOOT
# Window size
frame_size_x = 420
frame_size_y = 420

#NEW
fakebodys = 0
#NEW

# Checks for errors encountered
check_errors = pygame.init()
# pygame.init() example output -> (6, 0)
# second number in tuple gives number of errors
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')


# Initialise game window
pygame.display.set_caption('Snake Eater')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))


# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)


# FPS (frames per second) controller
fps_controller = pygame.time.Clock()


# Game variables
snake_pos = [200, 200]
snake_body = []
for i in range(3+fakebodys):
  snake_body.append([50-10*fakebodys,300])

food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
food_spawn = True

direction = 'RIGHT'
change_to = direction

score = 0


# Game Over
def game_over():
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('YOU DIED', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x/2, frame_size_y/4)
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, red, 'times', 20)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()


# Score
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x/10, 15)
    else:
        score_rect.midtop = (frame_size_x/2, frame_size_y/1.25)
    game_window.blit(score_surface, score_rect)
    # pygame.display.flip()
    
    
##NEW##
rows = int((frame_size_x)/20)
cols = int((frame_size_x)/20)
rows, cols = rows, cols
maze = {}
for i in range(1,(rows)*2+1):
  for j in range(1,(cols)*2+1):
    maze[(i, j)] = []
edges = create()
decode()
path = turn2path()
#print(path)
leading = {}
order = {}
for i in range(len(path)-1):
    leading[path[i]] = path[i+1]
    order[path[i]] = i
leading[path[-1]] = path[0]
order[path[-1]]  = len(path) -1
incc = False
isAuto = True
true_sim_sol = []
auto_mode = 0
##NEW################################################################################################################################
# Main logic
#print(leading)
print(order)
timer = 0
while True:
    # print((f"head:{snake_pos}"))
    # print(f"food:{food_pos}")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Whenever a key is pressed down
        elif event.type == pygame.KEYDOWN:
            # W -> Up; S -> Down; A -> Left; D -> Right
            if event.key == ord('p'):
                print(f"plus:{difficulty}")
                difficulty += 100
            if event.key == ord('m'):
                print(f"min:{difficulty}")
                difficulty -= 100
            else:
                if event.key == pygame.K_UP or event.key == ord('w'):
                    change_to = 'UP'
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    change_to = 'RIGHT'
                # Esc -> Create event to quit the game
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    # Making sure the snake cannot move in the opposite direction instantaneously
    if isAuto:
        sim_gone2 = set()
        change_to = pathfinder()
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Moving the snake
    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10

    # Snake body growing mechanism
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    # Spawning food on the screen
    if not food_spawn:
      foodchecker = True
      while foodchecker:
        food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
        if (food_pos not in snake_body[:len(snake_body)-fakebodys]):
          foodchecker = False
    food_spawn = True

    # GFX
    game_window.fill(black)
    snake_color = pygame.Color(1, 1, 1)
    
    for pos in range(len(snake_body)-fakebodys+auto_mode):
        snake_color = pygame.Color((pos)%255, (pos*10)%255, (pos*100)%255)
        # Snake body
        # .draw.rect(play_surface, color, xy-coordinate)
        # xy-coordinate -> .Rect(x, y, size_x, size_y)
        if pos == 1:
          pygame.draw.rect(game_window, green, pygame.Rect(snake_body[pos][0], snake_body[pos][1], 10, 10))
        elif pos%2 == 1:
          pygame.draw.rect(game_window, snake_color, pygame.Rect(snake_body[pos][0], snake_body[pos][1], 10, 10))
        else: 
          pygame.draw.rect(game_window, snake_color, pygame.Rect(snake_body[pos][0], snake_body[pos][1], 10, 10))
    # Snake food
    pygame.draw.rect(game_window, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    # Game Over conditions
    # Getting out of bounds
    if snake_pos[0] < 0 or snake_pos[0] > frame_size_x-10:
        print(f"pos:{snake_pos}")
        print(f"dir:{direction}")
        print("sin1")
        game_over()
    if snake_pos[1] < 0 or snake_pos[1] > frame_size_y-10:
        print(f"pos:{snake_pos}")
        print(f"dir:{direction}")
        print("sin2")
        game_over()
    # Touching the snake body
    for block in snake_body[1:len(snake_body)-fakebodys+auto_mode]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
          print(f"pos:{snake_pos}")
          print(f"dir:{direction}")
          print(f"boday:{snake_body}")
          for i in snake_body:
            deb_col = int(i[0]/10)+1
            dub_row = int(i[1]/10)+1
            print(f"body:{dub_row},{deb_col}| weight: {order[dub_row,deb_col]}")
          print("sin3")
          game_over()

    show_score(1, white, 'consolas', 20)
    # Refresh game screen
    '''for i in snake_body:
      deb_col = int(i[0]/10)+1
      dub_row = int(i[1]/10)+1
      print(f"body:{dub_row},{deb_col}| weight: {order[dub_row,deb_col]}")'''
    pygame.display.update()
    # Refresh rate
    fps_controller.tick(difficulty)
    

