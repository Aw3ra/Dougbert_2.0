#!/bin/sh

# Generate the Prisma client
prisma generate

# Run the main Python script
exec "src/main.py"
