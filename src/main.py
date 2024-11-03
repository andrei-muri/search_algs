
from typing import List
import pygame 
from spot import Spot, GREY, WHITE
from search_algs import SearchAlgs
from queue import PriorityQueue, Queue, LifoQueue

WIDTH = 800

WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Searching algz")

def make_grid(rows, width):
    grid = []
    gap =  width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
             spot = Spot(i, j, gap, rows)
             grid[i].append(spot)
    
    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    cols = rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (i * gap, 0), (i * gap, width))
    for j in range(cols):
        pygame.draw.line(win, GREY, (0, j * gap), (width, j * gap))

def draw(win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()

def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()

def astar(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start.get_pos(), end.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)
		if current == end:
			reconstruct_path(came_from, end, draw)
			end.make_end()
			return True
		for neighbor in current.neighbours:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()
		draw()
		if current != start:
			current.make_closed()

	return False
     


def bfs(draw, grid, start, end):
    queue = Queue()
    queue.put(start)
    came_from = {}
    visited = {spot: False for row in grid for spot in row}
    visited[start] = True

    while not queue.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = queue.get()
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbours:
            if not visited[neighbor]:
                came_from[neighbor] = current
                visited[neighbor] = True
                queue.put(neighbor)
                neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False

from queue import LifoQueue

def dfs(draw, grid, start, end):
    stack = LifoQueue()
    stack.put(start)
    came_from = {}
    visited = {spot: False for row in grid for spot in row}
    visited[start] = True

    while not stack.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = stack.get()

        # If we reached the end, reconstruct the path
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbours:
            if not visited[neighbor]:
                came_from[neighbor] = current
                visited[neighbor] = True
                stack.put(neighbor)
                neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False


def dijkstra(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbours:
            temp_g_score = g_score[current] + 1  

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((g_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False

def main(win, width):
	ROWS = 50
	grid = make_grid(ROWS, width)

	start = None
	end = None

	algorithm = SearchAlgs.ASTAR
	print(f"The searching algorithm is: {SearchAlgs.ASTAR.name}")
	run = True
	while run:
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]: # LEFT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				if not start and spot != end:
					start = spot
					start.make_start()

				elif not end and spot != start:
					end = spot
					end.make_end()

				elif spot != end and spot != start:
					spot.make_barrier()

			elif pygame.mouse.get_pressed()[2]: # RIGHT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbours(grid)
					if algorithm == SearchAlgs.ASTAR:
						astar(lambda: draw(win, grid, ROWS, width), grid, start, end)
					elif algorithm == SearchAlgs.BREADTH:
						bfs(lambda: draw(win, grid, ROWS, width), grid, start, end)
					elif algorithm == SearchAlgs.DEPTH:
						dfs(lambda: draw(win, grid, ROWS, width), grid, start, end)
					elif algorithm == SearchAlgs.DIJKSTRA:
						dijkstra(lambda: draw(win, grid, ROWS, width), grid, start, end)
					else:
						print("No valid search algorithm")

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)
                
				if event.key == pygame.K_a:
					algorithm = SearchAlgs.ASTAR
					print(f"The searching algorithm is: {SearchAlgs.ASTAR.name}")
                
				if event.key == pygame.K_b:
					algorithm = SearchAlgs.BREADTH
					print(f"The searching algorithm is: {SearchAlgs.BREADTH.name}")

				if event.key == pygame.K_d:
					algorithm = SearchAlgs.DEPTH
					print(f"The searching algorithm is: {SearchAlgs.DEPTH.name}")
				
				if event.key == pygame.K_i:
					algorithm = SearchAlgs.DIJKSTRA
					print(f"The searching algorithm is: {SearchAlgs.DIJKSTRA.name}")

	pygame.quit()


main(WIN, WIDTH)