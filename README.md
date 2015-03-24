Crunchbase-Crawler via API
===========================

A crawler fetchs company's json data by its permalinks via Crunchbase's API

file structure:
- crawler.py: python script
- fetch_list.txt: file contains target permalinks
- keys.txt: file contains keys
- log.txt: log file
- status.txt: current system status

features:
- open and shut down anytime, system status stored in disk
- traffic control: read a file per 1.5 second, and 2450 files per key per day.
- easy management of keys(add, delete)

known bugs and wait to be fixed:
- Crunchbase might count API connections by 24 hours not a natural day
- After finishing the fetch_list, the crawler won't stop
