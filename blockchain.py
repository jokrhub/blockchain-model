import json
import datetime
import hashlib

class Block():
    def __init__(self, index, timestamp, transactions, proof, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.proof = proof
        self.previous_hash = previous_hash

    def __repr__(self):
        return '''
            Block [
                Index: {}
                Timestamp: {}
                Transactions: {}
                Proof: {}
                Previous Hash: {}
            ]
        '''.format(
            self.index,
            self.timestamp,
            "".join(['['] + [x.__repr__() for x in self.transactions] + ['\t]']),
            self.proof,
            self.previous_hash
        )

    # generate a hash of an entire block
    def hash(self):
        block = {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': self.transactions.__repr__(),
            'proof': self.proof,
            'previous_hash': self.previous_hash
        }
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()



class Transaction():
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    def __repr__(self):
        return '''
                    {} sent {} to {}
        '''.format(
            self.sender,
            self.amount,
            self.recipient
        )

class Blockchain():
    def __init__(self):
        self.block_chain = []
        self.pending_transactions = []

        # add genesis block
        self.mine_block(1, '0')

    def proof_of_work(self, previous_proof):
        # generate proof of work
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def is_chain_valid(self):
        # validate that blockchain is not tampered
        previous_block = self.block_chain[0]
        block_index = 1
        while block_index < len(self.block_chain):
            block = self.block_chain[block_index]
            if block.previous_hash != previous_block.hash():
                print("Block chain tempered!")

            previous_proof = previous_block.proof
            current_proof = block.proof

            hash_operation = hashlib.sha256(str(current_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                print("Block chain tempered!")
            previous_block = block
            block_index += 1
        print("Block chain is valid!")

    def mine_block(self, proof, previous_hash):
        # create new block
        new_block = Block(
            len(self.block_chain) + 1,
            str(datetime.datetime.now()),
            self.pending_transactions,
            proof,
            previous_hash
        )
        self.pending_transactions = []
        self.block_chain.append(new_block)

    def initiate_transaction(self, sender, recipient, amount):
        new_transaction = Transaction(sender, recipient, amount)
        self.pending_transactions.append(new_transaction)

    @property
    def last_block(self):
        return self.block_chain[-1]


if __name__=="__main__":

    block_chain = Blockchain()
    block_chain.initiate_transaction("Joe", "Karter", "5 BTC")
    block_chain.initiate_transaction("Harry", "Porter", "6 BTC")

    # mine a block
    previous_hash = block_chain.last_block.hash()
    previous_proof = block_chain.last_block.proof
    proof = block_chain.proof_of_work(previous_proof)

    block_chain.mine_block(proof, previous_hash)

    block_chain.initiate_transaction("Sammy", "Roger", "2 BTC")
    block_chain.initiate_transaction("Stella", "Coxy", "19 BTC")
    block_chain.initiate_transaction("Logan", "Alex", "23 BTC")
    
    # mine a block
    previous_hash = block_chain.last_block.hash()
    previous_proof = block_chain.last_block.proof
    proof = block_chain.proof_of_work(previous_proof)

    block_chain.mine_block(proof, previous_hash)

    # print the block chain
    for block in block_chain.block_chain:
        print(block)

    # validate the blockchain
    block_chain.is_chain_valid()