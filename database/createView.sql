CREATE VIEW experiment_overview AS
SELECT
    e.experiment_id,
    e.experiment_name,
    e.status,
    e.created_at,
    p.project_name,
    d.dataset_name,
    m.model_name,
    r.metric_name,
    r.metric_value
FROM experiment e
LEFT JOIN conduct c ON e.experiment_id = c.experiment_id
LEFT JOIN project p ON c.project_id = p.project_id
LEFT JOIN use_relation u ON e.experiment_id = u.experiment_id
LEFT JOIN dataset d ON u.dataset_id = d.dataset_id
LEFT JOIN choose_relation ch ON e.experiment_id = ch.experiment_id
LEFT JOIN model m ON ch.model_id = m.model_id
LEFT JOIN result r ON e.experiment_id = r.experiment_id;


-- 查询所有已完成实验的概览信息
SELECT * FROM experiment_overview WHERE status = 'done';

-- 查询指定实验的详细信息
SELECT * FROM experiment_overview WHERE experiment_id = 1;