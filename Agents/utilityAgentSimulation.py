import random
import pygame

class room_environment:
    def __init__(self, n, m, room=None, dirt=None):
        self.m = m
        self.n = n
        self.room = []
        self.num_dirt = 0
        if(room == None):
            for i in range(self.n):
                row = []
                for j in range(self.m):
                    row.append(0)
                self.room.append(row)
                
            num_walls = random.choice([random.randint(self.n//2, self.n-1), random.randint(self.m//2, self.m-1)])
            for i in range(num_walls):
                wall_x = random.randint(0, self.m-1)
                wall_y = random.randint(0, self.n-1)
                self.room[wall_x][wall_y] = -1
                
            num_dirt = random.choice([random.randint(1, self.n//2), random.randint(1, self.m//2)])
            self.num_dirt = num_dirt
            for i in range(num_dirt):
                dirt_x = random.randint(0, self.m-1)
                dirt_y = random.randint(0, self.n-1)
                self.room[dirt_x][dirt_y] = 1
        else:
            self.room = room
            self.num_dirt = dirt
    
    def draw_room(self, display):
        dx = 0
        dy = 0
        pygame.draw.rect(display, (0, 0, 0), pygame.Rect(0, 0, self.m*50, self.n*50), width=1)
        for i in range(0, self.m):
            for j in range(0, self.n):
                if(self.room[i][j] == -1):
                    pygame.draw.rect(display, (0, 0, 0), pygame.Rect(dx*50, dy*50, 50, 50))
                elif(self.room[i][j] == 1):
                    pygame.draw.rect(display, (185, 122, 87), pygame.Rect(dx*50, dy*50, 50, 50))
                dx = dx + 1
                if dx > self.m-1:
                    dx = 0 
                    dy = dy + 1
    
    def get_state(self, pos):
        if(pos[0] >= self.m or pos[0] < 0 or pos[1] >= self.n or pos[1] < 0):
            return -1
        return self.room[pos[1]][pos[0]]
    
    def pickup_dirt(self, pos):
        if(self.room[pos[1]][pos[0]] == 1):
            self.room[pos[1]][pos[0]] = 0
    
    def dirt_count(self):
        return self.num_dirt
    
    def print_room(self):
        for i in range(self.n):
            for j in range(self.m):
                print(self.room[i][j], end=' ')
            print()

class cleaner_agent:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.limit = 0
        self.dirt_collected = 0
        self.prev_move = -1
        self.result = ''

    def draw(self, display):
        draw_x = self.x
        draw_y = self.y
        pygame.draw.rect(display, (255, 0, 0), pygame.Rect(draw_x*50, draw_y*50, 50, 50))
        pygame.time.wait(100)
    
    def get_surroundings(self, x, y, room):          
        surroundings = [room.get_state([x+1, y]),
                        room.get_state([x, y+1]),
                        room.get_state([x-1, y]),
                        room.get_state([x, y-1])]
        return surroundings
    
    def make_move(self, direction, room):
        if(direction == 0):
            if(self.x < room.m and (room.get_state([self.x+1, self.y]) != -1)):
                self.x += 1
        elif(direction == 1):
            if(self.y < room.n and (room.get_state([self.x, self.y+1]) != -1)):
                self.y += 1
        elif(direction == 2):
            if(self.x > 0 and (room.get_state([self.x-1, self.y]) != -1)):
                self.x -= 1
        else:
            if(self.y > 0 and (room.get_state([self.x, self.y-1]) != -1)):
                self.y -= 1
            
    def get_pos(self):
        print("I am at:", self.x, self.y, " and picked up: ", self.dirt_collected, " dirt.")
    
    def move(self, room):
        if(self.limit >= room.m*room.n):
            print("Used all the moves, limit reached...")
            self.result = "Used all the moves, limit reached..."
            return False
        elif(self.dirt_collected == room.dirt_count()):
            print("Collected All the Dirst, Job Done...")
            self.result = "Collected All the Dirst, Job Done..."
            return False
        else:
            surroundings = self.get_surroundings(self.x, self.y, room)
            dirt_around = []
            for i in range(len(surroundings)):
                if surroundings[i] == 1:
                    dirt_around.append(i)
            if(dirt_around):
                rand_move = random.choice(dirt_around)
                self.make_move(rand_move, room)
                room.pickup_dirt([self.x, self.y])
                self.limit -= room.n
                self.prev_move = rand_move
                self.dirt_collected += 1
                self.limit += 1
                return True
            else:
                possible_scores = [0, 0, 0, 0]
                for i in range(self.x+1, room.m):
                    if(room.get_state([i, self.y]) == 1):
                        possible_scores[0] += 1
                    elif(room.get_state([i, self.y]) == -1):
                        break
                for j in range(self.y+1, room.n):
                    if(room.get_state([self.x, j]) == 1):
                        possible_scores[1] += 1
                    elif(room.get_state([self.x, j]) == -1):
                        break
                for i in range(self.x-1, -1, -1):
                    if(room.get_state([i, self.y]) == 1):
                        possible_scores[2] += 1
                    elif(room.get_state([i, self.y]) == -1):
                        break
                for j in range(self.y-1, -1, -1):
                    if(room.get_state([self.x, j]) == 1):
                        possible_scores[3] += 1
                    elif(room.get_state([self.x, j]) == -1):
                        break

                if(max(possible_scores) == 0):
                    moves = [0, 1, 2, 3]
                    if(self.prev_move == 0):
                        moves.remove(2)
                    elif(self.prev_move == 1):
                        moves.remove(3)
                    elif(self.prev_move == 2):
                        moves.remove(0)
                    elif(self.prev_move == 3):
                        moves.remove(1)
                    best_move = random.choice(moves)
                else:
                    best_move = possible_scores.index(max(possible_scores))
                self.make_move(best_move, room)
                self.prev_move = best_move
                self.limit += 1
                return True

class Simulation:
    windowHeight = 700
    windowWidth = 700

    def __init__(self, n, m, room=None, dirt=None):
        self._running = True
        self._display_surf = None
        self.room = room_environment(n, m, room, dirt)
        self.agent = cleaner_agent()
    
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
        pygame.display.set_caption('Utility Agent - Vaccume Cleaner')
        self._running = True
    
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
    
    def on_loop(self):
        pass
    
    def on_render(self):
        self._display_surf.fill((255, 255, 255))
        self.room.draw_room(self._display_surf)
        self.agent.draw(self._display_surf)
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
                agent_stop = not self.agent.move(self.room)
                self.agent.get_pos()
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
    simulation = Simulation(9, 9) 
    simulation.on_execute()