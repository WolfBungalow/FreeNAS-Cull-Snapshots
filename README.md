# FreeNAS-Cull-Snapshots
The script reduces the number snapshots created by FreeNAS Perodic Snapshots Tasks. It uses two methods, first it compares snapshots two at a time deleting newer snapshots that have no difference from the older one. Second, after a user specified time it reduces the number of snapshots taken throughout a day to one per day, then after another user defined length of time reduces the number to one per week.

# FreeNAS Verion Support
It has been tested with FreeNas-11. It worked on older versions back to FreeNAS-9 but I updated for FreeNAS-11 and am not going to go back and test on older versions.

# Multiple FreeNAS Periodic Snapshot Tasks
This script matches snapshots based on their name, particularly the "Volume/Dataset" and the "Snapshot Lifetime". In FreeNAS you can setup multiple Periodic Snapshot Tasks that have the same "Volume/Dataset" and the "Snapshot Lifetime" but different Begin, End, Interval and Weekday settings. The script will treat those snapshots as the same snapshot task when comparing.

# Config.py
Customize the config file with your system's particulars. Server username, password and URL. Customize the snapshot culling timeframes.

# Install
1. Copy the script and config.py to a user folder on your server or storage.
2. Customize the config.py.
3. Setup and a cron job to run as desired.

# Disclamer
I'm a noob. Use at your own risk.
