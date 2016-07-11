import random
import copy


def insert_entry(grid, new_entry):
	grid_width, grid_height = grid_width_and_height(grid)
	word = new_entry['word']
	word_length = len(word)
	x_coord = new_entry['x_coord']
	y_coord = new_entry['y_coord']
	if new_entry['direction'] == 'horizontal':
		if x_coord + word_length > grid_width:
			extra_columns = word_length - (grid_width - x_coord)
			extension = extra_columns * ['']
			for row in grid:
				row.extend(extension)
		if x_coord < 0:
			extra_columns = abs(x_coord)
			for row in grid:
				for i in range(0, extra_columns):
					row.insert(i, '')
			x_coord = 0
		for i in range(word_length):
			char = word[i]
			x = x_coord + i
			grid[y_coord][x] = char
	if new_entry['direction'] == 'vertical':
		if y_coord + word_length > grid_height:
			extra_rows = (y_coord + word_length) - grid_height
			for i in range(extra_rows):
				grid.append(grid_width * [''])
		if y_coord < 0:
			extra_rows = abs(y_coord)
			for i in range(0, extra_rows):
				grid.insert(i, grid_width * [''])
			y_coord = 0
		for i in range(word_length):
			char = word[i]
			y = y_coord + i
			grid[y][x_coord] = char
	return grid


def find_insertion_sites(grid, word):
	best_score = 1
	best_sites = {'horizontal': [], 'vertical': []}
	word_length = len(word)
	grid_width, grid_height = grid_width_and_height(grid)
	for x in range(1 - word_length, grid_width):
		for y in range(grid_height):
			score = insert_horizontally(grid, x, y, word)
			if score == best_score:
				best_sites['horizontal'].append((x, y))
			if score > best_score:
				best_score = score
				best_sites['horizontal'] = [(x, y)]
	for x in range(grid_width):
		for y in range(1 - word_length, grid_height):
			score = insert_vertically(grid, x, y, word)
			if score == best_score:
				best_sites['vertical'].append((x, y))
			if score > best_score:
				best_score = score
				best_sites['vertical'] = [(x, y)]
				best_sites['horizontal'] = []
	if not (best_sites['horizontal'] or best_sites['vertical']):
		best_score = 0
	return best_score, best_sites


def insert_horizontally(grid, x, y, word):
	grid_width, grid_height = grid_width_and_height(grid)
	score = 0
	if word_to_the_left(grid, x, y) or word_to_the_right(grid, x, y, len(word)):
		return 0
	for i in range(x, len(word)+x):
		char_index = i - x
		if 0 <= i < grid_width:
			if empty_cell(grid, i, y) and not up_and_down_empty(grid, i, y):
				return 0
			elif not empty_cell(grid, i, y) and cell_contents(grid, i, y) != word[char_index]:
				return 0
			elif not empty_cell(grid, i, y):
				score += 1
	return score


def insert_vertically(grid, x, y, word):
	grid_width, grid_height = grid_width_and_height(grid)
	score = 0
	if word_up(grid, x, y) or word_down(grid, x, y, len(word)):
		return 0
	for i in range(y, len(word)+y):
		char_index = i - y
		if 0 <= i < grid_height:
			if empty_cell(grid, x, i) and not left_and_right_empty(grid, x, i):
				return 0
			elif not empty_cell(grid, x, i) and cell_contents(grid, x, i) != word[char_index]:
				return 0
			elif not empty_cell(grid, x, i):
				score += 1
	return score


def grid_width_and_height(grid):
	return len(grid[0]), len(grid)


def cell_contents(grid, x, y):
	return grid[y][x]


def word_to_the_left(grid, x, y):
	if x <= 0:
		return False
	else:
		return not empty_cell(grid, x - 1, y)


def word_to_the_right(grid, x, y, word_length):
	final_x = x + word_length - 1
	grid_width, _ = grid_width_and_height(grid)
	if final_x >= grid_width - 1:
		return False
	else:
		return not empty_cell(grid, final_x + 1, y)


def word_up(grid, x, y):
	if y <= 0:
		return False
	else:
		return not empty_cell(grid, x, y - 1)


def word_down(grid, x, y, word_length):
	final_y = y + word_length
	_, grid_height = grid_width_and_height(grid)
	if final_y >= grid_height:
		return False
	else:
		return not empty_cell(grid, x, final_y)


def empty_cell(grid, x, y):
	return cell_contents(grid, x, y) == ''


def up_and_down_empty(grid, x, y):
	_, grid_height = grid_width_and_height(grid)
	if y == 0:
		return grid[y+1][x] == ''
	if y == grid_height-1:
		return grid[y-1][x] == ''
	else:
		return grid[y+1][x] == '' and grid[y-1][x] == ''


def left_and_right_empty(grid, x, y):
	grid_width, _ = grid_width_and_height(grid)
	if x == 0:
		return grid[y][x+1] == ''
	if x == grid_width-1:
		return grid[y][x-1] == ''
	else:
		return grid[y][x+1] == '' and grid[y][x-1] == ''


def extend_crossword(grid, word_list):
	if not word_list:
		return grid
	else:
		scores_and_sites = [(find_insertion_sites(grid, list(word)), list(word)) for word in word_list]
		max_score = max([x[0][0] for x in scores_and_sites])
		if max_score == 0:
			return grid
		else:
			best_sites = [item for item in scores_and_sites if item[0][0] == max_score]
			max_length = max([len(x[1]) for x in best_sites])
			best_candidates = [item for item in best_sites if len(item[1]) == max_length]
			next_entry = random.choice(best_candidates)
			next_word = next_entry[1]
			coordinates_dict = next_entry[0][1]
			coordinates = [(x_y, 'vertical') for x_y in coordinates_dict['vertical']]
			coordinates.extend([(x_y, 'horizontal') for x_y in coordinates_dict['horizontal']])
			next_coordinates = random.choice(coordinates)
			new_grid = insert_entry(grid, {'x_coord': next_coordinates[0][0],
											'y_coord': next_coordinates[0][1],
											'direction': next_coordinates[1],
											'word': list(next_word)})
			word_list.remove(''.join(next_word))
			return extend_crossword(new_grid, word_list)


def make_crossword(word_list):
	word_list_copy = copy.copy(word_list)
	max_length = max([len(list(x)) for x in word_list_copy])
	first_word = random.choice([w for w in word_list_copy if len(list(w)) == max_length])
	word_list_copy.remove(first_word)
	initial_grid = [list(first_word)]
	return extend_crossword(initial_grid, word_list_copy)


def make_decent_crossword(word_list, tries=20):
	options = [make_crossword(word_list) for i in range(tries)]
	compact_factor = [size[0] * size[1] for size in [grid_width_and_height(grid) for grid in options]]
	best = min(compact_factor)
	chosen = random.choice([option[0] for option in zip(options, compact_factor) if option[1] == best])
	return chosen


sample_list = ['akin', 'reduce', 'user', 'collar', 'city', 'issued', 'tabs', 'pencil', 'arch', 'travel',
			   'exam', 'easily', 'keeps', 'neutral', 'omits', 'you', 'rapid', 'elect', 'sue', 'leave',
			   'against', 'climb']

crossword = make_decent_crossword(sample_list)

for row in crossword:
	print ' | '.join([char if char != '' else ' ' for char  in row ])
