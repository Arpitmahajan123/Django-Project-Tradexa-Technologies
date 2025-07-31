# Distributed SQLite Simulation
This project simulates a distributed system using multiple SQLite databases for different models (Users, Orders, and Products). Each model is stored in its own SQLite database. The program supports simultaneous insertions using multithreading to simulate concurrent operations on distributed data stores.

https://github.com/user-attachments/assets/a85e98a6-3181-4a92-9ac6-bc7dd83edfac

# Models and Databases
Model	Fields	Database
Users	id, name, email	users.db
Orders	id, user_id, product_id, quantity	orders.db
Products	id, name, price	products.db

# Features
- Simulates distributed data with separate databases.

- Performs 10 simultaneous insertions for each model using multithreading.

- All validations (e.g., field presence, value constraints) are done at the application level (not at the DB level).

Outputs results for all insertions in a single command.

# Setup
- 1. Clone the Repository
bash
Copy
Edit
git clone https://github.com/Arpitmahajan123/distributed-sqlite-simulation.git
cd distributed-sqlite-simulation
- 2. Install Requirements
This project uses Python 3 and standard libraries. No extra installations required.

# How to Run
- Run the simulation using:

- bash
Copy
Edit
python simulate_insertions.py
This will:

- Create the three databases (if they don’t exist).

- Create necessary tables.

- Simulate 10 concurrent insertions for each model using threads.

- Print the insertion results on the terminal.

- All insertions are application-validated only.

This project is ideal for testing concurrency in SQLite with thread-safe operations using separate DB files.

# Example Output

- [Users] Inserted: {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'}

- [Products] Inserted: {'id': 1, 'name': 'Laptop', 'price': 999.99}

- [Orders] Inserted: {'id': 1, 'user_id': 1, 'product_id': 1, 'quantity': 2}
