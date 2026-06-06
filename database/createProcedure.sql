CREATE PROCEDURE update_experiment_results(IN exp_id INT)
BEGIN
    DECLARE avg_acc DECIMAL(5,2);
    SELECT AVG(metric_value) INTO avg_acc
    FROM result
    WHERE experiment_id = exp_id AND metric_name = 'Accuracy';
    UPDATE experiment
    SET config = CONCAT(config, ',avg_acc=', avg_acc)
    WHERE experiment_id = exp_id;
END;

-- 示例调用
CALL update_experiment_results(1);