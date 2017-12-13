from .decorators import async_process, async_thread
from engine import coordinator
from numpy import arange
import collections
from db_connection import rdb
from engine.coordinator import WAITING, EXECUTING, DONE

#-------------------------------------------------------------------------------

def get_discrete_parameter(parameter):

    if isinstance(parameter, list):
        return parameter
    else:
        return [parameter]


def get_continuous_parameter(parameter):

    if isinstance(parameter, tuple):

        start = parameter[0]
        stop = parameter[1]
        step = parameter[2]

        return arange(start, stop, step).tolist()
    else:
        return [parameter]

@async_process  ## isso executa em um processo novo no servidor
def start_experiment():
    '''
    atualiza o controle interno de multiplos experimentos e inicia a execução
    '''
    coordinator.create_experiment()

def finalize_or_abort_experiment():
    '''
    atualiza o controle interno de multiplos experimentos e indica que a execução foi concluída normalmente ou interrompe forçadamente a execução
    '''
    coordinator.finalize_or_abort_experiment()

def is_experiment_active():
    if coordinator.get_experiment_status() == 0:
        return True
    else:
        return False

#-------------------------------------------------------------------------------

def remove_block(block_id):
    coordinator.remove_block_from_queue(block_id)

def move_block_up(block_id):
    coordinator.move_task_up(block_id)

def move_block_down(block_id):
    coordinator.move_task_down(block_id)

def add_blocks_to_queue(PARAMETERS_DICT, split_size=None, batchMode=True):
    '''
    recebe um PARAMETERS_DICT e o utiliza para criar um ÚNICO bloco, caso batchMode=False
    ou multiplos blocos de tamanho médio (numero de combinações distintas dentro dele) igual ao valor informado em "mean size", caso batchMode=True
    '''

    hyperparameters_dict = dict(
	    optimizer=get_discrete_parameter(PARAMETERS_DICT['optimizer']),
	    init_mode=get_discrete_parameter(PARAMETERS_DICT['init_mode']),
	    batch_size=get_continuous_parameter(PARAMETERS_DICT['batch_size']),
	    epochs=get_continuous_parameter(PARAMETERS_DICT['epochs']),
	    learn_rate=get_continuous_parameter(PARAMETERS_DICT['learn_rate']),
	    momentum=get_continuous_parameter(PARAMETERS_DICT['momentum']),
        n_neurons_per_layer=PARAMETERS_DICT['n_neurons_per_layer']
    )

    if split_size is not None and batchMode:
        coordinator.add_blocks_to_queue(hyperparameters_dict, split_size=split_size)
    else:
        coordinator.add_block_to_queue(hyperparameters_dict)


def get_blocks(task_id=None):
    '''
    retorna um array de objetos com os detalhes de cada block, em qualquer ordem, para a task_id passada
    ou para mais recente se nenhuma for passado
    '''
    pass

def get_queue(task_id=None):
    '''
    retorna um array de objetos com os detalhes de cada block incluindo o status de execução (executando, a executar, já executado), na ordem em que serão executados, para a task_id passada
    ou para mais recente se nenhuma for passado
    '''

    queue_list = []

    for block in coordinator.get_task_queue():
        block_dict = coordinator.json_to_dict(block)
        block_view = dict(
            block_id = block_dict['block_id'],
            status = coordinator.WAITING,
            block_size = block_dict['block_size']
        )
        queue_list.append(block_view)

    for block in coordinator.get_execution_queue():
        block_dict = coordinator.json_to_dict(block)
        block_view = dict(
            block_id = block_dict['block_id'],
            status = coordinator.EXECUTING,
            block_size = block_dict['block_size']
        )
        queue_list.append(block_view)

    for block in coordinator.get_done_queue():
        block_dict = coordinator.json_to_dict(block)
        block_view = get_block_view(block_dict)
        queue_list.append(block_view)

    queue_list.reverse()

    return queue_list


def get_legend(hyperparameters_list):

    legend_list = []

    for hyperparameters_dict in hyperparameters_list:

        item_list = []

        for label, value in hyperparameters_dict.items():
            #print(key)
            item = str(label)+': '+str(value)
            item_list.append(item)

        legend = ', '.join(item_list)
        legend_list.append(legend)

    return legend_list


def get_block_view(block_dict):
    results_dict = block_dict['results']
    block_view =collections.OrderedDict(
        block_id = block_dict['block_id'],
        labels = get_legend(results_dict['hyperparameters']),
        accuracy = results_dict['score'],
        status = coordinator.DONE,
        block_size = block_dict['block_size']
        )
    return block_view

def get_blocks_results(task_id=None):
    '''
    retorna um array de objetos com os detalhes de cada block já executado com o resultado, na ordem em que foram executados, para a task_id passada
    ou para mais recente se nenhuma for passado
    '''

    experiment_id = coordinator.get_experiment_id()
    block_data = list()

    for block in coordinator.get_done_queue():
        block_dict = coordinator.json_to_dict(block)
        block_view = get_block_view(block_dict)
        block_data.append(block_view)

    block_data.reverse()

    result_dict = dict(
        experiment_id= experiment_id,
        block_data= block_data
    )

    return result_dict



#-------------------------------------------------------------------------------

def get_queue_data_as_table():
    blocksData = get_queue()

    # import mock_data
    # blocksData = mock_data.blocksData

    queueData = list()

    i = 1

    for blockData in blocksData:
        blockQueueData = list()

        blockQueueData.append(i)
        i+=1

        blockQueueData.append(blockData['block_id'])
        blockQueueData.append(blockData['block_size'])

        if 'accuracy' in blockData:
            idx = blockData['accuracy'].index(max(blockData['accuracy']))
            blockQueueData.append(blockData['accuracy'][idx])
        else:
            blockQueueData.append(' - ');

        if blockData['status'] == EXECUTING:
            blockQueueData.append(' Running ')
        elif blockData['status'] == DONE:
            blockQueueData.append(' Ready ')
        else:
            blockQueueData.append(' Waiting ')

        blockQueueData.append('')

        queueData.append(blockQueueData)

    result_dict = dict(
        experiment_id = coordinator.get_experiment_id(),
        data = queueData
    )

    return result_dict
