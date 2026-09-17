# Poker Player Analysis

This project analyzes a large poker dataset to study player behavior and preflop tendencies, with an initial focus on measuring **3-bet frequency** across players.

## Dataset

You can find the full dataset here, https://zenodo.org/records/13997158

The analysis uses a large structured poker dataset containing three primary tables:

* `hands` — approximately 21.6 million poker hands
* `player_hands` — approximately 116.9 million player-hand records
* `actions` — approximately 322.9 million individual player actions


The dataset contains information about individual hands, players participating in each hand, and the sequence of actions taken during each betting round.

## Technologies

* Python
* pandas
* NumPy
* SQL / structured data querying
* Jupyter Notebook

## Goals

The broader goal of the project is to build a scalable pipeline for analyzing poker strategy and player tendencies from large-scale hand-history data. Eventually I plan to get more recent datasets and develop a full profitable online poker strategy from data analysis.
