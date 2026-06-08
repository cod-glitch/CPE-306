"""
Test Script for BankAccount Class
Student: Omolola Fathiu Adedamola
Matric No: CPE/2023/1093
"""

from bank_account import BankAccount, InsufficientFundsError

def test_bank_account():
    # ========== STUDENT HEADER ==========
    print("=" * 55)
    print(f"STUDENT: Omolola Fathiu Adedamola")
    print(f"MATRIC NO: CPE/2023/1093")
    print("=" * 55)
    print("TESTING BankAccount CLASS")
    print("=" * 55)

    # 1. Constructor with default balance
    print("\n1. Constructor with default balance")
    acc1 = BankAccount("Alice")
    print(f"Created: {acc1}")
    assert acc1.balance == 0.0
    assert acc1.owner == "Alice"

    # 2. Constructor with initial balance
    print("\n2. Constructor with initial balance")
    acc2 = BankAccount("Bob", 100.0)
    print(f"Created: {acc2}")
    assert acc2.balance == 100.0

    # 3. Constructor with negative initial balance -> ValueError
    print("\n3. Constructor with negative balance (should raise ValueError)")
    try:
        acc3 = BankAccount("Eve", -50.0)
        print("ERROR: Should have raised ValueError")
    except ValueError as e:
        print(f"Correctly caught: {e}")

    # 4. Deposit
    print("\n4. Deposit")
    acc1.deposit(25.0)
    print(f"After depositing 25.0: {acc1}")
    assert acc1.balance == 25.0

    print("   Deposit with negative amount (should raise ValueError)")
    try:
        acc1.deposit(-5.0)
        print("ERROR: Should have raised ValueError")
    except ValueError as e:
        print(f"Correctly caught: {e}")

    # 5. Withdraw (fee applies)
    print("\n5. Withdraw (fee = 0.50 applies)")
    acc2.withdraw(30.0)          # deducts 30 + 0.50 = 30.50
    print(f"After withdrawing 30.0 from Bob: {acc2}")
    assert abs(acc2.balance - 69.50) < 0.0001   # 100 - 30.50 = 69.50

    # 6. Withdraw with non-positive amount -> ValueError
    print("\n6. Withdraw with invalid amount (should raise ValueError)")
    try:
        acc2.withdraw(0)
        print("ERROR: Should have raised ValueError")
    except ValueError as e:
        print(f"Correctly caught: {e}")

    # 7. Insufficient funds (including fee)
    print("\n7. Withdraw more than balance + fee (should raise InsufficientFundsError)")
    try:
        acc2.withdraw(100.0)      # needs 100 + 0.50 = 100.50, but balance is 69.50
        print("ERROR: Should have raised InsufficientFundsError")
    except InsufficientFundsError as e:
        print(f"Correctly caught: {e}")

    # 8. from_dict class method
    print("\n8. from_dict factory method")
    data = {'owner': 'Charlie', 'balance': 200.0}
    acc4 = BankAccount.from_dict(data)
    print(f"Created from dict: {acc4}")
    assert acc4.owner == 'Charlie'
    assert acc4.balance == 200.0

    # 9. __str__ and __repr__
    print("\n9. String representations")
    print(f"__str__ : {acc4}")
    print(f"__repr__: {repr(acc4)}")

    # 10. Transaction fee is a class attribute (can be changed)
    print("\n10. Class attribute transaction_fee")
    print(f"Default fee: {BankAccount.transaction_fee}")
    old_fee = BankAccount.transaction_fee
    BankAccount.transaction_fee = 1.00
    acc5 = BankAccount("Diana", 50.0)
    acc5.withdraw(10.0)           # deducts 10 + 1.00 = 11.00
    print(f"With new fee 1.00, after withdrawing 10: {acc5}")
    assert acc5.balance == 39.0
    # Restore original fee
    BankAccount.transaction_fee = old_fee

    print("\n" + "=" * 55)
    print("ALL TESTS PASSED SUCCESSFULLY")
    print("=" * 55)

if __name__ == "__main__":
    test_bank_account()
