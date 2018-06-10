import datetime
import hashlib


class BlockChain(object):
    PROOF_OF_WORK_PROBLEM = '0000'

    def __init__(self):
        self.chain = []
        self.create_block(previous_hash='0')

    def create_block(self, previous_hash):
        '''
        :param previous_hash:
        :return:
        '''

        block = {
            'index': len(self.chain),
            'time_stamp': str(datetime.datetime.now()),
            'data': '',
            'previous_hash': previous_hash,
        }

        if not self.chain:
            # this is genesis block
            block['hash'] = '0'
            block['nonce'] = '1'
        else:
            proof_of_work = self.proof_of_work(block)
            block['hash'] = proof_of_work['hash']
            block['nonce'] = proof_of_work['nonce']

        self.chain.append(block)

        return block

    @staticmethod
    def hash(block):
        hash_string = '{0}{1}{2}{3}{4}'.format(block['index'],
                                               block['time_stamp'],
                                               block['data'],
                                               block['previous_hash'],
                                               block['nonce'])
        data = hash_string.encode()
        return hashlib.sha256(data).hexdigest()

    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, block):
        nonce = 1
        block['nonce'] = nonce
        new_hash = self.hash(block)

        while new_hash[:4] != self.PROOF_OF_WORK_PROBLEM:
            nonce = nonce + 1
            block['nonce'] = nonce
            new_hash = self.hash(block)
        return {'nonce': nonce,
                'hash': new_hash}

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
            if self.hash(current_block) != current_block['hash']:
                return False
            index = index + 1
        return True

    def get_chain(self):
        return self.chain
