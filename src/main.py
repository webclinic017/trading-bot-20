import logging
from typing import Dict, List, Tuple, Any

from flask import render_template, jsonify, make_response, request

from src import app, db
from src.constants import TARGET, ARGS
from src.dao.evaluation_dao import EvaluationDAO
from src.dao.forward_dao import ForwardDAO
from src.dao.intraday_dao import IntradayDAO
from src.dao.stock_dao import StockDAO
from src.entity.intraday_entity import IntradayEntity
from src.forward import Forward
from src.optimizer import Optimizer
from src.portfolio import Portfolio
from src.process_manager import ProcessManager

process_manager: ProcessManager = ProcessManager()
processes: Dict[str, Dict[str, Tuple[Any, ...]]] = {
    'update-table-stock': {
        TARGET: StockDAO.update,
        ARGS: Portfolio.test_prod_portfolio()
    },
    'update-table-intraday': {
        TARGET: IntradayDAO.update,
        ARGS: Portfolio.test_prod_portfolio()
    },
    'optimize': {
        TARGET: Optimizer.start,
        ARGS: (Portfolio.test_portfolio(), 100, 4)
    },
    'forward': {
        TARGET: Forward.start,
        ARGS: []
    }
}


@app.before_first_request
def create_all() -> None:
    db.create_all()


@app.route('/')
def main_view() -> str:
    return render_template('index.html')


@app.route('/stock')
def stock_view() -> str:
    return render_template('stock.html', stocks=StockDAO.read_all())


@app.route('/intraday')
def intraday_view() -> str:
    return render_template('intraday.html', tables=[IntradayDAO.dataframe_ticker().to_html(classes='data',
                                                                                           header='true')])


@app.route('/evaluation')
def evaluation_view() -> str:
    return render_template('evaluation.html', evaluations=EvaluationDAO.read_all())


@app.route('/forward')
def forward_view() -> str:
    inventory, cash = Forward.init()
    inventory, total_value, total = Forward.update(inventory, cash)
    return render_template('forward.html', forwards=ForwardDAO.read_all(), inventory=inventory, cash=cash,
                           total_value=total_value, total=total)


@app.route('/stock/intraday/<ticker>')
def stock_intraday_view(ticker: str) -> str:
    return render_template('stock-intraday.html', intradays=IntradayDAO.read_filter_by_ticker(ticker))


@app.route('/process')
def process_view() -> str:
    active_processes: List[str] = list(map(lambda j: j.name, process_manager.get_processes()))
    inactive_processes: List[str] = list(filter(lambda j: j not in active_processes, processes.keys()))
    return render_template('process.html', running=process_manager.running(), active_processes=active_processes,
                           inactive_processes=inactive_processes)


@app.route('/process/start/<process_name>')
def process_start_view(process_name: str) -> str:
    process: Dict[str, Tuple[Any, ...]] = processes.get(process_name)
    if process is not None and not process_manager.contains(process_name):
        process_manager.start(process_name, process.get(TARGET), process.get(ARGS))
    return render_template('process-start.html', process_name=process_name)


@app.route('/process/stop/<process_name>')
def process_stop_view(process_name: str) -> str:
    process_manager.stop(process_name)
    return render_template('process-stop.html', process_name=process_name)


@app.route('/import', defaults={'data': ''})
@app.route('/import/<path:data>', methods=['GET', 'POST'])
def import_view(data: str) -> str:
    if data == 'intraday':
        IntradayDAO.create_from_file(request.files['file'])
    return render_template('import.html')


@app.route('/export', defaults={'data': ''})
@app.route('/export/<path:data>')
def export_view(data: str) -> str:
    if data == 'intraday':
        rows: List[IntradayEntity] = IntradayDAO.read_order_by_date_asc()
        rows_dict: List[Dict[str, str]] = list(
            map(lambda row: dict(filter(lambda e: not e[0].startswith('_'), row.__dict__.items())), rows))
        return make_response(jsonify(rows_dict), 200)
    return render_template('export.html')


@app.errorhandler(500)
def server_error(e: exec) -> Tuple[str, int]:
    logging.exception('An error occurred during a request.')
    return '''
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    '''.format(e), 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
