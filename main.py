from block import Block

block = Block("Hello world")
block.mine(10)

print(block.hash.hexdigest())
print(block.nonce)
print(block.data)


