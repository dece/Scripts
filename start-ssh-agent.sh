#!/bin/bash
# A script to ensure one and only SSH agent is running, especially in Tmux or
# remote sessions. You can add it to your bashrc/zshrc without issues.
# Inspired from: http://rabexc.org/posts/pitfalls-of-ssh-agents

AGENT_CONFIG="$HOME/.ssh-agent"

# First try to list identities.
ssh-add -l &> /dev/null

# If it returned 2, try to load a running agent config.
if [ "$?" = 2 ]; then
    test -r $AGENT_CONFIG && eval "$(<$AGENT_CONFIG)" > /dev/null

    # Retry.
    ssh-add -l &> /dev/null
    # If it still does not work, start a new agent.
    if [ "$?" = 2 ]; then
        (umask 066; ssh-agent > $AGENT_CONFIG)
        eval "$(<$AGENT_CONFIG)" > /dev/null
    fi
fi
