import hashlib
import json
import time
from datetime import datetime
from typing import List, Dict, Any, Optional


class Block:
    """
    Represents a single block in the blockchain.
    """
    
    def __init__(self, index: int, data: str, previous_hash: str, timestamp: float = None):
        """
        Initialize a new block.
        
        Args:
            index: Block number in the chain
            data: Transaction information or data stored in the block
            previous_hash: Hash of the previous block
            timestamp: Time when block was created (defaults to current time)
        """
        self.index = index
        self.timestamp = timestamp or time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0  # For proof of work
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """
        Calculate SHA256 hash of the block's contents.
        
        Returns:
            Hexadecimal string representation of the hash
        """
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int = 2):
        """
        Mine the block using proof of work algorithm.
        
        Args:
            difficulty: Number of leading zeros required in hash
        """
        target = "0" * difficulty
        print(f"⛏️  Mining block {self.index}...")
        
        start_time = time.time()
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        
        end_time = time.time()
        print(f"✅ Block {self.index} mined in {end_time - start_time:.2f} seconds!")
        print(f"📋 Hash: {self.hash}")
        print(f"🔢 Nonce: {self.nonce}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert block to dictionary for JSON serialization."""
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "hash": self.hash,
            "nonce": self.nonce
        }
    
    def __str__(self) -> str:
        """String representation of the block."""
        readable_time = datetime.fromtimestamp(self.timestamp).strftime("%Y-%m-%d %H:%M:%S")
        return f"""
╭─────────────────────────────────────╮
│ Block #{self.index:<28} │
├─────────────────────────────────────┤
│ 🕒 Time: {readable_time:<19} │
│ 📝 Data: {self.data:<27} │
│ 🔗 Prev: {self.previous_hash[:10]}...{self.previous_hash[-10:]:<8} │
│ 🔐 Hash: {self.hash[:10]}...{self.hash[-10:]:<8} │
│ 🔢 Nonce: {self.nonce:<26} │
╰─────────────────────────────────────╯"""


class Blockchain:
    """
    Represents the entire blockchain with methods for adding blocks and validation.
    """
    
    def __init__(self, difficulty: int = 2):
        """
        Initialize the blockchain with a genesis block.
        
        Args:
            difficulty: Mining difficulty (number of leading zeros required)
        """
        self.chain: List[Block] = []
        self.difficulty = difficulty
        self.pending_transactions: List[str] = []
        self.mining_reward = 100
        
        # Create genesis block
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """Create the first block in the chain (Genesis Block)."""
        print("🌟 Creating Genesis Block...")
        genesis_block = Block(0, "Genesis Block - The beginning of BlockSim", "0")
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
        print("✨ Genesis Block created successfully!\n")
    
    def get_latest_block(self) -> Block:
        """Get the most recent block in the chain."""
        return self.chain[-1]
    
    def add_transaction(self, transaction: str):
        """
        Add a transaction to the pending transactions list.
        
        Args:
            transaction: Transaction description
        """
        self.pending_transactions.append(transaction)
        print(f"📤 Transaction added: {transaction}")
    
    def mine_pending_transactions(self, mining_reward_address: str = "BlockSim Miner"):
        """
        Mine all pending transactions and create a new block.
        
        Args:
            mining_reward_address: Address to send mining reward to
        """
        if not self.pending_transactions:
            print("❌ No pending transactions to mine!")
            return
        
        # Add mining reward transaction
        reward_transaction = f"Mining Reward: {self.mining_reward} coins to {mining_reward_address}"
        transactions = self.pending_transactions + [reward_transaction]
        
        # Create new block with all transactions
        transaction_data = " | ".join(transactions)
        new_block = Block(
            index=len(self.chain),
            data=transaction_data,
            previous_hash=self.get_latest_block().hash
        )
        
        # Mine the block
        new_block.mine_block(self.difficulty)
        
        # Add to chain and clear pending transactions
        self.chain.append(new_block)
        self.pending_transactions = []
        
        print(f"🎉 Block #{new_block.index} added to blockchain!\n")
    
    def add_block_direct(self, data: str):
        """
        Add a block directly to the chain (for simple testing).
        
        Args:
            data: Data to store in the block
        """
        new_block = Block(
            index=len(self.chain),
            data=data,
            previous_hash=self.get_latest_block().hash
        )
        
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        print(f"🎉 Block #{new_block.index} added to blockchain!\n")
    
    def is_chain_valid(self) -> bool:
        """
        Validate the entire blockchain by checking hashes and links.
        
        Returns:
            True if chain is valid, False otherwise
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Check if current block's hash is valid
            if current_block.hash != current_block.calculate_hash():
                print(f"❌ Invalid hash at block {i}")
                return False
            
            # Check if current block points to previous block
            if current_block.previous_hash != previous_block.hash:
                print(f"❌ Invalid previous hash at block {i}")
                return False
        
        return True
    
    def display_chain(self):
        """Display the entire blockchain in a formatted way."""
        print("🔗 BLOCKCHAIN DISPLAY")
        print("=" * 50)
        
        for block in self.chain:
            print(block)
            if block.index < len(self.chain) - 1:
                print("     │")
                print("     ▼")
        
        print(f"\n📊 BLOCKCHAIN STATS:")
        print(f"   • Total Blocks: {len(self.chain)}")
        print(f"   • Difficulty: {self.difficulty}")
        print(f"   • Chain Valid: {'✅ Yes' if self.is_chain_valid() else '❌ No'}")
    
    def get_balance(self, address: str) -> float:
        """
        Calculate balance for a given address by parsing all transactions.
        
        Args:
            address: Address to calculate balance for
            
        Returns:
            Current balance
        """
        balance = 0
        
        for block in self.chain:
            if block.index == 0:  # Skip genesis block
                continue
            
            # Parse transactions in the block data
            transactions = block.data.split(" | ")
            for transaction in transactions:
                if "sends" in transaction and "to" in transaction:
                    # Parse "A sends 5 coins to B" format
                    parts = transaction.split()
                    if len(parts) >= 5:
                        sender = parts[0]
                        amount = float(parts[2])
                        recipient = parts[5]
                        
                        if sender == address:
                            balance -= amount
                        if recipient == address:
                            balance += amount
                
                elif "Mining Reward:" in transaction and address in transaction:
                    # Parse mining reward
                    parts = transaction.split()
                    if len(parts) >= 3:
                        amount = float(parts[2])
                        balance += amount
        
        return balance
    
    def tamper_with_block(self, block_index: int, new_data: str):
        """
        Tamper with a block to demonstrate blockchain immutability.
        
        Args:
            block_index: Index of block to tamper with
            new_data: New data to replace existing data
        """
        if 0 <= block_index < len(self.chain):
            print(f"🚨 TAMPERING WITH BLOCK {block_index}...")
            original_data = self.chain[block_index].data
            self.chain[block_index].data = new_data
            print(f"   Original: {original_data}")
            print(f"   Modified: {new_data}")
            print(f"   Chain valid after tampering: {'✅ Yes' if self.is_chain_valid() else '❌ No'}")
        else:
            print(f"❌ Block {block_index} does not exist!")
    
    def export_chain(self, filename: str = "blockchain.json"):
        """Export blockchain to JSON file."""
        chain_data = [block.to_dict() for block in self.chain]
        with open(filename, 'w') as f:
            json.dump(chain_data, f, indent=2)
        print(f"💾 Blockchain exported to {filename}")


def demo_blockchain():
    """Demonstrate the blockchain functionality."""
    print("🚀 WELCOME TO BLOCKSIM - MINI BLOCKCHAIN DEMO")
    print("=" * 60)
    
    # Create blockchain with difficulty 2
    blockchain = Blockchain(difficulty=2)
    
    print("🏦 Adding some transactions...")
    
    # Method 1: Using transaction pool (more realistic)
    blockchain.add_transaction("Alice sends 50 coins to Bob")
    blockchain.add_transaction("Bob sends 25 coins to Charlie")
    blockchain.mine_pending_transactions("Miner1")
    
    # Method 2: Direct block addition (for simplicity)
    blockchain.add_block_direct("Charlie sends 10 coins to Diana")
    blockchain.add_block_direct("Diana sends 5 coins to Eve")
    
    # Add more transactions to pending pool
    blockchain.add_transaction("Eve sends 3 coins to Alice")
    blockchain.add_transaction("Alice sends 20 coins to Frank")
    blockchain.mine_pending_transactions("Miner2")
    
    # Display the complete blockchain
    blockchain.display_chain()
    
    # Show balances
    print("\n💰 ACCOUNT BALANCES:")
    addresses = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Miner1", "Miner2"]
    for address in addresses:
        balance = blockchain.get_balance(address)
        if balance != 0:
            print(f"   {address}: {balance} coins")
    
    # Demonstrate blockchain validation
    print(f"\n🔒 BLOCKCHAIN VALIDATION:")
    print(f"   Chain is valid: {'✅ Yes' if blockchain.is_chain_valid() else '❌ No'}")
    
    # Demonstrate tampering detection
    print(f"\n🚨 TAMPERING DEMONSTRATION:")
    blockchain.tamper_with_block(2, "HACKED: All coins belong to Hacker!")
    
    # Export blockchain
    blockchain.export_chain("/Users/pritam/Desktop/Dapps/BlockSim/blockchain_export.json")
    
    return blockchain


if __name__ == "__main__":
    demo_blockchain()
