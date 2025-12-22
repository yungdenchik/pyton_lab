inventory = {}


def update_inventory(product, amount):
    inventory[product] = inventory.get(product, 0) + amount
    if inventory[product] <= 0:
        del inventory[product]


while True:
    product = input("Введіть назву продукту (або exit): ")
    if product == "exit":
        break

    amount = int(input("Введіть кількість (+ додати / - забрати): "))
    update_inventory(product, amount)

print("Інвентар:", inventory)

low_stock = [p for p, q in inventory.items() if q < 5]
print("Продукти з кількістю менше 5:", low_stock)
