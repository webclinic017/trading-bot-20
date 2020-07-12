import logging
from typing import Tuple

from flask import render_template, make_response, request, jsonify

from src import app, db
from src.bo.forward_bo import ForwardBO
from src.bo.intraday_bo import IntradayBO
from src.dao.evaluation_dao import EvaluationDAO
from src.dao.forward_dao import ForwardDAO
from src.dao.intraday_dao import IntradayDAO
from src.dao.stock_dao import StockDAO
from src.process_manager import ProcessManager

process_manager: ProcessManager = ProcessManager()


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
    inventory, cash = ForwardBO.init()
    inventory, total_value, total = ForwardBO.update(inventory, cash)
    return render_template('forward.html', forwards=ForwardDAO.read_all(), inventory=inventory, cash=cash,
                           total_value=total_value, total=total)


@app.route('/stock/intraday/<ticker>')
def stock_intraday_view(ticker: str) -> str:
    return render_template('stock-intraday.html', intradays=IntradayDAO.read_filter_by_ticker(ticker))


@app.route('/process')
def process_view() -> str:
    return render_template('process.html', running=process_manager.running(),
                           active_processes=process_manager.get_active_names(),
                           inactive_processes=process_manager.get_inactive_names())


@app.route('/process/start/<process_name>')
def process_start_view(process_name: str) -> str:
    successful: bool = process_manager.start(process_name)
    return render_template('process-start.html', successful=successful, process_name=process_name)


@app.route('/process/stop/<process_name>')
def process_stop_view(process_name: str) -> str:
    successful: bool = process_manager.stop(process_name)
    return render_template('process-stop.html', successful=successful, process_name=process_name)


@app.route('/import', defaults={'data': ''})
@app.route('/import/<path:data>', methods=['GET', 'POST'])
def import_view(data: str) -> str:
    if data == 'intraday':
        IntradayBO.from_file(request)
    return render_template('import.html')


@app.route('/export', defaults={'data': ''})
@app.route('/export/<path:data>')
def export_view(data: str) -> str:
    if data == 'intraday':
        content = IntradayBO.to_file()
        return make_response(jsonify(content), 200)
    return render_template('export.html')


@app.errorhandler(404)
def server_error(e: exec) -> Tuple[str, int]:
    logging.exception('An error occurred during a request.')
    return '''
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    '''.format(e), 404


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
