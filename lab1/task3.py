sales = []


def calculate_revenue(sales_list):
    revenue = {}

    for sale in sales_list:
        product = sale["продукт"]
        total = sale["кількість"] * sale["ціна"]
        revenue[product] = revenue.get(product, 0) + total

    return revenue


while True:
    product = input("Введіть продукт (або exit): ")
    if product == "exit":
        break

    quantity = int(input("Кількість: "))
    price = float(input("Ціна: "))

    sales.append({
        "продукт": product,
        "кількість": quantity,
        "ціна": price
    })

revenue = calculate_revenue(sales)
print("Загальний дохід:", revenue)

high_income = [p for p, r in revenue.items() if r > 1000]
print("Продукти з доходом більше 1000:", high_income)
