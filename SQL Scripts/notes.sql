USE notes;

drop database notes;

create database notes;

SELECT * FROM note;
SELECT * FROM note ORDER BY date_created;

DROP TABLE note;
DROP TABLE tag; 

CREATE TABLE IF NOT EXISTS note(
	note_id INT AUTO_INCREMENT PRIMARY KEY,
	content BLOB NOT NULL,
	date_created DATE NOT NULL DEFAULT (CURDATE()),
	active BOOL NOT NULL DEFAULT true
);


SELECT note_id FROM note;

CREATE TABLE IF NOT EXISTS tag(
	fk_note_id INT,
	name VARCHAR(255) NOT NULL,
	FOREIGN KEY (fk_note_id) REFERENCES note(note_id),
	PRIMARY KEY(fk_note_id, name)
);

DROP TABLE tag;

INSERT INTO note(date_created) VALUES(CURDATE());

INSERT INTO tag VALUES(2, "CS");

SELECT fk_note_id FROM tag;

SELECT 
	note.note_id FROM note
WHERE 
	note_id IN (SELECT 
	fk_note_id FROM tag
	WHERE name = "CS");


INSERT INTO note (content) VALUES (LOAD_FILE("D:\\School\\AP Project\\Note\\test.txt"));




