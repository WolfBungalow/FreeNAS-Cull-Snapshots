#!/usr/bin/env python

# SCRIPT CONFIG

# Server username and password, and URL
auth = ('root', 'root')
serverURL = 'http://testnas.local'

# Minimum Snap Age: Keep all snapshots less than X days old.
snapAgeMin = 3

# Snapshots older than the "Minimum Snap Age" but less than X days old. Keep only
# one snapshot per day. The newest snapshot that day will be kept all other will
# be destroyed. Snapshots older than X days, only one snapshot per week is kept.
# The newest that week is kept, all others are destroyed. 
snapAgeDay = 14
