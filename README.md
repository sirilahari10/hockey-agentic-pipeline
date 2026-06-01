# Hockey R&D: Agentic Data Pipeline

As the description notes said, modern sports R&D isn't just about storing data—it's about "exploring and prototyping agentic AI workflows" to assist in decision support. 

This repository demonstrates a lightweight pipeline that bridges traditional Data Engineering (dbt/SQL transformations) with Agentic AI. 

## The Architecture
1. Raw Ingestion (Bronze): Simulates raw, messy NHL play-by-play (PxP) and shift data.
2. dbt Transformation (Silver/Gold): Cleans events, calculates Expected Goals (xG), and maps events to player shifts.
3. Agentic AI Layer: An LLM-simulated agent that parses the Gold tables to surface natural-language coaching insights (e.g., identifying fatigue-driven defensive breakdowns).

