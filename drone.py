import random
import math
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class Drone:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.data = {'temperature': random.uniform(20, 30), 'humidity': random.uniform(40, 60), 'air_quality': random.uniform(0, 1)}

    def move(self):
        self.x += random.uniform(-1, 1)
        self.y += random.uniform(-1, 1)

    def get_position(self):
        return self.x, self.y

    def communicate(self, other_drones):
        for drone in other_drones:
            if drone.id != self.id:
                distance = math.sqrt((drone.x - self.x) ** 2 + (drone.y - self.y) ** 2)
                if distance < 10:  # Communication range
                    print(f"Drone {self.id} communicates with Drone {drone.id}")

    def collect_data(self):
        # Simulate data collection
        self.data = {'temperature': random.uniform(20, 30), 'humidity': random.uniform(40, 60), 'air_quality': random.uniform(0, 1)}

    def get_data(self):
        return self.data
    
    def detect_obstacles(self):
        # Simulate obstacle detection based on environmental data
        if self.data['air_quality'] < 0.3:  # Example condition for detecting obstacles
            self.environment.update_obstacles(self.x, self.y)

class CentralHub:
    def __init__(self):
        self.data_points = []

    def receive_data(self, drone):
       self.data_points.append({'id': drone.id, 'data': drone.get_data().copy()})  # Store drone's id and data

    def analyze_data(self):
     if self.data_points:
        for drone_data in self.data_points:
            drone_id = drone_data['id']
            drone_data1 = drone_data['data']
            print(f"Drone {drone_id} Data:")
            print(f"Temperature: {drone_data1['temperature']}, Humidity: {drone_data1['humidity']}, Air Quality: {drone_data1['air_quality']}")
            print()
            drone_df = pd.DataFrame([drone_data['data']])
            avg_values = drone_df.mean()

            # Plotting using seaborn for each drone
            sns.set(style="whitegrid")
            plt.figure(figsize=(6, 4))
            ax = sns.barplot(x=avg_values.index, y=avg_values.values)
            ax.set_title(f'Average Environmental Parameters for Drone {drone_id}')
            ax.set_ylabel('Average Values')
            ax.set_xlabel('Parameters')
            plt.show()

class Environment:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.obstacles = []

    def update_obstacles(self, obstacles):
        self.obstacles = obstacles

    def plot(self, drones):
        plt.figure(figsize=(8, 8))
        for obstacle in self.obstacles:
            plt.scatter(obstacle[0], obstacle[1], color='red', marker='x', label='Obstacle')
        for drone in drones:
            plt.scatter(drone.x, drone.y, color='blue', marker='o', label='Drone {}'.format(drone.id))  # Each drone gets its own label
        plt.xlim(0, self.width)
        plt.ylim(0, self.height)
        plt.title('Environment with Drones and Obstacles')
        plt.xlabel('X-coordinate')
        plt.ylabel('Y-coordinate')
        plt.legend()
        plt.grid(True)
        plt.show()

def main():
    num_drones = 5
    drones = [Drone(i, random.uniform(0, 100), random.uniform(0, 100)) for i in range(num_drones)]
    hub = CentralHub()
    environment = Environment(width=100, height=100)  # Define environment dimensions
    obstacles = [(20, 30), (50, 70), (80, 20)]  # Example obstacles
    environment.update_obstacles(obstacles)

    num_iterations = 10
    for _ in range(num_iterations):
        # Move drones within the environment
        for drone in drones:
            drone.move()
            # Ensure drones stay within the environment bounds
            drone.x = max(0, min(drone.x, environment.width))
            drone.y = max(0, min(drone.y, environment.height))

        # Collect data and communicate
        for drone in drones:
            drone.collect_data()
            drone.communicate(drones)

        # Receive and analyze data at central hub
        for drone in drones:
            hub.receive_data(drone)
        hub.analyze_data()

        # Plot environment with drones and obstacles
        environment.plot(drones)
