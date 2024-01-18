-- Write a SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser

DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id_param INT)
BEGIN
    DECLARE total_weighted_score FLOAT;
    DECLARE total_weight INT;
    SET total_weighted_score = 0;
    SET total_weight = 0;
    SELECT 
        SUM(c.score * p.weight) AS total_weighted_score,
        SUM(p.weight) AS total_weight
    INTO 
        total_weighted_score, total_weight
    FROM corrections c
    JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = user_id_param;
    UPDATE users
    SET average_score = total_weighted_score / total_weight
    WHERE id = user_id_param;
END $$
DELIMITER ;
