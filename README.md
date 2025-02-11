# 🧩 Nonogram Maker and Solver

## 📌 Overview
This project implements a **Nonogram Maker and Solver**, allowing users to generate, visualize, and solve Nonogram puzzles efficiently. Nonograms, also known as **Picross, Griddlers, or Hanjie**, are logic puzzles where players must fill a grid based on numerical clues. These clues indicate the number of consecutive filled squares in each row and column, helping users logically deduce the correct pattern.

### 🔍 What is a Nonogram?
A Nonogram is a grid-based puzzle where each row and column has a set of **clues** specifying how many cells should be filled. The challenge is to use logic and deduction to determine the exact positions of these filled cells to complete the hidden picture.

🔹 **Maker:** Generates custom Nonogram puzzles with varying difficulty levels.  
🔹 **Solver:** Uses advanced algorithms to find solutions to given puzzles with optimized logic.  
🔹 **Visualization:** Displays puzzles and solutions in a user-friendly format for better gameplay experience.  

## 🎯 Features
✅ **Create custom Nonogram puzzles** of varying sizes, from simple to complex.  
✅ **Efficient solving algorithms** to compute puzzle solutions quickly.  
✅ **Graphical representation** of puzzles using Python visualization tools such as `matplotlib`.  
✅ **Error handling and validation** to ensure proper puzzle generation and prevent inconsistencies.  
✅ **User-friendly interface** allowing easy interaction for puzzle creation and solving.  
✅ **Random puzzle generator** for unlimited gameplay possibilities.  
✅ **Step-by-step solving approach** demonstrating logical deductions.  

## 🛠️ Installation
Follow these simple steps to get started:

1. **Clone this repository** 📥:
   ```bash
   git clone https://github.com/Arpan-shrma/Nonogram_maker_and_Solver.git
   cd Nonogram_maker_and_Solver
   ```
2. Ensure you have **Python 3.x** installed 🐍.
3. Install dependencies by running:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Running the Program
To generate and solve a Nonogram puzzle, execute the following command:
```bash
python nonogram_solver.py
```
For generating a custom puzzle:
```bash
python nonogram_maker.py
```

### 🔹 Example Commands
- Run the **Nonogram solver** with a predefined puzzle:
  ```bash
  python nonogram_solver.py --input puzzle.txt
  ```
- Generate a **random Nonogram puzzle**:
  ```bash
  python nonogram_maker.py --size 10
  ```
- Visualize the puzzle in an interactive GUI (if available):
  ```bash
  python visualization.py --file solved_puzzle.txt
  ```

## 🧠 How It Works
### 🔹 Nonogram Maker
The **Nonogram Maker** allows users to create customized puzzles or generate random ones. Key features:
- Accepts user input for defining row and column clues.
- Ensures the puzzle is solvable and adheres to logical constraints.
- Outputs a **valid Nonogram grid** for solving or playing.

### 🔹 Nonogram Solver
The **Nonogram Solver** is designed to efficiently find solutions to Nonogram puzzles using a combination of:
- **Constraint Satisfaction Problem (CSP) techniques** to systematically analyze possible solutions.
- **Backtracking Algorithm** for recursive solving in case of ambiguities.
- **Logical Deduction Techniques** to minimize brute-force operations.
- Outputs the **solved Nonogram grid** visually for better understanding.

### 🖼️ Visualization
This project includes visualization tools to enhance the user experience by:
- Displaying Nonogram grids in a clear and readable format.
- Animating the solving process step by step.
- Providing an interactive interface for puzzle exploration.

## 📂 File Structure
📜 `nonogram_maker.py` - Creates Nonogram puzzles based on user input or randomly.  
📜 `nonogram_solver.py` - Solves given Nonogram puzzles efficiently.  
📜 `visualization.py` - Handles graphical display of puzzles and solutions.  
📜 `puzzle_examples/` - Contains sample puzzles for testing.  
📜 `README.md` - Project documentation (this file 📄).  

## 🔮 Future Enhancements
🔹 Implement an **interactive GUI** for an enhanced user experience.  
🔹 Optimize solving algorithms for **larger Nonogram puzzles**.  
🔹 Add **hints, difficulty levels, and step-by-step guidance** for better learning.  
🔹 Allow users to **save and load** puzzles for future solving.  

## 📜 License
This project is **open-source** and available under the **MIT License** 📃.

## 📬 Contact
💡 Have suggestions or want to contribute? Open an **issue** or **pull request** on the repository!  

---
Enjoy solving Nonograms with this powerful tool! 🎨🧩

