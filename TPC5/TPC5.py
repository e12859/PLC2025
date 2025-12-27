import json
import os
import re
from datetime import date

STOCK_FILE = "stock.json"

COINS = {
    "2e": 200,
    "1e": 100,
    "50c": 50,
    "20c": 20,
    "10c": 10,
    "5c": 5,
    "2c": 2,
    "1c": 1,
}

DENOMS = [200, 100, 50, 20, 10, 5, 2, 1]

RE_LIST = re.compile(r"^\s*LIST\s*$", re.I)
RE_EXIT = re.compile(r"^\s*EXIT\s*$", re.I)
RE_SELECT = re.compile(r"^\s*SELECT\s+(\w+)\s*$", re.I)
RE_COINS_LINE = re.compile(r"^\s*COIN\s+(.+?)\s*\.\s*$", re.I)
RE_COIN_TOKEN = re.compile(r"\d+(?:e|c)", re.I)


def price_to_cents(price):
    return int(round(float(price) * 100))


def cents_to_price(cents: int):
    return round(cents / 100.0, 2)


def format_balance(cents: int):
    euros, rem = divmod(max(0, cents), 100)
    return f"{euros}e{rem:02d}c" if euros > 0 else f"{rem}c"


def load_stock():
    if not os.path.exists(STOCK_FILE):
        return [
            { "cod": "A23", "name": "water 0.5L",        "amount": 8,  "price": 0.70 },
            { "cod": "B10", "name": "coffee",           "amount": 12, "price": 0.50 },
            { "cod": "C05", "name": "chips",            "amount": 6,  "price": 1.20 },
            { "cod": "D99", "name": "cola",             "amount": 10, "price": 1.50 },
            { "cod": "E12", "name": "chocolate bar",    "amount": 9,  "price": 1.10 },
            { "cod": "F07", "name": "sandwich",         "amount": 4,  "price": 2.40 }
        ]

    with open(STOCK_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, list) else []


def save_stock(stock: list):
    for p in stock:
        if "price" in p:
            p["price"] = cents_to_price(price_to_cents(p["price"]))
    with open(STOCK_FILE, "w", encoding="utf-8") as f:
        json.dump(stock, f, ensure_ascii=False, indent=2)


def list_products(stock: list):
    print("vm:")
    print("code | name | amount | price")
    print("-------------------------------")
    for p in stock:
        print(f"{p.get('cod','')} {p.get('name','')} {p.get('amount',0)} {p.get('price',0)}")


def find_product(stock: list, code: str):
    code = code.strip().upper()
    for p in stock:
        if str(p.get("cod", "")).strip().upper() == code:
            return p
    return None


def add_coins_from_line(line: str):
    m = RE_COINS_LINE.match(line)
    if not m:
        return 0

    body = m.group(1)
    tokens = RE_COIN_TOKEN.findall(body)

    total = 0
    for t in tokens:
        t = t.lower()
        if t in COINS:
            total += COINS[t]
    return total


def make_change_text(cents: int):
    if cents <= 0:
        return "no change."

    parts = []
    remaining = cents

    for d in DENOMS:
        n, remaining = divmod(remaining, d)
        if n > 0:
            coin = f"{d//100}e" if d >= 100 else f"{d}c"
            parts.append(f"{n}x {coin}")

    if len(parts) == 1:
        return parts[0] + "."
    return ", ".join(parts[:-1]) + " and " + parts[-1] + "."


def select_product(stock: list, balance_cents: int, code: str):
    product = find_product(stock, code)
    if not product:
        print("vm: Product does not exist.")
        print(f"vm: Balance = {format_balance(balance_cents)}")
        return balance_cents

    qty = int(product.get("amount", 0))
    if qty <= 0:
        print("vm: Product out of stock.")
        print(f"vm: Balance = {format_balance(balance_cents)}")
        return balance_cents

    price_cents = price_to_cents(product.get("price", 0.0))
    if balance_cents < price_cents:
        print("vm: Insufficient balance to complete your request.")
        print(f"vm: Balance = {format_balance(balance_cents)}; Price = {format_balance(price_cents)}")
        return balance_cents

    product["amount"] = qty - 1
    balance_cents -= price_cents
    print(f'vm: Please take your product "{product.get("name","")}"')
    print(f"vm: Balance = {format_balance(balance_cents)}")
    return balance_cents


def main():
    stock = load_stock()

    print(f"vm: {date.today().isoformat()}, Stock loaded, State updated.")
    print("vm: Hello. I am ready to serve your request.")

    balance_cents = 0

    while True:
        try:
            line = input(">> ").strip()
        except (EOFError, KeyboardInterrupt):
            line = "EXIT"

        if not line:
            continue

        if RE_LIST.match(line):
            list_products(stock)

        elif RE_COINS_LINE.match(line):
            balance_cents += add_coins_from_line(line)
            print(f"vm: Balance = {format_balance(balance_cents)}")

        elif (m := RE_SELECT.match(line)):
            code = m.group(1)
            balance_cents = select_product(stock, balance_cents, code)

        elif RE_EXIT.match(line):
            if balance_cents > 0:
                print(f"vm: Please take your change: {make_change_text(balance_cents)}")
            print("vm: See you next time.")
            save_stock(stock)
            break

        else:
            print("vm: Unknown command.")
            print("vm: Commands: LIST, COIN <v>., SELECT <code>, EXIT")
