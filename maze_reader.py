from PIL import Image
import numpy as np
from matplotlib import pyplot as plt

class MazeReader:
	def __init__(self, filename):
		self.maze = self.open_image_to_arr(filename)
		plt.imshow(self.maze, interpolation='nearest')
		plt.savefig("original.png")

		self.height = len(self.maze)
		self.width = len(self.maze[0])

		v,e = self.get_graph_representation()
		'''
		print("New vertices")
		print(v)
		print("New edges")
		print(e)
		'''

	def get_graph_representation(self):
		white_coords = []
		for row in range(len(self.maze)):
			for col in range(len(self.maze[row])):
				if(self.maze[row][col][0] == 255):
					white_coords.append([row, col])

		vertices = self.get_vertices(white_coords)
		'''
		print("Old vertices")
		print(vertices)
		'''
		edges = self.get_edges(vertices)

		self.output_vertices(self.maze, vertices)

		# Convert to stage coords
		stage_vertices = []
		stage_edges = []
		for vertex in vertices:
			stage_vertices.append([vertex[1], self.height - vertex[0] - 1])

		for edge in edges:
			new_edge = []
			new_edge.append([edge[0][1], self.height - edge[0][0] - 1])
			new_edge.append([edge[1][1], self.height - edge[1][0] - 1])
			stage_edges.append(new_edge)

		return stage_vertices, stage_edges

	'''
	Get any point of interest, which is an intersection, a dead end, or a corner
	'''
	def get_vertices(self, white_coords):
		vertices = []
		for coord in white_coords:
			num_connected = self.get_num_connected(coord, white_coords)
			if(num_connected == 1 or num_connected > 2):
				vertices.append(coord)
			if(num_connected == 2):
				# Check for corner
				north = [coord[0] + 1, coord[1]]
				south = [coord[0] - 1, coord[1]]
				east = [coord[0], coord[1] + 1]
				west = [coord[0], coord[1] - 1]

				if(not(north in white_coords and south in white_coords) and not(east in white_coords and west in white_coords)):
					vertices.append(coord)

		return vertices

	'''
	Once we have vertices, get edges between them 
	'''
	def get_edges(self, vertices):
		edges = []
		# Get horizontal edges
		for vertex in vertices:
			y_pos = vertex[1]
			while(y_pos < self.width):
				y_pos += 1
				new_vertex = [vertex[0], y_pos]
				if(new_vertex in vertices):
					# We found next vertex
					edges.append([vertex, new_vertex])
					break

		# Get vertical edges
		for vertex in vertices:
			x_pos = vertex[0]
			while(x_pos < self.height):
				x_pos += 1
				new_vertex = [x_pos, vertex[1]]
				if(new_vertex in vertices):
					# We found next vertex
					edges.append([vertex, new_vertex])
					break

		return edges

	'''
	Get the number of other white coords connected to a coord
	'''
	def get_num_connected(self, coord, white_coords):
		north = [coord[0] + 1, coord[1]]
		south = [coord[0] - 1, coord[1]]
		east = [coord[0], coord[1] + 1]
		west = [coord[0], coord[1] - 1]

		num_connected = 0
		if(north in white_coords):
			num_connected += 1
		if(south in white_coords):
			num_connected += 1
		if(east in white_coords):
			num_connected += 1
		if(west in white_coords):
			num_connected += 1

		return num_connected

	def open_image_to_arr(self, filename):
		img = Image.open(filename)
		arr = np.array(img)
		return arr

	def output_vertices(self, maze, vertices):
		for vertex in vertices:
			maze[vertex[0], vertex[1]][1] = 0
			maze[vertex[0], vertex[1]][2] = 0


		plt.imshow(maze, interpolation='nearest')
		plt.savefig("intersections.png")


if __name__ == "__main__":
	m = MazeReader("medmaze2.png")





