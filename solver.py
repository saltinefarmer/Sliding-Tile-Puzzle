"""
    Solver provides a function to solve a sliding tile puzzle.

"""

__author__ = "Silver Lippert"
__version__ = "24.9.18"

import heapq


def solve(puzzle: list) -> list:
    """
        Solve function accepts a 2D list as input. The list must
        contain the values of a sliding tile puzzle, with the
        empty space represented as a 0. It will solve the tile
        puzzle, and return a list of the fewest moves required to
        make in order to solve the puzzle.

    """
    closed = set()
    open = []
    # add starting puzzle to open list

    if not __is_solvable(puzzle):
        return None

    entry = State(puzzle, 0, __calc_heuristic(puzzle), [])

    # sort by the heuristic, moves_made serves as a tie breaker to favor heuristics that are further along
    # as those heuristics are more likely to be more accurate
    heapq.heappush(open, (entry.total_heuristic, -(entry.moves_made), entry))

    # iter = 0
    while True:
    
        # current puzzle
        entry = heapq.heappop(open)
                
        
        if entry[2] in closed:
            continue
        closed.add(entry[2])

        # check if this puzzle is the solution
        if entry[2].moves_made == entry[0]:
            break

        # check all possible moves by finding the 0 in the 2D list
        __find_zero(entry[2], open, closed)
        
        # iter += 1

    # print(iter) # for bug testing
    return entry[2].steps_taken

# this function finds the 0 in the puzzle, and then creates new puzzle
# states based on the possible moves from that position
def __find_zero(entry, open: list, closed: set):

    i, j = 0, 0
    while i < len(entry.puzzle): # outer loop of puzzle (height)
        while j < len(entry.puzzle[0]): # inner loop of the puzzle (width)

            if entry.puzzle[i][j] == 0: # if 0 has been found
                # creating a new state with each of the moves made
                if j > 0: # if the 0 is not against the left-hand wall
                    # that means it can make a move by sliding the left tile to the right
                    moved_puz = [list(x[:]) for x in entry.puzzle] # make a copy so no aliasing occurs
                    moved_puz[i][j], moved_puz[i][j-1] = moved_puz[i][j-1], moved_puz[i][j]
                    steps = entry.steps_taken.copy()
                    steps.append('R')
                    temp = State(moved_puz, entry.moves_made + 1, __calc_heuristic(moved_puz), steps)
                    # check if temp is in closed list
                    if temp not in closed:
                        heapq.heappush(open, (temp.total_heuristic, -(temp.moves_made), temp))

                if j < len(entry.puzzle[i]) -1: # if the 0 is not against the right hand wall
                    # that means it can make a move by sliding the right tile to the left
                    moved_puz = [list(x[:]) for x in entry.puzzle]
                    moved_puz[i][j], moved_puz[i][j+1] = moved_puz[i][j+1], moved_puz[i][j]
                    steps = entry.steps_taken.copy()
                    steps.append('L')
                    temp = State(moved_puz, entry.moves_made + 1, __calc_heuristic(moved_puz), steps)
                    # check if temp is in closed list
                    if temp not in closed:
                        heapq.heappush(open, (temp.total_heuristic, -(temp.moves_made), temp))

                if i > 0: # if 0 is not in the top row
                    # that means a move can be made by pushing the top tile down
                    moved_puz = [list(x[:]) for x in entry.puzzle]
                    moved_puz[i][j], moved_puz[i-1][j] = moved_puz[i-1][j], moved_puz[i][j]
                    steps = entry.steps_taken.copy()
                    steps.append('D')
                    temp = State(moved_puz, entry.moves_made + 1, __calc_heuristic(moved_puz), steps)
                    # check if temp is in closed list
                    if temp not in closed:
                        heapq.heappush(open, (temp.total_heuristic, -(temp.moves_made), temp))

                if i < len(entry.puzzle) - 1: # if 0 is not in the bottom row
                    # that means a move can be made by pushing the bottom tile up
                    moved_puz = [list(x[:]) for x in entry.puzzle]
                    moved_puz[i][j], moved_puz[i+1][j] = moved_puz[i+1][j], moved_puz[i][j]
                    steps = entry.steps_taken.copy()
                    steps.append('U')
                    temp = State(moved_puz, entry.moves_made + 1, __calc_heuristic(moved_puz), steps)
                    # check if temp is in closed list
                    if temp not in closed:
                        heapq.heappush(open, (temp.total_heuristic, -(temp.moves_made), temp))
                j += 1

                break
            j += 1
            
        if entry.puzzle[i][j - 1] == 0:
            break
        i += 1
        j = 0


# this function test a puzzle to see if it is solvable. 
# Returns a bool indicating as such
def __is_solvable(puzzle: list) -> bool:

    two_d_list = []
    i, j, gap = 0, 0, 0

    # flatten puzzle into 1D list
    while i < len(puzzle):
        while j < len(puzzle[i]):
            if puzzle[i][j] == 0: # if this square is the gap
                gap = len(puzzle) - 1 - i # distance from bottom to current height
                j += 1
                continue
            two_d_list.append(puzzle[i][j])
            j += 1
        i += 1
        j = 0

    # count inversions
    inversions, i, j = 0, 0, 0
    while i < len(two_d_list):
        while j < len(two_d_list):
            if two_d_list[j] < two_d_list[i]:
                inversions += 1
            j += 1
        i += 1
        j = i + 1

    
    if len(puzzle[0]) % 2 == 1: # if width is odd
        if inversions % 2 == 0: # and inversions is even
            return True # solvable
        else:
            return False
    else: # width is even
        if (inversions + gap) % 2 == 0: # add inversion to gap
            return True
        else:
            return False

    
# this function calculates the manhattan distance of each tile
def __calc_heuristic(current_puzzle: list) -> int:
    # set up variables
    total_moves, i, j, goal_i, goal_j, num = 0, 0, 0, 0, 0, 0

    # iterate through each item in the puzzle
    while i < len(current_puzzle):
        while j < len(current_puzzle[i]):

            if current_puzzle[i][j] == 0: # doesn't have a manhattan distance
                j += 1
                continue

            num = current_puzzle[i][j]

            # calculate goal row and column of the tile in question
            goal_j = (num -1) % len(current_puzzle[i])
            goal_i = int((num -1) / len(current_puzzle[i]))

            # add moves required to get to its destination
            total_moves += abs(i - goal_i) + abs(j - goal_j)
            j += 1
        i += 1
        j = 0
    
    # in case of emergency, comment out the following line
    total_moves += __fancy_heuristic(current_puzzle)

    return total_moves

# this function adds to the original heuristic function to 
# make the heuristic more accurate, without compromising its
# admissability.
def __fancy_heuristic(current_puzzle: list) -> int:
    # warning: heavy commenting incoming, mainly for my own comprehension :/

    # code based on:
    # https://medium.com/swlh/looking-into-k-puzzle-heuristics-6189318eaca2
    # https://cdn.aaai.org/AAAI/1996/AAAI96-178.pdf
        
    col_conflict = False
    last_tile_conflict = False
    total_moves = 0


    # The following two nested loops are apart of the "linear conflict heuristic"
    # in short, if two tiles are in their destination row / conflict, but their
    # positions are inverted, additional moves will be required to put them in
    # place that are not calculated by the manhattan distance.
    # Each linear conflict adds at minimum 2 moves - one to get out of the row / column, and then
    # one more back in after the other tile has moved past

    # column conflicts
    j = 0 # j is for columns, i is for rows
    while j < len(current_puzzle[0]): # Search puzzle based on columns
        i = 0

        while i < len(current_puzzle):
            tile = current_puzzle[i][j]
            if tile == 0: # if this is the empty space, skip
                i += 1
                continue

            # calc the j column the tile belongs in
            goal_j = (tile -1) % len(current_puzzle[i])
            if goal_j != j: # if tile does not belong in this column
                i += 1
                continue

            n = int((tile -1) / len(current_puzzle[i])) # remember row if it belongs in this column

            # then iterate through other tiles after it in the column
            for new_i in range(i+1, len(current_puzzle)):
                if current_puzzle[new_i][j] == 0: # if is empty tile
                    continue # skip it

                # calc the target j for new tile
                second_goal_j = (current_puzzle[new_i][j] -1) % len(current_puzzle[new_i]) 
                if second_goal_j == j: # if it belongs in this column
                    m = int((current_puzzle[new_i][j] -1) / len(current_puzzle[new_i])) # remember this tile's row
                    if m < n: # if these tiles would have to cross paths to get to their target locations
                        col_conflict = True # we found a conflict
                        break  

            if col_conflict: # only handle one set of col conflicts per row, more can exist but that is harder to calculate
                total_moves += 2 
                col_conflict = False # reset for next column(s)

                # if conflict in 2nd to last column, do not do last move heuristic - potential interactions detailed below
                if j == len(current_puzzle[i]) -2: 
                    last_tile_conflict = True
                break

            i += 1
        j += 1

    
    row_conflict = False
    # row conflicts! yay (:
    # same process as column conflicts mostly
    i = 0
    while i < len(current_puzzle):
        
        j = 0
        for tile in current_puzzle[i]: # for each tile in the row
            # if tile is the empty space, continue
            if tile == 0:
                j += 1
                continue

            # if tile's current row doesnt match its destination row, continue
            goal_i = int((tile -1) / len(current_puzzle[i]))
            if goal_i != i:
                j += 1
                continue

            # if the tile belongs in the row, remember its target column (n)
            n = (tile -1) % len(current_puzzle[i])

            # then loop through following tiles
            for new_j in range(j+1, len(current_puzzle[i])):
                if current_puzzle[i][new_j] == 0: # skip empty space
                    continue

                # check all tiles to the right. If the tile belongs in the row,
                # check it's target column 
                m_goal_i = int((current_puzzle[i][new_j] -1) / len(current_puzzle[i]))
                if m_goal_i == i: # if 2nd tile belongs in row

                    # check for conflict
                    m = (current_puzzle[i][new_j] -1) % len(current_puzzle[i])

                    # if tiles have to cross paths to get to their destinations
                    if m < n:
                        row_conflict = True
                        break

            if row_conflict:
                total_moves += 2
                row_conflict = False

                if i == len(current_puzzle) - 2:
                    last_tile_conflict = True
                break

            j += 1
        i += 1


    # the last tile heuristic stipulates that the final move of the puzzle is either
    # the bottom right tile (for example, in a 3x3 that would be 8) moving left into
    # its final position, or the bottom right tile (in a 3x3, that would be 6) moving up
    # into the final position. The manhattan distance will compute the moves of these tiles
    # to their destination locations, not the bottom right corner. However, if the upper tile
    # (6) is in the bottom row then its manhattan distance will bring it through that point.
    # the same goes for the lefthand tile (8). So, the rule is that if the upper tile is not
    # in the bottom row AND the left tile is not in the right column, an additional 2 moves
    # should be added to the heuristic

    # The linear conflict heuristic interacts with the last tile heuristic.
    # If the upper tile is in its target column (right hand column), it will add 2 moves 
    # as per the last tile heuristic to move it down and then back up. However, if the upper
    # tile is in a row conflict, the row conflict will add 2 steps to the heuristic that
    # accomidates the upper tile to move up and down. The linear conflict and the last tile
    # heuristics will both add 2 steps to allow vertical movement, however those steps can be
    # combined into one movement, meaning that the last tile heuristic may end up adding on 
    # 2 moves that the conflict is already executing. Thus, any row conflict that the upper tile
    # participates in or any column conflict that the lefthand tile participates in should
    # result in the forgoeing of the last tile heuristic.

    # my code forgoes the last tile heuristic if ANY conflict occurs in the row that the upper
    # tile resides in as well as the column that the left tile resides in. This streamlines my code
    # as there are fewer conditions to check.
    # If the upper tile and left tile are both in place, and not in conflict, it will trigger
    # the last tile heuristic. This is an issue when the puzzle completes, as a 
    # completed puzzle should have 0 moves left, but by the definition of the last tile
    # heuristic, it will add 2 moves. I have added safeguards against it.

    if not last_tile_conflict: # no conflict with linear conflicts
            
            h = len(current_puzzle) # height
            w = len(current_puzzle[0]) # width

            upper_tile = (h-1) * w # tile above bottom right corner
            left_tile = upper_tile + w -1 # tile to the left of bottom right corner

            # if tiles are in the row / column that manhattan distance will account for
            there = False 
            upper_in_pos = False # if upper tile is in its destination position
            left_in_pos = False # if left tile is in its destination position

            for j in range(len(current_puzzle[h-1])): # scan row 

                if current_puzzle[h-1][j] == left_tile:
                    left_in_pos = True

                if current_puzzle[h-1][j] == (upper_tile): # tile is in the row
                    there = True
                    break

            for i in range(len(current_puzzle)): # scan column
                if current_puzzle[i][w-1] == upper_tile:
                    upper_in_pos = True

                if current_puzzle[i][w-1] == (left_tile): # tile is in upper column
                    there = True
                    break
            
            # if this puzzle state satisfies the heuristic
            if not there and not (upper_in_pos and left_in_pos):
                total_moves += 2

    return total_moves


class State:
    """
        The state class creates a given sliding tile puzzle and its
        relevant information. It requires the puzzle, the number of
        moves made thus far, it's calculated heuristic and a list
        of the steps taken to get to that point.
    
    """

    puzzle = None
    moves_made = None
    total_heuristic = None
    steps_taken = []
    
    def __init__(self, puz: list, moves: int, heuristic: int, steps: list):
        """
           The class State requires a puzzle in list format, the number of moves made so far,
           the calculated number of moves remaining, and the list of steps taken to
           get to this point 
            
        """
        self.puzzle = tuple([tuple(x) for x in puz])
        self.moves_made = moves
        self.total_heuristic = heuristic + moves
        self.steps_taken = steps

    def __hash__(self):
        """
        hashes the object based on the puzzle variable
        """
        return hash(self.puzzle)
    
    def __eq__(self, input):
        """
        assess equality of the hash of itself to the input
        """
        return hash(self) == input
    
    def __lt__(self, input):
        """
        assess inequality of the hash of itself to the input
        """
        return hash(self) < input
    
    def __gt__(self, input):
        """
        assess inequality of the hash of itself to the input
        """
        return hash(self) > input