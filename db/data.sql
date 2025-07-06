-- Insert Objectives
INSERT INTO objectives (name, description, progress) VALUES
('Training Program', 'Complete a 12-week training program to improve fitness.', 40),
('Weight Loss Goal', 'Lose 10 kilograms in 3 months through diet and exercise.', 60);

-- Insert Key Results for Training Program
INSERT INTO key_results (objective_id, description, progress, metric) VALUES
(1, 'Attend 3 training sessions per week', 50, 'Sessions per week'),
(1, 'Increase bench press weight by 20%', 30, 'Weight increase'),
(1, 'Run 5 kilometers in under 30 minutes', 40, 'Time in minutes');

-- Insert Key Results for Weight Loss Goal
INSERT INTO key_results (objective_id, description, progress, metric) VALUES
(2, 'Reduce daily calorie intake to 1800 calories', 70, 'Calories per day'),
(2, 'Exercise 5 times per week', 60, 'Sessions per week'),
(2, 'Drink 2 liters of water daily', 80, 'Liters per day');
