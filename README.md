# Distributed Depth-First Search with Token

## Description
This project implements a distributed system that performs a Depth-First Search (DFS) using a "TOKEN" as the traversal agent.

## Details:
- The system uses **AMQP middleware** for communication between nodes.
- **1-second delay** is implemented to observe the sequence of messages being sent and received by each component.
- Upon receiving the last **R** from the final neighbor, the initiator will print the total time in seconds since it first sent the **T** message.

#### Logic Overview:
- **INITIATOR**: This node starts the traversal by sending a **TOKEN (T)** to its neighbors. It begins visiting other nodes.
- **IDLE**: A node in this state waits for a **TOKEN (T)**. When it receives it, it sends the **TOKEN (T)** to its unvisited neighbors.
- **VISITED**: A node in this state marks neighbors as visited and continues the traversal. If it receives a **RETURN (R)** or **BACK EDGE (B)**, it moves on to visit the next node.
- **OK**: Once all neighbors have been visited, the node enters the **OK** state. If it is not the initiator, it sends a **RETURN (R)** back to the origin.

And below is the pseudocode that represents the main logic:

```bash

// States
enum State { INITIATOR, IDLE, VISITED, OK }

// Initial States
State[] initialStates = { INITIATOR, IDLE }

// Final States
State[] finalStates = { OK }

// Transitions

// INITIATOR
if (state == INITIATOR) {
    // Spontaneously
    non_visited = N(x)
    initiator = true
    visit()
}

// IDLE
if (state == IDLE) {
    // Receiving (T) from origin
    entry = origin
    non_visited = N(x) - { origin }
    initiator = false
    visit()
}

// VISITED
if (state == VISITED) {
    // Receiving (T) from origin
    if (msg == "T") {
        non_visited = non_visited - { origin }
        send("B", origin)
    }

    // Receiving (R)
    if (msg == "R") {
        visit()
    }

    // Receiving (B)
    if (msg == "B") {
        visit()
    }
}

// Procedure: visit()
function visit() {
    if (non_visited != empty) {
        next = non_visited.pop()
        state = VISITED
        send("T", next)
    } else {
        state = OK
        if (!initiator) {
            send("R", entry)
        }
    }
}
```

## Topology
![Topology](https://github.com/user-attachments/assets/6e4ac133-9608-4387-a64c-ce62f5269c4a)


## Execution

To run the system, use the following commands:

1. Run the `path.py` script with the respective nodes:
    ```bash
    python path.py A B
    python path.py B C D
    python path.py C B D
    python path.py D C B E
    python path.py E D
    ```

2. Run the `starter.py` script to initiate the process with the **TOKEN**:
    ```bash
    python starter.py T A
    ```

### Terminology:
- **T (TOKEN)**: The message used to start the depth-first traversal.
- **R (RETURN)**: The message sent when returning from a node.
- **B (BACK EDGE)**: The message sent when backtracking.

## Clone the repository:
   ```bash
   git clone  https://github.com/ThomasFrentzel/Distributed-Path
