#!/bin/bash
# Quickly setup user name and email.
echo "Current name: $(git config user.name)"
echo "Current email: $(git config user.email)"
read -p "User name: " name
git config user.name "$name"
read -p "User email: " email
git config user.email "$email"
