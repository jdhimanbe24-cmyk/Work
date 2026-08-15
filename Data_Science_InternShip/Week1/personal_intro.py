# Personal Introduction Program
# Week 1 - Python Basics

print("========================================")
print("     Welcome to the Personal Intro!")
print("========================================")
print()

name = input("What is your name? ").strip()
age = input("How old are you? ").strip()
city = input("Which city do you live in? ").strip()
hobby = input("What is your favorite hobby? ").strip()
food = input("What is your favorite food? ").strip()

print()
print("========================================")
print(f"🎉 Welcome, {name}! 🎉")
print("========================================")
print(f"You are {age} years old and live in {city}.")
print(f"You enjoy {hobby} and your favorite food is {food}.")
print("It's great to meet you!")
print("========================================")
