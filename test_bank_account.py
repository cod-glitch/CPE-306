"""
test_bank_account.py
Manual test script for BankAccount — covers every specified behaviour.
Run with:  python test_bank_account.py
"""

from bank_account import BankAccount, InsufficientFundsError


# ── Helpers ────────────────────────────────────────────────────────────────

def section(title: str) -> None:
    print(f"\n{'─' * 55}")
    print(f"  {title}")
    print('─' * 55)

def passed(msg: str) -> None:
    print(f"  ✅  {msg}")

def failed(msg: str) -> None:
    print(f"  ❌  {msg}")


# ── 1. Constructor ─────────────────────────────────────────────────────────

section("1 · Constructor")

# Normal construction with explicit balance
acc = BankAccount("Fathiu", 100.0)
assert acc.owner == "Fathiu" and acc.balance == 100.0
passed("BankAccount('Fathiu', 100.0) created with correct owner & balance")

# Default balance of 0.0
acc_zero = BankAccount("Aminah")
assert acc_zero.balance == 0.0
passed("Default initial_balance is 0.0")

# Negative initial balance raises ValueError
try:
    BankAccount("Bad Actor", -50.0)
    failed("Should have raised ValueError for negative balance")
except ValueError as e:
    passed(f"ValueError raised for negative balance → {e}")


# ── 2. Balance is a read-only property ────────────────────────────────────

section("2 · Read-only balance property")

try:
    acc.balance = 9999.0          # type: ignore[misc]
    failed("Should have raised AttributeError when setting balance")
except AttributeError:
    passed("balance is read-only; direct assignment raises AttributeError")


# ── 3. deposit() ──────────────────────────────────────────────────────────

section("3 · deposit()")

acc2 = BankAccount("Test User", 50.0)
new_bal = acc2.deposit(25.0)
assert new_bal == 75.0 and acc2.balance == 75.0
passed(f"deposit(25.0) → balance is now {acc2.balance}")

# Zero deposit
try:
    acc2.deposit(0)
    failed("Should have raised ValueError for zero deposit")
except ValueError as e:
    passed(f"ValueError for zero deposit → {e}")

# Negative deposit
try:
    acc2.deposit(-10.0)
    failed("Should have raised ValueError for negative deposit")
except ValueError as e:
    passed(f"ValueError for negative deposit → {e}")


# ── 4. withdraw() ─────────────────────────────────────────────────────────

section("4 · withdraw() — basic + non-positive guard")

acc3 = BankAccount("Withdraw Tester", 200.0)
# 50.00 withdrawal + 0.50 fee = 50.50 deducted
new_bal = acc3.withdraw(50.0)
expected = 200.0 - 50.0 - BankAccount.transaction_fee
assert abs(new_bal - expected) < 1e-9, f"Expected {expected}, got {new_bal}"
passed(f"withdraw(50.0) deducted amount + fee → balance now {new_bal:.2f}")

# Zero withdrawal
try:
    acc3.withdraw(0)
    failed("Should have raised ValueError for zero withdrawal")
except ValueError as e:
    passed(f"ValueError for zero withdrawal → {e}")

# Negative withdrawal
try:
    acc3.withdraw(-5.0)
    failed("Should have raised ValueError for negative withdrawal")
except ValueError as e:
    passed(f"ValueError for negative withdrawal → {e}")


# ── 4b. InsufficientFundsError ─────────────────────────────────────────────

section("4b · InsufficientFundsError")

acc4 = BankAccount("Edge Tester", 10.0)

# ⚠️  THE PROBLEM IN ACTION:
# Trying to withdraw the entire balance (₦10.00) should FAIL because the
# total cost is ₦10.00 + ₦0.50 fee = ₦10.50, which exceeds the ₦10.00 balance.
# A naive implementation that checks (amount > balance) instead of
# (amount + fee > balance) would INCORRECTLY allow this and create a
# negative balance of -₦0.50.

try:
    acc4.withdraw(10.0)   # amount == balance, but total cost > balance
    failed(
        "⚠️  BUG PRESENT: withdrew ₦10.00 from ₦10.00 balance — "
        "fee has been silently ignored, balance is now negative!"
    )
except InsufficientFundsError as e:
    passed(f"InsufficientFundsError raised correctly (fee factored in) → {e}")

# Genuinely affordable withdrawal (balance covers amount + fee)
acc5 = BankAccount("Safe Tester", 10.0)
acc5.withdraw(9.0)    # 9.00 + 0.50 = 9.50 ≤ 10.00  → ok
assert abs(acc5.balance - 0.50) < 1e-9
passed(f"withdraw(9.0) succeeded (9.00 + 0.50 fee = 9.50 ≤ 10.00); balance = {acc5.balance:.2f}")

# Overdraft attempt
try:
    BankAccount("Empty", 0.0).withdraw(100.0)
    failed("Should have raised InsufficientFundsError")
except InsufficientFundsError as e:
    passed(f"InsufficientFundsError on overdraft → {e}")


# ── 5. transaction_fee class attribute ────────────────────────────────────

section("5 · transaction_fee class attribute")

assert BankAccount.transaction_fee == 0.50
passed(f"BankAccount.transaction_fee == {BankAccount.transaction_fee}")

# Also accessible on instance
assert acc5.transaction_fee == 0.50
passed("transaction_fee accessible on instance too")


# ── 6. from_dict() class method ───────────────────────────────────────────

section("6 · from_dict()")

acc_d = BankAccount.from_dict({"owner": "Dict User", "balance": 300.0})
assert acc_d.owner == "Dict User" and acc_d.balance == 300.0
passed(f"from_dict with balance → {acc_d}")

acc_d2 = BankAccount.from_dict({"owner": "No Balance"})
assert acc_d2.balance == 0.0
passed("from_dict without 'balance' key defaults to 0.0")

try:
    BankAccount.from_dict({"balance": 100.0})   # missing 'owner'
    failed("Should have raised KeyError for missing 'owner'")
except KeyError as e:
    passed(f"KeyError raised for missing 'owner' key → {e}")


# ── 7. __str__ and __repr__ ───────────────────────────────────────────────

section("7 · __str__ and __repr__")

acc_s = BankAccount("Repr Test", 42.0)
s = str(acc_s)
r = repr(acc_s)
assert "Repr Test" in s and "42.00" in s
assert "Repr Test" in r and "42.0" in r
passed(f"__str__  → {s}")
passed(f"__repr__ → {r}")


# ── Summary ────────────────────────────────────────────────────────────────

section("All tests completed")
print()
