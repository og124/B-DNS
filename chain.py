import hashlib

class Chain():
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.blocks = []
        self.pool = []

    def proof_of_work(self, block):
        hash = hashlib.sha256()
        hash.update(str(block).encode("utf-8"))
