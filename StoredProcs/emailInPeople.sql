DELIMITER //

CREATE PROCEDURE emailInPeople(inEmail varchar(50))
BEGIN

#Get the number of entries in People with the given email.

SELECT COUNT(*) FROM People
WHERE inEmail = email;

END //

