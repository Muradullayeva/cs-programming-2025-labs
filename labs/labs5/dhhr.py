#1

numbers = [5, 12, 3, 8, 15, 7, 3, 20, 1, 9]

for i in range(len(numbers)):
    if numbers[i] == 3:
        numbers[i] = 30

print("Результат:", numbers)

#2

numbers = [2, 5, 8, 3, 7]
squares = [x**2 for x in numbers]

print("Исходный список:", numbers)
print("Квадраты чисел:", squares)

#3

numbers = [12, 45, 23, 67, 34, 89, 56]
max_number = max(numbers)
result = max_number / len(numbers)

print(f"Список: {numbers}")
print(f"Максимальное число: {max_number}")
print(f"Длина списка: {len(numbers)}")
print(f"Результат деления: {result:.4f}")

#4

def sort_tuple(t):
    try:
        return tuple(sorted(t))
    except TypeError:
        return t

# Тестирование
tuple1 = (5, 2, 8, 1, 9)
tuple2 = (3, "hello", 7, 4)

print("Кортеж 1 до сортировки:", tuple1)
print("Кортеж 1 после сортировки:", sort_tuple(tuple1))
print("Кортеж 2 до сортировки:", tuple2)
print("Кортеж 2 после сортировки:", sort_tuple(tuple2))

#5

products = {
    "хлеб": 50,
    "молоко": 80,
    "сыр": 300,
    "яблоки": 120,
    "кофе": 450,
    "чай": 200
}

min_price = min(products.values())
max_price = max(products.values())

min_products = [name for name, price in products.items() if price == min_price]
max_products = [name for name, price in products.items() if price == max_price]

print("Товары с минимальной ценой:", min_products, f"({min_price} руб.)")
print("Товары с максимальной ценой:", max_products, f"({max_price} руб.)")

#6

elements = ["apple", "banana", "cherry", "date"]
result_dict = {element: element for element in elements}

print("Исходный список:", elements)
print("Результирующий словарь:", result_dict)

#7

eng_rus_dict = {
    "apple": "яблоко",
    "banana": "банан",
    "cat": "кот",
    "dog": "собака",
    "house": "дом"
}

rus_word = input("Введите русское слово: ")

rus_eng_dict = {russian: english for english, russian in eng_rus_dict.items()}

if rus_word in rus_eng_dict:
    print(f"Перевод на английский: {rus_eng_dict[rus_word]}")
else:
    print("Слово не найдено в словаре")

#8

import random

choices = ["камень", "ножницы", "бумага", "ящерица", "спок"]

rules = {
    "камень": ["ножницы", "ящерица"],
    "ножницы": ["бумага", "ящерица"],
    "бумага": ["камень", "спок"],
    "ящерица": ["бумага", "спок"],
    "спок": ["камень", "ножницы"]
}

print("Доступные варианты:", ", ".join(choices))
user_choice = input("Ваш выбор: ").lower()

if user_choice not in choices:
    print("Неверный выбор!")
else:
    computer_choice = random.choice(choices)
    print(f"Компьютер выбрал: {computer_choice}")

    if user_choice == computer_choice:
        print("Ничья!")
    elif computer_choice in rules[user_choice]:
        print("Вы победили!")
    else:
        print("Компьютер победил!")

#9

words = ["яблоко", "груша", "банан", "киви", "апельсин", "ананас", "арбуз"]

result = {}
for word in words:
    first_letter = word[0]
    if first_letter not in result:
        result[first_letter] = []
    result[first_letter].append(word)

print("Исходный список слов:", words)
print("Сгруппированный словарь:", result)

#10

students = [
    ("Анна", [5, 4, 5, 4]),
    ("Иван", [3, 4, 4, 3]),
    ("Мария", [5, 5, 5, 5]),
    ("Петр", [4, 3, 5, 4])
]

# словарь средних оценок
average_grades = {}
for name, grades in students:
    average = sum(grades) / len(grades)
    average_grades[name] = average

# студент с макс ср баллом
best_student = max(average_grades, key=average_grades.get)
best_grade = average_grades[best_student]

print("Средние оценки студентов:")
for student, avg in average_grades.items():
    print(f"{student}: {avg:.2f}")

print(f"\n{best_student} имеет наивысший средний балл: {best_grade:.2f}")