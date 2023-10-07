# No.0 - Create timeclock report table
CREATE TABLE timeclock_1 (
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
    PROG_ITEM_BSKT_PERC float(6,5),
    COUNTRY varchar(75)
);

# Add index
ALTER TABLE timeclock
ADD COLUMN id INT NOT NULL AUTO_INCREMENT FIRST,
ADD PRIMARY KEY (id);
