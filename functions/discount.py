def calculate_discount(price, discount_percentage):
    if discount_percentage >= 20:
        discount_amount = price * (discount_percentage / 100)
        final_price = price - discount_amount
        return final_price
    else:
        print("No discount applied.")
        return price 

# print(calculate_discount(100, 20))

price = float(input("Enter the original price of the item: "))
discount_percentage = float(input("Enter the discount percentage: "))

final_price = calculate_discount(price, discount_percentage)

print(f"The final price is: {final_price:.2f}")