from numpy import array
from pandas import read_csv
from engine.executer import init_spark, train_model
from json import dumps, loads
from db_connection import redis_db_connection
from time import sleep
import engine.provenance as provenance
import collections
import os

redis_db = redis_db_connection()
spark_context = init_spark()

EXPERIMENT_PREFIX = 'EXPERIMENT_'
EXPERIMENT_STATUS = 'EXPERIMENT_STATUS'
TASK_QUEUE_PREFIX = 'TASK_QUEUE_'
EXECUTION_QUEUE_PREFIX = 'EXECUTION_QUEUE_'
DONE_QUEUE_PREFIX = 'DONE_QUEUE_'

EXPERIMENT_ID = 'EXPERIMENT_ID'
BLOCK_ID = 'BLOCK_ID'

WAITING = -1
EXECUTING = 1
DONE = 0

STARTED = 0
ENDED = 1

DATASET_SOURCE = os.path.join('dataset','pima-indians-diabetes.data.txt')

OPTIMIZER = 'optimizer'
INIT_MODE = 'init_mode'
BATCH_SIZE = 'batch_size'
EPOCHS = 'epochs'
LEARN_RATE = 'learn_rate'
MOMENTUM = 'momentum'

PARAMETERS_DICT = collections.OrderedDict(
    optimizer = ['Adam', 'Adamax'],
    init_mode = ['uniform'],
    batch_size =  [10],
    epochs = [10],
    learn_rate = [0.1, 0.2, 0.3],
    momentum = [0.1, 0.2, 0.3])


def read_dataset():
    df = read_csv(DATASET_SOURCE, sep=',', index_col=None, header=None)
    X = array(df.iloc[:,0:-1])
    y = array(df.iloc[:,-1])
    return X, y


def dict_to_json(_dict):
    return dumps(_dict)


def json_to_dict(_json):
    return loads(_json)


def get_task_queue_key():
    experiment_id = get_experiment_id()
    return TASK_QUEUE_PREFIX + str(experiment_id)


def get_execution_queue_key():
    experiment_id = get_experiment_id()
    return EXECUTION_QUEUE_PREFIX + str(experiment_id)


def get_done_queue_key():
    experiment_id = get_experiment_id()
    return DONE_QUEUE_PREFIX + str(experiment_id)


def queue_not_empty(queue_key):

    queue_len = redis_db.llen(queue_key)

    if queue_len is None:
        return False
    elif queue_len > 0:
        return True
    else:
        return False


def get_chunks(l, n):

    if l is None:
        return []
    elif len(l) <= n:
        return [l]
    else:
        return [l[i:i + n] for i in range(0, len(l), n)]


def build_hyperparameters_list(hyparameter_dict, split_size):

    optimizer_list = hyparameter_dict[OPTIMIZER]
    init_mode_list = hyparameter_dict[INIT_MODE]

    batch_size_list = get_chunks(hyparameter_dict[BATCH_SIZE], split_size)
    epoch_list = get_chunks(hyparameter_dict[EPOCHS], split_size)
    learn_rate_list = get_chunks(hyparameter_dict[LEARN_RATE], split_size)
    momentum_list = get_chunks(hyparameter_dict[MOMENTUM], split_size)

    blocks = list()

    for optimizer in optimizer_list:
        for init_mode in init_mode_list:
            for batch_size in batch_size_list:
                for epoch in epoch_list:
                    for learn_rate in learn_rate_list:
                        for momentum in momentum_list:

                            block = {}
                            block[OPTIMIZER] = [optimizer]
                            block[INIT_MODE] = [init_mode]
                            block[BATCH_SIZE] = batch_size
                            block[EPOCHS] = epoch
                            block[LEARN_RATE] = learn_rate
                            block[MOMENTUM] = momentum

                            blocks.append(block)

    return blocks


def increment_experiment_id():

    experiment_id = redis_db.get(EXPERIMENT_ID)

    if experiment_id is not None:
        experiment_id = int(experiment_id) + 1
        redis_db.set(EXPERIMENT_ID, experiment_id)
        return experiment_id
    else:
        experiment_id = 0
        redis_db.set(EXPERIMENT_ID, experiment_id)
        return experiment_id


def increment_block_id():

    block_id = redis_db.get(BLOCK_ID)

    if block_id is not None:
        block_id = int(block_id) + 1
        redis_db.set(BLOCK_ID, block_id)
        return block_id
    else:
        block_id = 0
        redis_db.set(BLOCK_ID, block_id)
        return block_id


def get_experiment_id():
    experiment_id = redis_db.get(EXPERIMENT_ID)
    return experiment_id


def get_block_id():
    block_id = redis_db.get(BLOCK_ID)
    return block_id

def get_block_size(block):

    block_size = 1

    for parameter_list in block.values():
        if isinstance(parameter_list, list) and len(parameter_list) > 1:
            block_size = block_size * len(parameter_list)

    return block_size


def reset_block_count():
    redis_db.delete(BLOCK_ID)


def create_block(hyperparameters_dict):

    block_id = increment_block_id()
    block_size = get_block_size(hyperparameters_dict)

    block = dict(
        block_id = block_id,
        hyperparameters = hyperparameters_dict,
        block_size = block_size
    )

    block = dict_to_json(block)

    experiment_id = get_experiment_id()
    provenance.persist_block(block_id, experiment_id)

    return block


def get_block_index_by_id(block_id, task_list):
    for index, block in enumerate(task_list):
        block_dict = json_to_dict(block)
        if block_dict['block_id'] == block_id:
            return index
    return None

def move_task_up(block_id):

    task_queue_key = get_task_queue_key()

    task_list = get_task_queue()
    redis_db.delete(task_queue_key)
    task_list.reverse()

    block_index = get_block_index_by_id(block_id, task_list)

    if block_index is None:
        redis_db.lpush(task_queue_key, *task_list)
        raise ValueError('Coordinator: block_id not in task_queue')
    elif block_index == 0:
        redis_db.lpush(task_queue_key, *task_list)
        raise ValueError('Coordinator: block_id already in the top')
    else:

        task_list[block_index], task_list[block_index-1] = task_list[block_index-1], task_list[block_index]
        redis_db.lpush(task_queue_key, *task_list)
        experiment_id = get_experiment_id()
        provenance.persist_change(block_id, experiment_id, "move_up", block_index, block_index-1)


def move_task_down(block_id):

    task_queue_key = get_task_queue_key()

    task_list = get_task_queue()
    redis_db.delete(task_queue_key)
    task_list.reverse()

    block_index = get_block_index_by_id(block_id, task_list)

    if block_index is None:
        redis_db.lpush(task_queue_key, *task_list)
        raise ValueError('Coordinator: block_id not in task_queue')
    elif block_index == len(task_list)-1:
        redis_db.lpush(task_queue_key, *task_list)
        raise ValueError('Coordinator: block_id already in the bottom')
    else:
        task_list[block_index], task_list[block_index+1] = task_list[block_index+1], task_list[block_index]
        redis_db.lpush(task_queue_key, *task_list)
        experiment_id = get_experiment_id()
        provenance.persist_change(block_id, experiment_id, "move_down", block_index, block_index + 1)


def get_task_queue():
    task_queue_key = get_task_queue_key()
    task_queue = redis_db.lrange(task_queue_key, 0, -1)
    if task_queue is None:
        return []
    else:
        return task_queue


def remove_block_from_queue(block_id):

    task_queue_key = get_task_queue_key()

    task_list = get_task_queue()
    redis_db.delete(task_queue_key)

    block_index = get_block_index_by_id(block_id, task_list)

    if block_index is None:
        redis_db.lpush(task_queue_key, *task_list)
        raise ValueError('Coordinator: block_id not in task_queue')
    else:
        del task_list[block_index]
        redis_db.lpush(task_queue_key, *task_list)


def get_execution_queue():
    execution_queue_key = get_execution_queue_key()
    executing_queue = redis_db.lrange(execution_queue_key, 0, -1)
    if executing_queue is None:
        return []
    else:
        return executing_queue


def get_done_queue():
    done_queue_key = get_done_queue_key()
    done_queue = redis_db.lrange(done_queue_key, 0, -1)
    if done_queue is None:
        return []
    else:
        return done_queue


def add_block_to_queue(hyperparameters_dict):

    task_queue_key = get_task_queue_key()
    block = create_block(hyperparameters_dict)
    redis_db.lpush(task_queue_key, block)

def add_blocks_to_queue(hyperparameters_dict, split_size=2):

    task_queue_key = get_task_queue_key()

    hyperparameters_list = build_hyperparameters_list(hyperparameters_dict, split_size)

    for hyperparameters in hyperparameters_list:

        block = create_block(hyperparameters)
        redis_db.lpush(task_queue_key, block)


def set_experiment_status(status):
    redis_db.set(EXPERIMENT_STATUS, status)


def get_experiment_status():
    experiment_status = redis_db.get(EXPERIMENT_STATUS)
    experiment_status = int(experiment_status)
    return experiment_status


def experiment_not_ended():
    experiment_status = get_experiment_status()
    return experiment_status == STARTED


def move_task_to_excuting_queue():

    task_queue_key = get_task_queue_key()
    executing_queue_key = get_execution_queue_key()

    block = redis_db.brpoplpush(task_queue_key, executing_queue_key)
    block = json_to_dict(block)

    return block


def finalize_task(results):

    executing_queue_key = get_execution_queue_key()
    done_queue_key = get_done_queue_key()

    block = redis_db.rpop(executing_queue_key)
    block = json_to_dict(block)

    hyperparameters_list = results.cv_results_['params']
    cv_score_list = list(results.cv_results_['mean_test_score'])

    results_dict = dict(
        hyperparameters = hyperparameters_list,
        score = cv_score_list
    )

    block['results'] = results_dict

    block = dict_to_json(block)

    redis_db.lpush(done_queue_key, block)


def execute_task():

    block = move_task_to_excuting_queue()

    hyperparameters = block['hyperparameters']

    block_id = get_block_id()
    experiment_id = get_experiment_id()
    provenance.persist_hyperparameter_combination(block_id, experiment_id, hyperparameters)

    X, y = read_dataset()

    results = train_model(X, y, hyperparameters, spark_context)

    provenance.persist_hyperparameter_result(block_id, experiment_id, results.cv_results_)

    finalize_task(results)


def cosume_task_queue():
    while experiment_not_ended():
        executing_queue_key = get_execution_queue_key()
        task_queue_key = get_task_queue_key()
        if not queue_not_empty(executing_queue_key) and queue_not_empty(task_queue_key):
            execute_task()
        else:
            sleep(5)


def create_experiment():
    increment_experiment_id()
    experiment_id = get_experiment_id()
    provenance.persist_experiment(experiment_id)
    set_experiment_status(STARTED)
    reset_block_count()
    cosume_task_queue()


def finalize_or_abort_experiment():
    set_experiment_status(ENDED)
    reset_block_count()
    executing_queue_key = get_execution_queue_key()
    task_queue_key = get_task_queue_key()
    redis_db.delete(task_queue_key)
    redis_db.delete(executing_queue_key)
    experiment_id = get_experiment_id()
    provenance.update_experiment(experiment_id)