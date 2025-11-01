#!/usr/bin/env python3
"""
BlockSim Visualizer
Simple ASCII visualization tools for blockchain data
"""

import json
import time
from datetime import datetime
from mini_blockchain import Blockchain, Block
from config import Colors


class BlockchainVisualizer:
    """Create ASCII visualizations of blockchain data."""
    
    def __init__(self, blockchain: Blockchain = None):
        self.blockchain = blockchain
        self.colors = Colors()
    
    def set_blockchain(self, blockchain: Blockchain):
        """Set the blockchain to visualize."""
        self.blockchain = blockchain
    
    def draw_chain_flow(self):
        """Draw a horizontal flow chart of the blockchain."""
        if not self.blockchain or not self.blockchain.chain:
            print("❌ No blockchain to visualize!")
            return
        
        print(f"\n{self.colors.BOLD}🔗 BLOCKCHAIN FLOW DIAGRAM{self.colors.ENDC}")
        print("=" * 80)
        
        # Create flow representation
        flow_lines = []
        
        for i, block in enumerate(self.blockchain.chain):
            # Block box
            block_box = f"┌─ Block {block.index} ─┐"
            hash_line = f"│ {block.hash[:8]}... │"
            data_line = f"│ {block.data[:10]}... │" if len(block.data) > 13 else f"│ {block.data:<13} │"
            bottom_box = "└──────────────┘"
            
            if i == 0:
                # Genesis block
                flow_lines.extend([
                    f"{self.colors.GREEN}{block_box}{self.colors.ENDC}",
                    f"{self.colors.GREEN}{hash_line}{self.colors.ENDC}",
                    f"{self.colors.GREEN}{data_line}{self.colors.ENDC}",
                    f"{self.colors.GREEN}{bottom_box}{self.colors.ENDC}"
                ])
            else:
                flow_lines.extend([
                    f"{self.colors.BLUE}{block_box}{self.colors.ENDC}",
                    f"{self.colors.BLUE}{hash_line}{self.colors.ENDC}",
                    f"{self.colors.BLUE}{data_line}{self.colors.ENDC}",
                    f"{self.colors.BLUE}{bottom_box}{self.colors.ENDC}"
                ])
            
            # Add arrow if not last block
            if i < len(self.blockchain.chain) - 1:
                flow_lines.append("      ↓")
                flow_lines.append("")
        
        for line in flow_lines:
            print(line)
    
    def draw_network_topology(self, nodes_info):
        """Draw a simple network topology diagram."""
        print(f"\n{self.colors.BOLD}🌐 NETWORK TOPOLOGY{self.colors.ENDC}")
        print("=" * 50)
        
        # Simple circular arrangement
        node_positions = []
        center_x, center_y = 25, 10
        radius = 8
        
        import math
        for i, node in enumerate(nodes_info):
            angle = (2 * math.pi * i) / len(nodes_info)
            x = int(center_x + radius * math.cos(angle))
            y = int(center_y + radius * math.sin(angle))
            node_positions.append((x, y, node['name'], node['status']))
        
        # Create grid
        grid = [[' ' for _ in range(50)] for _ in range(20)]
        
        # Place nodes
        for x, y, name, status in node_positions:
            if 0 <= y < 20 and 0 <= x < 45:
                color = self.colors.GREEN if status == 'online' else self.colors.RED
                symbol = '●' if status == 'online' else '○'
                
                # Place node symbol
                grid[y][x] = symbol
                
                # Place node name
                for i, char in enumerate(name[:6]):
                    if x + i + 1 < 50:
                        grid[y][x + i + 1] = char
        
        # Draw connections (simple lines to center)
        for x, y, name, status in node_positions:
            if status == 'online':
                # Draw line to center
                dx = 1 if x < center_x else -1 if x > center_x else 0
                dy = 1 if y < center_y else -1 if y > center_y else 0
                
                curr_x, curr_y = x, y
                while abs(curr_x - center_x) > 1 or abs(curr_y - center_y) > 1:
                    curr_x += dx
                    curr_y += dy
                    if 0 <= curr_y < 20 and 0 <= curr_x < 50:
                        if grid[curr_y][curr_x] == ' ':
                            grid[curr_y][curr_x] = '─' if dy == 0 else '│' if dx == 0 else '┼'
        
        # Print grid
        for row in grid:
            print(''.join(row))
        
        # Legend
        print(f"\n{self.colors.GREEN}● Online{self.colors.ENDC}  {self.colors.RED}○ Offline{self.colors.ENDC}")
    
    def draw_transaction_flow(self, transactions):
        """Visualize transaction flow between addresses."""
        print(f"\n{self.colors.BOLD}💸 TRANSACTION FLOW{self.colors.ENDC}")
        print("=" * 60)
        
        # Collect unique addresses
        addresses = set()
        for tx in transactions:
            addresses.add(tx['from'])
            addresses.add(tx['to'])
        
        addresses = list(addresses)[:8]  # Limit to 8 for display
        
        # Create transaction matrix
        matrix = [[0 for _ in range(len(addresses))] for _ in range(len(addresses))]
        
        for tx in transactions:
            if tx['from'] in addresses and tx['to'] in addresses:
                from_idx = addresses.index(tx['from'])
                to_idx = addresses.index(tx['to'])
                matrix[from_idx][to_idx] += tx['amount']
        
        # Display matrix
        print("From\\To  ", end="")
        for addr in addresses:
            print(f"{addr[:8]:<9}", end="")
        print()
        
        for i, from_addr in enumerate(addresses):
            print(f"{from_addr[:8]:<9}", end="")
            for j, to_addr in enumerate(addresses):
                amount = matrix[i][j]
                if amount > 0:
                    print(f"{self.colors.YELLOW}{amount:>8.1f}{self.colors.ENDC}", end=" ")
                else:
                    print("      .  ", end="")
            print()
    
    def draw_mining_progress(self, difficulty, current_nonce, target_hash):
        """Show animated mining progress."""
        print(f"\n⛏️  Mining Block (Difficulty: {difficulty})")
        print(f"Target: {target_hash}")
        print("Progress: ", end="", flush=True)
        
        # Simulate progress bar
        progress_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        
        for i in range(20):
            char = progress_chars[i % len(progress_chars)]
            print(f"\r⛏️  Mining: {char} Nonce: {current_nonce + i * 100:<8}", end="", flush=True)
            time.sleep(0.1)
        
        print(f"\r✅ Block mined! Final nonce: {current_nonce + 2000}")
    
    def create_block_ascii_art(self, block: Block):
        """Create detailed ASCII art for a single block."""
        readable_time = datetime.fromtimestamp(block.timestamp).strftime("%Y-%m-%d %H:%M:%S")
        
        art = f"""
{self.colors.CYAN}╔══════════════════════════════════════════════════════════════╗
║                         BLOCK #{block.index:<3}                           ║
╠══════════════════════════════════════════════════════════════╣
║ 🕐 Timestamp: {readable_time:<41} ║
║ 📊 Index:     {block.index:<45} ║
║ 🔗 Previous:  {block.previous_hash[:50]:<45} ║
║ 🔐 Hash:      {block.hash[:50]:<45} ║
║ 🔢 Nonce:     {block.nonce:<45} ║
║ 📝 Data:      {block.data[:50]:<45} ║
╚══════════════════════════════════════════════════════════════╝{self.colors.ENDC}"""
        
        return art
    
    def animate_chain_building(self):
        """Animate the process of building a blockchain."""
        print(f"\n{self.colors.BOLD}🎬 BLOCKCHAIN BUILDING ANIMATION{self.colors.ENDC}")
        print("=" * 60)
        
        if not self.blockchain:
            print("❌ No blockchain to animate!")
            return
        
        for i, block in enumerate(self.blockchain.chain):
            print(f"\n📦 Adding Block #{i}")
            time.sleep(0.5)
            
            # Show mining process
            if i > 0:
                print("⛏️  Mining in progress...")
                for j in range(5):
                    print(f"   Trying nonce {j * 100}...")
                    time.sleep(0.3)
            
            # Show completed block
            print(self.create_block_ascii_art(block))
            
            if i < len(self.blockchain.chain) - 1:
                print(f"{self.colors.YELLOW}      ⬇️  Linking to next block...{self.colors.ENDC}")
                time.sleep(0.5)
        
        print(f"\n{self.colors.GREEN}✨ Blockchain construction complete!{self.colors.ENDC}")
    
    def show_balance_chart(self, balances):
        """Create a simple ASCII bar chart for balances."""
        print(f"\n{self.colors.BOLD}💰 BALANCE CHART{self.colors.ENDC}")
        print("=" * 50)
        
        if not balances:
            print("❌ No balance data!")
            return
        
        # Filter out zero balances
        non_zero_balances = {addr: bal for addr, bal in balances.items() if bal != 0}
        
        if not non_zero_balances:
            print("📊 All balances are zero!")
            return
        
        max_balance = max(abs(bal) for bal in non_zero_balances.values())
        if max_balance == 0:
            return
        
        for address, balance in sorted(non_zero_balances.items(), key=lambda x: x[1], reverse=True):
            # Calculate bar length (max 30 chars)
            bar_length = int((abs(balance) / max_balance) * 30)
            
            if balance >= 0:
                bar = f"{self.colors.GREEN}{'█' * bar_length}{self.colors.ENDC}"
                sign = "+"
            else:
                bar = f"{self.colors.RED}{'█' * bar_length}{self.colors.ENDC}"
                sign = ""
            
            print(f"{address[:10]:<10} │{bar:<30}│ {sign}{balance:.1f}")
        
        print("           └" + "─" * 30 + "┘")
        print(f"            0{' ' * 25}{max_balance:.1f}")


def demo_visualization():
    """Demonstrate visualization features."""
    print("🎨 BLOCKSIM VISUALIZATION DEMO")
    print("=" * 60)
    
    # Create sample blockchain
    blockchain = Blockchain(difficulty=2)
    blockchain.add_transaction("Alice sends 100 coins to Bob")
    blockchain.add_transaction("Bob sends 50 coins to Charlie")
    blockchain.mine_pending_transactions("Miner1")
    
    blockchain.add_block_direct("Charlie sends 25 coins to Diana")
    blockchain.add_block_direct("Diana sends 10 coins to Eve")
    
    # Create visualizer
    viz = BlockchainVisualizer(blockchain)
    
    # Demo different visualizations
    print("\n1. Chain Flow Diagram:")
    viz.draw_chain_flow()
    
    print("\n2. Balance Chart:")
    balances = {}
    addresses = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Miner1"]
    for addr in addresses:
        balances[addr] = blockchain.get_balance(addr)
    viz.show_balance_chart(balances)
    
    print("\n3. Network Topology:")
    nodes_info = [
        {"name": "Alice", "status": "online"},
        {"name": "Bob", "status": "online"},
        {"name": "Charlie", "status": "offline"},
        {"name": "Diana", "status": "online"}
    ]
    viz.draw_network_topology(nodes_info)
    
    print("\n4. Transaction Flow:")
    transactions = [
        {"from": "Alice", "to": "Bob", "amount": 100},
        {"from": "Bob", "to": "Charlie", "amount": 50},
        {"from": "Charlie", "to": "Diana", "amount": 25},
        {"from": "Diana", "to": "Eve", "amount": 10}
    ]
    viz.draw_transaction_flow(transactions)
    
    print(f"\n{Colors.GREEN}✨ Visualization demo complete!{Colors.ENDC}")


if __name__ == "__main__":
    demo_visualization()
