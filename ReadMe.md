=> Minesweeper Board working correctly
=> Right click toggle facility gives an option for suspecting Mines
=> First click Make sures you dont select a mine and reveals the blocks around it


Update:

tkinter thing not needed as such
Made a 2D array of 16X30
Placed random mines in it
Ishan tu CLI_real_use.py chala ke dekh skta h

ab mai acha heuristic dekh rha hu which can automate this!

time hai abhi

if Sat night tak nhi milta h!
Then we will use the github wala solution

Thanks!

#over


Message 2

Three approaches I have found to automate/solve this neatly!

1.) basic probabilistic algorithm to make safer moves. The algorithm will attempt to reveal cells with the lowest probability of containing a mine based on the information available

2.)  a more advanced strategy. This could involve implementing a constraint satisfaction algorithm that uses the information from the numbers revealed to deduce the positions of mines more effectively.

    Implement a constraint satisfaction algorithm that can analyze the numbers on the board to deduce safe moves.
    The algorithm will consider the numbers revealed on the board as constraints and try to satisfy them by placing flags or revealing cells.
    The algorithm will use backtracking to handle situations where multiple solutions are possible, choosing the move that satisfies the most constraints.
    Run the simulation with the new algorithm and observe the results.

3.) Aur last hai a machine learning model that can learn from previous games to predict the probability of a mine being in a particular location.
