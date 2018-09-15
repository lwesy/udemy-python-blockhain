import json
from functools import reduce
from hashlib import sha256

from block import Block
from transaction import Transaction
from hash_util import hash_block, hash_string_256
from create_utils import convert_block
from tx_utils import calc_sum_of_tx
from print_utils import print_balance, print_menu, print_blockchain_elements

MINING_REWARD = 10
owner = "Liam"
blockchain = []
open_transactions = []
participants = {owner}


def save_data():
    try:
        with open("blockchain.txt", mode="w") as f:
            saveable_blockchain = [block.__dict__ for block in [
                Block(block_el.previous_hash, block_el.index, [tx.__dict__ for tx in block_el.transactions], block_el.proof) for block_el in blockchain]]
            f.write(json.dumps(saveable_blockchain))
            f.write("\n")
            saveable_transactions = [tx.__dict__ for tx in open_transactions]
            f.write(json.dumps(saveable_transactions))
    except IOError:
        print("Savin failed!")


def load_data():
    global blockchain
    global open_transactions
    try:
        with open("blockchain.txt", mode="r") as f:
            file_contents = f.readlines()
            global blockchain
            global open_transactions
            json_blockchain = json.loads(file_contents[0][:-1])
            json_open_transaction = json.loads(file_contents[1])
            blockchain = list(map(convert_block, json_blockchain))
            open_transactions = [Transaction(
                tx["sender"], tx["recipient"], tx["amount"]) for tx in json_open_transaction]
    except (IOError, IndexError):
        genesis_block = Block("", 0, [], 100)
        blockchain = [genesis_block]
        open_transactions = []


load_data()


def valid_proof(transactions, last_hash, proof):
    guess = (str([tx.to_ordered_dict()
                  for tx in transactions]) + last_hash + str(proof)).encode()
    guess_hash = sha256(guess).hexdigest()
    return guess_hash[0:2] == "00"


def proof_of_work():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    proof = 0
    while not valid_proof(open_transactions, hashed_block, proof):
        proof += 1
    return proof


def get_last_blockchain_value():
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(sender, recipient, amount):
    transaction = Transaction(sender, recipient, amount)
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        save_data()
        return True
    return False


def get_transaction_value():
    recipient = input("Enter the recipient of the transaction: ")
    amount = float(input("Your transaction amount: "))
    return recipient, amount


def get_user_choice():
    return input("Your choice: ")


def verify_blockchain():
    for index, block in enumerate(blockchain):
        if index == 0:
            continue
        if block.previous_hash != hash_block(blockchain[index - 1]):
            return False
        if not valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
            print("Proof of Work invalid")
            return False
    return True


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    proof = proof_of_work()
    reward_transaction = Transaction("MINING", owner, MINING_REWARD)
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = Block(hashed_block, len(blockchain), copied_transactions, proof)
    blockchain.append(block)
    return True


def verify_transaction(transaction):
    sender_balance = get_balance(transaction.sender)
    return sender_balance >= transaction.amount


def get_all_tx_of(participant):
    tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant]
                 for block in blockchain]
    open_tx_sender = [tx.amount
                      for tx in open_transactions if tx.sender == participant]
    tx_sender.append(open_tx_sender)
    tx_recipient = [[tx.amount for tx in block.transactions if tx.recipient == participant]
                    for block in blockchain]
    return tx_sender, tx_recipient


def get_balance(participant):
    tx_sender, tx_recipient = get_all_tx_of(participant)
    amount_sent = reduce(calc_sum_of_tx, tx_sender, 0)
    amount_received = reduce(calc_sum_of_tx, tx_recipient, 0)
    return amount_received - amount_sent


def check_transactions_validity():
    return any([verify_transaction(tx) for tx in open_transactions])


waiting_for_input = True

while waiting_for_input:
    print_menu()
    choice = get_user_choice()

    if choice == "1":
        recipient, amount = get_transaction_value()
        if add_transaction(owner, recipient, amount):
            print("Added Transaction.")
        else:
            print("Transaction failed.")
    elif choice == "2":
        if mine_block():
            open_transactions = []
            save_data()
    elif choice == "3":
        print_blockchain_elements(blockchain)
    elif choice == "4":
        print(participants)
    elif choice == "5":
        print(check_transactions_validity())
    elif choice == "q":
        waiting_for_input = False
    else:
        print("Input is invalid.")
    if not verify_blockchain():
        print("Blockchain is not valid!")
        waiting_for_input = False
    print_balance("Marlena", get_balance("Marlena"))
    print_balance("Liam", get_balance("Liam"))
else:
    print("User left.")

print("Done!")
