import pymonetdb
from datetime import datetime
from db_connection import monet_db_connection


monetdb_connection = monet_db_connection()
cursor = monetdb_connection.cursor()


def persist_block(block_id, experiment_id):
    cursor.execute("INSERT INTO task(task_id, experiment_id) VALUES ({}, {});".format(block_id, experiment_id))
    cursor.execute("COMMIT;")

def persist_change(block_id, experiment_id, change, old, new):
    sql = "INSERT INTO user_activity(type_activity) VALUES ('{}');".format(change)
    print (str(sql))
    cursor.execute(str(sql))
    cursor.execute("COMMIT;")
    cursor.execute("SELECT max(ua_id) FROM user_activity;")
    id_activity = cursor.fetchone()[0]
    sql = "INSERT INTO change_priority(ua_id, task_id,experiment_id, old_priority, new_priority) VALUES ({},{},{},{}, {});".format(id_activity,
                                                                                                                                   block_id,
                                                                                                                                   experiment_id,
                                                                                                                                   old,
                                                                                                                                   new)
    print(str(sql))
    cursor.execute(str(sql))
    cursor.execute("COMMIT;")


def persist_hyperparameter_result(block_id, experiment_id, results):
    for x, y in zip(results["params"], results["mean_test_score"]):
        sql = "SELECT hpc_id FROM hyperparameter_combination where task_id ={} and experiment_id={};".format(block_id,
                                                                                                        experiment_id)
        print(sql)
        cursor.execute(sql)
        id_combination = cursor.fetchone()[0]
        sql = "INSERT INTO rel_hpc_hp (hp_id, hpc_id, value) VALUES (1,{},'{}');".format(id_combination,x['optimizer'])
        print(sql)
        cursor.execute(sql)
        cursor.execute("COMMIT;")

        sql = "INSERT INTO rel_hpc_hp (hp_id, hpc_id, value) VALUES (2,{},'{}');".format(id_combination, x['init_mode'])
        print(sql)
        cursor.execute(sql)
        cursor.execute("COMMIT;")

        sql = "INSERT INTO rel_hpc_hp (hp_id, hpc_id, value) VALUES (3,{},'{}');".format(id_combination, x['batch_size'])
        print(sql)
        cursor.execute(sql)
        cursor.execute("COMMIT;")

        sql = "INSERT INTO rel_hpc_hp (hp_id, hpc_id, value) VALUES (4,{},'{}');".format(id_combination, x['epochs'])
        print(sql)
        cursor.execute(sql)
        cursor.execute("COMMIT;")

        sql = "INSERT INTO rel_hpc_hp (hp_id, hpc_id, value) VALUES (5,{},'{}');".format(id_combination, x['learn_rate'])
        print(sql)
        cursor.execute(sql)
        cursor.execute("COMMIT;")

        sql = "INSERT INTO rel_hpc_hp (hp_id, hpc_id, value) VALUES (6,{},'{}');".format(id_combination, x['momentum'])
        print(sql)
        cursor.execute(sql)
        cursor.execute("COMMIT;")

        sql = "INSERT INTO hpc_result (hpc_id, accuracy) VALUES ({},{});".format(id_combination, y)
        print(sql)
        cursor.execute(sql)
        cursor.execute("COMMIT;")

def persist_hyperparameter_combination(block_id, experiment_id, hyperparameters):
    sql = "INSERT INTO hyperparameter_combination (task_id, experiment_id) VALUES ({}, {});".format(block_id, experiment_id)
    print(sql)
    cursor.execute(sql)
    cursor.execute("COMMIT;")
    cursor.execute("SELECT max(hpc_id) FROM hyperparameter_combination;")
    id_combination = cursor.fetchone()[0]
    sql = "INSERT INTO hyperparameter_variation (init_mode, hpc_id, hp_id,task_id, experiment_id ) VALUES ('{}',{},2, {}, " \
          "{});".format(str(" ".join(hyperparameters["init_mode"])), id_combination, block_id, experiment_id)
    print(sql)
    cursor.execute(sql)
    cursor.execute("COMMIT;")

    cursor.execute("INSERT INTO hyperparameter_variation (optimizer, hpc_id, hp_id,task_id, experiment_id ) VALUES ('{}',"
                   "{},1, {}, {});".format(str(" ".join(hyperparameters["optimizer"])), id_combination, block_id, experiment_id))
    cursor.execute("COMMIT;")

    if len(hyperparameters["batch_size"])>1:
        sql = "INSERT INTO hyperparameter_variation (start_value, end_value, step_value, hpc_id, hp_id,task_id," \
              "experiment_id ) VALUES ({},{},{},{},3, {}, {});".format(hyperparameters["batch_size"][0],
                                                                    hyperparameters["batch_size"][-1],
                                                                    hyperparameters["batch_size"][1] - hyperparameters["batch_size"][0],
                                                                    id_combination,
                                                                    block_id,
                                                                    experiment_id)
    else:
        sql="INSERT INTO hyperparameter_variation (start_value, end_value, hpc_id, hp_id,task_id, " \
            "experiment_id ) VALUES ({},{},{},3, {}, {});".format(hyperparameters["batch_size"][0],
                                                                    hyperparameters["batch_size"][0],
                                                                    id_combination,
                                                                    block_id,
                                                                    experiment_id)
    cursor.execute(sql)
    cursor.execute("COMMIT;")

    if len(hyperparameters["epochs"])>1:
        sql = "INSERT INTO hyperparameter_variation (start_value, end_value, step_value, hpc_id, hp_id,task_id, " \
           "experiment_id ) VALUES ({},{},{},{},4, {}, {});".format(hyperparameters["epochs"][0],
                                                                        hyperparameters["epochs"][-1],
                                                                        hyperparameters["epochs"][1] - hyperparameters["epochs"][0],
                                                                        id_combination,
                                                                        block_id,
                                                                        experiment_id)

    else:
        sql="INSERT INTO hyperparameter_variation (start_value, end_value, hpc_id, hp_id,task_id, " \
         "experiment_id ) VALUES ({},{},{},4, {}, {});".format(hyperparameters["epochs"][0],
                                                                    hyperparameters["epochs"][0],
                                                                    id_combination,
                                                                    block_id,
                                                                    experiment_id)
    cursor.execute(sql)
    cursor.execute("COMMIT;")

    if len(hyperparameters["learn_rate"]) >1:
        sql = "INSERT INTO hyperparameter_variation (start_value, end_value, step_value, hpc_id, hp_id,task_id, " \
            "experiment_id ) VALUES ({},{},{},{},5, {}, {});".format(hyperparameters["learn_rate"][0],
                                                                    hyperparameters["learn_rate"][-1],
                                                                    hyperparameters["learn_rate"][1] - hyperparameters["learn_rate"][0],
                                                                    id_combination,
                                                                    block_id,
                                                                    experiment_id)

    else:
        sql = "INSERT INTO hyperparameter_variation (start_value, end_value, hpc_id, hp_id,task_id, " \
           "experiment_id ) VALUES ({},{},{},5, {}, {});".format(hyperparameters["learn_rate"][0],
                                                                 hyperparameters["learn_rate"][0],
                                                                 id_combination,
                                                                 block_id,
                                                                 experiment_id)
    cursor.execute(sql)
    cursor.execute("COMMIT;")

    if len(hyperparameters["momentum"])>1:
        sql = "INSERT INTO hyperparameter_variation (start_value, end_value, step_value, hpc_id, hp_id,task_id, " \
           "experiment_id ) VALUES ({},{},{},{},6, {}, {});".format(hyperparameters["momentum"][0],
                                                                    hyperparameters["momentum"][-1],
                                                                    hyperparameters["momentum"][1] - hyperparameters["momentum"][0],
                                                                    id_combination,
                                                                    block_id,
                                                                    experiment_id)

    else:
        sql = "INSERT INTO hyperparameter_variation (start_value, end_value, hpc_id, hp_id,task_id, " \
           "experiment_id ) VALUES ({},{},{},6, {}, {});".format(hyperparameters["momentum"][0],
                                                                 hyperparameters["momentum"][0],
                                                                 id_combination,
                                                                 block_id,
                                                                 experiment_id)
    cursor.execute(sql)
    cursor.execute("COMMIT;")


def persist_experiment(experiment_id):
    cursor.execute("INSERT INTO experiment (experiment_id, date_start) VALUES ({}, '{}');".format(experiment_id,
                                                                                                  datetime.now() ))
    cursor.execute("COMMIT;")


def update_experiment(experiment_id):
    cursor.execute("update experiment set date_finish = '{}' where experiment_id = {};".format(datetime.now(),
                                                                                               experiment_id))
    cursor.execute("COMMIT;")
