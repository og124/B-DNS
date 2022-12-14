import hashlib

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calc_hash()

    def calc_hash(self):
        return hashlib.sha256(str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash)).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(data="Genesis block")

    def create_block(self, data):
        index = len(self.chain)
        timestamp = time.time()
        previous_hash = self.chain[-1].hash if len(self.chain) > 0 else None
        block = Block(index, timestamp, data, previous_hash)
        self.chain.append(block)
        return block

    def get_last_block(self):
        return self.chain[-1]

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            if current_block.hash != current_block.calc_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

app = Flask(__name__)
CORS(app)

blockchain = Blockchain()

@app.route('/new-transaction', methods=['POST'])
def new_transaction():
    data = request.get_json()
    required_fields = ['domain_name', 'ip_address']

    for field in required_fields:
        if not data.get(field):
            return "Invalid transaction data", 400

    data['timestamp'] = time.time()
    blockchain.create_block(data)

    response = {
        'message': 'Success: new transaction added to the blockchain.'
    }
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def get_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/is-valid', methods=['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid()
    if is_valid:
        response = {'message': 'The blockchain is valid.'}
    else:
        response = {'message': 'The blockchain is not valid.'}
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

@app.route('/get-domain-name/<string:domain_name>', methods=['GET'])
def get_domain_name(domain_name):
    for block in blockchain.chain:
        if domain_name == block['data']['domain_name']:
            response = {
                'message': 'Success: domain name found in the blockchain.',
                'ip_address': block['data']['ip_address']
            }
            return jsonify(response), 200
    response = {
        'message': 'Error: domain name not found in the blockchain.'
    }
    return jsonify(response), 404

@app.route('/get-ip-address/<string:ip_address>', methods=['GET'])
def get_ip_address(ip_address):
    domain_names = []
    for block in blockchain.chain:
        if ip_address == block['data']['ip_address']:
            domain_names.append(block['data']['domain_name'])
    if len(domain_names) > 0:
        response = {
            'message': 'Success: IP address found in the blockchain.',
            'domain_names': domain_names
        }
        return jsonify(response), 200
    response = {
        'message': 'Error: IP address not found in the blockchain.'
    }
    return jsonify(response), 404

@app.route('/update-domain-name/<string:domain_name>', methods=['PUT'])
def update_domain_name(domain_name):
    data = request.get_json()
    required_fields = ['new_ip_address']

    for field in required_fields:
        if not data.get(field):
            return "Invalid transaction data", 400

    for block in blockchain.chain:
        if domain_name == block['data']['domain_name']:
            block['data']['ip_address'] = data['new_ip_address']
            response = {
                'message': 'Success: domain name updated in the blockchain.'
            }
            return jsonify(response), 200

    response = {
        'message': 'Error: domain name not found in the blockchain.'
    }
    return jsonify(response), 404

@app.route('/delete-domain-name/<string:domain_name>', methods=['DELETE'])
def delete_domain_name(domain_name):
    for block in blockchain.chain:
        if domain_name == block['data']['domain_name']:
            blockchain.chain.remove(block)
            response = {
                'message': 'Success: domain name deleted from the blockchain.'
            }
            return jsonify(response), 200

    response = {
        'message': 'Error: domain name not found in the blockchain.'
    }
    return jsonify(response), 404

@app.route('/update-ip-address/<string:ip_address>', methods=['PUT'])
def update_ip_address(ip_address):
    data = request.get_json()
    required_fields = ['new_ip_address']

    for field in required_fields:
        if not data.get(field):
            return "Invalid transaction data", 400

    for block in blockchain.chain:
        if ip_address == block['data']['ip_address']:
            block['data']['ip_address'] = data['new_ip_address']

    response = {
        'message': 'Success: IP address updated in the blockchain.'
    }
    return jsonify(response), 200

@app.route('/delete-ip-address/<string:ip_address>', methods=['DELETE'])
def delete_ip_address(ip_address):
    for block in blockchain.chain:
        if ip_address == block['data']['ip_address']:
            blockchain.chain.remove(block)

    response = {
        'message': 'Success: IP address deleted from the blockchain.'
    }
    return jsonify(response), 200

@app.route('/delete-chain', methods=['DELETE'])
def delete_chain():
    blockchain.chain = []
    response = {
        'message': 'Success: blockchain deleted.'
    }
    return jsonify(response), 200
