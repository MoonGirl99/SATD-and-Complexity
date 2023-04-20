# SATD and Complexity

This project involves investigating the relationship between self-admitted technical debt (SATD) and code complexity. 

It works on:
1) Checking out a repository, 
2) Creating a Python script to extract complexity, name, and SATD comments for each method, 
3) Extending the script to collect data for modified Java files,
4) Extracting patterns in commit messages. 

Then uses statistical tests to evaluate the correlation between SATD and code complexity.

The process of doing this project is:
1) List Java Files
2) Extract Complexity
3) Extract SATD comments
4) Statistical tests on data

Statistical Test: T-test

Packages which are used in this project:
1) Lizard (Provided by the Professor)
2) [Seaborn](https://seaborn.pydata.org/)
3) [Matplotlib](https://matplotlib.org/stable/index.html)
4) [Numpy](https://numpy.org/)
5) [Pandas](https://pandas.pydata.org/)
6) [SciPy](https://scipy.org/)