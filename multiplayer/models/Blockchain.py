import hashlib
import json
from time import time



class Blockchain:
    def __init__(self, author):
        self.curr_proof = 10
        self.chain = []
        self.author = author
        # Create the genesis block
        self.new_block(previous_hash='1', proof=10)

    def new_block(self, proof, previous_hash, comment="generic comment"):
        block = {
            'timestamp': time(),
            'proof': proof or self.curr_proof,
            'comment': comment,
            'author': self.author,
            'previous_hash': previous_hash or self.chain[-1]['hash'],
        }
        block['hash'] = self.hash(block)
        self.chain.append(block)
        return block

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block
        :param block: Block
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_block):
        """
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains leading 4 zeroes
         - Where p is the previous proof, and p' is the new proof

        :param last_block: <dict> last Block
        :return: <int>
        """

        last_proof = last_block['proof']
        last_hash = self.hash(last_block)

        proof = 0
        while self.valid_proof(last_proof, proof, last_hash) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof, last_hash):
        """
        Validates the Proof
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :param last_hash: <str> The hash of the Previous Block
        :return: <bool> True if correct, False if not.
        """

        guess = str(str(last_proof)+str(proof)+str(last_hash)).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
