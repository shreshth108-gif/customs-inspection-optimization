"""Model 2: two-dimensional container stacks with opening and movement costs.
Interactive menu: (1) example plot, (2) Monte Carlo mean/std of undetected
contraband, (3) smugglers that learn from seizures. Listing from Appendix B."""


# Import the necessary libraries.
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import random
import numpy as np

# q_i is the probability of drugs being in a container.
# For now, it is assumed that this value is constant.
q_i = 0.3

# Define the number of horizontal crates n.
n = 10
# Define maximum height.
m = 5

# Define opening cost and movement cost.
c_o = 100
c_m = 1000

# Define a lambda value
LAMBDA = 0.0001

width_box = 1
height_box = 0.5

# Function definitions.
def I_p(i,j):
    return containers[i][j]

def u(i: int, j: int, costs) -> float:
    return q_i/(q_i + costs[i][j])  

def c() -> float:
    """ This function is used to calculate the costs of opening a crate.
    """
    
    costs = [[0] * m for _ in range(n)]
    
    for i in range(n):
        crates = 0
        for j in range(m):
            crate_present = I_p(i, m - 1 - j)
            crates += crate_present
            
            if crate_present: costs[i][m - 1 - j] += c_o + 2 * crates * c_m
            
    costs[0][0] = c_o * containers[0][0]
    costs[-1][0] = c_o * containers[-1][0]
    
    for i in range(1, n-1):
        if I_p(i,0):
            if not (I_p(i-1,0) * I_p(i+1,0)): 
                costs[i][0] = c_o    
    return costs

# Set the random seed
random.seed(9999)

print("What would u like to do?")
print("1. look at the plot for an example")
print("2. find mean and variance through simulation")
print("3. Implement drug dealers learning model then print the first 3 and the last 3 simulations.")
choice = int(input())

def plot(containers, drugs, costs):
    x_positions = [(i+1/2) * width_box for i in range(n)]

    fig, ax = plt.subplots()

    ax.set_xlim([-width_box / 2, (n + 1/2) * width_box])
    ax.set_ylim([0, (m+1) * height_box])

    ax.xaxis.set_ticks( [ i * width_box / 2 for i in range(1,2*n,2)])
    ax.yaxis.set_ticks( [ i * height_box / 2 for i in range(1,2*m,2)])

    ax.set_xticklabels([str(i) for i in range(1,n+1)])
    ax.set_yticklabels([str(i) for i in range(1,m+1)])

    container_dict = {}

    for i in range(n):
        for j in range(m):
            if containers[i][j]:
                rect = Rectangle((i*width_box,j * height_box), width_box, height_box, 
                                 facecolor="gray", edgecolor="black")

                container_dict[(i,j)] = rect

                ax.add_patch(rect)

    ax.set_xlabel("Horizontal container index");
    ax.set_ylabel("Vertical container index");

    for (i,j) in container_dict.keys():
        if drugs[i][j]:
                container_dict[(i,j)].set_facecolor("red")   
        if LAMBDA <= u(i,j, costs ):
            container_dict[(i,j)].set_facecolor("blue")
            if drugs[i][j]:
                container_dict[(i,j)].set_facecolor("green")
                

    for i in range(n):
        for j in range(m):
            if costs[i][j]:
                plt.text((i + 1/2) * width_box, (j+1/2) * height_box, str(costs[i][j]), 
                         fontsize = 8, fontweight="bold", color="yellow", 
                         horizontalalignment='center', verticalalignment='center')

    # Save the figure
    # plt.savefig(f"Containers with lambda = {LAMBDA_VALUE}.png")

    # Display plot
    plt.show()

if (choice == 1):
    
    containers = [[False] * m for i in range(n)]
    # initializing drugs to randomly assign drugs to containers
    drugs = [[False] * m for i in range(n)]
    

    for i in range(n):
        num_of_containers = random.randint(0,m)  
        for j in range(num_of_containers):
            containers[i][j] = True
            d = random.random()
            if (d < q_i):  
                drugs[i][j] = True
    costs = c()
                  
    plot(containers, drugs, costs)
    

elif (choice == 2):
    
    # initialize drugs history to store lost drugs.
    Drugs_history = []
    
    for i in range(100):
        
        containers = [[False] * m for i in range(n)]

        # initializing drugs to randomly assign drugs to containers
        drugs = [[False] * m for i in range(n)]
        
        # initializing drugs lost variable to find how many drugs were not caught
        drugs_lost = 0
        
        # randomly assigning drugs to crates
        for i in range(n):
            num_of_containers = random.randint(0,m)  
            for j in range(num_of_containers):
                containers[i][j] = True
                d = random.random()
                if (d < q_i):  
                    drugs[i][j] = True
                    drugs_lost += 1
                   
        # finding the number of drugs that pass through
        costs = c()         
        for i in range(n):
            for j  in range(m):
                if drugs[i][j] and LAMBDA <= u(i,j, costs):  
                    drugs_lost -= 1
        Drugs_history.append(drugs_lost)
        
                    
    D_data = np.array(Drugs_history)
    D_data.std(), D_data.mean()
    print(D_data.std(), D_data.mean())


elif (choice == 3):

    # initialize drug dealers learning algorithm.

    Learning = [[0]*m for i in range(n)]
                  
    no_of_iterations = 1000
    
    for iterations in range(no_of_iterations):
        containers = [[False] * m for i in range(n)]

        # initializing drugs to randomly assign drugs to containers
        drugs = [[False] * m for i in range(n)]
        # initializing drugs lostr variable to find how many drugs were not caught
        drugs_lost = 0

        for i in range(n):
            num_of_containers = random.randint(0,m)  
            for j in range(num_of_containers):
                containers[i][j] = True
                d = random.random()
                if (d < q_i + Learning[i][j]):  
                    drugs[i][j] = True
                    drugs_lost += 1
        
        drugs_found = 0
                  
        # finding the number of drugs that pass through
        costs = c()         
        for i in range(n):
            for j  in range(m):
                if drugs[i][j] and LAMBDA <= u(i,j, costs):  
                    drugs_lost -= 1
                    drugs_found += 1
                  
                    
        #drug dealers learning algorithm
        x = 0.01 # how fast they learn

        for i in range(n):
            for j in range(m):
                if drugs[i][j]:
                    if LAMBDA <= u(i,j, costs):
                        Learning[i][j] -= x/drugs_found
                    else:
                        Learning[i][j] += x/drugs_lost
                        
        l = [0,1,2, no_of_iterations -1, no_of_iterations -2, no_of_iterations -3]
        
        if (iterations in l):
            plot(containers, drugs, costs)


