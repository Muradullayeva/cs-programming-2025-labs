#1
def time_converter(value, from_unit, to_unit):
    if from_unit == 's':
        seconds = value
    elif from_unit == 'm':
        seconds = value * 60
    elif from_unit == 'h':
        seconds = value * 3600
    else:
        return "Ошибка: неверная исходная единица измерения"
    
    if to_unit == 's':
        return seconds
    elif to_unit == 'm':
        return seconds / 60
    elif to_unit == 'h':
        return seconds / 3600
    else:
        return "Ошибка: неверная целевая единица измерения"

a = int(input("Введите количество исходной единицы измерения времени: "))
b = str(input("Введите исходную единицу измерения (s, m, h): "))
c = str(input("Введите целевую единицу измерения (s, m, h): "))
print("Ваше время", a, "переведено из", b, "в", c)
print("Результат:", time_converter(a, b, c))

#2
def calculate_profit (amount, years) :
    if amount < 30000:
        return "Ошибка: минимальный вклад — 30 000 рублей"
    bonus = min ((amount // 10000) * 0.3, 5)

    if years <= 3:
        rate = 3
    elif 4 < years <= 6:
        rate = 5
    else:
        rate = 2

    total_rate = rate + bonus
    total_amount = amount * ((1 + total_rate / 100) ** years)
    profit = total_amount - amount

    return round (profit, 2)

a = int(input("Введите сумму вклада: "))
y = int(input ("Введите количество лет: "))

print ( "Ваш доход по вкладу: ", calculate_profit (a,y), " руб.")
#3
def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

def primes_in_range(start, end):
    if start > end:
        return "Ошибка! Первая граница больше второй."
    
    primes = []
    for num in range(start, end + 1):
        if is_prime(num):
            primes.append(num)
    
    if not primes:
        return "Ошибка! Простых чисел в указанном диапазоне нет."
    return primes

s = int(input("Введите меньшую границу диапазона чисел: "))
e = int(input("Введите большую границу диапазона чисел: "))
print("Простые числа из указанного диапазона:")
print(primes_in_range(s, e))

#4
def add_matrices_compact():
    try:
        n = int(input("Введите размер квадратной матрицы (n > 2): "))
        if n <= 2:
            print("Ошибка размера")
            return
        
        print(f"\nВведите элементы первой матрицы {n}x{n}:")
        print("(введите все числа матрицы построчно, разделяя пробелами)")
        matrix1 = []
        for i in range(n):
            row = list(map(int, input().split()))
            if len(row) != n:
                print("Ошибка. Размерность не совпадает с количеством элементов строки")
                return
            matrix1.append(row)
        
        print(f"\nВведите элементы второй матрицы {n}x{n}:")
        matrix2 = []
        for i in range(n):
            row = list(map(int, input().split()))
            if len(row) != n:
                print("Ошибка. Размерность не совпадает с количеством элементов строки")
                return
            matrix2.append(row)
        
        result = []
        for i in range(n):
            row = []
            for j in range(n):
                row.append(matrix1[i][j] + matrix2[i][j])
            result.append(row)
        
        print("\nРезультат сложения матриц:")
        for row in result:
            print(" ".join(str(num) for num in row))
            
    except (ValueError, IndexError):
        print("Ошибка!")

add_matrices_compact()

#5
def is_palindrome(text):
    # Приводим к нижнему регистру и оставляем только буквы
    cleaned = ''.join(char.lower() for char in text if char.isalpha())
    # Сравниваем строку с её обратной версией
    return cleaned == cleaned[::-1]

# Примеры
print(is_palindrome("А роза упала на лапу Азора"))
print(is_palindrome("Borrow or rob"))
print(is_palindrome("Алфавитный порядок"))
