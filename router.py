import numpy as np

class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        self.W1 = np.random.randn(input_size, hidden_size) / np.sqrt(input_size)
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, output_size) / np.sqrt(hidden_size)
        self.b2 = np.zeros((1, output_size))

    def forward(self, X):
        self.z1 = np.dot(X, self.W1) + self.b1
        self.a1 = self.sigmoid(self.z1)
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        self.a2 = self.softmax(self.z2)
        return self.a2

    def backward(self, X, y, output, learning_rate):
        self.dZ2 = output - y
        self.dW2 = np.dot(self.a1.T, self.dZ2)
        self.db2 = np.sum(self.dZ2, axis=0, keepdims=True)
        self.dZ1 = np.dot(self.dZ2, self.W2.T) * self.sigmoid_derivative(self.z1)
        self.dW1 = np.dot(X.T, self.dZ1)
        self.db1 = np.sum(self.dZ1, axis=0)

        self.W1 -= learning_rate * self.dW1
        self.b1 -= learning_rate * self.db1
        self.W2 -= learning_rate * self.dW2
        self.b2 -= learning_rate * self.db2

    def train(self, X, y, learning_rate):
        output = self.forward(X)
        self.backward(X, y, output, learning_rate)

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def sigmoid_derivative(self, x):
        return x * (1 - x)

    def softmax(self, x):
        exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=1, keepdims=True)

class Router:
    def __init__(self, num_nodes):
        self.num_nodes = num_nodes
        input_size = num_nodes * 2  # current node and destination node one-hot encoded
        hidden_size = num_nodes * 2
        output_size = num_nodes
        self.nn = NeuralNetwork(input_size, hidden_size, output_size)
        self.learning_rate = 0.01

    def find_route(self, start, end):
        route = [start]
        current = start
        max_hops = self.num_nodes * 2  # Failsafe to prevent infinite loops
        
        print(f"Finding route from Node {start} to Node {end}")
        
        for _ in range(max_hops):
            next_hop = self._choose_next_hop(current, end)
            print(f"  Current: {current}, Next hop: {next_hop}")
            
            if next_hop == end:
                route.append(next_hop)
                print(f"Route found: {route}")
                return route
            
            if next_hop in route:
                print(f"Loop detected, falling back to direct route")
                return [start, end]
            
            route.append(next_hop)
            current = next_hop
        
        print(f"Max hops reached, falling back to direct route")
        return [start, end]

    def _choose_next_hop(self, current, end):
        input_vector = self._create_input_vector(current, end)
        probabilities = self.nn.forward(input_vector)
        next_hop = np.argmax(probabilities)
        
        print(f"  Probabilities: {probabilities}")
        print(f"  Chosen next hop: {next_hop}")
        
        return next_hop

    def _create_input_vector(self, current, end):
        input_vector = np.zeros((1, self.num_nodes * 2))
        input_vector[0, current] = 1  # One-hot encode current node
        input_vector[0, self.num_nodes + end] = 1  # One-hot encode destination node
        return input_vector

    def update_route(self, route, actual_time):
        print(f"Updating neural network with route: {route}")
        for i in range(len(route) - 1):
            current = route[i]
            next_hop = route[i + 1]
            end = route[-1]

            X = self._create_input_vector(current, end)
            y = np.zeros((1, self.num_nodes))
            y[0, next_hop] = 1

            self.nn.train(X, y, self.learning_rate)

        # Adjust learning rate based on performance
        self.learning_rate *= 0.99  # Decay learning rate over time
        print(f"Learning rate adjusted to: {self.learning_rate}")