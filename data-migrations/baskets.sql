# Basket Definitions
CREATE TABLE baskets AS SELECT * FROM src_prgdef_bskdef_working;

# Add index
ALTER TABLE baskets
ADD COLUMN id INT NOT NULL AUTO_INCREMENT FIRST,
ADD PRIMARY KEY (id);

# Drop uneeded cols
ALTER TABLE baskets 
DROP BRANDOM,
DROP START_DATE,
DROP END_DATE,
DROP START_TIME,
DROP END_TIME,
DROP BPLAYMON,
DROP BPLAYTUE,
DROP BPLAYWED,
DROP BPLAYTHU,
DROP BPLAYFRI,
DROP BPLAYSAT,
DROP BPLAYSUN,
DROP RECURRENCE,
DROP ID_LN_PRGDEF_BSKDEF,
DROP TIMESTMP,
DROP PROG_LINE;

# covering index
CREATE INDEX covering_index
ON baskets (ID_DEFBSK, BASKET_ID, BASKET);
# index on prog and bsk
CREATE INDEX bsk_id_index ON baskets (BASKET_ID);
CREATE INDEX bsk_idbsk_index ON baskets (ID_DEFBSK);