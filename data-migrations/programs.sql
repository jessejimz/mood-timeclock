# Program Definitions
CREATE TABLE programs AS SELECT * FROM src_defined_prg_working;
SELECT COUNT(*) FROM programs;
SELECT * FROM programs limit 10;

# Add index
ALTER TABLE programs
ADD COLUMN id INT NOT NULL AUTO_INCREMENT FIRST,
ADD PRIMARY KEY (id);

# Drop uneeded cols
ALTER TABLE programs 
DROP TARGET_START_DATE,
DROP TARGET_END_DATE,
DROP VALIDATED,
DROP IN_PRODUCTION,
DROP VALIDATED_DATE,
DROP TIMESTMP;

# covering index
CREATE INDEX covering_index
ON programs (ID_DEFPRG, ID_PROGRAM, PROGRAM);
