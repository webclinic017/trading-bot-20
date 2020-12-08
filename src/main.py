import logging
from typing import List, Any

from flask import render_template, make_response, request, jsonify, redirect, url_for, Response

from src import app, db
from src.bo.configuration_bo import ConfigurationBO
from src.bo.forward_bo import ForwardBO
from src.bo.intraday_bo import IntradayBO
from src.bo.portfolio_bo import PortfolioBO
from src.dao.evaluation_dao import EvaluationDAO
from src.dao.forward_dao import ForwardDAO
from src.dao.intraday_dao import IntradayDAO
from src.dao.stock_dao import StockDAO
from src.entity.configuration_entity import ConfigurationEntity
from src.enums.mode_enum import ModeEnum
from src.form.configuration_field_form import ConfigurationFieldForm
from src.form.configuration_form import ConfigurationForm
from src.form.portfolio_form import PortfolioForm
from src.process_manager import ProcessManager

process_manager: ProcessManager = ProcessManager()
GET = 'GET'
POST = 'POST'


@app.before_first_request
def create_all() -> None:
    db.create_all()


@app.route('/')
def main_view() -> Response:
    return make_response(render_template('index.html'), 200)


@app.route('/stock')
def stock_view() -> Response:
    return make_response(render_template('stock.html', stocks=StockDAO.read_all()), 200)


@app.route('/stock/intraday/<ticker>')
def stock_intraday_view(ticker: str) -> Response:
    return make_response(render_template('stock-intraday.html', intradays=IntradayDAO.read_filter_by_ticker(ticker)),
                         200)


@app.route('/intraday')
def intraday_view() -> Response:
    return make_response(render_template('intraday.html', tables=[IntradayDAO.dataframe_ticker().to_html(
        classes='data', header='true')]), 200)


@app.route('/evaluation')
def evaluation_view() -> Response:
    return make_response(render_template('evaluation.html', evaluations=EvaluationDAO.read_all()), 200)


@app.route('/forward')
def forward_view() -> Response:
    inventory, cash, fee = ForwardBO.init()
    inventory, total_value, total = ForwardBO.update(inventory, cash)
    return make_response(render_template('forward.html', forwards=ForwardDAO.read_all(), inventory=inventory, cash=cash,
                                         total_value=total_value, total=total), 200)


@app.route('/process')
def process_view() -> Response:
    return make_response(render_template('process.html', running=process_manager.running(),
                                         active_processes=process_manager.get_active_names(),
                                         inactive_processes=process_manager.get_inactive_names()), 200)


@app.route('/process/start/<process_name>')
def process_start_view(process_name: str) -> Response:
    successful: bool = process_manager.start(process_name)
    return make_response(render_template('process-start.html', successful=successful, process_name=process_name), 200)


@app.route('/process/stop/<process_name>')
def process_stop_view(process_name: str) -> Response:
    successful: bool = process_manager.stop(process_name)
    return make_response(render_template('process-stop.html', successful=successful, process_name=process_name), 200)


@app.route('/import', defaults={'data': ''})
@app.route('/import/<path:data>', methods=[GET, POST])
def import_view(data: str) -> Response:
    if data == 'intraday':
        IntradayBO.from_file(request)
    return make_response(render_template('import.html'), 200)


@app.route('/export', defaults={'data': ''})
@app.route('/export/<path:data>')
def export_view(data: str) -> Response:
    if data == 'intraday':
        content = IntradayBO.to_file()
        return make_response(jsonify(content), 200)
    return make_response(render_template('export.html'), 200)


@app.route('/configuration', defaults={'operation': 'read', 'identifier': ''}, methods=[GET, POST])
@app.route('/configuration/<path:operation>', defaults={'identifier': ''}, methods=[GET, POST])
@app.route('/configuration/<path:operation>/<path:identifier>', methods=[GET, POST])
def configuration_view(operation: str, identifier: str) -> Response:
    form: ConfigurationForm = ConfigurationForm(request.form)
    configuration: List[ConfigurationEntity] = []
    if request.method == GET:
        if operation == 'read':
            configuration = ConfigurationBO.read_all()
        elif operation == 'update':
            configuration: ConfigurationEntity = ConfigurationBO.read_filter_by_identifier(identifier)
            field_form: ConfigurationFieldForm = ConfigurationFieldForm(request.form)
            field_form.identifier = configuration.identifier
            field_form.value = configuration.value
            field_form.description = configuration.description
            form.form_list.append_entry(field_form)
    elif request.method == POST and form.validate():
        for entry in form.form_list.entries:
            ConfigurationBO.update(entry.form.identifier.data, entry.form.value.data)
        return redirect(url_for('configuration_view'))
    return make_response(render_template('configuration.html', form=form, configuration=configuration,
                                         operation=operation), 200)


@app.route('/portfolio', defaults={'operation': 'read', 'ticker': ''}, methods=[GET, POST])
@app.route('/portfolio/<path:operation>', defaults={'ticker': ''}, methods=[GET, POST])
@app.route('/portfolio/<path:operation>/<path:ticker>', methods=[GET, POST])
def portfolio_view(operation: str, ticker: str) -> Response:
    form: PortfolioForm = PortfolioForm(request.form)
    portfolio: List[Any] = []
    if request.method == GET:
        if operation == 'create':
            PortfolioForm.append_form('', '', None, form)
        elif operation == 'read':
            portfolio = PortfolioBO.read()
        elif operation == 'update':
            entity: Any = PortfolioBO.read_filter_by_ticker_isin(ticker)
            PortfolioForm.append_form(entity.isin, entity.ticker, entity.mode, form)
        elif operation == 'delete':
            PortfolioBO.delete(ticker)
            return redirect(url_for('portfolio_view'))
    elif request.method == POST and form.validate():
        for entry in form.form_list.entries:
            PortfolioBO.update(entry.form.ticker.data.strip(), ModeEnum[entry.form.mode.data[9:]])
        return redirect(url_for('portfolio_view'))
    return make_response(render_template('portfolio.html', form=form, portfolio=portfolio, operation=operation), 200)


@app.errorhandler(404)
def server_error(exception: exec) -> Response:
    logging.exception('An error occurred during a request.')
    return make_response(render_template('not_found.html', exception=exception), 404)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=False)
