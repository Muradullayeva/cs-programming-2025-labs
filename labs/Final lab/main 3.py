import json
import datetime
import os
import sys

# Константы
DATA_FILE = "azs_data.json"
FUEL_TYPES = ["АИ-92", "АИ-95", "АИ-98", "ДТ"]
PRICES = {"АИ-92": 67.50, "АИ-95": 69.30, "АИ-98": 82.20, "ДТ": 78.10}
MIN_LEVEL_PERCENT = 10

# Структура данных
DEFAULT_DATA = {
    "cisterns": [
        {"id": 1, "fuel_type": "АИ-95", "max_volume": 20000, "current_volume": 18000, "enabled": True},
        {"id": 2, "fuel_type": "АИ-95", "max_volume": 20000, "current_volume": 1200, "enabled": False},
        {"id": 3, "fuel_type": "АИ-92", "max_volume": 20000, "current_volume": 12400, "enabled": True},
        {"id": 4, "fuel_type": "АИ-98", "max_volume": 15000, "current_volume": 10000, "enabled": False},
        {"id": 5, "fuel_type": "ДТ", "max_volume": 25000, "current_volume": 15600, "enabled": True}
    ],
    "columns": {
        1: ["АИ-92", "АИ-95"],
        2: ["АИ-92", "АИ-95"],
        3: ["АИ-92", "АИ-95", "АИ-98", "ДТ"],
        4: ["АИ-92", "АИ-95", "АИ-98", "ДТ"],
        5: ["АИ-92", "АИ-95", "АИ-98", "ДТ"],
        6: ["АИ-92", "АИ-95", "АИ-98", "ДТ"],
        7: ["АИ-95", "ДТ"],
        8: ["АИ-95", "ДТ"]
    },
    "cistern_mapping": {
        "АИ-92": [3],
        "АИ-95": [1, 2],
        "АИ-98": [4],
        "ДТ": [5]
    },
    "stats": {
        "total_cars": 0,
        "total_income": 0.0,
        "fuel_sold": {ft: 0 for ft in FUEL_TYPES},
        "fuel_income": {ft: 0.0 for ft in FUEL_TYPES},
        "transactions_count": {ft: 0 for ft in FUEL_TYPES}
    },
    "history": [],
    "emergency": False
}


class AZSManager:
    def __init__(self):
        self.load_data()
        self.check_cisterns_levels()

    def clear_screen(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            sys.stdout.write('\033[2J\033[H')
            sys.stdout.flush()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        else:
            self.data = DEFAULT_DATA.copy()
            self.save_data()

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def add_history(self, action, details):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.data["history"].append({
            "timestamp": timestamp,
            "action": action,
            "details": details
        })
        if len(self.data["history"]) > 100:
            self.data["history"] = self.data["history"][-100:]

    def check_cisterns_levels(self):
        for cistern in self.data["cisterns"]:
            min_level = cistern["max_volume"] * MIN_LEVEL_PERCENT / 100
            if cistern["current_volume"] < min_level and cistern["enabled"]:
                cistern["enabled"] = False
                self.add_history("Автоотключение цистерны",
                                 f"{cistern['fuel_type']} №{cistern['id']} - низкий уровень")

    def get_cistern(self, fuel_type, cistern_id=None):
        for cistern in self.data["cisterns"]:
            if cistern["fuel_type"] == fuel_type:
                if cistern_id is None or cistern["id"] == cistern_id:
                    return cistern
        return None

    def get_available_cisterns(self, fuel_type):
        return [c for c in self.data["cisterns"] if c["fuel_type"] == fuel_type]

    def get_cistern_for_column(self, column_num, fuel_type):
        if column_num not in self.data["columns"] or fuel_type not in self.data["columns"][column_num]:
            return None

        cistern_ids = self.data["cistern_mapping"][fuel_type]
        for cistern in self.data["cisterns"]:
            if cistern["id"] in cistern_ids and cistern["enabled"]:
                return cistern
        return None

    def print_header(self):
        print("=" * 50)
        print("АЗС <<СеверНефть>>")
        print("Система управления заправочной станцией")
        print("=" * 50)

        if self.data["emergency"]:
            print("\n⚠️  ВНИМАНИЕ! АВАРИЙНЫЙ РЕЖИМ! ⚠️")
            print("Все цистерны заблокированы. Работа приостановлена.")
            return

        # Проверка отключенных цистерн
        disabled_cisterns = []
        for cistern in self.data["cisterns"]:
            if not cistern["enabled"]:
                reason = "низкий уровень топлива" if cistern["current_volume"] < cistern[
                    "max_volume"] * MIN_LEVEL_PERCENT / 100 else "ручное отключение"
                disabled_cisterns.append(f"{cistern['fuel_type']} №{cistern['id']} ({reason})")

        if disabled_cisterns:
            print("\nВНИМАНИЕ!")
            print("Обнаружены отключённые цистерны:")
            for c in disabled_cisterns:
                print(f" - {c}")

    def serve_customer(self): #обслужить клиента
        if self.data["emergency"]:
            print("Работа невозможна в аварийном режиме!")
            return

        print("\n--- Обслуживание клиента ---")

        # Выбор колонки
        print("\nДоступные колонки:")
        for i in range(1, 9):
            print(f"{i}) Колонка {i}")

        try:
            column_num = int(input("\nВыберите колонки: "))
            if column_num not in range(1, 9):
                print("Ошибка: неверный номер колонки")
                return
        except ValueError:
            print("Ошибка: введите число")
            return

        available_fuels = self.data["columns"][column_num]
        print(f"\nКолонка {column_num}")
        print("Доступные виды топлива:")

        for i, fuel in enumerate(available_fuels, 1):
            cistern = self.get_cistern_for_column(column_num, fuel)
            status = "✓" if cistern and cistern["enabled"] else "✗ (цистерна отключена)"
            print(f"{i}) {fuel} {status}")

        try:
            choice = int(input("\nВыберите тип топлива: "))
            if choice not in range(1, len(available_fuels) + 1):
                print("Ошибка: неверный выбор")
                return
            fuel_type = available_fuels[choice - 1]
        except ValueError:
            print("Ошибка: введите число")
            return

        cistern = self.get_cistern_for_column(column_num, fuel_type)
        if not cistern:
            print(f"\nОШИБКА: Нет доступной цистерны для {fuel_type}")
            return
        if not cistern["enabled"]:
            print(f"\nОШИБКА: Цистерна {cistern['fuel_type']} №{cistern['id']} отключена.")
            print("Отпуск топлива невозможен.")
            return

        try:
            liters = float(input("\nВведите количество литров: "))
            if liters <= 0:
                print("Ошибка: количество должно быть положительным")
                return
            if liters > cistern["current_volume"]:
                print(f"Ошибка: недостаточно топлива в цистерне (доступно: {cistern['current_volume']} л)")
                return
        except ValueError:
            print("Ошибка: введите число")
            return

        price = PRICES[fuel_type]
        cost = liters * price

        print(f"\nСтоимость:")
        print(f"{liters} л × {price:.2f} ₽ = {cost:.2f} ₽")

        confirm = input("\nПодтвердить оплату? (y/n): ").lower()
        if confirm != 'y':
            print("Операция отменена")
            return

        cistern["current_volume"] -= liters

        self.data["stats"]["total_cars"] += 1
        self.data["stats"]["total_income"] += cost
        self.data["stats"]["fuel_sold"][fuel_type] += liters
        self.data["stats"]["fuel_income"][fuel_type] += cost
        self.data["stats"]["transactions_count"][fuel_type] += 1

        self.add_history("Продажа топлива",
                         f"Колонка {column_num}, {fuel_type}, {liters} л, {cost:.2f} ₽")

        self.save_data()
        print("\nОперация выполнена успешно.")
        print("Спасибо за покупку!")

    def show_cisterns_status(self): #состояние цистерн
        print("\n--- Состояние цистерн ---")

        for cistern in self.data["cisterns"]:
            fuel_type = cistern["fuel_type"]
            status = "ВКЛ" if cistern["enabled"] else "ВЫКЛ"

            min_level = cistern["max_volume"] * MIN_LEVEL_PERCENT / 100
            warning = " (ниже порога)" if cistern["current_volume"] < min_level else ""

            print(f"{fuel_type} №{cistern['id']} | "
                  f"{cistern['current_volume']} / {cistern['max_volume']} л | "
                  f"{status}{warning}")

    def refuel_cistern(self): #пополнить цистерну
        if self.data["emergency"]:
            print("Работа невозможна в аварийном режиме!")
            return

        print("\n--- Пополнение топлива ---")

        print("Доступные типы топлива:")
        for i, fuel in enumerate(FUEL_TYPES, 1):
            print(f"{i}) {fuel}")

        try:
            choice = int(input("\nВыберите тип топлива: "))
            if choice not in range(1, len(FUEL_TYPES) + 1):
                print("Ошибка: неверный выбор")
                return
            fuel_type = FUEL_TYPES[choice - 1]
        except ValueError:
            print("Ошибка: введите число")
            return

        cisterns = self.get_available_cisterns(fuel_type)
        if not cisterns:
            print(f"Ошибка: нет цистерн для {fuel_type}")
            return

        print(f"\nДоступные цистерны для {fuel_type}:")
        for i, cistern in enumerate(cisterns, 1):
            print(f"{i}) Цистерна №{cistern['id']} | "
                  f"{cistern['current_volume']} / {cistern['max_volume']} л")

        try:
            choice = int(input("\nВыберите цистерну: "))
            if choice not in range(1, len(cisterns) + 1):
                print("Ошибка: неверный выбор")
                return
            cistern = cisterns[choice - 1]
        except ValueError:
            print("Ошибка: введите число")
            return

        try:
            liters = float(input("\nВведите количество литров для пополнения: "))
            if liters <= 0:
                print("Ошибка: количество должно быть положительным")
                return

            if cistern["current_volume"] + liters > cistern["max_volume"]:
                available = cistern["max_volume"] - cistern["current_volume"]
                print(f"Ошибка: превышение максимального объема (можно добавить не более {available} л)")
                return
        except ValueError:
            print("Ошибка: введите число")
            return

        print(f"\nБудет добавлено: {liters} л {fuel_type}")
        print(f"Новый уровень: {cistern['current_volume'] + liters} л")

        confirm = input("Подтвердить? (y/n): ").lower()
        if confirm != 'y':
            print("Операция отменена")
            return

        cistern["current_volume"] += liters

        self.add_history("Пополнение цистерны",
                         f"{fuel_type} №{cistern['id']}, +{liters} л, новый уровень: {cistern['current_volume']} л")

        self.save_data()
        print("\nЦистерна успешно пополнена!")

    def show_stats(self): #вывод статистики и баланса
        print("\n--- Баланс и статистика ---")

        stats = self.data["stats"]
        print(f"\nОбслужено автомобилей: {stats['total_cars']}")
        print(f"Общий доход: {stats['total_income']:,.2f} ₽")

        print("\nПродано топлива:")
        for fuel in FUEL_TYPES:
            liters = stats['fuel_sold'][fuel]
            income = stats['fuel_income'][fuel]
            print(f"{fuel} - {liters} л ({income:,.2f} ₽)")

    def show_history(self): #вывод истории
        print("\n--- История операций ---")

        if not self.data["history"]:
            print("История пуста")
            return

        for record in self.data["history"][-20:]:  # Последние 20 записей
            print(f"\n[{record['timestamp']}]")
            print(f"Действие: {record['action']}")
            print(f"Детали: {record['details']}")

    def transfer_fuel(self): #перекачка топлива
        if self.data["emergency"]:
            print("Работа невозможна в аварийном режиме!")
            return

        print("\n--- Перекачка топлива ---")

        print("Выберите тип топлива для перекачки:")
        for i, fuel in enumerate(FUEL_TYPES, 1):
            print(f"{i}) {fuel}")

        try:
            choice = int(input("\nВыберите тип топлива: "))
            if choice not in range(1, len(FUEL_TYPES) + 1):
                print("Ошибка: неверный выбор")
                return
            fuel_type = FUEL_TYPES[choice - 1]
        except ValueError:
            print("Ошибка: введите число")
            return

        cisterns = self.get_available_cisterns(fuel_type)
        if len(cisterns) < 2:
            print(f"Ошибка: для {fuel_type} нужно как минимум 2 цистерны")
            return

        print(f"\nДоступные цистерны {fuel_type}:")
        for i, cistern in enumerate(cisterns, 1):
            status = "ВКЛ" if cistern["enabled"] else "ВЫКЛ"
            print(f"{i}) Цистерна №{cistern['id']} | "
                  f"{cistern['current_volume']} / {cistern['max_volume']} л | {status}")

        try:
            src_choice = int(input("\nВыберите исходную цистерну (откуда перекачивать): "))
            if src_choice not in range(1, len(cisterns) + 1):
                print("Ошибка: неверный выбор")
                return
            src_cistern = cisterns[src_choice - 1]
        except ValueError:
            print("Ошибка: введите число")
            return

        try:
            dst_choice = int(input("Выберите целевую цистерну (куда перекачивать): "))
            if dst_choice not in range(1, len(cisterns) + 1):
                print("Ошибка: неверный выбор")
                return
            if dst_choice == src_choice:
                print("Ошибка: нельзя перекачивать в ту же цистерну")
                return
            dst_cistern = cisterns[dst_choice - 1]
        except ValueError:
            print("Ошибка: введите число")
            return

        try:
            liters = float(input("\nВведите количество литров для перекачки: "))
            if liters <= 0:
                print("Ошибка: количество должно быть положительным")
                return

            if liters > src_cistern["current_volume"]:
                print(f"Ошибка: недостаточно топлива в исходной цистерне (доступно: {src_cistern['current_volume']} л)")
                return

            if dst_cistern["current_volume"] + liters > dst_cistern["max_volume"]:
                available = dst_cistern["max_volume"] - dst_cistern["current_volume"]
                print(
                    f"Ошибка: превышение максимального объема целевой цистерны (можно добавить не более {available} л)")
                return
        except ValueError:
            print("Ошибка: введите число")
            return

        print(f"\nПерекачка {liters} л {fuel_type}:")
        print(f"Из: Цистерна №{src_cistern['id']} ({src_cistern['current_volume']} л)")
        print(f"В: Цистерна №{dst_cistern['id']} ({dst_cistern['current_volume']} л)")

        confirm = input("Подтвердить? (y/n): ").lower()
        if confirm != 'y':
            print("Операция отменена")
            return

        src_cistern["current_volume"] -= liters
        dst_cistern["current_volume"] += liters

        self.add_history("Перекачка топлива",
                         f"{fuel_type}: {liters} л из №{src_cistern['id']} в №{dst_cistern['id']}")

        self.save_data()
        print("\nПерекачка выполнена успешно!")

    def manage_cisterns(self): #включение/отключение цистерн
        if self.data["emergency"]:
            print("Работа невозможна в аварийном режиме!")
            return

        print("\n--- Управление цистернами ---")

        print("Доступные действия:")
        print("1) Включить цистерну")
        print("2) Отключить цистерну")

        try:
            action = int(input("\nВыберите действия: "))
            if action not in [1, 2]:
                print("Ошибка: неверный выбор")
                return
        except ValueError:
            print("Ошибка: введите число")
            return

        if action == 1:  # Включение
            available_cisterns = [c for c in self.data["cisterns"] if not c["enabled"]]
            action_text = "включения"
        else:  # Отключение
            available_cisterns = [c for c in self.data["cisterns"] if c["enabled"]]
            action_text = "отключения"

        if not available_cisterns:
            print(f"\nНет цистерн для {action_text}")
            return

        print(f"\nЦистерны, доступные для {action_text}:")
        for i, cistern in enumerate(available_cisterns, 1):
            print(f"{i}) {cistern['fuel_type']} №{cistern['id']} | "
                  f"{cistern['current_volume']} / {cistern['max_volume']} л")

        try:
            choice = int(input(f"\nВыберите цистерну для {action_text}: "))
            if choice not in range(1, len(available_cisterns) + 1):
                print("Ошибка: неверный выбор")
                return
            cistern = available_cisterns[choice - 1]
        except ValueError:
            print("Ошибка: введите число")
            return

        if action == 1:
            min_level = cistern["max_volume"] * MIN_LEVEL_PERCENT / 100
            if cistern["current_volume"] < min_level:
                print(
                    f"\nВНИМАНИЕ: Уровень топлива ({cistern['current_volume']} л) ниже минимального ({min_level:.0f} л)")
                confirm = input("Всё равно включить? (y/n): ").lower()
                if confirm != 'y':
                    print("Операция отменена")
                    return

        cistern["enabled"] = (action == 1)

        action_name = "включена" if action == 1 else "отключена"
        self.add_history(f"Цистерна {action_name}",
                         f"{cistern['fuel_type']} №{cistern['id']} - ручное {action_name.lower()}")

        self.save_data()
        print(f"\nЦистерна {cistern['fuel_type']} №{cistern['id']} успешно {action_name}.")

    def show_columns_status(self): #состояние колонок
        print("\n--- Состояние колонок ---")

        for col_num in range(1, 9):
            fuels = self.data["columns"][col_num]
            print(f"\nКолонка {col_num}:")

            for fuel in fuels:
                cistern = self.get_cistern_for_column(col_num, fuel)
                if cistern:
                    status = "✓" if cistern["enabled"] else "✗ (цистерна отключена)"
                    print(f"  {fuel}: цистерна №{cistern['id']} {status}")
                else:
                    print(f"  {fuel}: ✗ (нет доступной цистерны)")

    def emergency_procedure(self): #авария
        print("\n--- АВАРИЙНАЯ СИТУАЦИЯ ---")
        print("\n⚠️  ВНИМАНИЕ! АВАРИЙНАЯ СИТУАЦИЯ! ⚠️")
        print("1) Все цистерны будут заблокированы")
        print("2) Заправка прекращает работу")
        print("3) Будет зафиксировано аварийное событие")
        print("4) Имитируется вызов аварийных служб")

        confirm = input("\nВы уверены? Это серьезное действие! (y/n): ").lower()
        if confirm != 'y':
            print("Отмена аварийной процедуры")
            return

        self.data["emergency"] = True

        for cistern in self.data["cisterns"]:
            cistern["enabled"] = False

        self.add_history("АВАРИЙНЫЙ РЕЖИМ", "Активирован аварийный режим, все цистерны отключены")

        self.save_data()
        print("\n" + "=" * 50)
        print("АВАРИЙНЫЙ РЕЖИМ АКТИВИРОВАН!")
        print("=" * 50)
        print("\nИмитация вызова аварийных служб...")
        print("01, 02, 03 - вызваны на АЗС <<СеверНефть>>")
        print("\nОжидание прибытия спасателей...")

    def exit_emergency(self): #выход из аварийного режима
        if not self.data["emergency"]:
            print("Аварийный режим не активен")
            return

        print("\n--- Выход из аварийного режима ---")
        print("ВНИМАНИЕ: После выхода из аварийного режима")
        print("цистерны НЕ будут автоматически включены!")
        print("Их нужно будет включить вручную через меню.")

        confirm = input("\nВыйти из аварийного режима? (y/n): ").lower()
        if confirm != 'y':
            print("Отмена")
            return

        self.data["emergency"] = False
        self.add_history("Выход из аварийного режима", "Аварийный режим деактивирован")
        self.save_data()
        print("\nАварийный режим деактивирован.")

    def run(self): #запуск программы и меню
        while True:
            self.clear_screen()
            self.print_header()

            if self.data["emergency"]:
                print("\n" + "-" * 50)
                print("В аварийном режиме доступны только:")
                print("2) Проверить состояние цистерн")
                print("5) История операций")
                print("10) Выход из аварийного режима")
                print("0) Выход")
            else:
                print("\n" + "-" * 50)
                print("Выберите действия:")
                print("1) Обслужить клиента (касса)")
                print("2) Проверить состояние цистерн")
                print("3) Оформить пополнение топлива")
                print("4) Баланс и статистика")
                print("5) История операций")
                print("6) Перекачка топлива между цистернами")
                print("7) Включение / отключение цистерн")
                print("8) Состояние колонок")
                print("9) EMERGENCY - аварийная ситуация")
                print("0) Выход")

            print("-" * 50)

            try:
                choice = input("> ")

                if self.data["emergency"]:
                    if choice == "2":
                        self.show_cisterns_status()
                    elif choice == "5":
                        self.show_history()
                    elif choice == "10":
                        self.exit_emergency()
                    elif choice == "0":
                        print("\nВыход из программы...")
                        break
                    else:
                        print("Неверный выбор в аварийном режиме")
                else:
                    if choice == "1":
                        self.serve_customer()
                    elif choice == "2":
                        self.show_cisterns_status()
                    elif choice == "3":
                        self.refuel_cistern()
                    elif choice == "4":
                        self.show_stats()
                    elif choice == "5":
                        self.show_history()
                    elif choice == "6":
                        self.transfer_fuel()
                    elif choice == "7":
                        self.manage_cisterns()
                    elif choice == "8":
                        self.show_columns_status()
                    elif choice == "9":
                        self.emergency_procedure()
                    elif choice == "0":
                        print("\nВыход из программы...")
                        break
                    else:
                        print("Неверный выбор. Попробуйте снова.")

                if choice != "0":
                    input("\nНажмите Enter для возврата в меню...")

            except KeyboardInterrupt:
                print("\n\nПрограмма прервана пользователем")
                break
            except Exception as e:
                print(f"\nПроизошла ошибка: {e}")
                input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    azs = AZSManager()
    azs.run()