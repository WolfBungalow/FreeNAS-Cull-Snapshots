# FreeNAS-Cull-Snapshots
The script reduces the number snapshots created by FreeNAS Perodic Snapshots Tasks. It uses two methods, first it compares snapshots two at a time deleting newer snapshots that have no difference from the older one. Second, after a user specified time it reduces the number of snapshots taken throughout a day to one per day, then after another user defined length of time reduces the number to one per week.

It has been tested with FreeNas-11.

The script first destroys snaps that have no difference between them. It then destroys snaps by date, reducing multiple snaps per day snaps to one per day then one per week. The timeframe is customizable in the config. I've included comments within the script.

# Config.py
Customize the config file with your system's particulars. Server username, password and URL. Customize the snapshot culling timeframes.
