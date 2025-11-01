#!/usr/bin/env python3
"""
BlockSim Launcher
Main entry point for the BlockSim blockchain education platform
"""

import sys
import os
import subprocess
from config import Colors


class BlockSimLauncher:
    """Main launcher for BlockSim applications."""
    
    def __init__(self):
        self.colors = Colors()
        self.options = {
            '1': ('Basic Blockchain Demo', self.run_basic_demo),
            '2': ('Interactive Explorer', self.run_explorer),
            '3': ('🌐 Web Interface (New!)', self.run_web_interface),
            '4': ('Advanced Network Simulation', self.run_advanced_features),
            '5': ('Blockchain Visualizer', self.run_visualizer),
            '6': ('Run Test Suite', self.run_tests),
            '7': ('Performance Benchmarks', self.run_benchmarks),
            '8': ('View Documentation', self.show_documentation),
            '9': ('Quick Tutorial', self.run_tutorial),
            '0': ('Exit', self.exit_launcher)
        }
    
    def display_banner(self):
        """Display the BlockSim banner."""
        banner = f"""
{self.colors.CYAN}
██████╗ ██╗      ██████╗  ██████╗██╗  ██╗███████╗██╗███╗   ███╗
██╔══██╗██║     ██╔═══██╗██╔════╝██║ ██╔╝██╔════╝██║████╗ ████║
██████╔╝██║     ██║   ██║██║     █████╔╝ ███████╗██║██╔████╔██║
██╔══██╗██║     ██║   ██║██║     ██╔═██╗ ╚════██║██║██║╚██╔╝██║
██████╔╝███████╗╚██████╔╝╚██████╗██║  ██╗███████║██║██║ ╚═╝ ██║
╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝╚═╝     ╚═╝
{self.colors.ENDC}
{self.colors.BOLD}🔗 Educational Blockchain Implementation from Scratch{self.colors.ENDC}
{self.colors.YELLOW}📚 Learn • 🔨 Build • 🧪 Experiment • 🚀 Understand{self.colors.ENDC}
"""
        return banner
    
    def display_menu(self):
        """Display the main menu."""
        print(self.display_banner())
        print("=" * 70)
        print(f"{self.colors.BOLD}🎯 CHOOSE YOUR BLOCKSIM ADVENTURE:{self.colors.ENDC}")
        print()
        
        for key, (description, _) in self.options.items():
            icon = self.get_option_icon(key)
            print(f"   {key}. {icon} {description}")
        
        print()
        print("=" * 70)
    
    def get_option_icon(self, key):
        """Get appropriate icon for each option."""
        icons = {
            '1': '🎬', '2': '🔍', '3': '🌐', '4': '�', '5': '�🎨',
            '6': '🧪', '7': '⚡', '8': '📖', '9': '🎓', '0': '👋'
        }
        return icons.get(key, '📋')
    
    def run_basic_demo(self):
        """Run the basic blockchain demonstration."""
        print(f"\n{self.colors.GREEN}🎬 Starting Basic Blockchain Demo...{self.colors.ENDC}")
        try:
            subprocess.run([sys.executable, 'mini_blockchain.py'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"{self.colors.RED}❌ Error running demo: {e}{self.colors.ENDC}")
        except FileNotFoundError:
            print(f"{self.colors.RED}❌ mini_blockchain.py not found!{self.colors.ENDC}")
    
    def run_explorer(self):
        """Run the interactive blockchain explorer."""
        print(f"\n{self.colors.GREEN}🔍 Starting Interactive Explorer...{self.colors.ENDC}")
        try:
            subprocess.run([sys.executable, 'blockchain_explorer.py'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"{self.colors.RED}❌ Error running explorer: {e}{self.colors.ENDC}")
        except FileNotFoundError:
            print(f"{self.colors.RED}❌ blockchain_explorer.py not found!{self.colors.ENDC}")
    
    def run_web_interface(self):
        """Run the web-based blockchain interface."""
        print(f"\n{self.colors.GREEN}🌐 Starting Web Interface...{self.colors.ENDC}")
        print("💡 This will start a web server and open your browser!")
        
        try:
            subprocess.run([sys.executable, 'start_web.py'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"{self.colors.RED}❌ Error running web interface: {e}{self.colors.ENDC}")
            print("💡 Make sure Flask is installed: pip3 install Flask")
        except FileNotFoundError:
            print(f"{self.colors.RED}❌ start_web.py not found!{self.colors.ENDC}")
        except KeyboardInterrupt:
            print(f"\n{self.colors.YELLOW}🌐 Web interface stopped by user{self.colors.ENDC}")
    
    def run_advanced_features(self):
        """Run advanced network simulation."""
        print(f"\n{self.colors.GREEN}🌐 Starting Advanced Network Simulation...{self.colors.ENDC}")
        try:
            subprocess.run([sys.executable, 'advanced_features.py'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"{self.colors.RED}❌ Error running simulation: {e}{self.colors.ENDC}")
        except FileNotFoundError:
            print(f"{self.colors.RED}❌ advanced_features.py not found!{self.colors.ENDC}")
    
    def run_visualizer(self):
        """Run the blockchain visualizer."""
        print(f"\n{self.colors.GREEN}🎨 Starting Blockchain Visualizer...{self.colors.ENDC}")
        try:
            subprocess.run([sys.executable, 'visualizer.py'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"{self.colors.RED}❌ Error running visualizer: {e}{self.colors.ENDC}")
        except FileNotFoundError:
            print(f"{self.colors.RED}❌ visualizer.py not found!{self.colors.ENDC}")
    
    def run_tests(self):
        """Run the comprehensive test suite."""
        print(f"\n{self.colors.GREEN}🧪 Starting Test Suite...{self.colors.ENDC}")
        try:
            subprocess.run([sys.executable, 'test_blockchain.py'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"{self.colors.RED}❌ Error running tests: {e}{self.colors.ENDC}")
        except FileNotFoundError:
            print(f"{self.colors.RED}❌ test_blockchain.py not found!{self.colors.ENDC}")
    
    def run_benchmarks(self):
        """Run performance benchmarks."""
        print(f"\n{self.colors.GREEN}⚡ Starting Performance Benchmarks...{self.colors.ENDC}")
        print("This will test mining performance at different difficulties...")
        
        from mini_blockchain import Blockchain
        import time
        
        print("\n📊 MINING PERFORMANCE TEST")
        print("-" * 40)
        
        for difficulty in range(1, 4):
            blockchain = Blockchain(difficulty=difficulty)
            
            start_time = time.time()
            blockchain.add_block_direct(f"Benchmark block at difficulty {difficulty}")
            end_time = time.time()
            
            mining_time = end_time - start_time
            print(f"Difficulty {difficulty}: {mining_time:.3f}s")
        
        print(f"\n{self.colors.GREEN}✅ Benchmarks complete!{self.colors.ENDC}")
    
    def show_documentation(self):
        """Display documentation and help."""
        print(f"\n{self.colors.BLUE}📖 BLOCKSIM DOCUMENTATION{self.colors.ENDC}")
        print("=" * 60)
        
        docs = """
🎯 WHAT IS BLOCKSIM?
   BlockSim is an educational blockchain implementation designed to help
   you understand how blockchains work from the ground up.

🏗️  KEY CONCEPTS DEMONSTRATED:
   • Block Structure - Index, timestamp, data, previous hash, hash
   • Cryptographic Hashing - SHA256 for security
   • Proof of Work - Mining with configurable difficulty
   • Chain Validation - Detecting tampering and maintaining integrity
   • Transaction Processing - Managing digital payments
   • Network Simulation - Multi-node blockchain networks

🚀 GETTING STARTED:
   1. Run Basic Demo - See a simple blockchain in action
   2. Try Interactive Explorer - Build your own blockchain
   3. Experiment with Network Simulation - Multiple nodes
   4. Use Visualizer - See blockchain data graphically
   5. Run Tests - Validate all functionality

📚 FILES OVERVIEW:
   • mini_blockchain.py - Core blockchain implementation
   • blockchain_explorer.py - Interactive CLI interface
   • advanced_features.py - Network simulation
   • visualizer.py - ASCII art visualizations
   • test_blockchain.py - Comprehensive test suite
   • config.py - Configuration settings
   
🎓 LEARNING PATH:
   1. Start with Basic Demo to see blockchain in action
   2. Use Interactive Explorer to experiment
   3. Read the code in mini_blockchain.py to understand implementation
   4. Try Advanced Features for network concepts
   5. Run tests to see validation in action

💡 TIPS:
   • Start with low difficulty (1-2) for fast mining
   • Use Interactive Explorer to experiment safely
   • Read error messages carefully - they're educational!
   • Try tampering with blocks to see immutability in action
"""
        
        print(docs)
        
        # Check if README.md exists and offer to display it
        if os.path.exists('README.md'):
            choice = input(f"\n📋 Display full README.md? (y/n): ").strip().lower()
            if choice == 'y':
                try:
                    with open('README.md', 'r') as f:
                        print(f"\n{self.colors.CYAN}📄 README.md:{self.colors.ENDC}")
                        print("-" * 60)
                        print(f.read())
                except Exception as e:
                    print(f"{self.colors.RED}❌ Error reading README.md: {e}{self.colors.ENDC}")
    
    def run_tutorial(self):
        """Run a quick interactive tutorial."""
        print(f"\n{self.colors.GREEN}🎓 BLOCKSIM QUICK TUTORIAL{self.colors.ENDC}")
        print("=" * 60)
        
        tutorial_steps = [
            ("Welcome to BlockSim!", "This tutorial will guide you through blockchain basics."),
            ("What is a Block?", "A block contains: index, timestamp, data, previous_hash, and hash."),
            ("What is a Hash?", "A hash is like a fingerprint - unique for each block's content."),
            ("What is Mining?", "Mining finds a nonce value that makes the hash start with zeros."),
            ("What is a Chain?", "Blocks link together using hashes, forming an immutable chain."),
            ("What is Validation?", "Checking that all hashes and links are correct."),
            ("What about Tampering?", "Changing any data breaks the chain - that's immutability!")
        ]
        
        for i, (title, description) in enumerate(tutorial_steps, 1):
            print(f"\n📚 Step {i}: {self.colors.BOLD}{title}{self.colors.ENDC}")
            print(f"   {description}")
            
            if i < len(tutorial_steps):
                input(f"\n   Press Enter to continue...")
        
        print(f"\n{self.colors.GREEN}🎉 Tutorial complete! Ready to explore BlockSim!{self.colors.ENDC}")
        print(f"💡 Recommendation: Start with option 1 (Basic Demo) to see it in action!")
    
    def exit_launcher(self):
        """Exit the launcher."""
        print(f"\n{self.colors.YELLOW}👋 Thanks for exploring BlockSim!{self.colors.ENDC}")
        print("🎓 Keep learning and building amazing blockchain applications!")
        print(f"{self.colors.CYAN}🔗 Remember: Understanding blockchain is understanding the future of digital trust.{self.colors.ENDC}")
        return True
    
    def run(self):
        """Main launcher loop."""
        try:
            while True:
                self.display_menu()
                choice = input(f"{self.colors.BOLD}🎯 Enter your choice (0-8): {self.colors.ENDC}").strip()
                
                if choice in self.options:
                    _, command_func = self.options[choice]
                    
                    if command_func():  # Exit returns True
                        break
                    
                    # Pause after each operation (except exit)
                    if choice != '0':
                        input(f"\n{self.colors.YELLOW}⏸️  Press Enter to return to main menu...{self.colors.ENDC}")
                else:
                    print(f"{self.colors.RED}❌ Invalid choice! Please enter a number from 0-9.{self.colors.ENDC}")
                    input(f"⏸️  Press Enter to continue...")
        
        except KeyboardInterrupt:
            print(f"\n\n{self.colors.YELLOW}👋 BlockSim interrupted. Goodbye!{self.colors.ENDC}")
        except Exception as e:
            print(f"\n{self.colors.RED}❌ An error occurred: {e}{self.colors.ENDC}")


def main():
    """Main function."""
    launcher = BlockSimLauncher()
    launcher.run()


if __name__ == "__main__":
    main()
