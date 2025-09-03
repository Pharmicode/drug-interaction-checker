# Drug Interaction Checker (openFDA)

Simple CLI that fetches FDA label excerpts for two drugs and highlights potential cross-mentions in the **Drug Interactions** section.

## Why not RxNav?
NIH retired the RxNav interaction endpoints (404s). This project now uses **openFDA** drug labels, which are public and actively maintained.

## Features
- Fetches label text for each drug (Drug Interactions, Warnings & Cautions, Warnings, Precautions)
- Simple cross-mention check (e.g., “warfarin” mentioned in ibuprofen’s interactions)
- Pure Python, no keys needed

## Setup
```bash
py -3 -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt

## run
.\.venv\Scripts\python -u .\main.py

