from flask import Flask, render_template, request, jsonify, redirect, url_for
import sys
import os

# Add the current directory to Python path to import our blockchain
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mini_blockchain import Blockchain, Block
import json
import time
from datetime import datetime

app = Flask(__name__)

# Global blockchain instance
blockchain = None

def init_blockchain():
    """Initialize a new blockchain."""
    global blockchain
    blockchain = Blockchain(difficulty=2)
    return blockchain

def get_blockchain():
    """Get the current blockchain instance."""
    global blockchain
    if blockchain is None:
        blockchain = init_blockchain()
    return blockchain

@app.route('/')
def index():
    """Main dashboard page."""
    bc = get_blockchain()
    
    # Get blockchain stats
    stats = {
        'total_blocks': len(bc.chain),
        'difficulty': bc.difficulty,
        'pending_transactions': len(bc.pending_transactions),
        'is_valid': bc.is_chain_valid(),
        'latest_block_hash': bc.get_latest_block().hash if bc.chain else None
    }
    
    # Get account balances
    addresses = set()
    for block in bc.chain[1:]:  # Skip genesis block
        transactions = block.data.split(" | ")
        for tx in transactions:
            if "sends" in tx and "to" in tx:
                parts = tx.split()
                if len(parts) >= 5:
                    addresses.add(parts[0])  # sender
                    addresses.add(parts[5])  # recipient
            elif "Mining Reward:" in tx:
                parts = tx.split()
                if "to" in tx:
                    addr_index = parts.index("to") + 1
                    if addr_index < len(parts):
                        addresses.add(parts[addr_index])
    
    balances = {}
    for addr in addresses:
        balance = bc.get_balance(addr)
        if balance != 0:
            balances[addr] = balance
    
    return render_template('index.html', stats=stats, balances=balances)

@app.route('/blockchain')
def view_blockchain():
    """View the entire blockchain."""
    bc = get_blockchain()
    
    # Format blocks for display
    blocks_data = []
    for block in bc.chain:
        block_info = {
            'index': block.index,
            'timestamp': datetime.fromtimestamp(block.timestamp).strftime("%Y-%m-%d %H:%M:%S"),
            'data': block.data,
            'previous_hash': block.previous_hash,
            'hash': block.hash,
            'nonce': block.nonce
        }
        blocks_data.append(block_info)
    
    return render_template('blockchain.html', blocks=blocks_data)

@app.route('/add_transaction', methods=['GET', 'POST'])
def add_transaction():
    """Add a new transaction."""
    if request.method == 'POST':
        sender = request.form['sender']
        receiver = request.form['receiver']
        amount = request.form['amount']
        
        if sender and receiver and amount:
            transaction = f"{sender} sends {amount} coins to {receiver}"
            bc = get_blockchain()
            bc.add_transaction(transaction)
            
            return redirect(url_for('transactions'))
        else:
            return render_template('add_transaction.html', error="All fields are required!")
    
    return render_template('add_transaction.html')

@app.route('/transactions')
def transactions():
    """View pending transactions."""
    bc = get_blockchain()
    return render_template('transactions.html', 
                         pending_transactions=bc.pending_transactions)

@app.route('/mine', methods=['POST'])
def mine_block():
    """Mine pending transactions."""
    bc = get_blockchain()
    miner_address = request.form.get('miner_address', 'Web Miner')
    
    if bc.pending_transactions:
        start_time = time.time()
        bc.mine_pending_transactions(miner_address)
        end_time = time.time()
        mining_time = end_time - start_time
        
        return jsonify({
            'success': True,
            'message': f'Block mined successfully in {mining_time:.2f} seconds!',
            'new_block_index': len(bc.chain) - 1
        })
    else:
        return jsonify({
            'success': False,
            'message': 'No pending transactions to mine!'
        })

@app.route('/validate')
def validate_chain():
    """Validate the blockchain."""
    bc = get_blockchain()
    is_valid = bc.is_chain_valid()
    
    return jsonify({
        'valid': is_valid,
        'message': 'Blockchain is valid!' if is_valid else 'Blockchain validation failed!'
    })

@app.route('/reset')
def reset_blockchain():
    """Reset the blockchain."""
    global blockchain
    blockchain = init_blockchain()
    return redirect(url_for('index'))

@app.route('/api/stats')
def api_stats():
    """API endpoint for blockchain statistics."""
    bc = get_blockchain()
    
    return jsonify({
        'total_blocks': len(bc.chain),
        'difficulty': bc.difficulty,
        'pending_transactions': len(bc.pending_transactions),
        'is_valid': bc.is_chain_valid(),
        'latest_block': {
            'index': bc.get_latest_block().index,
            'hash': bc.get_latest_block().hash,
            'timestamp': bc.get_latest_block().timestamp
        } if bc.chain else None
    })

@app.route('/api/blocks')
def api_blocks():
    """API endpoint for all blocks."""
    bc = get_blockchain()
    
    blocks = []
    for block in bc.chain:
        blocks.append({
            'index': block.index,
            'timestamp': block.timestamp,
            'data': block.data,
            'previous_hash': block.previous_hash,
            'hash': block.hash,
            'nonce': block.nonce
        })
    
    return jsonify(blocks)

@app.route('/api/balances')
def api_balances():
    """API endpoint for account balances."""
    bc = get_blockchain()
    
    # Get all addresses
    addresses = set()
    for block in bc.chain[1:]:  # Skip genesis block
        transactions = block.data.split(" | ")
        for tx in transactions:
            if "sends" in tx and "to" in tx:
                parts = tx.split()
                if len(parts) >= 5:
                    addresses.add(parts[0])  # sender
                    addresses.add(parts[5])  # recipient
            elif "Mining Reward:" in tx:
                parts = tx.split()
                if "to" in tx:
                    addr_index = parts.index("to") + 1
                    if addr_index < len(parts):
                        addresses.add(parts[addr_index])
    
    balances = {}
    for addr in addresses:
        balance = bc.get_balance(addr)
        balances[addr] = balance
    
    return jsonify(balances)

@app.route('/demo')
def demo():
    """Load demo data."""
    global blockchain
    blockchain = init_blockchain()
    
    # Add demo transactions
    bc = get_blockchain()
    bc.add_transaction("Alice sends 50 coins to Bob")
    bc.add_transaction("Bob sends 25 coins to Charlie")
    bc.mine_pending_transactions("Miner1")
    
    bc.add_transaction("Charlie sends 10 coins to Diana")
    bc.add_transaction("Diana sends 5 coins to Eve")
    bc.mine_pending_transactions("Miner2")
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Initialize blockchain on startup
    init_blockchain()
    app.run(debug=True, host='0.0.0.0', port=5001)
