def get_grade(marks):
    if marks >= 90:
        return "A", "Excellent! Outstanding performance! 🌟"
    elif marks >= 80:
        return "B", "Very Good! Keep it up! 👍"
    elif marks >= 70:
        return "C", "Good job! Keep improving! 😊"
    elif marks >= 60:
        return "D", "You passed! Keep working harder! 💪"
    else:
        return "F", "Don't give up! Learn from this and try again! 📚"


def get_valid_marks():
    while True:
        try:
            marks = float(input("Enter marks (0-100): "))

            if 0 <= marks <= 100:
                return marks
            else:
                print("Invalid input! Marks must be between 0 and 100.")

        except ValueError:
            print("Invalid input! Please enter a valid number.")


def main():
    print("===== STUDENT GRADE CALCULATOR =====")

    name = input("Enter student name: ")
    marks = get_valid_marks()

    grade, message = get_grade(marks)

    print("\n===== RESULT FOR", name.upper(), "=====")
    print(f"Marks: {marks}/100")
    print(f"Grade: {grade}")
    print(f"Message: {message}")


main()
