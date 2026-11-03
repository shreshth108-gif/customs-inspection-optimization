"""Model 1: a single row of crates. Plots which crates are inspected for a given
lambda (green = inspect, red = skip) against the opening cost. Listing from Appendix A."""

# Import the necessary libraries.
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Function definitions.

def c(i: int) -> float:
    """ This function is used to calculate the costs of opening a crate.
    """
    return (N+1)/2 - abs(i - (N+1)/2)

def u(i: int) -> float:
    return q_i/(q_i + c(i))    


# q_i is the probability of drugs being in a container.
# For now, it is assumed that this value is constant.
q_i = 0.1

# Define the number of crates N.
N = 10 
    

LAMBDA_VALUES = []
prev = 0

width_box = 1
height_box = 0.5


FINAL_ANS = []

LAMBDA_VALUE = 0.025

for i in range(0, N+1, 1):
    
    LAMBDA_VALUES.append(i/N/10)

for j in range(1, N + 1, 1):
    if (LAMBDA_VALUE <= u(j)):
        FINAL_ANS.append(1)
    else:
        FINAL_ANS.append(0)
    
print(FINAL_ANS)
        
x_positions = [(i+1/2) * width_box for i in range(N)]
y_values = [c(i) for i in range(1,N+1)]

fig, ax = plt.subplots()

ax.plot(x_positions, y_values, '*--', color="grey")

color = None

for i, val in enumerate(FINAL_ANS):
    if val:
        color = "green"
    else: 
        color = "red"
    
    ax.add_patch(Rectangle((i,0),width_box, height_box, facecolor=color, 
                           edgecolor = "black"))


ax.xaxis.set_ticks( [ 0.5 * i for i in range(1,2*N,2)])

ax.set_xticklabels([str(i) for i in range(1,N+1)])

ax.set_xlabel("Container");
ax.set_ylabel("Cost");

# Save the figure
plt.savefig(f"Containers with lambda = {LAMBDA_VALUE}.png")

# Display plot
plt.show()


