#TBL_DEFINED_PRG_202304182317-WORKING.csv
CREATE TABLE mood.`src_defined_prg_working` (
	ID_DEFPRG int(11),
    ID_PROGRAM varchar(75),
    PROGRAM varchar(75),
    TARGET_START_DATE varchar(50),
    TARGET_END_DATE varchar(50),
    VALIDATED int(11),
    IN_PRODUCTION int(11),
    VALIDATED_DATE varchar(50),
    TIMESTMP varchar(50)
);
select count(*) from mood.`src_defined_prg_working`;

#TBL_LN_PRGDEF_BSKDEF_202304182317-WORKING.csv
CREATE TABLE mood.`src_prgdef_bskdef_working` (
	ID_DEFPRG int(11),
    PROGRAM_ID int(11),
    PROGRAM varchar(75),
    ID_DEFBSK int(11),
    BASKET_ID int(11),
    BASKET varchar(75),
    PROG_LINE int(11),
    BRANDOM int(11),
    START_DATE varchar(50),
    END_DATE varchar(50),
    START_TIME varchar(50),
    END_TIME varchar(50),
    BPLAYMON int(11),
    BPLAYTUE int(11),
    BPLAYWED int(11),
    BPLAYTHU int(11),
    BPLAYFRI int(11),
    BPLAYSAT int(11),
    BPLAYSUN int(11),
    RECURRENCE int(11),
    ID_LN_PRGDEF_BSKDEF int(11),
    TIMESTMP varchar(50)
);
select count(*) from mood.`src_prgdef_bskdef_working`;