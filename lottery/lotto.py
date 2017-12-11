import csv
import copy
print("> Importing networkx...")
import networkx as nx
print("> Importing plt...")
try:
	import matplotlib.pyplot as plt
except:
	raise
print("> Finished imports.")

LOTTO_7 = 0
LOTTO_6 = 1
MINILOTTO = 2
NUMBERS_3 = 3
NUMBERS_4 = 4

DARK_GRAY = '#CCCCCC'
BLACK = '#000000'
PURPLE = '#8E44AD'
DARK_BLUE = '#1F3A93'
BLUE = '#19B5FE'
DARK_GREEN = '#16A085'

EDGE_WIDTH = 2
NODE_SIZE = 350

class Prizes:
	def __init__(self, rank, prize, match_draw_count, match_bonus_count=0):
		self.match_draw_count = match_draw_count
		self.match_bonus_count = match_bonus_count
		self.rank = rank
		self.prize = prize
		self.win_status = False
		self.draw = None
		self.bonus = None
		self.is_detail_print = False

	def is_win(self, bet, draw, bonus):
		draw_count = 0
		bonus_count = 0
		self.draw = draw
		self.bonus = bonus
		for number in bet:
			if number in draw:
				draw_count += 1
			if number in bonus:
				bonus_count += 1
		if draw_count >= self.match_draw_count and bonus_count >= self.match_bonus_count:
			self.win_status = True
		return self.win_status

	def reset(self):
		self.draw = None
		self.bonus = None
		self.win_status = False

	def earnings(self):
		if self.win_status:
			return self.prize
		return 0

	def print_win(self, date):
		print(self.rank, "place win | Prize money:", self.prize, 
			"| Draw date:", date, 
			"| Draw:", self.draw, 
			"| Bonus:", self.bonus)

class Lotto:
	def __init__(self, lotto_type, edge_type_count=4):
		self.lotto_type = lotto_type
		self.parameter_setup()
		self.number_matrix = None
		self.adjacency_matrix = None 
		self.min_weight = 0
		self.graph = None
		self.edge_type_count = edge_type_count
		self.edge_colors = [BLACK, PURPLE, DARK_BLUE, BLUE, DARK_GREEN]
		self.printed_cycles = []
		self.check_combination_earnings = False
		self.is_detail_print = False

	def parameter_setup(self):
		self.prizes = []

		if self.lotto_type == LOTTO_7:
			self.filename = 'loto7.csv'
			self.total_count = 37
			self.bonus_count = 2
			self.draw_count = 7
			self.prizes.append(Prizes('1st', 100000000, 7))
			self.prizes.append(Prizes('2nd', 10000000, 6, match_bonus_count=1))
			self.prizes.append(Prizes('3rd', 1000000, 6))
			self.prizes.append(Prizes('4th', 15000, 5))
			self.prizes.append(Prizes('5th', 2200, 4))
			self.prizes.append(Prizes('6th', 1100, 3, match_bonus_count=1))
			self.ticket_cost = 300

		elif self.lotto_type == LOTTO_6:
			self.filename = 'loto6.csv'
			self.total_count = 43
			self.bonus_count = 1
			self.draw_count = 6
			self.prizes.append(Prizes('1st', 200000000, 6))
			self.prizes.append(Prizes('2nd', 5000000, 5, match_bonus_count=1))
			self.prizes.append(Prizes('3rd', 200000, 5))
			self.prizes.append(Prizes('4th', 5000, 4))
			self.prizes.append(Prizes('5th', 1000, 3))
			self.ticket_cost = 200

		elif self.lotto_type == MINILOTTO:
			self.filename = 'miniloto.csv'
			self.total_count = 31
			self.bonus_count = 1
			self.draw_count = 5
			self.prizes.append(Prizes('1st', 10000000, 5))
			self.prizes.append(Prizes('2nd', 250000, 4, match_bonus_count=1))
			self.prizes.append(Prizes('3rd', 10000, 4))
			self.prizes.append(Prizes('4th', 1000, 3))
			self.ticket_cost = 200

	def build_number_matrix(self):
		print("> Building the number matrix... ", end='', flush=True)
		file_pointer = open(self.filename, newline='', encoding='utf-8')
		file_reader = csv.reader(file_pointer)

		number_start_index = 2
		date_index = 1
		data_start_buffer = 1

		number_matrix = []
		bonus_numbers = []
		dates = []

		number_end_index = number_start_index + self.draw_count
		bonus_end_index = number_end_index + self.bonus_count
		
		for row in file_reader:
			if data_start_buffer > 0:
				data_start_buffer -= 1
			else:
				int_numbers = [int(x) for x in row[number_start_index:number_end_index]]
				int_bonus = [int(x) for x in row[number_end_index:bonus_end_index]]

				dates.append(row[date_index])
				number_matrix.append(int_numbers)
				bonus_numbers.append(int_bonus)

		self.number_matrix = {'numbers': number_matrix, 'bonus': bonus_numbers, 'dates': dates}
		print("Successful.")

	def build_adjacency_matrix(self):
		print("> Building the adjacency matrix... ", end='', flush=True)
		length = self.total_count + 1 
		self.adjacency_matrix = [[0]*length for _ in range(length)]
		for i in range(0, len(self.number_matrix['numbers'])):
			current_row = self.number_matrix['numbers'][i]
			for j in range(0, self.draw_count):
				start_index = j+1
				for k in range(start_index, self.draw_count):
					self.adjacency_matrix[current_row[j]][current_row[k]] += 1
					self.adjacency_matrix[current_row[k]][current_row[j]] += 1

		# Calculate min and max weight
		self.max_weight = max(map(max, self.adjacency_matrix))
		edge_types = self.edge_type_count
		for i in range(self.max_weight-1, 0, -1):
			if any(i in sub for sub in self.adjacency_matrix):
				edge_types -= 1
			if edge_types == 0:
				self.min_weight = i
				break

		print("| Minimum weight:", self.min_weight, "| Maximum weight:", self.max_weight, end='', flush=True)
		print(" ...Successful.")

	##############################
	# Graph building and display #
	##############################

	def build_undirected_graph_from_adjacency_matrix(self):
		print("> Building the graph...  ", end='', flush=True)
		self.graph = nx.Graph()
		for i in range(1, self.total_count+1):
			for j in range(i, self.total_count+1):
				weight = self.adjacency_matrix[i][j]
				if weight >= self.min_weight:
					self.graph.add_edge(str(i), str(j), weight=weight)
		print("Successful.")

	def build_edge_properties(self):
		print("> Building the edges... ", end='', flush=True)
		edges = []
		self.position = nx.shell_layout(self.graph)
		nx.draw_networkx_nodes(self.graph, self.position, node_size=NODE_SIZE, node_color=DARK_GRAY)

		for weight in range(self.max_weight, self.min_weight, -1):
			if any(weight in sub for sub in self.adjacency_matrix):
				edges.append([(u,v) for (u,v,d) in self.graph.edges(data=True) if d['weight'] == weight])
		
		for i in range(0, len(edges)):
			nx.draw_networkx_edges(self.graph, self.position, edgelist=edges[i], width=EDGE_WIDTH, edge_color=self.edge_colors[i])

		self.graph.add_nodes_from(self.position.keys())
		for n, p in self.position.items():
			self.graph.node[n]['pos'] = p
		print("Successful.")

	def display_graph(self):
		print("> Displaying the graph... ", end='', flush=True)
		nx.draw_networkx_labels(self.graph, self.position, font_size=13, font_family='sans-serif')
		plt.axis('off')
		plt.subplots_adjust(left=0.0, bottom=0.0, right=1.0, top=1.0)
		plt.show()
		print("Successful.")

	###################
	# Cycle detection #
	###################

	def is_cycle_in_printed_cycles(self, cycle_list):
		if len(self.printed_cycles) == 0:
			return False
		for element in cycle_list['nodes']:
			if element not in self.printed_cycles:
				return False
		return True

	def print_cycle(self, cycle_list={'nodes':[],'weights':[]}):
		if not self.is_cycle_in_printed_cycles(cycle_list):
			for i in range(0, self.draw_count):
				print(cycle_list['nodes'][i], '--> ', end='', flush=True)
			print(cycle_list['nodes'][0], '| Weights:', cycle_list['weights'], 'END')
			
			for item in cycle_list['nodes']:
				if item not in self.printed_cycles:
					self.printed_cycles.append(item)

			if self.check_combination_earnings:
				self.calculate_earnings(cycle_list['nodes'])
			
	def detect_cycle(self, cycle_list={'nodes':[],'weights':[]}, start_index=0, start_index_2=0):
		for i in range(0, len(self.adjacency_matrix)):
			if self.adjacency_matrix[start_index][i] >= self.min_weight and i != start_index_2:
				# Check if i is in the list
				if i not in cycle_list['nodes'] and len(cycle_list['nodes']) <= self.draw_count:
					# Push it in the list of significant indices
					if len(cycle_list['nodes']) == 0:
						cycle_list['nodes'].append(start_index)
					cycle_list['nodes'].append(i)
					cycle_list['weights'].append(self.adjacency_matrix[start_index][i])
					self.detect_cycle(cycle_list, i, start_index)
				elif i == cycle_list['nodes'][0] and len(cycle_list['nodes']) == self.draw_count:
					self.print_cycle(cycle_list)

		if len(cycle_list['nodes']) > 0:
			cycle_list['nodes'].pop()
			
		if len(cycle_list['weights']) > 0:
			cycle_list['weights'].pop()

	def start_cycle_detection(self):
		print("> Detecting cycles...")
		for i in range(0, len(self.adjacency_matrix)):
			cycle_list = {'nodes':[],'weights':[]}
			self.detect_cycle(cycle_list, i, 0)

	def calculate_earnings(self, bet):
		print("> Calculating earnings... Your bet:", bet)
		i = 0
		matches_won = 0
		total_prize_money = 0
		total_entries = len(self.number_matrix['dates'])
		for i in range(0, total_entries):
			date = self.number_matrix['dates'][i]
			draw = self.number_matrix['numbers'][i]
			bonus = self.number_matrix['bonus'][i]
			win_prize = None
			for prize in self.prizes:
				if prize.is_win(bet, draw, bonus):
					if self.is_detail_print:
						prize.print_win(date)
					total_prize_money += prize.earnings()
					matches_won += 1
					prize.reset()
					break
			i+=1

		print("Matches won: ", matches_won, "/", total_entries, 
			'| Rate:', matches_won*100/total_entries, '%',
			'| Total money earned:', total_prize_money, 
			'| Total money bet:', self.ticket_cost*total_entries,
			'| Net output', total_prize_money-(self.ticket_cost*total_entries), '\n')

	##################
	# Public methods #
	##################

	def run_adjacency_matrix(self):
		self.build_number_matrix()
		self.build_adjacency_matrix()

	def run_display_graph(self):
		self.run_adjacency_matrix()
		self.build_undirected_graph_from_adjacency_matrix()
		self.build_edge_properties()
		self.display_graph()

	def run_cycle_detection(self):
		self.run_adjacency_matrix()
		self.start_cycle_detection()
	
	def run_check_combination(self):
		self.check_combination_earnings = True
		self.is_detail_print = True
		self.run_cycle_detection()

	def run_check_single_combination(self, bet):
		self.is_detail_print = True
		self.run_adjacency_matrix()
		self.calculate_earnings(bet)

	def run_all(self):
		self.check_combination_earnings = True
		self.is_detail_print = True
		self.build_number_matrix()
		self.build_adjacency_matrix()
		self.start_cycle_detection()
		self.build_undirected_graph_from_adjacency_matrix()
		self.build_edge_properties()
		self.display_graph()

	def run_check_random_combinations(self, random_count=5):
		self.run_adjacency_matrix()
		from random import randint
		while random_count > 0:
			bet = []
			for i in range(0, self.draw_count):
				random = 0
				is_random_in_bet = True # I just want you to enter the loop
				while is_random_in_bet:
					random = randint(1, self.total_count)
					is_random_in_bet = random in bet
				bet.append(random)
			self.calculate_earnings(bet)
			random_count -= 1

lotto = Lotto(LOTTO_7, edge_type_count=5)
# lotto = Lotto(LOTTO_6, edge_type_count=5)
# lotto = Lotto(MINILOTTO, edge_type_count=5)

# lotto.run_display_graph()
# lotto.run_cycle_detection()
lotto.run_all()
# lotto.run_check_random_combinations(10)
