# Sliding-Tile-Puzzle

## What this project is
This project was the first assignment for my introduction to artificial intelligence course. This assignment was meant to redefine a familiar algorithm: A*. Additional credit was offered upon the additional inclusion of heuristics other than the Manhattan distance. The additional heuristics I included were the linear conflict heuristic and the last tile heuristic.

# Involved Parties
solver.py was of my own creation, made to specifications outlined by the instructing professor, Dr. Adam A. Smith. The slidingpuzzle.py file was created by Dr. Smith to utilize the solver.py file. The .puz files were also supplied by him for the purpose of bug testing.

# References
The papers at
https://medium.com/swlh/looking-into-k-puzzle-heuristics-6189318eaca2
https://cdn.aaai.org/AAAI/1996/AAAI96-178.pdf
Were used to learn and employ the linear conflict heuristic and the last tile heuristic.

Our textbook was Hands-On Machine Learning with Scikit-Learn, Keras & TensorFlow by Aurélien Géron.
# Instructions
solver.py utilizes the heapq package.
slidingpuzzle.py utilizes the sys and tkinter packages.
To run the program, enter slidingpuzzle.py and the .puz file to solve.