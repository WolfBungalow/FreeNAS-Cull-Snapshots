# FreeNAS-Cull-Snapshots
The script reduces the number snapshots created by FreeNAS Perodic Snapshots Tasks. It uses two methods, first it compares snapshots two at a time deleting newer snapshots that have no difference from the older one. Second, after a user specified time it reduces the number of snapshots taken throughout a day to one per day, then after another user defined length of time reduces the number to one per week.

It has been tested with FreeNas-11.

# Install
1. Copy the script and config.py to a user folder on your server or storage.
2. Customize the config.py.
3. Setup and a cron job to run as desired.

# Config.py
Customize the config file with your system's particulars. Server username, password and URL. Customize the snapshot culling timeframes.
