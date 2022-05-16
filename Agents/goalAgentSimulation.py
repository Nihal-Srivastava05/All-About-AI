import random
import math
import pygame

def puzzle_generator(n):
    row_num = int(math.sqrt(n))
    num = 1
    puzzle = []
    for i in range(row_num):
        row = []
        for j in range(row_num):
            row.append(num)
            num += 1
        puzzle.append(row)
    
    puzzle[row_num-1][row_num-1] = 0
    rand_suffle = random.randint(n, n*n)
    x = row_num - 1
    y = row_num - 1
    for i in range(rand_suffle):
        possible_moves = [0, 1, 2, 3]
        if(x - 1 < 0):
            possible_moves.remove(0)
        if(x + 1 >= row_num):
            possible_moves.remove(1)
        if(y - 1 < 0):
            possible_moves.remove(2)
        if(y + 1 >= row_num):
            possible_moves.remove(3)
        rand_move = random.choice(possible_moves)
        if(rand_move == 0): #UP
            puzzle[x][y] = puzzle[x-1][y] 
            puzzle[x-1][y] = 0
            x -= 1
        elif(rand_move == 1): #Down
            puzzle[x][y] = puzzle[x+1][y] 
            puzzle[x+1][y] = 0
            x += 1
        elif(rand_move == 2): #Left
            puzzle[x][y] = puzzle[x][y-1] 
            puzzle[x][y-1] = 0
            y -= 1
        elif(rand_move == 3): #Right
            puzzle[x][y] = puzzle[x][y+1] 
            puzzle[x][y+1] = 0
            y += 1
    return (puzzle, (x, y))

class puzzle_env:
    def __init__(self, n=9, puzzle=None, start=None):
        self.n = n
        self.row_len = int(math.sqrt(self.n))
        if(puzzle):
            self.puzzle = puzzle
            self.start = start
        else:
            create_puzzle = puzzle_generator(n)
            self.puzzle = create_puzzle[0]
            self.start = create_puzzle[1]
    
    def print_puzzle(self):
        for i in range(self.row_len):
            for j in range(self.row_len):
                print(self.puzzle[i][j], end=" ")
            print()
    
    def draw_puzzle(self, display):
        dx = 0
        dy = 0
        number_font = pygame.font.SysFont( None, 42 )
        pygame.draw.rect(display, (0, 0, 0), pygame.Rect(0, 0, self.row_len*50, self.row_len*50), width=1)
        margin = 2
        for i in range(0, self.row_len):
            for j in range(0, self.row_len):
                if(self.puzzle[i][j]):
                    pygame.draw.rect(display, (0, 0, 0), pygame.Rect(dx*50, dy*50, 50, 50))
                    pygame.draw.rect(display, (255, 255, 255), pygame.Rect(dx*50, dy*50, 50-margin, 50-margin))
                    number_text  = str(self.puzzle[i][j])
                    number_image = number_font.render(number_text, True,  (0, 0, 0))
                    margin_x = ( 50-1 - number_image.get_rect().x ) // 2
                    margin_y = ( 50-1 - number_image.get_rect().y ) // 2
                    display.blit(number_image, (dx*50+2 + margin_x, dy*50+2 + margin_y ))
                else:
                    pygame.draw.rect(display, (0, 0, 0), pygame.Rect(dx*50, dy*50, 50, 50))
                dx = dx + 1
                if dx > self.row_len-1:
                    dx = 0 
                    dy = dy + 1
                pygame.time.wait(10)
    
    def get_correct_index(self, element):
        if(element == 0):
            x = self.row_len - 1
            y = self.row_len - 1
        else:   
            if(element % self.row_len == 0):
                x = element // (self.row_len+1)
                y = self.row_len - 1
            else:
                x = element // self.row_len
                y = (element % self.row_len) - 1
        return (x, y)
    
    def manhattan_dist(self, pos, element):
        idx, idy = self.get_correct_index(element)
        d = abs(pos[0] - idx) + abs(pos[1] - idy)
        return d
    
    def get_total_distance(self):
        total_dist = 0
        num_disp = 0
        for i in range(self.row_len):
            for j in range(self.row_len):
                if(self.get_correct_index(self.puzzle[i][j]) != (i, j)):
                    num_disp += 1
                total_dist += self.manhattan_dist((i, j), self.puzzle[i][j])
        return total_dist + num_disp
    
    def make_move(self, pos, move):
        x = pos[0]
        y = pos[1]
        if(move == 0): #UP
            self.puzzle[x][y] = self.puzzle[x-1][y] 
            self.puzzle[x-1][y] = 0
            x -= 1
        elif(move == 1): #Down
            self.puzzle[x][y] = self.puzzle[x+1][y] 
            self.puzzle[x+1][y] = 0
            x += 1
        elif(move == 2): #Left
            self.puzzle[x][y] = self.puzzle[x][y-1] 
            self.puzzle[x][y-1] = 0
            y -= 1
        elif(move == 3): #Right
            self.puzzle[x][y] = self.puzzle[x][y+1] 
            self.puzzle[x][y+1] = 0
            y += 1
        return (x, y)

class puzzle_solver:
    def __init__(self, start):
        self.x = start[0]
        self.y = start[1]
        self.prev_move = -1
        self.memory = []
        self.result = ''
    
    def move(self, env):
        if(env.get_total_distance() == 0):
            print("Solved the puzzle...")
            self.result = "Solved the puzzle..."
            return False
        if(len(self.memory) > 10):
            self.memory.pop(0)
        
        loop_check = 0
        for i in range(len(self.memory)):
            for j in range(i+1, len(self.memory)):
                if(self.memory[i] == self.memory[j]):
                    loop_count = 0
                    for k in range(4):
                        if((i+k < len(self.memory)) and (j+k < len(self.memory)) and (self.memory[i+k] == self.memory[j+k])):
                            loop_count += 1
                    if(loop_count == 4):
                        loop_check = 1
                        next_move = self.memory[i+1]
                        break
        
        if(env.get_total_distance() == 0):
            print("Solved the puzzle...")
            self.result = "Solved the puzzle..."
            return False
        elif(loop_check):
            possible_moves = [0, 1, 2, 3]
            if(self.x - 1 < 0):
                possible_moves.remove(0)
            if(self.x + 1 >= env.row_len):
                possible_moves.remove(1)
            if(self.y - 1 < 0):
                possible_moves.remove(2)
            if(self.y + 1 >= env.row_len):
                possible_moves.remove(3)
            if(next_move in possible_moves):
                possible_moves.remove(next_move)
            
            rand_move = random.choice(possible_moves)
            nx, ny = env.make_move((self.x, self.y), rand_move)
            self.x = nx
            self.y = ny
            self.prev_move = rand_move
            self.memory.append(rand_move)
            print("I moved: ", rand_move)
            return True
        else:
            possible_moves = [0, 1, 2, 3]
            if(self.x - 1 < 0):
                possible_moves.remove(0)
            if(self.x + 1 >= env.row_len):
                possible_moves.remove(1)
            if(self.y - 1 < 0):
                possible_moves.remove(2)
            if(self.y + 1 >= env.row_len):
                possible_moves.remove(3)
                
            if(self.prev_move != -1):
                if(self.prev_move == 0):
                    possible_moves.remove(1)
                elif(self.prev_move == 1):
                    possible_moves.remove(0)
                elif(self.prev_move == 2):
                    possible_moves.remove(3)
                elif(self.prev_move == 3):
                    possible_moves.remove(2)

            best_move = -1
            best_score = env.row_len * env.n
            for move in possible_moves:
                nx, ny = env.make_move((self.x, self.y), move)
                score = env.get_total_distance()
                if(score < best_score):
                    best_score = score
                    best_move = move
                if(move == 0):
                    oppo_move = 1
                elif(move == 1):
                    oppo_move = 0
                elif(move == 2):
                    oppo_move = 3
                elif(move == 3):
                    oppo_move = 2
                env.make_move((nx, ny), oppo_move)

            nx, ny = env.make_move((self.x, self.y), best_move)
            self.x = nx
            self.y = ny
            self.prev_move = best_move
            self.memory.append(best_move)
            print("I moved: ", best_move, "Current score: ", best_score)
            return True

class Simulation:
    windowHeight = 700
    windowWidth = 700

    def __init__(self, n=9, puzzle=None, start=None):
        self._running = True
        self._display_surf = None
        if(puzzle):
            self.puzzle = puzzle_env(n, puzzle, start)
        else:
            self.puzzle = puzzle_env(n)
        self.agent = puzzle_solver(self.puzzle.start)
    
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
        pygame.display.set_caption('Goal Agent - Sliding Tile Game')
        self._running = True
    
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
    
    def on_loop(self):
        pass
    
    def on_render(self):
        self._display_surf.fill((255, 255, 255))
        self.puzzle.draw_puzzle(self._display_surf)
        pygame.display.flip()
 
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        agent_final_status = True
        agent_stop = False
        while(self._running):
            pygame.event.pump()

            keys = pygame.key.get_pressed()
            if (keys[pygame.K_ESCAPE]):
                self._running = False

            if(not agent_stop):
                agent_stop = not self.agent.move(self.puzzle)
            else:
                result_font = pygame.font.Font('freesansbold.ttf', 16)
                result_text = result_font.render(self.agent.result, True, (0, 0, 0))
                result_text_rect = result_text.get_rect()
                result_text_rect.center = (self.windowWidth//2, self.windowHeight-25)
                self._display_surf.blit(result_text, result_text_rect)

                if(agent_final_status):
                    ticks = pygame.time.get_ticks()
                ticks_font = pygame.font.Font('freesansbold.ttf', 16)
                ticks_text = ticks_font.render("Time taken by the agent: {} milliseconds".format(ticks), True, (0, 0, 0))
                ticks_text_rect = ticks_text.get_rect()
                ticks_text_rect.center = (self.windowWidth//2, result_text_rect[1]-25)
                self._display_surf.blit(ticks_text, ticks_text_rect)
                agent_final_status = False
                pass

            for event in pygame.event.get():
                self.on_event(event)

            pygame.display.update()
            self.on_loop()
            self.on_render()
        self.on_cleanup()

if __name__ == "__main__" :
    simulation = Simulation(9) 
    simulation.on_execute()