import time

class DeFiPlatform:
    def __init__(self):
        self.wallets = {}  # {user_address: balance}
        self.loans = {}    # {user_address: {'amount': x, 'interest_rate': y, 'start_time': z}}
        self.annual_interest_rate = 0.05

    def deposit(self, user, amount):
        self.wallets[user] = self.wallets.get(user, 0) + amount
        print(f"{user} deposited {amount}. New balance: {self.wallets[user]}")

    def borrow(self, user, amount):
        if amount > 0:
            self.loans[user] = {
                'amount': amount,
                'rate': self.annual_interest_rate,
                'timestamp': time.time()
            }
            self.wallets[user] = self.wallets.get(user, 0) + amount
            print(f"{user} borrowed {amount} at {self.annual_interest_rate*100}% interest.")

    def repay_loan(self, user):
        if user not in self.loans: return
        
        loan = self.loans[user]
        # Simplified interest calculation based on seconds for demo
        duration = time.time() - loan['timestamp']
        interest = loan['amount'] * loan['rate'] * (duration / 3600) # Per hour for demo
        total_due = loan['amount'] + interest
        
        if self.wallets.get(user, 0) >= total_due:
            self.wallets[user] -= total_due
            del self.loans[user]
            print(f"{user} repaid {total_due:.4f} (Interest: {interest:.4f})")
        else:
            print(f"Insufficient funds for {user} to repay loan.")

# Execution
defi = DeFiPlatform()
defi.deposit("User_A", 100)
defi.borrow("User_A", 50)
time.sleep(1) # Simulating time passage
defi.repay_loan("User_A")