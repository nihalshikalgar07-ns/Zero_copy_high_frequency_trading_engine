Zero-Copy High-Frequency Trading Engine

A high-performance High-Frequency Trading (HFT) Engine designed to process a large number of orders with minimal latency. The project focuses on zero-copy inter-process communication (IPC) using memory-mapped files, efficient order processing, and a price-time priority matching engine.

Project Overview

Traditional Python-based communication between processes often relies on serialization mechanisms such as "pickle", which can introduce CPU overhead and additional latency.

This project explores a zero-copy communication approach using memory-mapped files ("mmap") to exchange order data between processes without repeatedly copying and serializing large amounts of data.

The system receives market orders, transfers them through a shared-memory-based communication layer, processes them through a trading engine, and matches compatible buy and sell orders.
 
Architecture

Order Producer
      │
      ▼
┌──────────────────┐
│   mmap / Ring    │
│      Buffer      │
└──────────────────┘
      │
      ▼
Order Reader
      │
      ▼
Trade Engine
      │
      ▼
Matching Engine
      │
      ▼
Executed Trades
      │
      ▼
Latency Monitoring

Key Features

- Zero-Copy IPC
 
  - Uses Python "mmap" for shared memory communication.
  - Reduces unnecessary data copying between processes.

- Ring Buffer
 
  - Implements a fixed-size circular buffer for efficient order exchange.
  - Uses read and write positions to manage producer-consumer communication.

- High-Performance Order Processing
 
  - Designed to handle a high volume of incoming orders.
  - Uses efficient binary data structures instead of heavy serialization.

- Order Matching Engine
 
  - Supports BUY and SELL orders.
  - Matches orders based on price-time priority.

- Low-Latency Measurement
 
  - Uses "time.perf_counter_ns()" for high-resolution latency measurement.
  - Measures the time taken by the trading engine to process orders.

- Cython Optimization
 
  - Cython is used to optimize performance-critical sections.
  - Python objects can be replaced with C-level types where appropriate.

- Market Simulation
 
  - Generates simulated orders to test the engine under high order throughput.

- Monitoring Dashboard
 
  - Provides a dashboard for observing order processing and engine performance.

Technologies Used

- Python
- Cython
- mmap
- struct
- asyncio
- Inter-Process Communication (IPC)
- Ring Buffer
- Streamlit
- Git & GitHub

Project Structure

zero-copy-hft-engine/
│
├── producer/
│   └── order_producer.py
│
├── reader/
│   └── mmap_reader.py
│
├── engine/
│   ├── engine.py
│   └── matching_engine.py
│
├── simulator/
│   └── market_simulator.py
│
├── dashboard/
│   └── dashboard.py
│
├── cython/
│   └── optimized_engine.pyx
│
├── main.py
├── requirements.txt
└── README.md

How It Works

1. Order Generation

The market simulator generates buy and sell orders containing information such as:

- Order ID
- Price
- Quantity
- Order side
- Symbol

2. Memory-Mapped Communication

Orders are written into a memory-mapped file.

mmap
  ↓
Shared Memory Region
  ↓
Ring Buffer

Instead of serializing Python objects, the order is stored in a predefined binary format using the "struct" module.

3. Order Reading

The order reader monitors the shared memory region and reads new orders using the current read position.

4. Trade Engine

The Trade Engine receives orders from the reader and passes them to the matching engine.

It also measures processing latency using:

time.perf_counter_ns()

5. Matching Engine

The matching engine maintains BUY and SELL order books.

Orders are matched according to price-time priority.

For example:

BUY Orders              SELL Orders
---------               ----------
Price: 101              Price: 100
Price: 99               Price: 102
Price: 98               Price: 103

If the highest BUY price is greater than or equal to the lowest SELL price, a trade can be executed.

6. Latency Monitoring

The engine records timestamps before and after order processing:

Engine Entry
     │
     ▼
Order Processing
     │
     ▼
Matching
     │
     ▼
Engine Exit

Latency is calculated as:

Engine Latency =
Engine Exit Timestamp - Engine Entry Timestamp

Performance Focus

The main objective of this project is to study techniques used for low-latency order processing, including:

- Memory-mapped communication
- Zero-copy data exchange
- Binary data structures
- Ring buffers
- Efficient order matching
- Cython optimization
- High-resolution latency measurement

Performance can be evaluated using metrics such as:

- Orders processed per second
- Average latency
- Minimum latency
- Maximum latency
- Processing throughput

Zero-Copy Concept

The project avoids unnecessary serialization and copying of order objects.

Traditional approach:

Python Object
     ↓
Serialization
     ↓
Copy
     ↓
IPC
     ↓
Deserialization
     ↓
Python Object

Zero-copy-oriented approach:

Order Data
    ↓
Shared Memory / mmap
    ↓
Reader
    ↓
Trading Engine

This reduces the overhead associated with repeatedly converting Python objects into serialized representations.

Project Goals

The primary goals of this project are:

1. Build a low-latency order processing pipeline.
2. Implement zero-copy-oriented IPC using "mmap".
3. Implement a ring buffer for efficient data exchange.
4. Build a price-time priority matching engine.
5. Measure order-processing latency.
6. Explore Cython for performance-critical code.
7. Simulate high-volume market orders.
8. Provide visibility into engine performance.

Running the Project

Install the required dependencies:

pip install -r requirements.txt

Run the main engine:

python main.py

Run the dashboard:

streamlit run dashboard.py

Future Improvements

Possible future improvements include:

- Lock-free ring buffer implementation
- Better producer-consumer synchronization
- Advanced order types
- Multiple trading symbols
- More efficient order-book data structures
- Hardware-level performance optimization
- CPU affinity and process pinning
- Network-based market data ingestion
- Detailed latency benchmarking
- Linux-based performance testing
- Production-grade risk management
- 
Author

Nihal Shikalgar
