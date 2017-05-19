This program focuses on constraint satisfaction problems. I implement AC-3 algorithm, as well as a backtracking algorithm to solve sudoku problems. The current driver.py uses backtracking algorithm to solve each sudoku problem. AC-3 is not capable of solving all problems by nature of the algorithm.

To run (compiled in python 2):

python driver.py <input_string>

<input_string> should be a representation of a sudoku puzzle which starts from the top-left corner of the board and enumerates the digits in each tile row by row. Every time you input a string it will generate a output.txt containint a single line of text representing a finished sudoku board.

Example input_string:

003020600900305001001806400008102900700000008006708200002609500800203009005010300

In output.txt:

483921657967345821251876493548132976729564138136798245372689514814253769695417382

In the directory there is a sudokus_start.txt with 400 example sudoku possible instances of input_string. sudokus_finish.txt is the expected answers for those 400 sudoku problems. The output_backtrack.txt is my output from the backtracking algorithm which completes all 400 problems.

AC3 algorithm completes successfully 3 of the 400 problems, specifically lines, found in "output_AC3.txt":
1, 2, 332

Back tracking algorithm completes all 400 successfully. It is the algorithm
being ran in the driver .run() method.  
