# utils.py
import os

def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)          # bug: division by zero if empty

def read_config(filepath):
    f = open(filepath)                   # bug: file never closed
    return eval(f.read())                # bug: eval is a security risk

def get_user(users, user_id):
    for user in users:
        if user["id"] == user_id:
            return user["name"].upper()  # bug: KeyError if 'name' missing

def merge_lists(a, b=[]):               # bug: mutable default argument
    a.extend(b)
    return a
