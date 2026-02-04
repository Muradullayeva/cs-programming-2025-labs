#1
temp = float(input('Введите температуру: '))
if temp >= 20:
    print('Кондиционер выключен')
else:
    print('Кондиционер включен')

#2
month = int(input('Введите номер месяца: '))
if month == 12 or month == 1 or month == 2:
    print('Это зима')
if month == 3 or month == 4 or month == 5:
    print('Это весна')
if month == 6 or month == 7 or month == 8:
    print('Это лето')
if month == 9 or month == 10 or month == 11:
    print('Это осень')

#3
dog_age = input('Введите возраст собаки (в годах): ')
def is_num(dog_age):
    try:
        int(dog_age)
        return True
    except ValueError:
        return False
if is_num(dog_age) == False:
    print('Ошибка: должно быть введено целое число')
if is_num(dog_age) == True:
    dog_age = int(dog_age)
    if dog_age < 1:
        print('Ошибка: возраст должен быть не меньше 1')
    if dog_age > 20:
        print('Ошибка: возраст должен быть не больше 20')
    if dog_age == 1:
        print('Возраст собаки в человеческих годах: 10.5')
    if dog_age == 2:
        print('Возраст собаки в человеческих годах: 21')
    if dog_age > 2:
        dog_age -= 2
        human_age = float(21)
        for i in range(int(dog_age)):
            human_age += 4
        print('Возраст собаки в человеческих годах: ' + str(human_age))

#4
number = input('Введите число: ')
sum = sum(map(int, number))
if int(number[-1]) % 2 == 0 and sum % 3 == 0:
    print('Число делится на 6')
else:
    print('Число не делится на 6')

#5
import string
password = input('Введите пароль: ')
errors = []
if len(password) < 8:
    errors.append("длина менее 8 символов")
if not any(c.isupper() for c in password):
    errors.append("отсутствуют заглавные буквы")

#6
year = int(input('Введите год: '))
if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
    print(str(year) + ' - високосный год')
else:
    print(str(year) + ' - не високосный год')

#7
nums = input('Введите три числа: ')
nums = nums.split(' ')
nums = sorted(nums)
print('Наименьшее число: ' + str(nums[0]))

#8
sum_pok = float(input('Введите сумму покупки: '))
if sum_pok < 1000:
    print('Ваша скидка: 0%')
    print('К оплате: ' + str(sum_pok))
if sum_pok >= 1000 and sum_pok < 5000:
    sale = (sum_pok * 5) / 100
    without_sale = sum_pok - sale
    print('Ваша скидка: 5%')
    print('К оплате: ' + str(without_sale))
if sum_pok >= 5000 and sum_pok < 10000:
    sale = (sum_pok * 10) / 100
    without_sale = sum_pok - sale
    print('Ваша скидка: 10%')
    print('К оплате: ' + str(without_sale))
if sum_pok > 10000:
    sale = (sum_pok * 15) / 100
    without_sale = sum_pok - sale
    print('Ваша скидка: 15%')
    print('К оплате: ' + str(without_sale))

#9
hour = int(input('Введите час (0-23): '))
if hour < 6: print('Сейчас ночь')
if hour < 11 and hour >= 6: print('Сейчас утро')
if hour < 17 and hour >= 12: print('Сейчас день')
if hour <= 23 and hour >= 18: print('Сейчас вечер')

#10
labubu = input('Введите число: ')

if not labubu.isdigit():
    print('Некорректный ввод')
else:
    labubu = int(labubu)
    if labubu < 2:
        print('Ошибка: число должно быть больше 1')
    else:
        isprime = True
  
        for i in range(2, int(labubu**0.5) + 1):
            if labubu % i == 0:
                isprime = False
                break
        
        if isprime:
            print(f'{labubu} - простое число')
        else:
            print(f'{labubu} - составное число')