# Student Grade Calculator

## Project Overview
A beginner-friendly Python project that takes a student's name and marks, validates the marks, calculates a grade, and displays an encouraging message.

## Grading Logic
- A: 90-100
- B: 80-89
- C: 70-79
- D: 60-69
- F: 0-59

## Features
- Uses if-elif-else statements for grading logic
- Validates marks between 0 and 100
- Uses functions for reusable code
- Uses a while loop to handle invalid input
- Uses try-except for basic error handling
- Displays encouraging messages for each grade

## Setup Instructions
1. Install Python 3.
2. Download or clone this repository.
3. Open a terminal in the project folder.
4. Run:

```bash
python grade_calculator.py
```

## Code Structure
- `grade_calculator.py` - Main Python program
- `test_cases.txt` - Test cases for validation and grading
- `screenshots/` - Folder for screenshots demonstrating program functionality

## Functions Used
### get_grade(marks)
Accepts marks and returns the corresponding grade and encouraging message.

### get_valid_marks()
Uses a while loop and error handling to ensure marks are between 0 and 100.

### main()
Controls the overall program flow by collecting input, calculating the grade, and displaying the result.

## Testing
The project has been tested with:
- Valid marks for every grade
- Marks above 100
- Negative marks
- Non-numeric input
