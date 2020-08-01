from msvcrt import getch
import random
import os

class game():
	def __init__(self):
		self.clear()
		self.file_path   = 'scores.txt'
		self.score       = 0
		#self.n is the size of the table
		self.n           = 3
		self.table       = [[0 for _ in range(0, self.n)] for _ in range(0, self.n)]
		self.empty       = [[0 for _ in range(0, self.n)] for _ in range(0, self.n)]
		self.RANDOM_NUMS = [2, 4]
		first_num_row    = random.randint(0, self.n-1)
		first_num_col	 = random.randint(0, self.n-1)
		first_num        = random.choice(self.RANDOM_NUMS)

		second_num_row   = first_num_row
		second_num_col	 = first_num_col
		while (second_num_row == first_num_row) or (second_num_col == first_num_col):
			second_num_row    = random.randint(0, self.n-1)
			second_num_col	  = random.randint(0, self.n-1)
		second_num            = random.choice(self.RANDOM_NUMS)

		self.table[first_num_row][first_num_col]   = first_num
		self.table[second_num_row][second_num_col] = second_num

		self.gameplay()

	def gameplay(self):
		self.show_table()
		while True:
			self.ask_move()

	def ask_move(self):
		Cont = True
		while Cont ==  True:
			act = str(getch())
			Cont = False
			if   act == "b'w'":
				self.move(self.up,    self.table)
			elif act == "b'd'":
				self.move(self.right, self.table)
			elif act == "b's'":
				self.move(self.down,  self.table)
			elif act == "b'a'":
				self.move(self.left,  self.table)
			elif act == "b'`'":
				self.quit()
			else:
				Cont = True

	def show_table(self):
		self.clear()
		print('')
		for i in range(self.n):
			for j in range(self.n):
				if (self.n != j+1):
					print(self.table[i][j], end = ' ')
				else:
					print(self.table[i][j])
		print('\nScore: ', self.score)

	def table_copying(self, table_name):
		return [[element for element in array] for array in table_name]

	def move(self, direction, table_name):
		""" Every move goes through this function """
		copy_table = self.table_copying(table_name)
		try:
			(self.table[0][0])+= 0
		except:
			self.table = None
		[direction(i, table_name) for i in range(self.n)]
		if table_name == self.table:
			if copy_table == self.table:
				if self.empty_slots() == [] and not self.can_move():
					self.quit()
			else:
				self.add_random()
				self.show_table()


	def can_move(self):
		""" Checking the possibility of making the moves """
		copy1 = self.table_copying(self.table)
		copy2 = self.table_copying(self.table)
		del(self.table)
		self.move(self.left,  copy1)
		self.move(self.right, copy1)
		self.move(self.up,    copy1)
		self.move(self.down,  copy1)
		self.table = self.table_copying(copy2)
		if (copy1 == copy2):
			return False
		else:
			return True

	def left(self, row, table_name):
		already_changed = [False]*self.n
		for i in range(self.n):
			for element in range(1, self.n):
				previous = table_name[row][element-1]
				current  = table_name[row][element]
				if (previous == 0) :
					table_name[row][element-1] = current
					table_name[row][element]   = 0
				elif (current == previous) and (already_changed[element-1]!=True)  \
				and (already_changed[element]!=True):
					table_name[row][element-1] *= 2
					table_name[row][element]    = 0
					already_changed[element-1]  = True
					if (table_name == self.table):
						self.score 			   += table_name[row][element-1]

	def up(self, col, table_name):
		already_changed = [False]*self.n
		for i in range(self.n):
			for element in range(1, self.n):
				above = table_name[element-1][col]
				current  = table_name[element][col]
				if (above == 0) :
					table_name[element-1][col] = current
					table_name[element][col]   = 0
				elif (current == above) and (already_changed[element-1]!=True)  \
				and (already_changed[element]!=True):
					table_name[element-1][col] *= 2
					table_name[element][col]    = 0
					already_changed[element-1]  = True
					if (table_name == self.table):
						self.score 			   += table_name[element-1][col]

	def right(self, row, table_name):
		already_changed = [False]*self.n
		for i in range(self.n-1, -1, -1):
			for element in range(self.n-2, -1, -1):
				following = table_name[row][element+1]
				current   = table_name[row][element]
				if (following == 0) :
					table_name[row][element+1] = current
					table_name[row][element]   = 0
				elif (current == following) and (already_changed[element+1]!=True) \
				and (already_changed[element]!=True):
					table_name[row][element+1] *= 2
					table_name[row][element]    = 0
					already_changed[element+1]  = True
					if (table_name == self.table):
						self.score 			   += table_name[row][element+1]

	def down(self, col, table_name):
		already_changed = [False]*self.n
		for i in range(self.n-1, -1, -1):
			for element in range(self.n-2, -1, -1):
				below = table_name[element+1][col]
				current  = table_name[element][col]
				if (below == 0) :
					table_name[element+1][col] = current
					table_name[element][col]   = 0
				elif (current == below) and (already_changed[element+1]!=True) \
				and (already_changed[element]!=True):
					table_name[element+1][col] *= 2
					table_name[element][col]    = 0
					already_changed[element+1]  = True
					if (table_name == self.table):
						self.score 			   += table_name[element+1][col]

	def empty_slots(self):
		return [x for x in range(self.n**2) if self.table[x//self.n][x%self.n] == 0]

	def add_random(self):
		place   = random.choice(self.empty_slots())
		row     = place//self.n
		col     = place% self.n
		new_num = random.choice(self.RANDOM_NUMS)
		self.table[row][col] = new_num

	def clear(self):
		os.system("cls")

	def save_score(self):
		with open(self.file_path, 'r') as f:
			scores  = [(line.rstrip('\n')) for line in f.readlines()]
		scores      = [int(score) for score in scores]
		scores_copy = scores.copy()
		scores.append(self.score)
		scores      = sorted(scores, reverse = True)
		del(scores[-1])
		with open(self.file_path, 'w') as f:
			for score in scores:
				f.write(str(score) + '\n')
		f.close()
		if (scores_copy != scores):
			print('Your score has been saved')

	def quit(self):
		self.show_table()
		print('Game end')
		self.save_score()
		print('*** Shutting down ***')
		exit(0)

if __name__ == '__main__':
	a=game()
