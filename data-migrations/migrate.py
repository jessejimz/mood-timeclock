import psycopg2


# connect
conn = psycopg2.connect(
    database="mood",
    user="mooduser",
    password="mood123",
    host="0.0.0.0",
    port="5432"
)

# Open cursor
cur = conn.cursor()

# Introduce Known Counties
cur.execute("CREATE TABLE IF NOT EXISTS src_countries (\
    COUNTRY_ID INT,\
    COUNTRY VARCHAR(75)")
rows = cur.fetchall()
print(rows)

if rows.count() == 0:
    cur.execute(
        "INSERT INTO `src_countries` VALUES\
            (1,'US'),\
            (2,'Albania'),\
            (4,'Andorra'),\
            (5,'Anguilla'),\
            (6,'Antigua and Barbuda'),\
            (7,'Saudi Arabia'),\
            (8,'Argentina'),\
            (9,'Armenia'),\
            (10,'Australia'),\
            (11,'Austria'),\
            (12,'Azerbaijan'),\
            (13,'Bahamas'),\
            (14,'Bahrain'),\
            (15,'Bangladesh'),\
            (16,'Barbados'),\
            (17,'Belgium'),\
            (18,'Belize'),\
            (19,'Belorussia'),\
            (20,'Bolivia'),\
            (21,'Bosnia and Herzegovina'),\
            (22,'Brazil'),\
            (23,'Brunei'),\
            (24,'Bulgaria'),\
            (25,'Cambodia'),\
            (27,'Canada'),\
            (29,'Chile'),\
            (30,'China'),\
            (31,'Colombia'),\
            (33,'Costa Rica'),\
            (34,'Croatia'),\
            (35,'Cuba'),\
            (36,'Cyprus (Turish part)'),\
            (37,'Czech Republic'),\
            (38,'Denmark'),\
            (40,'Dominica'),\
            (41,'Dominican Republic'),\
            (42,'Ecuador'),\
            (44,'El Salvador'),\
            (45,'Estonia'),\
            (47,'Finland'),\
            (48,'France'),\
            (48,'French Polynesia'),\
            (51,'Germany'),\
            (52,'Georgia'),\
            (54,'Greece'),\
            (55,'Grenada'),\
            (57,'Guatemala'),\
            (58,'Haiti'),\
            (59,'Netherlands'),\
            (60,'Honduras'),\
            (61,'Hong Kong'),\
            (62,'Hungary'),\
            (63,'Iceland'),\
            (64,'India'),\
            (65,'Indonesia'),\
            (66,'Iran'),\
            (67,'Iraq'),\
            (68,'Ireland'),\
            (69,'Israel'),\
            (70,'Italy'),\
            (71,'Jamaica'),\
            (72,'Japan'),\
            (73,'Jordan'),\
            (74,'Kazakhstan'),\
            (76,'North Korea'),\
            (76,'South Korea'),\
            (77,'Kuwait'),\
            (78,'Kyrgyzstan'),\
            (79,'Latvia'),\
            (80,'Lebanon'),\
            (81,'Lithuania'),\
            (82,'Macedonia'),\
            (84,'Malaysia'),\
            (85,'Maldives'),\
            (86,'Malta'),\
            (89,'Mexico'),\
            (90,'Moldova'),\
            (91,'Mongolia'),\
            (92,'Montenegro'),\
            (94,'Morocco'),\
            (95,'Nepal'),\
            (96,'New Zealand'),\
            (97,'Nicaragua'),\
            (98,'Nigeria'),\
            (99,'Norway'),\
            (100,'Oman'),\
            (101,'Uganda'),\
            (102,'Pakistan'),\
            (103,'Panama'),\
            (104,'Paraguay'),\
            (105,'Peru'),\
            (106,'Philippines'),\
            (107,'Poland'),\
            (108,'Portugal'),\
            (110,'Qatar'),\
            (112,'Romania'),\
            (113,'Russia'),\
            (114,'Saint Kitts and Nevis'),\
            (115,'Saint Lucia'),\
            (116,'Saint Vincent and the Grenadines'),\
            (118,'Serbia'),\
            (120,'Singapore'),\
            (121,'Slovakia'),\
            (122,'Slovenia'),\
            (123,'Spain'),\
            (124,'Sri Lanka'),\
            (125,'Sweden'),\
            (126,'Switzerland'),\
            (127,'Syria'),\
            (128,'Taiwan'),\
            (129,'Thailand'),\
            (130,'Trindad & Tobago'),\
            (131,'Tunisia'),\
            (132,'Turkey'),\
            (133,'UAE'),\
            (134,'UK'),\
            (135,'Ukraine'),\
            (136,'Uruguay'),\
            (137,'Venezuela'),\
            (138,'Vietnam'),\
            (139,'Virgin Islands'),\
            (140,'Yemen'),\
            (142,'French Guiana'),\
            (143,'Guyana'),\
            (144,'Suriname'),\
            (145,'South Africa'),\
            (148,'Algeria'),\
            (149,'Myanmar'),\
            (150,'Caribbean'),\
            (151,'Luxembourg'),\
            (152,'Libya'),\
            (153,'Fiji')")
    
cur.execute("SELECT * FROM src_countries")
rows = cur.fetchall()
print(rows)

# do smth

# close connection
cur.close()
conn.close()
