
######## TANSFORM & CALCULATE - programming ###########################
##### (MERGE IN PROGRAMS, BASKETS, COUNTRY) #####

CREATE TABLE programming_3  LIKE programming;
CREATE TABLE timeclock_debug LIKE programming;
TRUNCATE programming_3;
TRUNCATE timeclock_debug;
DROP TABLE programming_1;
DROP TABLE timeclock_debug;

# 1.a Merge program names from country mappings (cheating)
-- Populate programming_1 from programming, chunked into 250K records
SELECT COUNT(*) FROM programming;
SELECT COUNT(*) FROM programming_1;
SELECT COUNT(*) FROM programs WHERE ID_PROGRAM IS NULL;
SELECT id, ID_DEFPRG, ID_PROGRAM, PROGRAM FROM programs WHERE CHAR_LENGTH(ID_PROGRAM) > 8 ORDER BY ID_PROGRAM DESC limit 50;
TRUNCATE programming_1;
SELECT COUNT(*) FROM programming_1 WHERE PROGRAM IS NULL;

-- Do it
INSERT INTO programming_3
SELECT * FROM programming
LIMIT 1000001, 500000;

-- MERGE Program ID and name 673749
SELECT * FROM programming LIMIT 673730, 25;
-- Do it | get it from Programs
UPDATE programming_3 pm
LEFT JOIN programs_clean p
ON pm.ID_DEFPRG = p.ID_DEFPRG
SET 
pm.PROGRAM_ID = CAST(p.ID_PROGRAM AS UNSIGNED),
pm.PROGRAM = p.PROGRAM;
-- OR...  Do it | get it and exclude weird long calues for prog id
SELECT MAX(ID_PROGRAM) FROM programs_clean;
UPDATE programming_3 pm
LEFT JOIN programs_clean p
ON pm.ID_DEFPRG = p.ID_DEFPRG
SET 
pm.PROGRAM_ID = p.ID_PROGRAM,
pm.PROGRAM = p.PROGRAM
WHERE CAST(p.ID_PROGRAM AS UNSIGNED) < 6020003001 OR (p.ID_PROGRAM) <= 10;

# remove 'ZZZ' PROGRAMS inactives
SELECT COUNT(*) FROM programming_1;
SELECT id, ID_DEFPRG, PROGRAM_ID, PROGRAM, PROGRAM ID_DEFBSK, 
BASKET_ID, BASKET, COUNTRY FROM programming_1 ORDER BY PROGRAM DESC LIMIT 100;
select * from programming_1 WHERE PROGRAM LIKE '%ZZZ%' ORDER BY PROGRAM ASC LIMIT 100;
-- Do it
DELETE FROM programming_1
WHERE PROGRAM LIKE '%ZZZ%';

# 2.a Merge basket names
#------
# MERGE Baskets v-1  (05:13:27 00:00:00)
SHOW FULL PROCESSLIST;
KILL 9;
SELECT COUNT(*) FROM programming_1;
SELECT id, PROG_LINE, ID_DEFPRG, PROGRAM_ID, PROGRAM, PROGRAM ID_DEFBSK, 
BASKET_ID, BASKET, COUNTRY FROM programming_1 LIMIT 100;
-- Do it
UPDATE programming_1 pm
LEFT JOIN baskets b
ON pm.ID_DEFBSK = b.ID_DEFBSK
SET pm.BASKET_ID = b.BASKET_ID, pm.BASKET = b.BASKET;
#2.b remove 'ZZZ' BASKET inactives (Goes from 143,307 TO 111,021)
SELECT COUNT(*) FROM programming_1;
SELECT * from programming_1 WHERE BASKET_NAME LIKE '%ZZZ%' ORDER BY BASKET_NAME ASC LIMIT 100;
-- Do it
DELETE FROM programming_1
WHERE BASKET LIKE '%ZZZ%';

# 3. Merge country names
SELECT COUNT(*) FROM country_mappings;
SELECT * FROM country_mappings LIMIT 10;
SELECT id, ID_DEFPRG, PROGRAM_ID, PROGRAM, PROGRAM ID_DEFBSK, 
BASKET_ID, BASKET, COUNTRY, IS_ACTIVE FROM programming_1 WHERE COUNTRY IS NOT NULL LIMIT 100;
-- DO IT
UPDATE programming_1 pm
LEFT JOIN country_mappings cm
ON pm.PROGRAM_ID = cm.SourceProgramID
SET pm.COUNTRY = cm.Country;

# 4. Set programming IS_ACTIVE = 0/1
SELECT COUNT(*) FROM programming_1 WHERE IS_ACTIVE = 0;
-- DO IT
UPDATE programming_1 SET IS_ACTIVE = 1;
UPDATE programming_1 SET IS_ACTIVE = 0 WHERE PROGRAM LIKE '%zzz%';
UPDATE programming_1 SET IS_ACTIVE = 0 WHERE BASKET LIKE '%zzz%';

############################### TIECLOCK REPORT SOUTION ##########

# ------------------------------------------------------
# No.1 - Merge in Src Programmed data + Baskets + Program Name 
# and generate base debug timeclock report
TRUNCATE timeclock_debug;
SELECT COUNT(*) FROM timeclock_debug;
SELECT * FROM timeclock_debug WHERE COUNTRY IS NOT NULL LIMIT 10;
-- Do it
INSERT INTO timeclock_debug (
	ID_DEFPRG, PROGRAM_ID, PROGRAM_NAME, ID_DEFBSK, BASKET_ID, BASKET_NAME, 
    PROG_LINE, START_DATE, END_DATE, START_TIME, END_TIME, COUNTRY
)
SELECT 
	mood.programming_1.ID_DEFPRG,
    mood.programming_1.PROGRAM_ID,
    mood.programming_1.PROGRAM as PROGRAM_NAME,
    mood.programming_1.ID_DEFBSK,
    mood.programming_1.BASKET_ID,
    mood.programming_1.BASKET as BASKET_NAME,
    mood.programming_1.PROG_LINE,
    mood.programming_1.START_DATE,
    mood.programming_1.END_DATE,
    mood.programming_1.START_TIME,
    mood.programming_1.END_TIME,
    mood.programming_1.COUNTRY
FROM mood.programming_1;

# No.2 - Cleanup dates into format 2027-12-32 00:00:00
UPDATE mood.timeclock_debug 
SET mood.timeclock_debug.START_DATE=concat(left(mood.timeclock_debug.START_DATE,length(mood.timeclock_debug.START_DATE) -4),''), 
mood.timeclock_debug.END_DATE=concat(left(mood.timeclock_debug.END_DATE,length(mood.timeclock_debug.END_DATE) -4),'');

# No.3 - Calculate prgram item duration in seconds <---- HANGING!!
UPDATE mood.timeclock_debug SET
timeclock_debug.PROG_ITEM_DURATION_SEC = mood.timeclock_debug.END_TIME - mood.timeclock_debug.START_TIME
WHERE mood.timeclock_debug.END_TIME > 0 AND mood.timeclock_debug.START_TIME >= 0;

# No.4.a - SET Prog UUID TO FIND DUPES EASIER
SELECT * FROM timeclock_debug ORDER BY BASKET_NAME ASC LIMIT 100;
-- Do it
UPDATE timeclock_debug
SET progbskt_uuid = MD5(CONCAT(PROGRAM_NAME, BASKET_NAME, PROG_LINE, START_DATE, 
END_DATE, START_TIME, END_TIME, PROG_ITEM_DURATION_SEC, TIME_SPAN));
-- DELETE IF UUID IS SAME, AS THESE ARE DUPES 
SELECT COUNT(*) FROM timeclock_debug;
-- Do it
DELETE FROM timeclock_debug
WHERE id NOT IN (
    SELECT * FROM (
        SELECT MAX(id)
        FROM timeclock_debug
        GROUP BY progbskt_uuid
    ) AS tmp
);

# No.4.b - SET Playlist UUID TO FIND GROUPINGS OF SONGS EASIER
SELECT COUNT(*) FROM timeclock_debug;
UPDATE timeclock_debug set playlist_uuid = NULL;
SELECT * FROM timeclock_debug ORDER BY  playlist_uuid desc LIMIT 10;
-- Do it
UPDATE timeclock_debug
SET playlist_uuid = MD5(CONCAT(PROGRAM_ID, START_DATE, END_DATE, START_TIME, END_TIME)) 
WHERE CHAR_LENGTH(BASKET_NAME) > 0 AND CHAR_LENGTH(BASKET_NAME) < 50;

# No.5 - Calc basket window size
SELECT * FROM timeclock_debug ORDER BY  playlist_uuid ASC LIMIT 10;
-- Do it
UPDATE timeclock_debug
SET mood.timeclock_debug.BASKET_SIZE_SEC = TIMESTAMPDIFF(SECOND, STR_TO_DATE(mood.timeclock_debug.START_DATE, "%Y-%m-%d %T.00"), STR_TO_DATE(mood.timeclock_debug.END_DATE, "%Y-%m-%d %T.00"));

#START @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# No.6 - Calc percent of Basket that song item takes up
UPDATE  timeclock_debug SET PROG_ITEM_BSKT_PERC = NULL, BASKET_PERCENT = NULL;
SELECT "Let's Get Started! :)";
SELECT id, PROGRAM_ID, PROGRAM_NAME, BASKET_ID, BASKET_NAME, progbskt_uuid, playlist_uuid, START_TIME, 
END_TIME, PROG_ITEM_BSKT_PERC, BASKET_PERCENT from timeclock_debug ORDER BY PROGRAM_ID ASC limit 500;
SELECT * from timeclock_debug WHERE PROGRAM_NAME = 'Dolce_Resto_Bel' ORDER BY PROGRAM_ID ASC limit 100;
SELECT COUNT(*) FROM timeclock_debug;
-- Do it
WITH derived_table AS (
    SELECT
		id,
        PROGRAM_ID,
        playlist_uuid,
        START_DATE,
        END_DATE,
        START_TIME,
        END_TIME,
        COUNT(*) OVER(PARTITION BY playlist_uuid) AS song_Count
    FROM timeclock_debug
)
UPDATE timeclock_debug td1
JOIN derived_table td2
ON td1.id = td2.id 
AND td1.playlist_uuid = td2.playlist_uuid 
AND td1.PROGRAM_ID = td2.PROGRAM_ID
AND td1.START_DATE = td2.START_DATE
AND td1.END_DATE = td2.END_DATE
AND td1.START_TIME = td2.START_TIME
AND td1.END_TIME = td2.END_TIME
SET td1.PROG_ITEM_BSKT_PERC = CAST((100/td2.song_Count) AS DECIMAL(10,4));
-- Add human friendly version
SELECT id, START_TIME, END_TIME, PROG_ITEM_BSKT_PERC, BASKET_PERCENT FROM timeclock_debug ORDER BY BASKET_NAME ASC LIMIT 20;
-- Do it
UPDATE timeclock_debug 
SET BASKET_PERCENT = CONCAT(ROUND(PROG_ITEM_BSKT_PERC,0), "%");

#END @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

#7 - Set prog item time span in format: 00:00-11: from mood.timeclock_debug.PROGRAM_ITEM_DURATION
select count(*) from timeclock_debug;
select * from timeclock_debug WHERE COUNTRY IS NOT NULL
ORDER BY COUNTRY DESC limit 100;
-- Do it
UPDATE timeclock_debug 
SET 
mood.timeclock_debug.TIME_SPAN = CONCAT(
        LPAD(FLOOR(mood.timeclock_debug.START_TIME / 3600), 2, '0'),
        ':',
        LPAD(FLOOR((mood.timeclock_debug.START_TIME % 3600) / 60), 2, '0'),
        ':',
        LPAD((mood.timeclock_debug.START_TIME % 60), 2, '0'),
        '-',
        LPAD(FLOOR(mood.timeclock_debug.END_TIME / 3600), 2, '0'),
        ':',
        LPAD(FLOOR((mood.timeclock_debug.END_TIME % 3600) / 60), 2, '0'),
        ':',
        LPAD((mood.timeclock_debug.END_TIME % 60), 2, '0')
    );

# No. 8 | Misc grooming & CLEANUP
-- NULL basket ID to zer (0)
SELECT * FROM timeclock_debug WHERE BASKET_ID IS NULL LIMIT 10;
SELECT COUNT(*) FROM timeclock_debug;
SELECT COUNT(*) FROM timeclock_debug WHERE BASKET_ID IS NULL;
-- Do it
UPDATE timeclock_debug SET BASKET_ID = 0 WHERE  BASKET_ID IS NULL;

# No.9 | CONCAT "SCHEDULE" STRING
# NOTE - We handle this in Pandas


########### Final Report timeclock #################################
# No.9 - Output to CSV (DOES NOT WORK)
SELECT * 
INTO OUTFILE '/var/lib/mysql/timeclock_report-20230929-A.csv'
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
FROM mood.timeclock
LIMIT 100;
#EError Code: 1290. The MySQL server is running with the --secure-file-priv option so it cannot execute this statement


