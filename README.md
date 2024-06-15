# Coordinated Group Detection

This tool helps identify coordinated groups based on social media data. It can be used to analyze social media datasets for coordinated activities. The main functionality includes detecting coordinated group activities within a specified time window and calculating user and group statistics.

This project is based on great work conducted by the people at [CooRNet](https://github.com/fabiogiglietto/CooRnet.git)[^1][^2][^3], but instead of focusing primarily on coordinated link sharing enpowers digital analysts who wish to examine other forms of coordination, e.g., co-posting, co-sharing, and hashtag inflation. The small changes and optimizations include the following: 
1. Refactored to Python
2. Refactored to first filter minimimum repetitions prior to examining timestamp differences thus reducing compute loads.
3. Alterations to include a broader definition of *objects* to be investigates which can take on any form as detailed below. 

[^1]: Giglietto, F., Righetti, N., Rossi, L., & Marino, G. (2020). Coordinated Link Sharing Behavior as a Signal to Surface Sources of Problematic Information on Facebook. International Conference on Social Media and Society, 85--91. [doi](https://doi.org/10.1145/3400806.3400817)
## Features

- Detects coordinated groups based on shared content within a time window.
- Filters users and content based on a minimum repetition threshold.
- Provides detailed group and user statistics.

## Installation

Clone the repository and install the dependencies:

```bash
git clone https://github.com/yourusername/coordinated-group-detection.git
cd coordinated-group-detection
pip install -r requirements.txt
