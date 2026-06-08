"""
BankAccount Class
Student: Omolola Fathiu Adedamola
Matric No: CPE/2023/1093
"""

class InsufficientFundsError(Exception):
    """Custom exception raised when withdrawal amount + fee exceeds balance."""
    pass

class BankAccount:
    """A simple bank account with deposit, withdrawal, and a transaction fee."""
    
    transaction_fee = 0.50   # class attribute deducted from every withdrawal
    
    def __init__(self, owner: str, initial_balance: float = 0.0):
        """Constructor with owner name and optional initial balance (default 0.0)."""
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative")
        self._owner = owner
        self._balance = initial_balance
    
    @property
    def balance(self) -> float:
        """Read-only property for balance."""
        return self._balance
    
    @property
    def owner(self) -> str:
        """Read-only property for owner."""
        return self._owner
    
    def deposit(self, amount: float) -> None:
        """Add positive amount to balance. Raises ValueError if amount <= 0."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self._balance += amount
    
    def withdraw(self, amount: float) -> None:
        """
        Subtract amount + transaction_fee from balance.
        Raises ValueError if amount <= 0.
        Raises InsufficientFundsError if amount + fee > balance.
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        total_deduction = amount + self.transaction_fee
        if total_deduction > self._balance:
            raise InsufficientFundsError(
                f"Insufficient funds: need {total_deduction:.2f}, available {self._balance:.2f}"
            )
        self._balance -= total_deduction
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create a BankAccount from a dictionary with 'owner' and 'balance' keys."""
        return cls(data['owner'], data['balance'])
    
    def __str__(self) -> str:
        """User-friendly string representation."""
        return f"BankAccount(owner='{self.owner}', balance={self.balance:.2f})"
    
    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return f"BankAccount('{self.owner}', {self.balance})"
