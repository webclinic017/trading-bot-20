from decimal import Decimal
from os import remove
from os.path import join, exists
from unittest.mock import patch

from tests.base_test_case import BaseTestCase
from trading_bot import db
from trading_bot.bo.broker_bo import BrokerBO
from trading_bot.bo.configuration_bo import ConfigurationBO
from trading_bot.bo.optimization_bo import OptimizationBO
from trading_bot.common.constants import ZERO
from trading_bot.common.predictor_adapter import PredictorAdapter
from trading_bot.dao.evaluation_dao import EvaluationDAO
from trading_bot.dto.attempt_dto import AttemptDTO
from trading_bot.entity.evaluation_entity import EvaluationEntity
from trading_bot.entity.intraday_entity import IntradayEntity
from trading_bot.enums.strategy_enum import StrategyEnum


class OptimizationBOTestCase(BaseTestCase):
    PATH_CHECKPOINT_FILE = join('..', '..', 'model', 'test_checkpoint.h5')
    PATH_MODEL_FILE = join('..', '..', 'model', 'test.h5')
    PATH_MODEL_DIR = join('..', '..', 'model')

    @classmethod
    def setUpClass(cls):
        db.create_all()

    def setUp(self):
        self.truncate_tables()
        ConfigurationBO.init()

    @classmethod
    def tearDownClass(cls):
        if exists(cls.PATH_MODEL_FILE):
            remove(cls.PATH_MODEL_FILE)

    @patch('trading_bot.utils.utils.Utils.negation')
    @patch('trading_bot.utils.utils.Utils.inverse')
    def test_optimise(self, negation, inverse):
        negation.return_value = ZERO
        inverse.return_value = ZERO
        rows = EvaluationDAO.read_all()
        self.assertEqual(len(rows), 0)
        OptimizationBO.optimise([self.create_default_dict()], StrategyEnum.COUNTER_CYCLICAL)
        evaluation = EvaluationDAO.read_filter_by_strategy_order_by_sum(StrategyEnum.COUNTER_CYCLICAL)
        self.assert_attributes(evaluation, sum=Decimal('185266.8'), funds='185266.8', amount_buy=Decimal('1000'),
                               amount_sell=Decimal('1000'), delta_buy=Decimal('1.5'), delta_sell=Decimal('1.5'),
                               distance_buy=Decimal('30'), distance_sell=Decimal('30'))

    @patch('trading_bot.bo.optimization_bo.choice')
    @patch('trading_bot.utils.utils.Utils.negation')
    @patch('trading_bot.utils.utils.Utils.inverse')
    def test_start_counter_cyclical(self, inverse, negation, choice):
        negation.return_value = Decimal('1')
        inverse.return_value = Decimal('1')
        choice.return_value = StrategyEnum.COUNTER_CYCLICAL
        attempt = AttemptDTO(Decimal('1000'), Decimal('10'), Decimal('0.25'), Decimal('1000'), Decimal('10'),
                             Decimal('0.25'))
        EvaluationDAO.create(Decimal('10000'), 'second', attempt, StrategyEnum.COUNTER_CYCLICAL)
        self.persist_default_intraday()
        OptimizationBO.start(lambda: ['AAA', 'BBB', 'CCC'], 3, 1)
        evaluation = EvaluationDAO.read_filter_by_strategy_order_by_sum(StrategyEnum.COUNTER_CYCLICAL)
        self.assertIsInstance(evaluation, EvaluationEntity)
        self.assert_attributes(evaluation, sum=Decimal('225520.3'), funds='225520.3', amount_buy=Decimal('2000'),
                               amount_sell=Decimal('2000'), delta_buy=Decimal('0.5'), delta_sell=Decimal('0.5'),
                               distance_buy=Decimal('20'), distance_sell=Decimal('20'),
                               strategy=StrategyEnum.COUNTER_CYCLICAL)

    # noinspection DuplicatedCode
    @patch('trading_bot.bo.optimization_bo.choice')
    @patch('trading_bot.utils.utils.Utils.negation')
    @patch('trading_bot.utils.utils.Utils.inverse')
    @patch('trading_bot.bo.portfolio_bo.PortfolioBO.forward_portfolio')
    @patch('predictor.utils.predictor_utils.PredictorUtils.PATH_CHECKPOINT_FILE', new=PATH_CHECKPOINT_FILE)
    @patch('predictor.utils.predictor_utils.PredictorUtils.PATH_MODEL_FILE', new=PATH_MODEL_FILE)
    @patch('predictor.utils.predictor_utils.PredictorUtils.PATH_MODEL_DIR', new=PATH_MODEL_DIR)
    def test_start_predictor(self, forward_portfolio, inverse, negation, choice):
        negation.return_value = Decimal('1')
        inverse.return_value = Decimal('1')
        choice.return_value = StrategyEnum.PREDICTOR
        forward_portfolio.return_value = ['AAA']
        attempt = AttemptDTO(Decimal('1000'), Decimal('10'), Decimal('0.025'), Decimal('1000'), Decimal('10'),
                             Decimal('0.025'))
        EvaluationDAO.create(Decimal('10000'), 'second', attempt, StrategyEnum.PREDICTOR)
        self.persist_large_intraday()
        PredictorAdapter.fit(sufficient_data=0, past=self.PAST, future=self.FUTURE)
        IntradayEntity.query.delete()
        self.persist_large_intraday(number=125)
        buy = self.spy_decorator(BrokerBO.buy)
        sell = self.spy_decorator(BrokerBO.sell)
        predict = self.spy_decorator(PredictorAdapter.predict, past=self.PAST, future=self.FUTURE)
        with patch.object(BrokerBO, 'buy', buy), patch.object(BrokerBO, 'sell', sell), \
                patch.object(PredictorAdapter, 'predict', predict):
            OptimizationBO.start(lambda: ['AAA'], 1, 1)
        self.assertEqual(buy.mock.call_count, 1)
        self.assertEqual(sell.mock.call_count, 5)
        evaluation = EvaluationDAO.read_filter_by_strategy_order_by_sum(StrategyEnum.PREDICTOR)
        self.assertIsInstance(evaluation, EvaluationEntity)
        self.assert_attributes(evaluation, sum=Decimal('17976.6'), funds='17976.6', amount_buy=Decimal('2000'),
                               amount_sell=Decimal('2000'), delta_buy=Decimal('0.05'), delta_sell=Decimal('0.05'),
                               distance_buy=Decimal('20'), distance_sell=Decimal('20'),
                               strategy=StrategyEnum.PREDICTOR)
