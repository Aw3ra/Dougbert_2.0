#!/usr/bin/env python3

# Generate the Prisma client
prisma generate

# Run the main Python script
exec "src/main.py"
