from hashlib import sha256
import json


def hash_string_256(string):
    return sha256(string).hexdigest()


def hash_block(block):
    block_dict = block.__dict__.copy()
    block_dict["transactions"] = [tx.to_ordered_dict()
                                  for tx in block_dict["transactions"]]
    return sha256(json.dumps(block_dict, sort_keys=True).encode()).hexdigest()
