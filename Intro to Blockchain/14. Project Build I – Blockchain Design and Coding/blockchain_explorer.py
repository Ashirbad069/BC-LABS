#!/usr/bin/env python3
"""
Interactive BlockSim Explorer
A command-line interface to explore and interact with your blockchain
"""

from mini_blockchain import Blockchain, Block
import json
import os


class BlockchainExplorer:
    """Interactive blockchain explorer with command-line interface."""
    
    def __init__(self):
        self.blockchain = None
        self.commands = {
            '1': ('Create New Blockchain', self.create_blockchain),
            '2': ('Add Transaction', self.add_transaction),
            '3': ('Mine Pending Transactions', self.mine_transactions),
            '4': ('Add Direct Block', self.add_direct_block),
            '5': ('Display Blockchain', self.display_blockchain),
            '6': ('Check Balance', self.check_balance),
            '7': ('Validate Chain', self.validate_chain),
            '8': ('Tamper with Block', self.tamper_block),
            '9': ('Export Blockchain', self.export_blockchain),
            '10': ('Load Blockchain', self.load_blockchain),
            '11': ('Blockchain Stats', self.show_stats),
            '0': ('Exit', self.exit_explorer)
        }
    
    def display_menu(self):
        """Display the main menu."""
        print("\n" + "=" * 60)
        print("🔗 BLOCKSIM INTERACTIVE EXPLORER")
        print("=" * 60)
        
        if self.blockchain:
            print(f"📊 Current Chain: {len(self.blockchain.chain)} blocks")
            print(f"⛏️  Difficulty: {self.blockchain.difficulty}")
            print(f"📋 Pending Transactions: {len(self.blockchain.pending_transactions)}")
        else:
            print("⚠️  No blockchain loaded")
        
        print("\n📋 MENU OPTIONS:")
        for key, (description, _) in self.commands.items():
            print(f"   {key}. {description}")
        print("-" * 60)
    
    def create_blockchain(self):
        """Create a new blockchain."""
        try:
            difficulty = input("🎯 Enter mining difficulty (default 2): ").strip()
            difficulty = int(difficulty) if difficulty else 2
            
            if difficulty < 1 or difficulty > 6:
                print("❌ Difficulty must be between 1 and 6!")
                return
            
            self.blockchain = Blockchain(difficulty=difficulty)
            print(f"✅ New blockchain created with difficulty {difficulty}!")
        
        except ValueError:
            print("❌ Invalid difficulty value!")
    
    def add_transaction(self):
        """Add a transaction to pending pool."""
        if not self.blockchain:
            print("❌ Create a blockchain first!")
            return
        
        print("📝 Enter transaction details:")
        sender = input("   Sender: ").strip()
        recipient = input("   Recipient: ").strip()
        amount = input("   Amount: ").strip()
        
        if sender and recipient and amount:
            try:
                amount = float(amount)
                transaction = f"{sender} sends {amount} coins to {recipient}"
                self.blockchain.add_transaction(transaction)
            except ValueError:
                print("❌ Invalid amount!")
        else:
            print("❌ All fields are required!")
    
    def mine_transactions(self):
        """Mine all pending transactions."""
        if not self.blockchain:
            print("❌ Create a blockchain first!")
            return
        
        if not self.blockchain.pending_transactions:
            print("❌ No pending transactions to mine!")
            return
        
        miner_address = input("⛏️  Enter miner address (default: 'Interactive Miner'): ").strip()
        miner_address = miner_address or "Interactive Miner"
        
        self.blockchain.mine_pending_transactions(miner_address)
    
    def add_direct_block(self):
        """Add a block directly to the chain."""
        if not self.blockchain:
            print("❌ Create a blockchain first!")
            return
        
        data = input("📝 Enter block data: ").strip()
        if data:
            self.blockchain.add_block_direct(data)
        else:
            print("❌ Block data cannot be empty!")
    
    def display_blockchain(self):
        """Display the entire blockchain."""
        if not self.blockchain:
            print("❌ Create a blockchain first!")
            return
        
        self.blockchain.display_chain()
    
    def check_balance(self):
        """Check balance for an address."""
        if not self.blockchain:
            print("❌ Create a blockchain first!")
            return
        
        address = input("💰 Enter address to check: ").strip()
        if address:
            balance = self.blockchain.get_balance(address)
            print(f"💰 Balance for {address}: {balance} coins")
        else:
            print("❌ Address cannot be empty!")
    
    def validate_chain(self):
        """Validate the blockchain."""
        if not self.blockchain:
            print("❌ Create a blockchain first!")
            return
        
        is_valid = self.blockchain.is_chain_valid()
        status = "✅ VALID" if is_valid else "❌ INVALID"
        print(f"🔒 Blockchain validation result: {status}")
    
    def tamper_block(self):
        """Tamper with a block to demonstrate immutability."""
        if not self.blockchain:
            print("❌ Create a blockchain first!")
            return
        
        try:
            block_index = int(input(f"🚨 Enter block index to tamper (0-{len(self.blockchain.chain)-1}): "))
            new_data = input("📝 Enter new data: ").strip()
            
            if new_data:
                self.blockchain.tamper_with_block(block_index, new_data)
            else:
                print("❌ New data cannot be empty!")
        
        except ValueError:
            print("❌ Invalid block index!")
    
    def export_blockchain(self):
        """Export blockchain to JSON file."""
        if not self.blockchain:
            print("❌ Create a blockchain first!")
            return
        
        filename = input("💾 Enter filename (default: blockchain_export.json): ").strip()
        filename = filename or "blockchain_export.json"
        
        try:
            self.blockchain.export_chain(filename)
        except Exception as e:
            print(f"❌ Export failed: {e}")
    
    def load_blockchain(self):
        """Load blockchain from JSON file."""
        filename = input("📁 Enter filename to load: ").strip()
        
        if not filename:
            print("❌ Filename cannot be empty!")
            return
        
        try:
            with open(filename, 'r') as f:
                chain_data = json.load(f)
            
            # Create new blockchain and reconstruct from data
            self.blockchain = Blockchain(difficulty=2)
            self.blockchain.chain = []  # Clear genesis block
            
            for block_data in chain_data:
                block = Block(
                    index=block_data['index'],
                    data=block_data['data'],
                    previous_hash=block_data['previous_hash'],
                    timestamp=block_data['timestamp']
                )
                block.hash = block_data['hash']
                block.nonce = block_data['nonce']
                self.blockchain.chain.append(block)
            
            print(f"✅ Blockchain loaded from {filename}")
            print(f"📊 Loaded {len(self.blockchain.chain)} blocks")
        
        except FileNotFoundError:
            print(f"❌ File {filename} not found!")
        except json.JSONDecodeError:
            print("❌ Invalid JSON file!")
        except Exception as e:
            print(f"❌ Load failed: {e}")
    
    def show_stats(self):
        """Show detailed blockchain statistics."""
        if not self.blockchain:
            print("❌ Create a blockchain first!")
            return
        
        print("\n📊 BLOCKCHAIN STATISTICS")
        print("-" * 40)
        print(f"🔗 Total Blocks: {len(self.blockchain.chain)}")
        print(f"⛏️  Mining Difficulty: {self.blockchain.difficulty}")
        print(f"💰 Mining Reward: {self.blockchain.mining_reward}")
        print(f"📋 Pending Transactions: {len(self.blockchain.pending_transactions)}")
        print(f"🔒 Chain Valid: {'✅ Yes' if self.blockchain.is_chain_valid() else '❌ No'}")
        
        # Calculate total transactions
        total_transactions = 0
        for block in self.blockchain.chain:
            if block.index > 0:  # Skip genesis block
                total_transactions += len(block.data.split(" | "))
        
        print(f"📈 Total Transactions: {total_transactions}")
        
        # Show latest block info
        if len(self.blockchain.chain) > 0:
            latest = self.blockchain.chain[-1]
            print(f"🆕 Latest Block Hash: {latest.hash[:20]}...")
            print(f"⏰ Latest Block Time: {latest.timestamp}")
    
    def exit_explorer(self):
        """Exit the explorer."""
        print("👋 Thanks for using BlockSim Explorer!")
        return True
    
    def run(self):
        """Main explorer loop."""
        print("🚀 Welcome to BlockSim Interactive Explorer!")
        
        while True:
            self.display_menu()
            choice = input("🎯 Enter your choice: ").strip()
            
            if choice in self.commands:
                command_name, command_func = self.commands[choice]
                print(f"\n🔄 Executing: {command_name}")
                
                if command_func():  # Exit returns True
                    break
            else:
                print("❌ Invalid choice! Please try again.")
            
            input("\n⏸️  Press Enter to continue...")


def main():
    """Main function to run the explorer."""
    explorer = BlockchainExplorer()
    try:
        explorer.run()
    except KeyboardInterrupt:
        print("\n\n👋 Explorer interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")


if __name__ == "__main__":
    main()
