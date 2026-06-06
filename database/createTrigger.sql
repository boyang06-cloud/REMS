DELIMITER //
CREATE TRIGGER set_experiment_created_at
BEFORE INSERT ON experiment
FOR EACH ROW
BEGIN
    IF NEW.created_at IS NULL THEN
        SET NEW.created_at = NOW();
    END IF;
END //
DELIMITER ;

-- 触发器控制下的插入：created_at 留空，由触发器自动填充当前时间
INSERT INTO experiment (experiment_name, status, config, description)
VALUES ('触发器测试实验', 'Draft', 'lr=0.001,batch=32', '测试触发器自动填充创建时间');

SELECT experiment_id, experiment_name, created_at FROM experiment
WHERE experiment_name = '触发器测试实验';