from uuid import uuid4

from wallet import Wallet
from blockchain import Blockchain
from utility.verification import Verification


class Node:
    def __init__(self):
        # self.wallet.public_key = str(uuid4())
        self.wallet = Wallet()
        self.blockchain = Blockchain(self.wallet.public_key)

    def get_user_choice(self):
        return input("Your choice: ")

    def print_blockchain_elements(self):
        for index, block in enumerate(self.blockchain.chain):
            print("Block at index " + str(index) + ":", block)
        else:
            print("-" * 20)

    def print_balance(self):
        calculate_balance = self.blockchain.get_balance()
        print("Balance of {}: {:6.2f}".format(
            self.wallet.public_key, calculate_balance))

    def get_transaction_value(self):
        recipient = input("Enter the recipient of the transaction: ")
        amount = float(input("Your transaction amount: "))
        return recipient, amount

    def listen_for_user_input(self):
        waiting_for_input = True
        while waiting_for_input:
            print("Please choose")
            print("1) Add a new value to blockchain.")
            print("2) Mine open transactions.")
            print("3) Print out blockchain.")
            print("4) Check open transactions for validity.")
            print("5) Create wallet.")
            print("6) Load wallet.")
            print("q) Quit program.")
            choice = self.get_user_choice()
            if choice == "1":
                recipient, amount = self.get_transaction_value()
                if self.blockchain.add_transaction(self.wallet.public_key, recipient, amount):
                    print("Added Transaction.")
                else:
                    print("Transaction failed.")
            elif choice == "2":
                self.blockchain.mine_block()
            elif choice == "3":
                self.print_blockchain_elements()
            elif choice == "4":
                print(Verification.check_transactions_validity(
                    self.blockchain.get_open_transactions, self.blockchain.get_balance))
            elif choice == "5":
                self.wallet.create_keys()
            elif choice == "6":
                pass
            elif choice == "q":
                waiting_for_input = False
            else:
                print("Input is invalid.")
            if not Verification.verify_blockchain(self.blockchain.chain):
                print("Blockchain is not valid!")
                waiting_for_input = False
            self.print_balance()
        else:
            print("User left.")


if __name__ == "__main__":
    node = Node()
    node.listen_for_user_input()
