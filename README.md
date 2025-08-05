# UFO Forex Trading Agent

The UFO Forex Trading Agent is a sophisticated platform designed for automated and semi-automated trading using the UFO methodology. It involves a combination of real-time data analysis, strategic risk management, and trade execution.

## Project Structure

1. **Main Components:**
   - `main.py`: The entry point for running the live trading loop using the `LiveTrader` class.
   - `src/agents/`: Houses different trading and support agents, like DataAnalyst, Trader, RiskManager, etc.
   - `src/`: Contains the core logic, including the trade executor, data collector, communication modules, and the UFO trading engine.

2. **Key Modules:**
   - `live_trader.py`: Manages the trading logic, collecting data, running calculations, and executing trades.
   - `ufo_trading_engine.py`: Implements the core UFO methodology, including session management, position reinforcement, and portfolio-level risk decisions.
   - `trade_executor.py`: Handles trade sending and management based on the UFO methodology.
   - `data_collector.py`: Interfaces with MetaTrader5 for historical and live data collection.
   - `ufo_calculator.py`: Computes currency variations to generate UFO data.

3. **Configuration:**
   - `config/config.ini`: Stores configuration details like login, API keys, and trading preferences.

## Dependencies

- **Pandas**: For data manipulation and analysis.
- **MetaTrader5**: For interacting with the MT5 terminal.
  - Note: A mock version exists (`mock_metatrader5.py`) for development on non-Windows platforms.
- **Finnhub**: To collect economic calendar data.
- **OpenAI**: To enable interaction with a large language model for decision support.

## Installing Dependencies

To run the project, install the necessary Python libraries:

```bash
pip install pandas MetaTrader5 finnhub-python openai
```

## Running the Project

Execute the main script to start the trading cycle:

```bash
python main.py
```

## Trading Mechanism

The UFO Trading Engine employs the following strategies:

- **Session Timing**: Trades are based on active trading sessions.
- **Risk Management**: Uses portfolio-level stops and dynamic reinforcement strategies.
- **LLM-Driven Decisions**: Utilizes language models for risk assessment and trade strategy formulation.
- **UFO Calculations**: Continuously calculates currency variations to maintain a positive portfolio trajectory.

## Notes on Usage

- Ensure the `config.ini` file is accurately configured with your MT5 and API credentials.
- The system is designed to be modified for various trading strategies, adjust configurations and agents as needed.
