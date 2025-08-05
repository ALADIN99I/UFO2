import configparser
import pandas as pd
import numpy as np
import datetime
import time
import json
import re
import os
from pathlib import Path

# Import necessary modules
try:
    import MetaTrader5 as mt5
except ImportError:
    from src import mock_metatrader5 as mt5

from src.data_collector import MT5DataCollector, EconomicCalendarCollector
from src.ufo_calculator import UfoCalculator
from src.llm.llm_client import LLMClient
from src.agents.trader_agent import TraderAgent
from src.agents.risk_manager_agent import RiskManagerAgent
from src.agents.data_analyst_agent import DataAnalystAgent
from src.agents.market_researcher_agent import MarketResearcherAgent
from src.agents.fund_manager_agent import FundManagerAgent
from src.trade_executor import TradeExecutor
from src.ufo_trading_engine import UFOTradingEngine
from src.portfolio_manager import PortfolioManager

class TradingSimulation:
    def __init__(self, simulation_date=datetime.datetime(2025, 7, 31)):
        self.simulation_date = simulation_date
        self.config = self.load_config()
        self.trades_executed = []
        self.portfolio_value = 10000.0  # Starting balance
        self.simulation_log = []
        
        # Fix config parsing issues
        self.fix_config_values()
        
        # Initialize components
        self.initialize_components()
        
    def load_config(self):
        """Load configuration with error handling"""
        config = configparser.ConfigParser()
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config', 'config.ini')
        config.read(config_path)
        return config
    
    def fix_config_values(self):
        """Fix configuration values that have comments or multiple values"""
        # Parse values with inline comments
        def parse_value(value, default):
            if isinstance(value, str):
                # Remove inline comments and extra spaces
                clean_value = value.split('#')[0].split('(')[0].strip()
                try:
                    return float(clean_value) if '.' in clean_value else int(clean_value)
                except ValueError:
                    return default
            return value
        
        # Fix portfolio equity stop parsing
        portfolio_stop = self.config['trading'].get('portfolio_equity_stop', '-5.0')
        self.portfolio_equity_stop = parse_value(portfolio_stop, -5.0)
        
        # Fix other config values
        self.cycle_period_minutes = parse_value(self.config['trading'].get('cycle_period_minutes', '20'), 20)
        self.max_concurrent_positions = parse_value(self.config['trading'].get('max_concurrent_positions', '11'), 11)
        self.target_positions_when_available = parse_value(self.config['trading'].get('target_positions_when_available', '6'), 6)
        self.min_positions_for_session = parse_value(self.config['trading'].get('min_positions_for_session', '5'), 5)
    
    def initialize_components(self):
        """Initialize all trading components"""
        # Initialize LLM client
        self.llm_client = LLMClient(api_key=self.config['openrouter']['api_key'])
        
        # Initialize MT5 data collector
        self.mt5_collector = MT5DataCollector(
            login=self.config['mt5']['login'],
            password=self.config['mt5']['password'],
            server=self.config['mt5']['server'],
            path=self.config['mt5']['path']
        )
        
        # Initialize UFO components
        self.ufo_calculator = UfoCalculator(self.config['trading']['currencies'].split(','))
        self.ufo_engine = UFOTradingEngine(self.config)
        
        # Initialize agents
        self.data_analyst = DataAnalystAgent("DataAnalyst", self.mt5_collector)
        self.market_researcher = MarketResearcherAgent("MarketResearcher", self.llm_client)
        self.trader = TraderAgent("Trader", self.llm_client, self.mt5_collector)
        self.risk_manager = RiskManagerAgent("RiskManager", self.llm_client, self.mt5_collector, self.config)
        self.fund_manager = FundManagerAgent("FundManager", self.llm_client)
        
        # Initialize trade executor
        self.trade_executor = TradeExecutor(self.mt5_collector, self.config)
        
        self.log_event("Simulation components initialized successfully")
    
    def log_event(self, message):
        """Log simulation events with timestamp"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.simulation_log.append(log_entry)
        print(log_entry)
    
    def simulate_data_collection(self):
        """Simulate data collection for the specified date"""
        self.log_event(f"Starting data collection simulation for {self.simulation_date.strftime('%Y-%m-%d')}")
        
        # Define timeframes and bars needed
        timeframes = [mt5.TIMEFRAME_M5, mt5.TIMEFRAME_M15, mt5.TIMEFRAME_H1, mt5.TIMEFRAME_H4, mt5.TIMEFRAME_D1]
        timeframe_bars = {
            mt5.TIMEFRAME_M5: 240,   # 20 hours = 240 M5 bars
            mt5.TIMEFRAME_M15: 80,   # 20 hours = 80 M15 bars  
            mt5.TIMEFRAME_H1: 20,    # 20 hours = 20 H1 bars
            mt5.TIMEFRAME_H4: 120,   # Multi-day analysis
            mt5.TIMEFRAME_D1: 100    # Multi-day analysis
        }
        
        # Collect data for base symbol
        base_symbol = 'EURUSD'
        symbol_suffix = self.config['mt5'].get('symbol_suffix', '')
        symbol_with_suffix = base_symbol + symbol_suffix
        
        try:
            data = self.data_analyst.execute({
                'source': 'mt5',
                'symbol': symbol_with_suffix,
                'timeframes': list(timeframe_bars.keys()),
                'num_bars': timeframe_bars
            })
            
            if data:
                self.log_event(f"Successfully collected data for {len(data)} timeframes")
                return data
            else:
                self.log_event("Warning: No data collected, using mock data")
                return self.generate_mock_data(timeframe_bars)
                
        except Exception as e:
            self.log_event(f"Error collecting data: {e}, using mock data")
            return self.generate_mock_data(timeframe_bars)
    
    def generate_mock_data(self, timeframe_bars):
        """Generate mock price data for simulation"""
        mock_data = {}
        base_price = 1.0850  # EUR/USD typical price
        
        for timeframe, num_bars in timeframe_bars.items():
            # Generate realistic price movement
            np.random.seed(42)  # For reproducible results
            price_changes = np.random.normal(0, 0.0001, num_bars)  # Small price movements
            
            prices = [base_price]
            for change in price_changes:
                new_price = prices[-1] + change
                prices.append(max(1.0700, min(1.1000, new_price)))  # Keep within realistic range
            
            # Create OHLC data
            mock_data[timeframe] = pd.DataFrame({
                'time': pd.date_range(start=self.simulation_date, periods=num_bars, freq='5T'),
                'open': prices[:-1],
                'high': [p + abs(np.random.normal(0, 0.00005)) for p in prices[:-1]],
                'low': [p - abs(np.random.normal(0, 0.00005)) for p in prices[:-1]],
                'close': prices[1:],
                'volume': [1000 + np.random.randint(0, 500) for _ in range(num_bars)]
            })
        
        return mock_data
    
    def calculate_ufo_data(self, price_data_dict):
        """Calculate UFO indicators from price data"""
        self.log_event("Calculating UFO indicators")
        
        incremental_sums_dict = {}
        for timeframe, price_data in price_data_dict.items():
            try:
                variation_data = self.ufo_calculator.calculate_percentage_variation(price_data)
                incremental_sums_dict[timeframe] = self.ufo_calculator.calculate_incremental_sum(variation_data)
            except Exception as e:
                self.log_event(f"Error calculating UFO data for {timeframe}: {e}")
        
        ufo_data = self.ufo_calculator.generate_ufo_data(incremental_sums_dict)
        self.log_event(f"UFO data calculated for {len(ufo_data)} timeframes")
        
        return ufo_data
    
    def run_full_day_simulation(self):
        """Simulate trading from 0 GMT to 18 GMT every 40 minutes"""
        self.log_event("Starting full day simulation (0 GMT to 18 GMT)")

        # Start time at 0:00 GMT
        current_time = datetime.datetime(self.simulation_date.year, self.simulation_date.month, self.simulation_date.day, 0, 0)
        end_time = datetime.datetime(self.simulation_date.year, self.simulation_date.month, self.simulation_date.day, 18, 0)

        while current_time <= end_time:
            self.log_event(f"Simulating session at {current_time.strftime('%H:%M')} GMT")

            # Perform a full trading session
            self.simulate_trading_session()

            # Increment time by the cycle period (40 minutes)
            current_time += datetime.timedelta(minutes=40)
            self.simulation_date = current_time

        self.log_event("Completed full day simulation")
        self.save_simulation_report()

if __name__ == "__main__":
    simulation = TradingSimulation(datetime.datetime(2025, 7, 31))
    simulation.run_full_day_simulation()
            'volume': volume,
            'entry_price': 1.0850 + np.random.normal(0, 0.0001),  # Mock price
            'timestamp': datetime.datetime.now(),
            'comment': 'UFO Simulation Trade'
        }
        
        executed_trades.append(trade_info)
        self.trades_executed.append(trade_info)
        
        self.log_event(f"🔹 Simulated trade: {full_symbol} {direction} {volume} lots @ {trade_info['entry_price']:.5f}")
                        
        except Exception as e:
            self.log_event(f"Error simulating trade execution: {e}")
        
        return executed_trades
    
    def generate_session_summary(self):
        """Generate comprehensive session summary"""
        self.log_event("\n📊 TRADING SESSION SUMMARY")
        self.log_event("-" * 40)
        self.log_event(f"Date: {self.simulation_date.strftime('%Y-%m-%d')}")
        self.log_event(f"Trades Executed: {len(self.trades_executed)}")
        self.log_event(f"Portfolio Value: ${self.portfolio_value:,.2f}")
        
        if self.trades_executed:
            self.log_event("\n📈 EXECUTED TRADES:")
            for i, trade in enumerate(self.trades_executed, 1):
                self.log_event(f"  {i}. {trade['symbol']} {trade['direction']} {trade['volume']} @ {trade['entry_price']:.5f}")
        
        self.log_event("\n🎯 DIVERSIFICATION STATUS:")
        current_positions = len(self.get_mock_positions()) + len(self.trades_executed)
        self.log_event(f"  Current Positions: {current_positions}/{self.max_concurrent_positions}")
        self.log_event(f"  Target Positions: {self.target_positions_when_available}")
        self.log_event(f"  Minimum Positions: {self.min_positions_for_session}")
        
        self.log_event("\n✅ SIMULATION COMPLETED SUCCESSFULLY")
    
    def save_simulation_report(self):
        """Save detailed simulation report to file"""
        report_filename = f"simulation_report_{self.simulation_date.strftime('%Y%m%d')}.txt"
        report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), report_filename)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("UFO FOREX AGENT v3 - SIMULATION REPORT\n")
            f.write("=" * 50 + "\n")
            f.write(f"Date: {self.simulation_date.strftime('%A, %B %d, %Y')}\n")
            f.write(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            for log_entry in self.simulation_log:
                f.write(log_entry + "\n")
        
        self.log_event(f"\n📁 Simulation report saved: {report_filename}")
        return report_path

def main():
    """Main simulation function"""
    print("🚀 Starting UFO Forex Agent v3 Simulation")
    print("📅 Target Date: Thursday, July 31, 2025")
    print("-" * 50)
    
    try:
        # Create simulation instance
        simulation = TradingSimulation(datetime.datetime(2025, 7, 31))
        
        # Run the trading session simulation
        success = simulation.simulate_trading_session()
        
        if success:
            # Save detailed report
            report_path = simulation.save_simulation_report()
            print(f"\n✅ Simulation completed successfully!")
            print(f"📊 Detailed report saved to: {report_path}")
        else:
            print("\n❌ Simulation ended early due to trading conditions")
            
    except Exception as e:
        print(f"\n💥 Simulation failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
