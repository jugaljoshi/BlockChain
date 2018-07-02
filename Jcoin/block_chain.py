import datetime
import hashlib
from urllib.parse import urlparse
import requests


class BlockChain(object):
    PROOF_OF_WORK_PROBLEM = '0000'

    def __init__(self):
        self.chain = []
        self.transaction = []
        self.add_block_to_chain(self.get_default_block(), 0, '0')
        self.nodes = set()

    def get_default_block(self, previous_hash='0'):
        return {
            'index': len(self.chain),
            'time_stamp': str(datetime.datetime.now()),
            'transaction': self.transaction,
            'previous_hash': previous_hash,
        }

    def add_block_to_chain(self, block, nonce, new_hash):
        '''
        :param block: dict
        :param nonce: int
        :param new_hash: string
        :return:
        '''
        block['nonce'] = nonce
        block['hash'] = new_hash
        self.transaction = []
        self.chain.append(block)
        return block

    def mine_block(self, previous_hash):
        block = self.get_default_block(previous_hash=previous_hash)
        proof_of_work = self.proof_of_work(block)
        new_hash = proof_of_work['new_hash']
        nonce = proof_of_work['nonce']
        block = self.add_block_to_chain(block, nonce, new_hash)
        return block

    @staticmethod
    def generate_hash(nonce, block):
        hash_string = '{0}{1}{2}{3}{4}'.format(block['index'],
                                               block['time_stamp'],
                                               block['transaction'],
                                               block['previous_hash'],
                                               nonce)
        data = hash_string.encode()
        return hashlib.sha256(data).hexdigest()

    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, block):
        nonce = 1
        new_hash = self.generate_hash(nonce, block)

        while new_hash[:4] != self.PROOF_OF_WORK_PROBLEM:
            nonce = nonce + 1
            new_hash = self.generate_hash(nonce, block)
        return {'nonce': nonce,
                'new_hash': new_hash}

    def is_chain_valid(self):
        # 1: check if previous block hash and current block hash matching
        # 2: check if each block hash is correct or not

        index = 1
        chain_length = len(self.chain)

        while index < chain_length:
            previous_block = self.chain[index - 1]
            current_block = self.chain[index]

            if previous_block['hash'] != current_block['previous_hash']:
                return False
            if self.generate_hash(current_block['nonce'], current_block) != current_block['hash']:
                return False
            index = index + 1
        return True

    def get_chain(self):
        return self.chain

    def add_nodes(self, nodes):
        for node in nodes:
            node_url = urlparse(node)
            if node_url and node_url.get('netloc'):
                self.nodes.add(node_url.get('netloc'))
        return self.nodes

    def add_transaction(self, sender, receiver, amount):
        self.transaction.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        })

        return self.last_block()['index'] + 1

    def sync_block(self):
        all_nodes = self.nodes

        # r = requests.get('https://api.spotify.com/v1/search?type=artist&q=snoop')
        # r.json()




