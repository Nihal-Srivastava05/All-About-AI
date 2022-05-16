# For this we will use Prims Randomized Algo Reference: (https://medium.com/swlh/fun-with-python-1-maze-generator-931639b4fb7e)
# F = Free (empty cell), B = Blocked (wall)
import random

class MazeGenerator:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.maze = []
        self.wall = 'B'
        self.cell = 'F'
        self.unvisited = 'U'

    def printMaze(self, maze):
        for i in range(0, self.height):
            for j in range(0, self.width):
                print(str(maze[i][j]), end=" ")
            print('\n')

    # Find number of surrounding cells
    def surroundingCells(self, rand_wall):
        s_cells = 0
        if (self.maze[rand_wall[0]-1][rand_wall[1]] == 'F'):
            s_cells += 1
        if (self.maze[rand_wall[0]+1][rand_wall[1]] == 'F'):
            s_cells += 1
        if (self.maze[rand_wall[0]][rand_wall[1]-1] == 'F'):
            s_cells +=1
        if (self.maze[rand_wall[0]][rand_wall[1]+1] == 'F'):
            s_cells += 1

        return s_cells
    
    def generate_maze(self):
        for i in range(0, self.height):
            line = []
            for j in range(0, self.width):
                line.append(self.unvisited)
            self.maze.append(line)
        
        starting_height = int(random.random()*self.height)
        starting_width = int(random.random()*self.width)
        if (starting_height == 0):
            starting_height += 1
        if (starting_height == self.height-1):
            starting_height -= 1
        if (starting_width == 0):
            starting_width += 1
        if (starting_width == self.width-1):
            starting_width -= 1

        # Mark it as cell and add surrounding walls to the list
        self.maze[starting_height][starting_width] = self.cell
        walls = []
        walls.append([starting_height - 1, starting_width])
        walls.append([starting_height, starting_width - 1])
        walls.append([starting_height, starting_width + 1])
        walls.append([starting_height + 1, starting_width])

        # Denote walls in maze
        self.maze[starting_height-1][starting_width] = 'B'
        self.maze[starting_height][starting_width - 1] = 'B'
        self.maze[starting_height][starting_width + 1] = 'B'
        self.maze[starting_height + 1][starting_width] = 'B'

        while (walls):
            # Pick a random wall
            rand_wall = walls[int(random.random()*len(walls))-1]

            # Check if it is a left wall
            if (rand_wall[1] != 0):
                if (self.maze[rand_wall[0]][rand_wall[1]-1] == 'U' and self.maze[rand_wall[0]][rand_wall[1]+1] == 'F'):
                    # Find the number of surrounding cells
                    s_cells = self.surroundingCells(rand_wall)

                    if (s_cells < 2):
                        # Denote the new path
                        self.maze[rand_wall[0]][rand_wall[1]] = 'F'

                        # Mark the new walls
                        # Upper cell
                        if (rand_wall[0] != 0):
                            if (self.maze[rand_wall[0]-1][rand_wall[1]] != 'F'):
                                self.maze[rand_wall[0]-1][rand_wall[1]] = 'B'
                            if ([rand_wall[0]-1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0]-1, rand_wall[1]])


                        # Bottom cell
                        if (rand_wall[0] != self.height-1):
                            if (self.maze[rand_wall[0]+1][rand_wall[1]] != 'F'):
                                self.maze[rand_wall[0]+1][rand_wall[1]] = 'B'
                            if ([rand_wall[0]+1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0]+1, rand_wall[1]])

                        # Leftmost cell
                        if (rand_wall[1] != 0):	
                            if (self.maze[rand_wall[0]][rand_wall[1]-1] != 'F'):
                                self.maze[rand_wall[0]][rand_wall[1]-1] = 'B'
                            if ([rand_wall[0], rand_wall[1]-1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1]-1])


                    # Delete wall
                    for wall in walls:
                        if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                            walls.remove(wall)

                    continue

            # Check if it is an upper wall
            if (rand_wall[0] != 0):
                if (self.maze[rand_wall[0]-1][rand_wall[1]] == 'U' and self.maze[rand_wall[0]+1][rand_wall[1]] == 'F'):

                    s_cells = self.surroundingCells(rand_wall)
                    if (s_cells < 2):
                        # Denote the new path
                        self.maze[rand_wall[0]][rand_wall[1]] = 'F'

                        # Mark the new walls
                        # Upper cell
                        if (rand_wall[0] != 0):
                            if (self.maze[rand_wall[0]-1][rand_wall[1]] != 'F'):
                                self.maze[rand_wall[0]-1][rand_wall[1]] = 'B'
                            if ([rand_wall[0]-1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0]-1, rand_wall[1]])

                        # Leftmost cell
                        if (rand_wall[1] != 0):
                            if (self.maze[rand_wall[0]][rand_wall[1]-1] != 'F'):
                                self.maze[rand_wall[0]][rand_wall[1]-1] = 'B'
                            if ([rand_wall[0], rand_wall[1]-1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1]-1])

                        # Rightmost cell
                        if (rand_wall[1] != self.width-1):
                            if (self.maze[rand_wall[0]][rand_wall[1]+1] != 'F'):
                                self.maze[rand_wall[0]][rand_wall[1]+1] = 'B'
                            if ([rand_wall[0], rand_wall[1]+1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1]+1])

                    # Delete wall
                    for wall in walls:
                        if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                            walls.remove(wall)

                    continue

            # Check the bottom wall
            if (rand_wall[0] != self.height-1):
                if (self.maze[rand_wall[0]+1][rand_wall[1]] == 'U' and self.maze[rand_wall[0]-1][rand_wall[1]] == 'F'):

                    s_cells = self.surroundingCells(rand_wall)
                    if (s_cells < 2):
                        # Denote the new path
                        self.maze[rand_wall[0]][rand_wall[1]] = 'F'

                        # Mark the new walls
                        if (rand_wall[0] != self.height-1):
                            if (self.maze[rand_wall[0]+1][rand_wall[1]] != 'F'):
                                self.maze[rand_wall[0]+1][rand_wall[1]] = 'B'
                            if ([rand_wall[0]+1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0]+1, rand_wall[1]])
                        if (rand_wall[1] != 0):
                            if (self.maze[rand_wall[0]][rand_wall[1]-1] != 'F'):
                                self.maze[rand_wall[0]][rand_wall[1]-1] = 'B'
                            if ([rand_wall[0], rand_wall[1]-1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1]-1])
                        if (rand_wall[1] != self.width-1):
                            if (self.maze[rand_wall[0]][rand_wall[1]+1] != 'F'):
                                self.maze[rand_wall[0]][rand_wall[1]+1] = 'B'
                            if ([rand_wall[0], rand_wall[1]+1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1]+1])

                    # Delete wall
                    for wall in walls:
                        if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                            walls.remove(wall)
                    continue

            # Check the right wall
            if (rand_wall[1] != self.width-1):
                if (self.maze[rand_wall[0]][rand_wall[1]+1] == 'U' and self.maze[rand_wall[0]][rand_wall[1]-1] == 'F'):

                    s_cells = self.surroundingCells(rand_wall)
                    if (s_cells < 2):
                        # Denote the new path
                        self.maze[rand_wall[0]][rand_wall[1]] = 'F'

                        # Mark the new walls
                        if (rand_wall[1] != self.width-1):
                            if (self.maze[rand_wall[0]][rand_wall[1]+1] != 'F'):
                                self.maze[rand_wall[0]][rand_wall[1]+1] = 'B'
                            if ([rand_wall[0], rand_wall[1]+1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1]+1])
                        if (rand_wall[0] != self.height-1):
                            if (self.maze[rand_wall[0]+1][rand_wall[1]] != 'F'):
                                self.maze[rand_wall[0]+1][rand_wall[1]] = 'B'
                            if ([rand_wall[0]+1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0]+1, rand_wall[1]])
                        if (rand_wall[0] != 0):	
                            if (self.maze[rand_wall[0]-1][rand_wall[1]] != 'F'):
                                self.maze[rand_wall[0]-1][rand_wall[1]] = 'B'
                            if ([rand_wall[0]-1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0]-1, rand_wall[1]])

                    # Delete wall
                    for wall in walls:
                        if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                            walls.remove(wall)
                    continue

            # Delete the wall from the list anyway
            for wall in walls:
                if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                    walls.remove(wall)
        
        # Mark the remaining unvisited cells as walls
        for i in range(0, self.height):
            for j in range(0, self.width):
                if (self.maze[i][j] == 'U'):
                    self.maze[i][j] = 'B'

        # Set entrance and exit
        end_point = [self.height - 1, 0]
        start_point = [0, 0]
        for i in range(0, self.width):
            if (self.maze[1][i] == 'F'):
                self.maze[0][i] = 'F'
                start_point[1] = i
                break

        for i in range(self.width-1, 0, -1):
            if (self.maze[self.height-2][i] == 'F'):
                self.maze[self.height-1][i] = 'F'
                end_point[1] = i
                break

        return [self.maze, start_point, end_point]

if __name__ == "__main__":
    maze_generator = MazeGenerator(5, 5)
    cust_maze = maze_generator.generate_maze()
    print(cust_maze)
