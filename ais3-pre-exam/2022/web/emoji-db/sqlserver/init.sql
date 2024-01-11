CREATE DATABASE CatEmojiDB;
GO
USE CatEmojiDB;
GO
CREATE LOGIN meow WITH PASSWORD = 'da7ab4s3_p455w0rd';
GO
CREATE USER meow FOR LOGIN meow WITH DEFAULT_SCHEMA = CatEmojiDB;

CREATE TABLE s3cr3t_fl4g_in_th1s_t4bl3 (
    m1ght_be_th3_f14g VARCHAR(255) NOT NULL,
);


INSERT INTO s3cr3t_fl4g_in_th1s_t4bl3 (m1ght_be_th3_f14g) VALUES ('nyan?');
INSERT INTO s3cr3t_fl4g_in_th1s_t4bl3 (m1ght_be_th3_f14g) VALUES ('nyan!');
INSERT INTO s3cr3t_fl4g_in_th1s_t4bl3 (m1ght_be_th3_f14g) VALUES ('nyan.');
INSERT INTO s3cr3t_fl4g_in_th1s_t4bl3 (m1ght_be_th3_f14g) VALUES ('meow~');
INSERT INTO s3cr3t_fl4g_in_th1s_t4bl3 (m1ght_be_th3_f14g) VALUES ('ny4nnnnn');
INSERT INTO s3cr3t_fl4g_in_th1s_t4bl3 (m1ght_be_th3_f14g) VALUES ('AIS3333{you_are_so_close}');
INSERT INTO s3cr3t_fl4g_in_th1s_t4bl3 (m1ght_be_th3_f14g) VALUES ('AIS3{Yep /r/BadUIBattles happened again}');
INSERT INTO s3cr3t_fl4g_in_th1s_t4bl3 (m1ght_be_th3_f14g) VALUES ('meow!!!');
INSERT INTO s3cr3t_fl4g_in_th1s_t4bl3 (m1ght_be_th3_f14g) VALUES ('meow?');
INSERT INTO s3cr3t_fl4g_in_th1s_t4bl3 (m1ght_be_th3_f14g) VALUES ('ny4nnnnn');
INSERT INTO s3cr3t_fl4g_in_th1s_t4bl3 (m1ght_be_th3_f14g) VALUES ('meow...');


CREATE TABLE Emoji
(
    Id INT NOT NULL IDENTITY(1, 1),
    Name VARCHAR(50) NOT NULL,
    Emoji VARCHAR(50) COLLATE Latin1_General_100_CI_AI_SC_UTF8 NOT NULL ,
    Description VARCHAR(MAX) NOT NULL,
    Unicode BIGINT NOT NULL,
    PRIMARY KEY (Id)
);

INSERT INTO Emoji
    (Name, Emoji, Description, Unicode)
VALUES
    ('cat', N'🐱', 'A cat', 128049);
INSERT INTO Emoji
    (Name, Emoji, Description, Unicode)
VALUES
    ('cat2', N'🐈', 'Another cat', 128008);
INSERT INTO Emoji
    (Name, Emoji, Description, Unicode)
VALUES
    ('secret_cat (hint here)', N'🐈‍⬛', 'The FLAG is in other table', 556694539487);
INSERT INTO Emoji
    (Name, Emoji, Description, Unicode)
VALUES
    ('cat_face', N'😺', 'A cat face', 128570);
INSERT INTO Emoji
    (Name, Emoji, Description, Unicode)
VALUES
    ('smiley_cat', N'😺', 'A smiley cat', 128570);
INSERT INTO Emoji
    (Name, Emoji, Description, Unicode)
VALUES
    ('smile_cat', N'😸', 'A smile cat', 128570);
INSERT INTO Emoji
    (Name, Emoji, Description, Unicode)
VALUES
    ('joy_cat', N'😹', 'A joy cat', 128569);
INSERT INTO Emoji
    (Name, Emoji, Description, Unicode)
VALUES
    ( 'heart_eyes_cat', N'😻', 'Smiling cat face with heart-eyes', 128571);
INSERT INTO Emoji
    (Name, Emoji, Description, Unicode)
VALUES
    ('smirk_cat', N'😼', 'Cat face with wry smile', 128572);
INSERT INTO Emoji
    (Name, Emoji, Description, Unicode)
VALUES
    ('kissing_cat', N'😽', 'A kissing cat face', 128573);
INSERT INTO Emoji
    (Name, Emoji, Description, Unicode)
VALUES
    ('scream_cat', N'🙀', 'A scream cat', 128576);
INSERT INTO Emoji
    (Name, Emoji, Description, Unicode)
VALUES
    ('crying_cat_face', N'😿', 'A crying cat face', 128575);
INSERT INTO Emoji
    (Name, Emoji, Description, Unicode)
VALUES
    ('pouting_cat', N'😾', 'A pouting cat', 128574);

ALTER ROLE db_owner ADD MEMBER meow;
GO