import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

sns.set_theme(style='darkgrid')

def get_distance(p1, p2):
    return np.sqrt(sum([(p2_coordinate - p1_coordinate) ** 2 for p1_coordinate, p2_coordinate in zip(p1, p2)]))

def get_midpoint(p1, p2):
    return tuple((p1 + p2) / 2)



def plot_line_segment(p1, p2, scaling_factor=1):
    L = get_distance(p1, p2)
    direction = (p2 - p1) / L
    arrow_start = p1 + (1 - scaling_factor) * direction * L
    arrow_end = p1 + scaling_factor * direction * L
    plt.arrow(arrow_start[0], arrow_start[1], arrow_end[0] - arrow_start[0], arrow_end[1] - arrow_start[1], head_width=0, color='black')



class Vertice():
    def __init__(self, id, value, paths=None):
        self.id = id
        self.value = value
        self.paths = paths or []
        self.circle_coordinates = (0, 0)

class Graph:
    def __init__(self, vertices=[]):
        self.vertices = vertices
        self.ids = []
        self.all_paths = []
        for vertice in vertices:
            self.ids.append(vertice.id)
            for path in vertice.paths:
                full_path = (vertice.id, path[0], path[1])
                if full_path not in self.all_paths:
                    self.all_paths.append(full_path)
    

    def add_vertice(self, vertice):
        if vertice.id in self.ids:
            print("Please enter an unique ID")
            return None
        self.vertices.append(vertice)
        self.ids.append(vertice.id)

    def get_vertice(self, id):
        for vertice in self.vertices:
            if vertice.id == id:
                return vertice

    def add_path(self, id1, id2, path_cost):
        if id1 not in self.ids or id2 not in self.ids:
            print("Vertices with the given ids do not exist in this graph")
            return None

        vertice1, vertice2 = self.get_vertice(id1), self.get_vertice(id2)
        existance_of_copy = False
        for i, path in enumerate(self.all_paths):
            if path[0] == id1 and path[1] == id2:
                existance_of_copy = True
                self.all_paths[i] = (id1, id2, path_cost)
                previous_cost = path[2]
                break
        if existance_of_copy:
            vertice1.paths[vertice1.paths.index((id2, previous_cost))] = (id2, path_cost)
            vertice2.paths[vertice2.paths.index((id1, previous_cost))] = (id1, path_cost)
        else:
            self.all_paths.append((id1, id2, path_cost))
            vertice1.paths.append((id2, path_cost))
            vertice2.paths.append((id1, path_cost))

        print("Path added succesfully")


    def bar_visuals(self):
        values = [vertice.value for vertice in self.vertices]
        sns.barplot(pd.DataFrame({
            'IDs': self.ids,
            'Values': values
        }), x='IDs', y='Values')

    def circle_visuals(self):
        n = len(self.vertices) # Number of vertices
        angles = np.array([(2*np.pi)*k/n for k in range(n)])
        x = np.cos(angles)
        y = np.sin(angles)
        fig, ax = plt.subplots()
        ax.scatter(x, y)

        # Annotate each vertice with its ID and Value
        for i, vertice in enumerate(self.vertices):
            ax.annotate('ID: {}, Value: {}'.format(vertice.id, vertice.value), (x[i], y[i]), textcoords="offset points", xytext=(0,10), ha='center')
            vertice.circle_coordinates = (x[i], y[i])

        # Draw paths
        for path in self.all_paths:
            p1 = self.get_vertice(path[0]).circle_coordinates
            p2 = self.get_vertice(path[1]).circle_coordinates
            path_cost = path[2]
            plot_line_segment(p1, p2)
            plt.annotate('{}'.format(path_cost), get_midpoint(p1, p2), textcoords="offset points", xytext=(0, 0.01), ha='center')


        ax.set_xlim(-1.25, 1.25)
        ax.set_ylim(-1.25, 1.25)
        plt.show()

    def get_detailed_dataframe(self):
        values = []
        paths = []
        for vertice in self.vertices:
            values.append(vertice.value)
            paths.append(vertice.paths)
        return pd.DataFrame({
            "IDs": self.ids,
            "Values": values,
            "Paths (id, cost)": paths,
        })
