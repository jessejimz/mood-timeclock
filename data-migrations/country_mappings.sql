# Create Programming interim table
CREATE TABLE country_mappings AS SELECT * FROM src_Program_Report_Unity;

# Drop uneeded cols
ALTER TABLE country_mappings 
DROP Program_Type,
DROP Source,
DROP No_of_Active_Clients,
DROP Total_no_of_Active_Devices_using_Program,
DROP Total_CD_Update_Devices,
DROP Total_NW_Update_Devices;

# Add indexes 
ALTER TABLE country_mappings
ADD COLUMN id INT NOT NULL AUTO_INCREMENT FIRST,
ADD PRIMARY KEY (id);
# # covering indexes
CREATE INDEX ctry_maps_cover_index
ON country_mappings (Program_Name, SourceProgramID, Country);
# index on prog and bsk
CREATE INDEX id_prog ON country_mappings (SourceProgramID);
