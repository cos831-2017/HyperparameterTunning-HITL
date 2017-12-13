DROP TABLE IF EXISTS hpc_result;
DROP TABLE IF EXISTS rel_hpc_hp;
DROP TABLE IF EXISTS change_variation;

DROP TABLE IF EXISTS hyperparameter_variation;
DROP TABLE IF EXISTS hyperparameter_combination;
DROP TABLE IF EXISTS hyperparameter;

DROP TABLE IF EXISTS change_priority;
DROP TABLE IF EXISTS user_Activity;

DROP TABLE IF EXISTS block;
DROP TABLE IF EXISTS task;
DROP TABLE IF EXISTS experiment;

CREATE TABLE experiment( --dominio
	experiment_id INTEGER PRIMARY KEY,
	date_start TIMESTAMP DEFAULT NOW,
	date_finish TIMESTAMP
);

CREATE TABLE task( --dominio
	task_id INTEGER,
	experiment_id INTEGER,
	priority INTEGER,
	status VARCHAR(30),
	PRIMARY KEY(task_id, experiment_id),
	FOREIGN KEY(experiment_id) REFERENCES experiment(experiment_id)
);


CREATE TABLE user_activity( --adapatação
	ua_id SERIAL,
	date_activity TIMESTAMP DEFAULT NOW,
	type_activity VARCHAR(10)
);

CREATE TABLE change_priority( --adapatação
	task_id INTEGER,
	experiment_id INTEGER,
	ua_id INTEGER,
	new_priority INTEGER,
	old_priority INTEGER,
	FOREIGN KEY(task_id, experiment_id) REFERENCES task(task_id, experiment_id),
	FOREIGN KEY(ua_id) REFERENCES user_activity(ua_id)
);

CREATE TABLE hyperparameter( --dominio
	hp_id SERIAL,
	name VARCHAR(50)
);

INSERT INTO hyperparameter (name) values ('optimizer'); 
INSERT INTO hyperparameter (name) values ('init_mode');
INSERT INTO hyperparameter (name) values ('batch_size');
INSERT INTO hyperparameter (name) values ('epochs');
INSERT INTO hyperparameter (name) values ('learn_rate');
INSERT INTO hyperparameter (name) values ('momentum');


CREATE TABLE hyperparameter_combination( --dominio
	hpc_id SERIAL,
	date_execution TIMESTAMP DEFAULT NOW,
	task_id INTEGER,
	experiment_id INTEGER,
	FOREIGN KEY(task_id, experiment_id) REFERENCES task(task_id, experiment_id)
);

CREATE TABLE hyperparameter_variation( --dominio
	hpv_id SERIAL,
	init_mode VARCHAR(50),
	optimizer VARCHAR(50),
	start_value REAL,
	end_value REAL,
	step_value REAL,
	hpc_id INTEGER,
	hp_id INTEGER,
	task_id INTEGER,
	experiment_id INTEGER,
	FOREIGN KEY(task_id, experiment_id) REFERENCES task(task_id, experiment_id),
	FOREIGN KEY(hp_id) REFERENCES hyperparameter(hp_id),
	FOREIGN KEY(hpc_id) REFERENCES hyperparameter_combination(hpc_id)
);

---CREATE TABLE change_variation( --adapatação
---	ua_id INTEGER,
---	hpv_old INTEGER,
---	hpv_new INTEGER,
--	FOREIGN KEY(hpv_old) REFERENCES hyperparameter_variation(hpv_id),
--	FOREIGN KEY(hpv_new) REFERENCES hyperparameter_variation(hpv_id)
--);

CREATE TABLE rel_hpc_hp( --dominio
	hp_id INTEGER,
	hpc_id INTEGER,	
	value VARCHAR(20),
	FOREIGN KEY(hp_id) REFERENCES hyperparameter(hp_id),
	FOREIGN KEY(hpc_id) REFERENCES hyperparameter_combination(hpc_id)
);

CREATE TABLE hpc_result( --dominio
	hpc_id INTEGER,
	AUC REAL,
	accuracy REAL,
	precision REAL,
	recall REAL,
	f1_score INTEGER,
	FOREIGN KEY(hpc_id) REFERENCES hyperparameter_combination(hpc_id)
);
