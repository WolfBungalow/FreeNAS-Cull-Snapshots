#!/usr/bin/env python

import datetime
import json
import re
import requests
import subprocess

# Customize the config file with your system's particulars.
import config

# Sends API request to server. Uses config settings.
def send_get(api_url):
	return requests.get(config.serverURL + api_url, auth=config.auth,
		headers={'Content-Type': 'application/json'})

# Returns a list of all periodic snapshot tasks.
def get_snapshottasks():
    return json.loads(send_get('/api/v1.0/storage/task/').text)

# Loop through snapshots from old to new. Compare two at a time, deleting newer
# snapshots with no difference from the older one.
def cull_IdenticalSnaps(snapTaskDetail):

    # Create system snap list. Get all system snapshots, their name and this
    # script's custom property. Split into list and sort from old to new.
    args = ['zfs', 'list', '-H', '-t', 'snapshot', '-o', 'name,ast:culled']
    sysSnaps = sorted(subprocess.check_output(args).decode('UTF-8').splitlines())

    for task_fileSystem, task_retention in snapTaskDetail:
        # RegEx system snaps list, match task filesystem and retention critera.
        pattern = '^' + task_fileSystem + '@auto-.*' + task_retention
        taskSnaps = [line.split("\t") for line in sysSnaps if re.search(pattern, line)]

        # Return if not enough snaps to compare.
        if len(taskSnaps) < 2: return

        # Compare snaps, set custom zfs property if different, else delete.
        lastSnap = taskSnaps[0][0]
        for snapName, culled in taskSnaps[1:]:
            # For snaps not culled before, compare with previous snap. If diff
            # found set custom property, else no diff found, destroy the snap.
            if culled != 'True':
                if subprocess.check_output(['zfs', 'diff', lastSnap, snapName]):
                    subprocess.check_output(['zfs', 'set', 'ast:culled=True', snapName])
                else:
                    subprocess.check_output(['zfs', 'destroy', snapName])
                    continue
            lastSnap = snapName

def cull_SnapsByDate(snapTaskDetail):

    # Create system snap list. Get all system snapshots names. Split into list
    # and sort from new to old.
    args = ['zfs', 'list', '-H', '-t', 'snapshot', '-o', 'name']
    sysSnaps = sorted(subprocess.check_output(args).decode('UTF-8').splitlines(), reverse=True)
    
    today = datetime.datetime.today()

    for task_fileSystem, task_retention in snapTaskDetail:
        # RegEx system snaps list, match task filesystem and retention critera.
        pattern = '^' + task_fileSystem + '@auto-.*' + task_retention
        taskSnaps = [line for line in sysSnaps if re.search(pattern, line)]

        lastCull = ''
        for snapName in taskSnaps:
            # Create a datetime from the date in the snap name.
            snapDate = datetime.datetime.strptime(snapName.split('@')[1][5:18], '%Y%m%d.%H%M')
            snapDaysOld = (today - snapDate).days

            # Keep all snaps less than X days old.
            if snapDaysOld < config.snapAgeMin: continue

            # Get the date string used to decide whether to keep a snap. If older
            # than X days return %Year%YearWeek; only the newest snap per week
            # will be saved. Else only the newest snap per day will be saved.
            cullDateStr = snapDate.strftime('%Y%U' if snapDaysOld > config.snapAgeDay else '%Y%m%d')

            # Starting from the newest snap, skip if cull date string doesn't
            # match the last one; either it's the first loop or a different day
            # or week. Else it does match which means its the same day/week.
            if lastCull != cullDateStr:
                lastCull = cullDateStr
            else:
                subprocess.check_output(['zfs', 'destroy', snapName])

def main():

    # Call FreeNAS API to get the system's periodic snapshot tasks. Then create
    # a list with the task's filesystem and snapshot combined retention count
    # and unit. Example: "2" and "week" becomes "2w"
    snapTaskDetail = []
    for a in get_snapshottasks():
        b = [a['task_filesystem'], str(a['task_ret_count']) + a['task_ret_unit'][0:1]]
        # Tasks with duplicate filesystem and retention critera are combined.
        if b not in snapTaskDetail:
            snapTaskDetail.append(b)

    cull_IdenticalSnaps(snapTaskDetail)
    cull_SnapsByDate(snapTaskDetail)

main()
