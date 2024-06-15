# Coordinated Group Detection

This tool helps identify coordinated groups based on social media data. It can be used to analyze social media datasets for coordinated activities. The main functionality includes detecting coordinated group activities within a specified time window and calculating user and group statistics, assuming that coordination can be defined as two or more accounts which disseminate an object, (e.g., post, hashtag, link, etc.), within a specified time range (*time window*) with a number of repeated occurences (*minimum repetitions*).

This project pulls from the great work conducted by the people at [CooRNet](https://github.com/fabiogiglietto/CooRnet.git)[^1] [^2] [^3], but instead of focusing primarily on coordinated link sharing, this tool empowers digital analysts who wish to examine other forms of coordination, e.g., **co-posting**, **co-sharing**, **hashtag inflation**., etc. This tool is therefore useful in research concerning co-posts or instances of co-posting where the same message or *similar*[^4] content are posted by multiple users. 

The small changes and optimizations include the following: 
1. Refactored to Python
2. Refactored to first filter minimimum repetitions prior to examining timestamp differences thus reducing compute loads.
3. Alterations to include a broader definition of *objects* to be investigates which can take on any form as detailed below. 


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


[^1]: Giglietto, F., Righetti, N., Rossi, L., & Marino, G. (2020). Coordinated Link Sharing Behavior as a Signal to Surface Sources of Problematic Information on Facebook. International Conference on Social Media and Society, 85--91. [doi](https://doi.org/10.1145/3400806.3400817)
[^2]: Giglietto, F., Righetti, N., Rossi, L., & Marino, G. (2020). It takes a village to manipulate the media: coordinated link sharing behavior during 2018 and 2019 Italian elections. Information, Communication and Society, 1--25. [doi](https://doi.org/10.1080/1369118X.2020.1739732)
[^3]: Giglietto, F., Righetti, N., & Marino, G. (2019). Understanding Coordinated and Inauthentic Link Sharing Behavior on Facebook in the Run-up to 2018 General Election and 2019 European Election in Italy. [doi](https://doi.org/10.31235/osf.io/3jteh)
[^4]: *My research team and I are currently working on integrating this technique with transformer models, which would help to identify semantic similarity among messages, which could in turn be a form of 'object'.*
