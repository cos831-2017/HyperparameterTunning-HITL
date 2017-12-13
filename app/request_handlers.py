from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
# from flask_login import login_user, logout_user, current_user, login_required
from app import app
from .forms import HyperparameterSettingForm

from app import engine_interface

### - Views ------------------------------------------------------------------------

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard_view():
    return render_template('view/dashboard_view.html', is_experiment_active=engine_interface.is_experiment_active())

@app.route('/dashboard/start', methods=['GET'])
def dashboard_view_start():
    start_experiment()
    flash("Experiment started!")
    return redirect(url_for('dashboard_view'))

@app.route('/dashboard/finalizeorabort', methods=['GET'])
def dashboard_view_abort():
    abort_experiment()
    flash("Experiment aborted!")
    return redirect(url_for('dashboard_view'))

@app.route('/addblocks', methods=['GET', 'POST'])
def add_blocks_view():
    if not engine_interface.is_experiment_active():
        return redirect(url_for('dashboard_view'))

    form = HyperparameterSettingForm()

    if form.validate_on_submit():

        PARAMETERS_DICT = dict(
            optimizer=form.optimizer.getData(),
            init_mode=form.init_mode.getData(),
            batch_size=form.batch.getData(),
            epochs=form.epoch.getData(),
            learn_rate=form.learn_rate.getData(),
            momentum=form.momentum.getData(),
            n_neurons_per_layer=[[12,8,8,8,8,8]])

        engine_interface.add_blocks_to_queue(PARAMETERS_DICT, split_size=form.split_size.data, batchMode=form.batchMode())

        if form.batchMode():
            flash("Batch of blocks added")
        else:
            flash("Sigle block added")

        return redirect(url_for('execution_queue_view'))

    return render_template('view/add_blocks_view.html', form=form, is_experiment_active=engine_interface.is_experiment_active())

@app.route('/executionqueue', methods=['GET'])
def execution_queue_view():
    if not engine_interface.is_experiment_active():
        return redirect(url_for('dashboard_view'))

    return render_template('view/execution_queue_view.html', is_experiment_active=engine_interface.is_experiment_active())


@app.route('/results', methods=['GET'])
def results_view():
    if not engine_interface.is_experiment_active():
        return redirect(url_for('dashboard_view'))

    return render_template('view/results_view.html', is_experiment_active=engine_interface.is_experiment_active())

### -----------------------------------------------------------------------------

### - Ajax ------------------------------------------------------------------------

@app.route('/startexperiment', methods=['GET'])
def start_experiment():
    engine_interface.start_experiment()
    return jsonify({"status":"success"})

@app.route('/finalizeorabortexperiment', methods=['GET'])
def abort_experiment():
    engine_interface.finalize_or_abort_experiment()
    return jsonify({"status":"success"})

@app.route('/moveup/<int:experiment_id>/<int:block_id>', methods=['GET'])
@app.route('/moveup/<int:block_id>', methods=['GET'])
def move_block_up(experiment_id=None,block_id=None):
    if not engine_interface.is_experiment_active():
        return jsonify({"status":"error"})

    engine_interface.move_block_up(block_id)
    return jsonify({"status":"success"})

@app.route('/movedown/<int:experiment_id>/<int:block_id>', methods=['GET'])
@app.route('/movedown/<int:block_id>', methods=['GET'])
def move_block_down(experiment_id=None,block_id=None):
    if not engine_interface.is_experiment_active():
        return jsonify({"status":"error"})

    engine_interface.move_block_down(block_id)
    return jsonify({"status":"success"})

@app.route('/removeblock/<int:experiment_id>/<int:block_id>', methods=['GET'])
@app.route('/removeblock/<int:block_id>', methods=['GET'])
def remove_block(experiment_id=None,block_id=None):
    if not engine_interface.is_experiment_active():
        return jsonify({"status":"error"})

    engine_interface.remove_block(block_id)
    return jsonify({"status":"success"})

@app.route('/blocks/<int:experiment_id>', methods=['GET'])
@app.route('/blocks', methods=['GET'])
def blocks(experiment_id=None):
    if not engine_interface.is_experiment_active():
        return jsonify({"status":"error"})

    blocks = engine_interface.get_blocks()

    if blocks is not None:
        d = blocks
    else:
        d = {}

    return jsonify(d)

@app.route('/blockresults/<int:experiment_id>', methods=['GET'])
@app.route('/blockresults', methods=['GET'])
def block_results(experiment_id=None):
    if not engine_interface.is_experiment_active():
        return jsonify({"status":"error"})

    results = engine_interface.get_blocks_results()

    if results is not None:
        d = results
    else:
        d = {}

    return jsonify(d)

@app.route('/blockqueue/<int:experiment_id>', methods=['GET'])
@app.route('/blockqueue', methods=['GET'])
def block_queue(experiment_id=None):
    if not engine_interface.is_experiment_active():
        return jsonify({"status":"error"})

    queue = engine_interface.get_queue_data_as_table()

    if queue is not None:
        d = queue
    else:
        d = {}

    return jsonify(d)

### -----------------------------------------------------------------------------

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html', is_experiment_active=engine_interface.is_experiment_active()), 404


@app.errorhandler(500)
def internal_error(error):
    # db.session.rollback()
    return render_template('500.html', is_experiment_active=engine_interface.is_experiment_active()), 500
