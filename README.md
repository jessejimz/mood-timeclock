![alt text](https://ixtenso.com/media/manufacturer/839/logo-01-mood-icons-logo2-black.png "Mood Media")
## Timeclock Report - Readme

Go over ths doc to learn how to run this app for _Mood TimeClock_ report.

For more documentation, [visit here](https://treehousetechgroup.atlassian.net/wiki/spaces/MM/overview) 

Note: Before contributing to this doc, [learn Markdown on Github](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)

**TOPICS COVERED:**

1. setting up local env
..A. cloning repo
..B. configuring app
..C. docker composer to build
2. seeding the DB
3. running report creation

---

**Endpoint for Adminer**: http://localhost:8585/?server=dbsvc&username=root


Snippet for you
```python
python3 manage.py
docker exec -it mood-db bash
mysql -u root -p[PWD]
show databases;
create database mood;
use mood;
source mood_db_backup.dump;
```

Lorem ipsum dolor

| Tables        | Are           | Cool  |
| ------------- |:-------------:| -----:|
| col 3 is      | right-aligned | $1600 |
| col 2 is      | centered      |   $12 |
| zebra stripes | are neat      |    $1 |

Lorem ipsum dolor..

> Don't forget to...

<a href="http://www.youtube.com/watch?feature=player_embedded&v=YOUTUBE_VIDEO_ID_HERE
" target="_blank"><img src="http://img.youtube.com/vi/YOUTUBE_VIDEO_ID_HERE/0.jpg" 
alt="IMAGE ALT TEXT HERE" width="240" height="180" border="10" /></a>

---
Footnotes:
[^1]: Needs to be refactored
[^2]: Must be ported over
blah

docker exec -it mood-db bash
mysql -u -p