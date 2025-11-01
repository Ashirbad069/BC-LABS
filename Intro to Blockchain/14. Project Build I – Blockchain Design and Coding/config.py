"""
BlockSim Configuration
Global settings and constants for the blockchain system
"""

# Mining Configuration
DEFAULT_DIFFICULTY = 2
MAX_DIFFICULTY = 6
MIN_DIFFICULTY = 1

# Blockchain Settings
GENESIS_BLOCK_DATA = "Genesis Block - The beginning of BlockSim"
DEFAULT_MINING_REWARD = 100
MAX_TRANSACTIONS_PER_BLOCK = 10

# Network Settings
MAX_PEERS = 10
DEFAULT_PORT = 8333
BLOCK_PROPAGATION_TIMEOUT = 30  # seconds

# File Settings
DEFAULT_EXPORT_FILENAME = "blockchain_export.json"
LOG_LEVEL = "INFO"

# Transaction Settings
MIN_TRANSACTION_FEE = 0.001
MAX_TRANSACTION_AMOUNT = 1000000
TRANSACTION_EXPIRY_TIME = 3600  # 1 hour in seconds

# Display Settings
HASH_DISPLAY_LENGTH = 10  # Number of characters to show in truncated hashes
BLOCK_DISPLAY_WIDTH = 40
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Performance Settings
BENCHMARK_BLOCK_COUNT = 5
MAX_CHAIN_LENGTH_FOR_FAST_VALIDATION = 1000

# API Keys (Example - replace with your actual keys)
PINATA_API_KEY = "4775ee72de059e64c185"
PINATA_SECRET = "29b2114ccabeca8b6ab11fdbffd3de2941bfca101f23d2ec70f8c708d883ac00"
ALCHEMY_API_KEY = "vxOyfjkY6lSF39OsNEhWL"
ETHERSCAN_API_KEY = "W4JNFREH4G3N4ST6AZG2HBER3WBI9XMNH2"

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Validation rules
VALIDATION_RULES = {
    'max_block_size': 1000000,  # 1MB in bytes
    'max_transaction_size': 10000,  # 10KB in bytes
    'require_positive_amounts': True,
    'allow_zero_fee_transactions': False,
    'validate_addresses': True
}

# Error messages
ERROR_MESSAGES = {
    'insufficient_balance': "❌ Insufficient balance for transaction",
    'invalid_transaction': "❌ Invalid transaction format",
    'chain_validation_failed': "❌ Blockchain validation failed",
    'mining_failed': "❌ Block mining failed",
    'network_error': "❌ Network communication error",
    'file_not_found': "❌ Blockchain file not found",
    'invalid_difficulty': "❌ Invalid mining difficulty"
}

# Success messages  
SUCCESS_MESSAGES = {
    'block_mined': "✅ Block successfully mined",
    'transaction_added': "✅ Transaction added to pool",
    'chain_validated': "✅ Blockchain validation passed",
    'file_exported': "✅ Blockchain exported successfully",
    'file_imported': "✅ Blockchain imported successfully"
}

# Demo configuration
DEMO_CONFIG = {
    'initial_accounts': {
        'Alice': 1000,
        'Bob': 500,
        'Charlie': 250,
        'Diana': 100
    },
    'demo_transactions': [
        ('Alice', 'Bob', 50),
        ('Bob', 'Charlie', 25),
        ('Charlie', 'Diana', 10),
        ('Diana', 'Alice', 5)
    ],
    'network_nodes': ['Alice', 'Bob', 'Charlie', 'Diana', 'Miner1', 'Miner2']
}
