Zero-Copy High-Frequency Trading Engine

A high-performance High-Frequency Trading (HFT) Engine designed to process a large number of orders with minimal latency. The project focuses on zero-copy inter-process communication (IPC) using memory-mapped files, efficient order processing, and a price-time priority matching engine.

Project Overview

Traditional Python-based communication between processes often relies on serialization mechanisms such as "pickle", which can introduce CPU overhead and additional latency.

This project explores a zero-copy communication approach using memory-mapped files ("mmap") to exchange order data between processes without repeatedly copying and serializing large amounts of data.

The system receives market orders, transfers them through a shared-memory-based communication layer, processes them through a trading engine, and matches compatible buy and sell orders.
