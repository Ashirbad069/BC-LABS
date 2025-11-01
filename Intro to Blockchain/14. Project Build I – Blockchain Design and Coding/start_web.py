#!/usr/bin/env python3
"""
BlockSim Web Interface Launcher
Start the web frontend for BlockSim blockchain explorer
"""

import sys
import os
import subprocess
import webbrowser
import time
import signal
from threading import Timer

def open_browser():
    """Open the browser after a short delay."""
    time.sleep(1.5)
    webbrowser.open('http://localhost:5001')

def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully."""
    print('\n\n👋 Shutting down BlockSim Web Interface...')
    print('Thanks for using BlockSim! 🚀')
    sys.exit(0)

def main():
    """Launch the web interface."""
    print("🚀 STARTING BLOCKSIM WEB INTERFACE")
    print("=" * 50)
    print("🌐 Starting Flask server...")
    print("📱 Web interface will be available at: http://localhost:5001")
    print("🔄 Auto-opening browser in 1.5 seconds...")
    print("\n💡 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    # Register signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    # Open browser after a delay
    Timer(1.5, open_browser).start()
    
    try:
        # Change to the script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
        # Import and run the Flask app
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5001, use_reloader=False)
        
    except ImportError as e:
        print(f"❌ Error: Could not import Flask app: {e}")
        print("💡 Make sure Flask is installed: pip3 install Flask")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
