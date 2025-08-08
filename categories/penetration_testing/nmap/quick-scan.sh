#!/bin/bash
# Quick nmap scan script
# Usage: ./quick-scan.sh <target>

TARGET=$1
if [ -z "$TARGET" ]; then
    echo "Usage: $0 <target>"
    exit 1
fi

echo "Running quick scan on $TARGET..."
nmap -sS -O -sV --top-ports 1000 $TARGET