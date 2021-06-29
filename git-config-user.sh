#!/bin/bash
# Quickly setup user name and email.
read -p "User name: " name
git config user.name "$name"
read -p "User email: " email
git config user.email "$email"
