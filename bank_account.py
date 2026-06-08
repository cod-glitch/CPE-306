# ─────────────────────────────────────────────
#  Custom Exception
# ─────────────────────────────────────────────

class InsufficientFundsError(Exception):
    """Raised when a withdrawal exceeds the available balance
    (including the transaction fee)."""

    def __init__(self, amount: float, balance: float, fee: float):
        self.amount = amount
        self.balance = balance
        self.fee = fee
        super().__init__(
            f"Cannot withdraw ₦{amount:.2f} + ₦{fee:.2f} fee "
            f"(total ₦{amount + fee:.2f}); available balance is ₦{balance:.2f}."
        )


# ─────────────────────────────────────────────
#  BankAccount Class
# ─────────────────────────────────────────────

class BankAccount:
    """A simple bank account with deposit/withdrawal support and a per-withdrawal fee."""

    # Class-level transaction fee deducted on every withdrawal
    transaction_fee: float = 0.50

    # ── Construction ──────────────────────────

    def __init__(self, owner: str, initial_balance: float = 0.0) -> None:
        """
        Parameters
        ----------
        owner           : Account holder's name.
        initial_balance : Starting balance (must be >= 0).

        Raises
        ------
        ValueError  If initial_balance is negative.
        """
        if initial_balance < 0:
            raise ValueError(
                f"Initial balance cannot be negative; got {initial_balance}."
            )
        self.owner: str = owner
        self._balance: float = float(initial_balance)   # private attribute

    # ── Read-only property ────────────────────

    @property
    def balance(self) -> float:
        """Current account balance (read-only)."""
        return self._balance

    # ── Deposit ───────────────────────────────

    def deposit(self, amount: float) -> float:
        """Add *amount* to the balance and return the new balance.

        Raises
        ------
        ValueError  If amount is not strictly positive.
        """
        if amount <= 0:
            raise ValueError(
                f"Deposit amount must be positive; got {amount}."
            )
        self._balance += amount
        return self._balance

    # ── Withdrawal ────────────────────────────

    def withdraw(self, amount: float) -> float:
        """Subtract *amount* + transaction_fee from the balance and return new balance.

        ⚠️  THE PROBLEM (see notes at bottom of file):
            The total cost of a withdrawal is  amount + transaction_fee.
            The InsufficientFundsError guard must therefore check against
            that *combined* total, NOT just the raw amount.

        Raises
        ------
        ValueError              If amount is not strictly positive.
        InsufficientFundsError  If (amount + transaction_fee) > balance.
        """
        if amount <= 0:
            raise ValueError(
                f"Withdrawal amount must be positive; got {amount}."
            )

        total_cost = amount + BankAccount.transaction_fee
        if total_cost > self._balance:
            raise InsufficientFundsError(amount, self._balance, BankAccount.transaction_fee)

        self._balance -= total_cost
        return self._balance

    # ── Alternate constructor ─────────────────

    @classmethod
    def from_dict(cls, data: dict) -> "BankAccount":
        """Create a BankAccount from a dictionary.

        Expected keys
        -------------
        'owner'   : str   – account holder name
        'balance' : float – initial balance (optional, defaults to 0.0)

        Raises
        ------
        KeyError    If 'owner' key is missing.
        ValueError  If balance is negative (propagated from __init__).
        """
        owner = data["owner"]                          # KeyError if missing
        balance = data.get("balance", 0.0)
        return cls(owner, balance)

    # ── String representations ────────────────

    def __str__(self) -> str:
        return (
            f"BankAccount(owner='{self.owner}', "
            f"balance=₦{self._balance:.2f})"
        )

    def __repr__(self) -> str:
        return (
            f"BankAccount(owner={self.owner!r}, "
            f"initial_balance={self._balance!r})"
        )


# ─────────────────────────────────────────────
#  ⚠️  THE PROBLEM — Identified & Explained
# ─────────────────────────────────────────────
#
#  The subtle but critical bug that a naive implementation produces:
#
#  WRONG guard (common mistake):
#      if amount > self._balance:          ← ignores the fee
#          raise InsufficientFundsError(...)
#      self._balance -= (amount + transaction_fee)   ← fee silently overdrafts!
#
#  SCENARIO:
#      balance = ₦10.00
#      withdraw(₦10.00)
#
#      Wrong code:  10.00 > 10.00 → False  →  proceeds
#                   balance becomes  10.00 - 10.00 - 0.50  =  -0.50  ← OVERDRAFT!
#
#  CORRECT guard (used above):
#      total_cost = amount + transaction_fee       # ₦10.50
#      if total_cost > self._balance:              # 10.50 > 10.00 → True → raises!
#          raise InsufficientFundsError(...)
#
#  The fee must be factored into the affordability check BEFORE the
#  balance is modified, not after. Doing it after allows the account
#  balance to go negative — silently breaking the class invariant.
