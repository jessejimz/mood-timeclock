# No.0 - Create timeclock report table
CREATE TABLE timeclock_debug (
    ID_DEFPRG int(11),
    PROGRAM_ID int(11),
    PROGRAM_NAME varchar(75),
    ID_DEFBSK int(11),
    BASKET_ID int(11),
    BASKET_NAME varchar(75),
    PROG_LINE varchar(75),
    START_DATE varchar(50),
    END_DATE varchar(50),
    START_TIME int(11),
    END_TIME int(11),
    BASKET_SIZE_SEC int(11),
    PROG_ITEM_DURATION_SEC int(11),
    TIME_SPAN varchar(25),
    PROG_ITEM_BSKT_PERC float(10,4),
    BASKET_PERCENT varchar(10),
    COUNTRY varchar(75),
    playlist_uuid varchar(255),
    progbskt_uuid varchar(35)
);

# Add index
ALTER TABLE timeclock_debug
ADD COLUMN id INT NOT NULL AUTO_INCREMENT FIRST,
ADD PRIMARY KEY (id);

# add UUID
ALTER TABLE timeclock_debug
ADD COLUMN progbskt_uuid varchar(7) AFTER COUNTRY;
-- create indexes
CREATE INDEX progbskt_uuid_index ON timeclock_debug (progbskt_uuid);

# add Playlist UUID
ALTER TABLE timeclock_debug
ADD COLUMN playlist_uuid varchar(255) AFTER COUNTRY;
-- create indexes
CREATE INDEX playlist_uuid_index ON timeclock_debug (progbskt_uuid);

# Add Time start-endstring 
ALTER TABLE timeclock_debug
ADD COLUMN mood.`TIME` varchar(20) AFTER PROG_ITEM_BSKT_PERC;

# Add human friendly percent
ALTER TABLE timeclock_debug
ADD COLUMN BASKET_PERCENT varchar(10) AFTER PROG_ITEM_BSKT_PERC;

ALTER TABLE timeclock_debug MODIFY PROG_ITEM_BSKT_PERC float(10,4);



