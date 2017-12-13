import collections

blocksData = [{
    'block_id': 10,
    'labels': ['epocas: 5, bath:30, ...', 'epocas: 98, bath: bla, ...'],
    'accuracy': [0.456, 0.98],
    'status': 1,
  }, {
    'block_id': 13,
    'labels': ['epocas: 5, bath:30, ...', 'epocas: 98, bath: bla, ...'],
    'accuracy': [0.456, 0.98],
    'status': 1,
  }, {
    'block_id': 23,
    'labels': ['epocas: 5, bath:30, ...', 'epocas: 98, bath: bla, ...'],
    'accuracy': [0.456, 0.98],
    'status': 1,
  }, {
    'block_id': 33,
    'labels': ['epocas: 5, bath:30, ...', 'epocas: 98, bath: bla, ...'],
    'accuracy': [0.456, 0.98],
    'status': 1,
  }, {
    'block_id': 43,
    'labels': ['epocas: 5, bath:30, ...', 'epocas: 98, bath: bla, ...'],
    'accuracy': [0.456, 0.98],
    'status': 1,
  }, {
    'block_id': 53,
    'labels': ['epocas: 5, bath:30, ...', 'epocas: 98, bath: bla, ...'],
    'accuracy': [0.456, 0.98],
    'status': 1,
  }, {
    'block_id': 63,
    'labels': ['epocas: 5, bath:30, ...', 'epocas: 98, bath: bla, ...'],
    'accuracy': [0.456, 0.98],
    'status': 1,
  }, {
    'block_id': 73,
    'labels': ['epocas: 5, bath:30, ...', 'epocas: 98, bath: bla, ...'],
    'accuracy': [0.456, 0.98],
    'status': 1,
  }, {
    'block_id': 83,
    'labels': ['epocas: 5, bath:30, ...', 'epocas: 98, bath: bla, ...'],
    'accuracy': [0.456, 0.98],
    'status': 1,
  }, {
    'block_id': 93,
    'labels': ['epocas: 5, bath:30, ...', 'epocas: 98, bath: bla, ...'],
    'accuracy': [0.456, 0.98],
    'status': 1,
  }, {
    'block_id': 433,
    'labels': ['epocas: 5, bath:30, ...', 'epocas: 98, bath: bla, ...'],
    'accuracy': [0.456, 0.98],
    'status': 1,
  }, {
    'block_id': 343,
    'labels': ['epocas: 5, bath:30, ...', 'epocas: 98, bath: bla, ...'],
    'accuracy': [0.456, 0.98],
    'status': 1,
  }, {
    'block_id': 3,
    'labels': ['epocas: 5, bath:30, ...', 'epocas: 98, bath: bla, ...'],
    'accuracy': [0.456, 0.98],
    'status': 1,
  }, {
    'block_id': 235,
    'labels': ['epocas: 5, bath:30, ...', 'epocas: 98, bath: bla, ...'],
    'accuracy': [0.456, 0.98],
    'status': 1,
  }, {
    'block_id': 3,
    'labels': ['epocas: 5, bath:30, ...', 'epocas: 98, bath: bla, ...'],
    'accuracy': [0.766, 0.65],
    'status': 1,
  }, {
    'block_id': 2,
    'status': 0,
  }, {
    'block_id': 0,
    'status': -1,
  }]


block = dict(
     	block_id=0,
     	hyperparameters=[collections.OrderedDict(
 		    optimizer = 'Adam',
 		    init_mode = 'uniform',
 		    batch_size =  10,
 		    epochs = 10,
 		    learn_rate = 0.1,
 		    momentum = 0.1), collections.OrderedDict(
 		    optimizer = 'Adam',
 		    init_mode = 'uniform',
 		    batch_size =  10,
 		    epochs = 10,
 		    learn_rate = 0.1,
 		    momentum = 0.1)],#,...
     	results=[0.6, 1.3],
     	status=1
     	)

block_final = dict(
     	block_id=0,
 	    hyperparameters=0,
 		results =dict(
 			hyperparameters=[collections.OrderedDict(
 			    optimizer = 'Adam',
 			    init_mode = 'uniform',
 			    batch_size =  10,
 			    epochs = 10,
 			    learn_rate = 0.1,
 			    momentum = 0.1), collections.OrderedDict(
 			    optimizer = 'Adam',
 			    init_mode = 'uniform',
 			    batch_size =  10,
 			    epochs = 10,
 			    learn_rate = 0.1,
 			    momentum = 0.1)],#,...
     		score=[0.6, 1.3])
 		)
