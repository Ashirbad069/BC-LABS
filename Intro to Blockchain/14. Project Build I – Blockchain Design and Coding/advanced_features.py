#!/usr/bin/env python3
"""
Advanced BlockSim Features
Additional blockchain features including network simulation, consensus, and more
"""

import hashlib
import json
import random
import time
from typing import List, Dict, Any
from mini_blockchain import Blockchain, Block


class ProofOfStakeBlock(Block):
    """Enhanced block with Proof of Stake features."""
    
    def __init__(self, index: int, data: str, previous_hash: str, validator: str, timestamp: float = None):
        self.validator = validator
        super().__init__(index, data, previous_hash, timestamp)
    
    def calculate_hash(self) -> str:
        """Calculate hash including validator info."""
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "validator": self.validator,
            "nonce": self.nonce
        }, sort_keys=True)
        
        return hashlib.sha256(block_string.encode()).hexdigest()


class NetworkNode:
    """Represents a node in the blockchain network."""
    
    def __init__(self, node_id: str, stake: float = 0):
        self.node_id = node_id
        self.stake = stake
        self.blockchain = Blockchain(difficulty=2)
        self.peers: List['NetworkNode'] = []
        self.is_online = True
    
    def add_peer(self, peer: 'NetworkNode'):
        """Add a peer node to the network."""
        if peer not in self.peers:
            self.peers.append(peer)
            peer.peers.append(self)
    
    def broadcast_block(self, block: Block):
        """Broadcast a new block to all peers."""
        if not self.is_online:
            return
        
        print(f"📡 Node {self.node_id} broadcasting block #{block.index}")
        for peer in self.peers:
            if peer.is_online and peer.validate_and_add_block(block):
                print(f"   ✅ Block accepted by {peer.node_id}")
            elif peer.is_online:
                print(f"   ❌ Block rejected by {peer.node_id}")
    
    def validate_and_add_block(self, block: Block) -> bool:
        """Validate and potentially add a block from a peer."""
        # Check if block is valid for our chain
        if (len(self.blockchain.chain) == block.index and 
            self.blockchain.get_latest_block().hash == block.previous_hash):
            self.blockchain.chain.append(block)
            return True
        return False
    
    def mine_block(self, data: str):
        """Mine a new block and broadcast it."""
        if not self.is_online:
            return
        
        new_block = Block(
            index=len(self.blockchain.chain),
            data=f"[{self.node_id}] {data}",
            previous_hash=self.blockchain.get_latest_block().hash
        )
        
        new_block.mine_block(self.blockchain.difficulty)
        self.blockchain.chain.append(new_block)
        self.broadcast_block(new_block)


class BlockchainNetwork:
    """Simulates a network of blockchain nodes."""
    
    def __init__(self):
        self.nodes: List[NetworkNode] = []
        self.transaction_pool: List[str] = []
    
    def add_node(self, node_id: str, stake: float = 0) -> NetworkNode:
        """Add a new node to the network."""
        node = NetworkNode(node_id, stake)
        self.nodes.append(node)
        
        # Connect to existing nodes (simplified full mesh)
        for existing_node in self.nodes[:-1]:
            node.add_peer(existing_node)
        
        print(f"🌐 Node {node_id} joined the network")
        return node
    
    def simulate_transaction(self, sender: str, receiver: str, amount: float):
        """Add a transaction to the pool."""
        transaction = f"{sender} sends {amount} coins to {receiver}"
        self.transaction_pool.append(transaction)
        print(f"💸 Transaction added: {transaction}")
    
    def random_mining_round(self):
        """Simulate a random node mining the next block."""
        if not self.transaction_pool or not self.nodes:
            return
        
        # Select a random online node to mine
        online_nodes = [node for node in self.nodes if node.is_online]
        if not online_nodes:
            return
        
        miner = random.choice(online_nodes)
        transactions = " | ".join(self.transaction_pool)
        
        print(f"\n⛏️  Mining round - {miner.node_id} selected as miner")
        miner.mine_block(transactions)
        
        # Clear transaction pool
        self.transaction_pool = []
    
    def show_network_status(self):
        """Display the status of all nodes in the network."""
        print("\n🌐 NETWORK STATUS")
        print("=" * 60)
        
        for node in self.nodes:
            status = "🟢 Online" if node.is_online else "🔴 Offline"
            peers_count = len([p for p in node.peers if p.is_online])
            
            print(f"📡 Node: {node.node_id}")
            print(f"   Status: {status}")
            print(f"   Blocks: {len(node.blockchain.chain)}")
            print(f"   Peers: {peers_count}")
            if node.blockchain.chain:
                latest_hash = node.blockchain.chain[-1].hash[:10]
                print(f"   Latest Hash: {latest_hash}...")
            print()
    
    def check_consensus(self) -> bool:
        """Check if all online nodes have the same blockchain."""
        if not self.nodes:
            return True
        
        online_nodes = [node for node in self.nodes if node.is_online]
        if not online_nodes:
            return True
        
        # Compare chain lengths and latest hashes
        reference_node = online_nodes[0]
        ref_length = len(reference_node.blockchain.chain)
        ref_hash = reference_node.blockchain.chain[-1].hash if reference_node.blockchain.chain else ""
        
        for node in online_nodes[1:]:
            if (len(node.blockchain.chain) != ref_length or
                (node.blockchain.chain and node.blockchain.chain[-1].hash != ref_hash)):
                return False
        
        return True


class TransactionPool:
    """Enhanced transaction pool with validation."""
    
    def __init__(self):
        self.transactions: List[Dict[str, Any]] = []
        self.balances: Dict[str, float] = {}
    
    def add_transaction(self, sender: str, receiver: str, amount: float, fee: float = 0):
        """Add a validated transaction to the pool."""
        # Check if sender has sufficient balance
        if self.balances.get(sender, 0) < amount + fee:
            print(f"❌ Insufficient balance for {sender}")
            return False
        
        transaction = {
            'sender': sender,
            'receiver': receiver,
            'amount': amount,
            'fee': fee,
            'timestamp': time.time(),
            'signature': self.sign_transaction(sender, receiver, amount, fee)
        }
        
        self.transactions.append(transaction)
        print(f"✅ Transaction added: {sender} → {receiver}: {amount} coins")
        return True
    
    def sign_transaction(self, sender: str, receiver: str, amount: float, fee: float) -> str:
        """Create a simple signature for the transaction."""
        transaction_string = f"{sender}{receiver}{amount}{fee}"
        return hashlib.sha256(transaction_string.encode()).hexdigest()[:16]
    
    def get_pending_transactions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get pending transactions sorted by fee (highest first)."""
        sorted_transactions = sorted(
            self.transactions, 
            key=lambda x: x['fee'], 
            reverse=True
        )
        return sorted_transactions[:limit]
    
    def update_balance(self, address: str, amount: float):
        """Update balance for an address."""
        self.balances[address] = self.balances.get(address, 0) + amount


def demo_advanced_features():
    """Demo advanced blockchain features."""
    print("🚀 ADVANCED BLOCKSIM FEATURES DEMO")
    print("=" * 60)
    
    # Create a network simulation
    network = BlockchainNetwork()
    
    # Add nodes to the network
    alice = network.add_node("Alice", stake=100)
    bob = network.add_node("Bob", stake=75)
    charlie = network.add_node("Charlie", stake=50)
    diana = network.add_node("Diana", stake=25)
    
    print(f"\n🌐 Network created with {len(network.nodes)} nodes")
    
    # Simulate some transactions
    print("\n💸 Simulating transactions...")
    network.simulate_transaction("Alice", "Bob", 10)
    network.simulate_transaction("Bob", "Charlie", 5)
    network.simulate_transaction("Charlie", "Diana", 3)
    
    # Run mining rounds
    print("\n⛏️  Running mining simulation...")
    for round_num in range(3):
        print(f"\n--- Mining Round {round_num + 1} ---")
        network.random_mining_round()
        time.sleep(0.5)  # Small delay for demo
    
    # Show network status
    network.show_network_status()
    
    # Check consensus
    consensus = network.check_consensus()
    print(f"🤝 Network Consensus: {'✅ Achieved' if consensus else '❌ Split'}")
    
    # Simulate a node going offline
    print(f"\n🔌 Taking {charlie.node_id} offline...")
    charlie.is_online = False
    
    # Add more transactions and mine
    network.simulate_transaction("Diana", "Alice", 2)
    network.random_mining_round()
    
    # Show updated status
    network.show_network_status()
    
    # Demonstrate transaction pool
    print("\n💰 TRANSACTION POOL DEMO")
    print("-" * 40)
    
    tx_pool = TransactionPool()
    
    # Initialize some balances
    tx_pool.update_balance("User1", 100)
    tx_pool.update_balance("User2", 50)
    tx_pool.update_balance("User3", 75)
    
    # Add transactions with different fees
    tx_pool.add_transaction("User1", "User2", 20, fee=2.0)
    tx_pool.add_transaction("User2", "User3", 10, fee=1.5)
    tx_pool.add_transaction("User3", "User1", 5, fee=3.0)
    
    # Show pending transactions
    pending = tx_pool.get_pending_transactions()
    print("\n📋 Pending Transactions (sorted by fee):")
    for i, tx in enumerate(pending, 1):
        print(f"   {i}. {tx['sender']} → {tx['receiver']}: {tx['amount']} coins (fee: {tx['fee']})")


if __name__ == "__main__":
    demo_advanced_features()
