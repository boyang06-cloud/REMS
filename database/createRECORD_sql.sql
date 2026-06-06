
-- =====================================
-- Project
-- =====================================

INSERT INTO project(project_name, description, created_at)
VALUES
('Semi-Supervised Emotion Recognition',
 'Research on semi-supervised facial emotion recognition',
 '2025-03-01'),

('Object Detection Study',
 'Research and comparison of object detection algorithms',
 '2025-03-10');

-- =====================================
-- Dataset
-- =====================================

INSERT INTO dataset(dataset_name, modality, description)
VALUES
('RAF-DB', 'Image', 'Facial expression recognition dataset'),
('FER2013', 'Image', 'Facial expression recognition benchmark'),
('AffectNet', 'Image', 'Large-scale facial expression dataset'),
('COCO2017', 'Image', 'Object detection dataset'),
('Pascal VOC 2012', 'Image', 'Object detection benchmark'),
('WIDER FACE', 'Image', 'Face detection dataset'),
('Emotion6', 'Image', 'Emotion image dataset');

-- =====================================
-- Model
-- =====================================

INSERT INTO model(model_name, type, version, description)
VALUES
('ResNet50', 'CNN', '1.0', 'Baseline CNN model'),
('ViT-B16', 'Transformer', '1.0', 'Vision Transformer'),
('FixMatch', 'SemiSupervised', '1.0', 'FixMatch framework'),
('S2VER', 'SemiSupervised', '1.0', 'S2VER framework'),
('YOLOv11', 'Detector', '1.0', 'Object detector'),
('RT-DETR', 'Detector', '1.0', 'Real-time DETR');

-- =====================================
-- Experiment
-- =====================================

INSERT INTO experiment
(experiment_name,status,config,created_at,description)
VALUES
(
'RAF-DB ResNet50 Baseline',
'done',
'lr=0.001,batch=32',
'2025-03-05',
'Baseline experiment'
),

(
'FixMatch Semi-Supervised',
'done',
'lr=0.001,batch=32,label_ratio=10%',
'2025-03-15',
'Semi-supervised learning'
),

(
'S2VER Comparison',
'done',
'lr=0.0005,batch=16',
'2025-04-01',
'S2VER evaluation'
),

(
'YOLOv11 COCO Training',
'done',
'img=640,epoch=100',
'2025-04-10',
'Object detection baseline'
),

(
'YOLOv11 vs RT-DETR',
'done',
'img=640,epoch=100',
'2025-04-20',
'Model comparison experiment'
);

-- =====================================
-- Tag
-- =====================================

INSERT INTO tag(tag_name)
VALUES
('baseline'),
('semi-supervised'),
('comparison'),
('detection'),
('final');

-- =====================================
-- Conduct
-- Project ↔ Experiment
-- =====================================

INSERT INTO conduct(project_id, experiment_id)
VALUES
(1,1),
(1,2),
(1,3),
(2,4),
(2,5);

-- =====================================
-- Use Relation
-- Dataset ↔ Experiment
-- =====================================

INSERT INTO use_relation(dataset_id, experiment_id)
VALUES

-- Experiment 1
(1,1),

-- Experiment 2
(1,2),
(2,2),

-- Experiment 3
(1,3),
(3,3),

-- Experiment 4
(4,4),

-- Experiment 5
(4,5),
(5,5),
(6,5),
(7,5);

-- =====================================
-- Choose Relation
-- Model ↔ Experiment
-- =====================================

INSERT INTO choose_relation(model_id, experiment_id)
VALUES

-- Exp1
(1,1),

-- Exp2
(3,2),

-- Exp3
(4,3),

-- Exp4
(5,4),

-- Exp5
(5,5),
(6,5);

-- =====================================
-- Belong To
-- Tag ↔ Experiment
-- =====================================

INSERT INTO belong_to(tag_id, experiment_id)
VALUES
(1,1),

(2,2),

(2,3),
(3,3),

(4,4),

(3,5),
(4,5),
(5,5);

-- =====================================
-- Result
-- =====================================

INSERT INTO result
(experiment_id, metric_name, metric_value, record_time)
VALUES

-- Experiment 1
(1,'Accuracy',0.842,'2025-03-06'),
(1,'F1',0.831,'2025-03-06'),

-- Experiment 2
(2,'Accuracy',0.891,'2025-03-16'),
(2,'F1',0.882,'2025-03-16'),

-- Experiment 3
(3,'Accuracy',0.903,'2025-04-02'),
(3,'F1',0.895,'2025-04-02'),

-- Experiment 4
(4,'mAP50',0.527,'2025-04-11'),
(4,'FPS',87.0,'2025-04-11'),

-- Experiment 5
(5,'YOLOv11_mAP50',0.541,'2025-04-21'),
(5,'RTDETR_mAP50',0.558,'2025-04-21');

