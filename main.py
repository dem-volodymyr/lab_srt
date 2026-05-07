import json
import os
from datetime import datetime

DB_FILE = 'xchange_db.json'


class XchangeSystem:
    def __init__(self):
        self.db = self.load_data()
        self.current_user = None

    def load_data(self):
        """Завантаження бази даних або створення нової, якщо файл не існує"""
        if os.path.exists(DB_FILE):
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            default_db = {
                "users": {
                    "admin": {"password": "admin", "role": "Адміністратор", "name": "Системний Адмін"},
                    "trader1": {"password": "123", "role": "Трейдер", "name": "Іван (Крипто-аналітик)"}
                },
                "accounts": {}
            }
            self.save_data(default_db)
            return default_db

    def save_data(self, data=None):
        """Збереження стану бази даних у JSON"""
        if data is None:
            data = self.db
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def login(self):
        print("\n" + "=" * 50)
        print(" АВТОМАТИЗОВАНА ТОРГОВА СИСТЕМА Xchange ")
        print("=" * 50)
        attempts = 3
        while attempts > 0:
            login = input("Логін: ").strip()
            password = input("Пароль: ").strip()
            user = self.db["users"].get(login)
            if user and user["password"] == password:
                self.current_user = user
                print(f"\n[АВТОРИЗАЦІЯ] Вітаємо, {user['name']}! Роль: {user['role']}")
                return True
            else:
                attempts -= 1
                print(f"[ПОМИЛКА] Невірні дані. Залишилось спроб: {attempts}")
        print("Систему заблоковано.")
        return False

    def add_user(self):
        if self.current_user['role'] != 'Адміністратор':
            print("[ВІДМОВА] Додавати користувачів може лише Адміністратор.")
            return
        print("\n--- Реєстрація нового співробітника ---")
        login = input("Логін: ")
        password = input("Пароль: ")
        name = input("ПІБ: ")
        self.db["users"][login] = {"password": password, "role": "Трейдер", "name": name}
        self.save_data()
        print(f"[УСПІХ] Користувача {name} додано до системи.")

    def add_account(self):
        if self.current_user['role'] != 'Адміністратор':
            print("[ВІДМОВА] Недостатньо прав. Лише Адміністратор відкриває рахунки.")
            return
        print("\n--- Відкриття нового торгового рахунку ---")
        account_id = f"ACC{len(self.db['accounts']) + 1000}"
        client_name = input("ПІБ клієнта: ")
        initial_balance = input("Початковий депозит (USDT): ")

        self.db["accounts"][account_id] = {
            "client_name": client_name,
            "balance": initial_balance,
            "history": []
        }
        self.save_data()
        print(f"[УСПІХ] Рахунок відкрито. ID рахунку: {account_id}")

    def execute_trade(self):
        if self.current_user['role'] != 'Трейдер':
            print("[ВІДМОВА] Здійснювати угоди може лише Трейдер.")
            return
        account_id = input("\nВведіть ID рахунку: ")
        account = self.db["accounts"].get(account_id)

        if not account:
            print("[ПОМИЛКА] Рахунок не знайдено.")
            return

        print(f"Клієнт: {account['client_name']} (Поточний баланс: {account['balance']} USDT)")
        print("--- Модуль прогнозування ---")
        print("AI Прогноз: Рекомендовано КУПУВАТИ Bitcoin (Очікуваний ріст 2.5%)")

        asset = input("Активи (напр. BTC/USDT): ")
        action = input("Дія (Купівля/Продаж): ")
        amount = input("Об'єм транзакції: ")

        date = datetime.now().strftime("%Y-%m-%d %H:%M")

        record = {
            "date": date,
            "trader": self.current_user['name'],
            "asset": asset,
            "action": action,
            "amount": amount
        }

        account["history"].append(record)
        self.save_data()
        print("[УСПІХ] Торгову угоду зафіксовано.")

    def view_account(self):
        account_id = input("\nВведіть ID рахунку: ")
        account = self.db["accounts"].get(account_id)
        if not account:
            print("[ПОМИЛКА] Рахунок не знайдено.")
            return

        print("\n" + "-" * 40)
        print(f"ТОРГОВИЙ РАХУНОК: {account['client_name']}")
        print(f"Баланс: {account['balance']} USDT")
        print("-" * 40)

        print("ІСТОРІЯ УГОД ТА ОПЕРАЦІЙ:")
        if not account["history"]:
            print("  Транзакцій немає.")
        else:
            for rec in account["history"]:
                print(f"  [{rec['date']}] Трейдер: {rec['trader']}")
                print(f"  Актив: {rec['asset']} | Дія: {rec['action']} | Об'єм: {rec['amount']}\n")
        print("-" * 40)

    def run(self):
        if not self.login():
            return
        while True:
            print(f"\n=== ГОЛОВНЕ МЕНЮ ({self.current_user['role']}) ===")
            if self.current_user['role'] == 'Адміністратор':
                print("1. Додати нового співробітника")
                print("2. Відкрити торговий рахунок клієнту")
            if self.current_user['role'] == 'Трейдер':
                print("3. Здійснити торгову угоду (на базі прогнозу)")

            print("4. Переглянути торговий рахунок")
            print("0. Вихід")

            choice = input("Оберіть дію: ")

            if choice == '1':
                self.add_user()
            elif choice == '2':
                self.add_account()
            elif choice == '3':
                self.execute_trade()
            elif choice == '4':
                self.view_account()
            elif choice == '0':
                print("Завершення роботи системи. До побачення!")
                break
            else:
                print("[ПОМИЛКА] Некоректний вибір або недостатньо прав.")


if __name__ == "__main__":
    app = XchangeSystem()
    app.run()