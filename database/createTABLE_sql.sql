
-- =====================================
-- 科研实验管理系统（REMS）
-- Database: MySQL
-- =====================================

-- =====================================
-- 1. Project
-- =====================================

CREATE TABLE project (
    project_id INT AUTO_INCREMENT PRIMARY KEY,
    project_name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at DATETIME
);

-- =====================================
-- 2. Dataset
-- =====================================

CREATE TABLE dataset (
    dataset_id INT AUTO_INCREMENT PRIMARY KEY,
    dataset_name VARCHAR(255) NOT NULL,
    modality VARCHAR(20),
    description TEXT
);

-- =====================================
-- 3. Model
-- =====================================

CREATE TABLE model (
    model_id INT AUTO_INCREMENT PRIMARY KEY,
    model_name VARCHAR(255) NOT NULL,
    type VARCHAR(30),
    version VARCHAR(20),
    description TEXT
);

-- =====================================
-- 4. Experiment
-- =====================================

CREATE TABLE experiment (
    experiment_id INT AUTO_INCREMENT PRIMARY KEY,
    experiment_name VARCHAR(255),
    status VARCHAR(10),
    config TEXT,
    created_at DATETIME,
    description TEXT
);

-- =====================================
-- 5. Tag
-- =====================================

CREATE TABLE tag (
    tag_id INT AUTO_INCREMENT PRIMARY KEY,
    tag_name VARCHAR(50) NOT NULL
);

-- =====================================
-- 6. Result
-- =====================================

CREATE TABLE result (
    result_id INT AUTO_INCREMENT PRIMARY KEY,
    experiment_id INT NOT NULL,
    metric_name VARCHAR(50),
    metric_value DOUBLE,
    record_time DATETIME,

    CONSTRAINT fk_result_experiment
    FOREIGN KEY (experiment_id)
    REFERENCES experiment(experiment_id)
);

-- =====================================
-- 7. Conduct
-- Project ↔ Experiment
-- =====================================

CREATE TABLE conduct (
    project_id INT,
    experiment_id INT,

    PRIMARY KEY (project_id, experiment_id),

    CONSTRAINT fk_conduct_project
    FOREIGN KEY (project_id)
    REFERENCES project(project_id),

    CONSTRAINT fk_conduct_experiment
    FOREIGN KEY (experiment_id)
    REFERENCES experiment(experiment_id)
);

-- =====================================
-- 8. Choose
-- Model ↔ Experiment
-- =====================================

CREATE TABLE choose_relation (
    model_id INT,
    experiment_id INT,

    PRIMARY KEY (model_id, experiment_id),

    CONSTRAINT fk_choose_model
    FOREIGN KEY (model_id)
    REFERENCES model(model_id),

    CONSTRAINT fk_choose_experiment
    FOREIGN KEY (experiment_id)
    REFERENCES experiment(experiment_id)
);

-- =====================================
-- 9. Use
-- Dataset ↔ Experiment
-- =====================================

CREATE TABLE use_relation (
    dataset_id INT,
    experiment_id INT,

    PRIMARY KEY (dataset_id, experiment_id),

    CONSTRAINT fk_use_dataset
    FOREIGN KEY (dataset_id)
    REFERENCES dataset(dataset_id),

    CONSTRAINT fk_use_experiment
    FOREIGN KEY (experiment_id)
    REFERENCES experiment(experiment_id)
);

-- =====================================
-- 10. Belong_to
-- Tag ↔ Experiment
-- =====================================

CREATE TABLE belong_to (
    tag_id INT,
    experiment_id INT,

    PRIMARY KEY (tag_id, experiment_id),

    CONSTRAINT fk_belong_tag
    FOREIGN KEY (tag_id)
    REFERENCES tag(tag_id),

    CONSTRAINT fk_belong_experiment
    FOREIGN KEY (experiment_id)
    REFERENCES experiment(experiment_id)
);

