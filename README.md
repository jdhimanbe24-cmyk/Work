# Week 1 Python Basics - Personal Introduction Program

## Project Overview

The **Personal Introduction Program** is a beginner-friendly Python program that asks the user for basic personal information and displays a friendly personalized welcome message.

The project was created to practice the fundamental Python concepts covered in Week 1.

## Objectives

- Learn how to run a Python program.
- Understand variables and data storage.
- Use `input()` to collect information from the user.
- Use `print()` to display information.
- Practice strings and f-strings.
- Practice basic program flow and formatting.
- Create and organize a simple GitHub project.

## Concepts Learned

### 1. Variables

Variables store information that can be used later in a program.

Example:

```python
name = input("What is your name? ")
```

### 2. User Input

The `input()` function allows the program to receive information from the user.

The program asks for five pieces of information:

- Name
- Age
- City
- Hobby
- Favorite food

### 3. Strings

The program works with text values such as names, cities, hobbies, and food.

### 4. F-Strings

F-strings are used to insert variable values into messages.

Example:

```python
print(f"Welcome, {name}!")
```

### 5. Print Function

The `print()` function displays messages and results on the screen.

## Code Structure

```text
Week-1-Python-Personal-Introduction/
├── README.md
├── personal_intro.py
├── requirements.txt
└── screenshot.png
```

## Setup Instructions

### Step 1: Install Python

Download and install Python from the official Python website.

During installation on Windows, make sure to enable **Add Python to PATH**.

### Step 2: Verify Python

Open a terminal or command prompt and run:

```bash
python --version
```

If that does not work on Windows, try:

```bash
py --version
```

### Step 3: Run the Program

Open the project folder in a terminal and run:

```bash
python personal_intro.py
```

On Windows, you can also use:

```bash
py personal_intro.py
```

## Sample Output

```text
========================================
     Welcome to the Personal Intro!
========================================

What is your name? Alex
How old are you? 21
Which city do you live in? Delhi
What is your favorite hobby? Coding
What is your favorite food? Pizza

========================================
🎉 Welcome, Alex! 🎉
========================================
You are 21 years old and live in Delhi.
You enjoy Coding and your favorite food is Pizza.
It's great to meet you!
========================================
```

## Technical Details

### Input

The program uses the Python `input()` function to collect user information.

### Variables

Five variables are used:

- `name`
- `age`
- `city`
- `hobby`
- `food`

### Data Structures

No complex data structures are required for this project. The project primarily uses string variables.

### Algorithm / Program Flow

1. Display a welcome heading.
2. Ask the user for their name.
3. Ask for their age.
4. Ask for their city.
5. Ask for their favorite hobby.
6. Ask for their favorite food.
7. Display the collected information using f-strings.
8. Display a friendly closing message.

## Testing Evidence

### Test Case 1 - Normal Input

Input:

```text
Name: Alex
Age: 21
City: Delhi
Hobby: Coding
Food: Pizza
```

Expected result:

The program displays Alex's information in a personalized welcome message.

### Test Case 2 - Different Input

Input:

```text
Name: Sam
Age: 19
City: Mumbai
Hobby: Drawing
Food: Pasta
```

Expected result:

The program displays Sam's information correctly.

### Test Case 3 - Single-word and multi-word values

Input:

```text
Name: Rahul
Age: 20
City: New Delhi
Hobby: Playing Guitar
Food: Butter Chicken
```

Expected result:

The program accepts the values and displays them correctly.

## What I Learned

Through this project, I learned the basics of Python programming, including variables, strings, user input, output using `print()`, and f-strings. I also learned how a Python program executes statements step by step and how to organize a small project for GitHub.

## Future Improvements

The program could be improved in the future by:

- Validating the age entered by the user.
- Handling empty inputs.
- Adding more personal questions.
- Creating a graphical user interface.
- Saving the information to a file.

## Conclusion

This project provides a simple introduction to Python programming and demonstrates how user input can be collected, stored, and displayed in a personalized format.
