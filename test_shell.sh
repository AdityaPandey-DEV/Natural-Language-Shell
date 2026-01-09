#!/bin/bash

# Advanced Mini Bash Shell Test Script
# This script demonstrates the various features of the mini-bash shell

echo "=== Advanced Mini Bash Shell Test Suite ==="
echo

# Test 1: Basic built-in commands
echo "Test 1: Basic built-in commands"
echo "pwd" | ./mini-bash
echo "echo 'Hello from mini-bash!'" | ./mini-bash
echo

# Test 2: Command history
echo "Test 2: Command history"
echo -e "pwd\nls\necho 'test'\nhistory" | ./mini-bash
echo

# Test 3: Directory navigation
echo "Test 3: Directory navigation"
echo -e "pwd\ncd ..\npwd\ncd -\npwd" | ./mini-bash
echo

# Test 4: External commands
echo "Test 4: External commands"
echo "ls -la | head -5" | ./mini-bash
echo

# Test 5: Pipeline functionality
echo "Test 5: Pipeline functionality"
echo "ls | grep .c" | ./mini-bash
echo

# Test 6: Background jobs (basic test)
echo "Test 6: Background jobs"
echo -e "jobs\necho 'No background jobs yet'" | ./mini-bash
echo

# Test 7: Error handling
echo "Test 7: Error handling"
echo "nonexistent_command" | ./mini-bash
echo

echo "=== Test Suite Complete ==="
