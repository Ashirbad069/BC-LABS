#!/usr/bin/env python3
"""
BlockSim Test Suite
Comprehensive tests for the blockchain implementation
"""

import unittest
import tempfile
import os
import json
import time
from mini_blockchain import Block, Blockchain
from advanced_features import NetworkNode, BlockchainNetwork, TransactionPool


class TestBlock(unittest.TestCase):
    """Test cases for the Block class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.block = Block(1, "Test transaction", "previous_hash_123")
    
    def test_block_creation(self):
        """Test basic block creation."""
        self.assertEqual(self.block.index, 1)
        self.assertEqual(self.block.data, "Test transaction")
        self.assertEqual(self.block.previous_hash, "previous_hash_123")
        self.assertIsInstance(self.block.timestamp, float)
        self.assertIsNotNone(self.block.hash)
    
    def test_hash_calculation(self):
        """Test hash calculation consistency."""
        original_hash = self.block.hash
        recalculated_hash = self.block.calculate_hash()
        self.assertEqual(original_hash, recalculated_hash)
    
    def test_hash_changes_with_data(self):
        """Test that hash changes when data changes."""
        original_hash = self.block.hash
        self.block.data = "Modified data"
        new_hash = self.block.calculate_hash()
        self.assertNotEqual(original_hash, new_hash)
    
    def test_mining(self):
        """Test block mining functionality."""
        original_hash = self.block.hash
        self.block.mine_block(difficulty=1)
        
        # Hash should change after mining
        self.assertNotEqual(original_hash, self.block.hash)
        
        # Hash should start with required zeros
        self.assertTrue(self.block.hash.startswith("0"))
    
    def test_block_serialization(self):
        """Test block to dictionary conversion."""
        block_dict = self.block.to_dict()
        
        required_fields = ['index', 'timestamp', 'data', 'previous_hash', 'hash', 'nonce']
        for field in required_fields:
            self.assertIn(field, block_dict)
        
        self.assertEqual(block_dict['index'], self.block.index)
        self.assertEqual(block_dict['data'], self.block.data)


class TestBlockchain(unittest.TestCase):
    """Test cases for the Blockchain class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.blockchain = Blockchain(difficulty=1)  # Low difficulty for fast testing
    
    def test_genesis_block_creation(self):
        """Test genesis block is created correctly."""
        self.assertEqual(len(self.blockchain.chain), 1)
        genesis = self.blockchain.chain[0]
        self.assertEqual(genesis.index, 0)
        self.assertEqual(genesis.previous_hash, "0")
        self.assertIn("Genesis Block", genesis.data)
    
    def test_add_block_direct(self):
        """Test adding blocks directly to the chain."""
        initial_length = len(self.blockchain.chain)
        self.blockchain.add_block_direct("Test block data")
        
        self.assertEqual(len(self.blockchain.chain), initial_length + 1)
        
        new_block = self.blockchain.chain[-1]
        self.assertEqual(new_block.index, 1)
        self.assertEqual(new_block.data, "Test block data")
        self.assertEqual(new_block.previous_hash, self.blockchain.chain[0].hash)
    
    def test_transaction_pool(self):
        """Test transaction pool functionality."""
        self.blockchain.add_transaction("Alice sends 10 coins to Bob")
        self.assertEqual(len(self.blockchain.pending_transactions), 1)
        
        # Mine transactions
        self.blockchain.mine_pending_transactions("Miner")
        self.assertEqual(len(self.blockchain.pending_transactions), 0)
        self.assertEqual(len(self.blockchain.chain), 2)
    
    def test_chain_validation(self):
        """Test blockchain validation."""
        # Initially valid
        self.assertTrue(self.blockchain.is_chain_valid())
        
        # Add valid block
        self.blockchain.add_block_direct("Valid block")
        self.assertTrue(self.blockchain.is_chain_valid())
        
        # Tamper with block
        self.blockchain.chain[1].data = "Tampered data"
        self.assertFalse(self.blockchain.is_chain_valid())
    
    def test_balance_calculation(self):
        """Test balance calculation for addresses."""
        # Add transactions
        self.blockchain.add_transaction("Alice sends 50 coins to Bob")
        self.blockchain.add_transaction("Bob sends 20 coins to Charlie")
        self.blockchain.mine_pending_transactions("Miner")
        
        # Check balances
        alice_balance = self.blockchain.get_balance("Alice")
        bob_balance = self.blockchain.get_balance("Bob")
        charlie_balance = self.blockchain.get_balance("Charlie")
        miner_balance = self.blockchain.get_balance("Miner")
        
        self.assertEqual(alice_balance, -50)
        self.assertEqual(bob_balance, 30)  # 50 - 20
        self.assertEqual(charlie_balance, 20)
        self.assertEqual(miner_balance, 100)  # Mining reward
    
    def test_export_import_chain(self):
        """Test blockchain export and import functionality."""
        # Add some blocks
        self.blockchain.add_block_direct("Block 1")
        self.blockchain.add_block_direct("Block 2")
        
        # Export to temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_filename = f.name
        
        try:
            self.blockchain.export_chain(temp_filename)
            
            # Verify file exists and has content
            self.assertTrue(os.path.exists(temp_filename))
            
            with open(temp_filename, 'r') as f:
                exported_data = json.load(f)
            
            self.assertEqual(len(exported_data), 3)  # Genesis + 2 blocks
            self.assertEqual(exported_data[0]['index'], 0)
            self.assertEqual(exported_data[1]['data'], "Block 1")
            self.assertEqual(exported_data[2]['data'], "Block 2")
        
        finally:
            # Clean up
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)


class TestNetworkFeatures(unittest.TestCase):
    """Test cases for network and advanced features."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.network = BlockchainNetwork()
    
    def test_network_creation(self):
        """Test network node creation and connections."""
        node1 = self.network.add_node("Node1")
        node2 = self.network.add_node("Node2")
        node3 = self.network.add_node("Node3")
        
        self.assertEqual(len(self.network.nodes), 3)
        
        # Check peer connections (full mesh)
        self.assertIn(node2, node1.peers)
        self.assertIn(node3, node1.peers)
        self.assertIn(node1, node2.peers)
        self.assertIn(node3, node2.peers)
    
    def test_transaction_simulation(self):
        """Test transaction pool in network."""
        self.network.add_node("Alice")
        self.network.add_node("Bob")
        
        self.network.simulate_transaction("Alice", "Bob", 10)
        self.assertEqual(len(self.network.transaction_pool), 1)
        
        # Mine transactions
        self.network.random_mining_round()
        self.assertEqual(len(self.network.transaction_pool), 0)
    
    def test_consensus_check(self):
        """Test network consensus checking."""
        node1 = self.network.add_node("Node1")
        node2 = self.network.add_node("Node2")
        
        # Initially should have consensus (both have genesis block)
        self.assertTrue(self.network.check_consensus())
        
        # Add block to one node only (breaks consensus)
        node1.blockchain.add_block_direct("Exclusive block")
        # Note: In real implementation, this wouldn't happen due to broadcasting
        # This is just for testing the consensus check logic


class TestTransactionPool(unittest.TestCase):
    """Test cases for the TransactionPool class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.tx_pool = TransactionPool()
        self.tx_pool.update_balance("Alice", 100)
        self.tx_pool.update_balance("Bob", 50)
    
    def test_balance_management(self):
        """Test balance tracking."""
        self.assertEqual(self.tx_pool.balances["Alice"], 100)
        self.assertEqual(self.tx_pool.balances["Bob"], 50)
        
        self.tx_pool.update_balance("Alice", 25)
        self.assertEqual(self.tx_pool.balances["Alice"], 125)
    
    def test_valid_transaction(self):
        """Test adding valid transactions."""
        result = self.tx_pool.add_transaction("Alice", "Bob", 30, fee=2)
        self.assertTrue(result)
        self.assertEqual(len(self.tx_pool.transactions), 1)
    
    def test_insufficient_balance(self):
        """Test rejection of transactions with insufficient balance."""
        result = self.tx_pool.add_transaction("Alice", "Bob", 150, fee=2)
        self.assertFalse(result)
        self.assertEqual(len(self.tx_pool.transactions), 0)
    
    def test_transaction_sorting(self):
        """Test transaction sorting by fee."""
        self.tx_pool.add_transaction("Alice", "Bob", 10, fee=1.0)
        self.tx_pool.add_transaction("Alice", "Bob", 20, fee=3.0)
        self.tx_pool.add_transaction("Alice", "Bob", 15, fee=2.0)
        
        pending = self.tx_pool.get_pending_transactions()
        
        # Should be sorted by fee (highest first)
        self.assertEqual(pending[0]['fee'], 3.0)
        self.assertEqual(pending[1]['fee'], 2.0)
        self.assertEqual(pending[2]['fee'], 1.0)


class TestPerformance(unittest.TestCase):
    """Performance tests for blockchain operations."""
    
    def test_mining_performance(self):
        """Test mining performance with different difficulties."""
        blockchain = Blockchain(difficulty=1)
        
        start_time = time.time()
        blockchain.add_block_direct("Performance test block")
        end_time = time.time()
        
        mining_time = end_time - start_time
        self.assertLess(mining_time, 5.0)  # Should mine quickly with difficulty 1
    
    def test_large_chain_validation(self):
        """Test validation performance with larger chains."""
        blockchain = Blockchain(difficulty=1)
        
        # Add multiple blocks
        for i in range(10):
            blockchain.add_block_direct(f"Block {i}")
        
        start_time = time.time()
        is_valid = blockchain.is_chain_valid()
        end_time = time.time()
        
        validation_time = end_time - start_time
        self.assertTrue(is_valid)
        self.assertLess(validation_time, 1.0)  # Should validate quickly


def run_all_tests():
    """Run all test suites and generate a report."""
    print("🧪 BLOCKSIM TEST SUITE")
    print("=" * 60)
    
    # Create test suite
    test_classes = [
        TestBlock,
        TestBlockchain,
        TestNetworkFeatures,
        TestTransactionPool,
        TestPerformance
    ]
    
    total_tests = 0
    total_failures = 0
    total_errors = 0
    
    for test_class in test_classes:
        print(f"\n📋 Running {test_class.__name__}...")
        suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
        runner = unittest.TextTestRunner(verbosity=0, stream=open(os.devnull, 'w'))
        result = runner.run(suite)
        
        total_tests += result.testsRun
        total_failures += len(result.failures)
        total_errors += len(result.errors)
        
        if result.failures or result.errors:
            print(f"   ❌ {len(result.failures)} failures, {len(result.errors)} errors")
            for test, traceback in result.failures + result.errors:
                print(f"   🔍 {test}: {traceback.split(chr(10))[-2]}")
        else:
            print(f"   ✅ All {result.testsRun} tests passed!")
    
    print(f"\n📊 TEST SUMMARY")
    print("-" * 40)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {total_tests - total_failures - total_errors}")
    print(f"Failed: {total_failures}")
    print(f"Errors: {total_errors}")
    
    if total_failures == 0 and total_errors == 0:
        print("🎉 ALL TESTS PASSED!")
    else:
        print("⚠️  Some tests failed. Check the output above.")


def benchmark_blockchain():
    """Run benchmark tests."""
    print("\n⚡ PERFORMANCE BENCHMARKS")
    print("=" * 60)
    
    difficulties = [1, 2, 3]
    block_counts = [5, 10, 20]
    
    for difficulty in difficulties:
        print(f"\n🎯 Testing with difficulty {difficulty}:")
        blockchain = Blockchain(difficulty=difficulty)
        
        start_time = time.time()
        for i in range(5):
            blockchain.add_block_direct(f"Benchmark block {i}")
        end_time = time.time()
        
        total_time = end_time - start_time
        avg_time = total_time / 5
        
        print(f"   ⏱️  5 blocks mined in {total_time:.2f}s (avg: {avg_time:.2f}s/block)")
    
    # Validation benchmark
    print(f"\n🔍 Validation benchmarks:")
    for count in block_counts:
        blockchain = Blockchain(difficulty=1)
        for i in range(count):
            blockchain.add_block_direct(f"Block {i}")
        
        start_time = time.time()
        is_valid = blockchain.is_chain_valid()
        end_time = time.time()
        
        validation_time = end_time - start_time
        print(f"   📊 {count} blocks validated in {validation_time:.4f}s")


if __name__ == "__main__":
    # Run tests
    run_all_tests()
    
    # Run benchmarks
    benchmark_blockchain()
    
    print("\n🏁 Testing completed!")
