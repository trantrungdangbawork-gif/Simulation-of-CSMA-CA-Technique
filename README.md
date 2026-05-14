# Simulation-of-CSMA-CA-Technique

## Overview

This project simulates the CSMA/CA (Carrier Sense Multiple Access with Collision Avoidance) protocol used in IEEE 802.11 wireless communication systems. The simulation models how multiple wireless nodes share a common channel and avoid packet collisions using mechanisms such as carrier sensing, random backoff, ACK, and optional RTS/CTS.

The project was developed to analyze network performance under different traffic conditions and node densities.

---

## Key Features

* Time-slot based CSMA/CA simulation
* Optional RTS/CTS collision avoidance mechanism
* DIFS and SIFS timing simulation
* Random backoff algorithm
* ACK and retransmission handling
* Throughput and collision performance evaluation
* Trade-off analysis between RTS/CTS overhead and collision reduction

---

## Communication Concepts

This project involves several wireless communication and networking concepts, including:

* IEEE 802.11 MAC protocol
* Carrier sensing
* Collision avoidance
* Backoff mechanism
* Optional RTS/CTS mechanism
* Wireless channel contention
* Throughput analysis

---

## Tools and Technologies

* Python
* Visual Studio Code
* Matplotlib
* NumPy

---

## Simulation Objectives

The simulation evaluates:

* Modeled node behavior using time-slot
* Network throughput under different numbers of nodes
* Number of collision in dense wireless environments
* Effectiveness of RTS/CTS mechanism
* Impact of retransmission and backoff strategies

---

## How to Run

1. Clone the repository
2. Open the project folder in Visual Studio Code
3. Install required Python libraries:

```bash
pip install numpy matplotlib
```

4. Run the main Python file:

```bash
python main.py
```

---


