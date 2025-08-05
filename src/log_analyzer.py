import re
import pandas as pd

def analyze_log_file(log_file):
    """
    Analyzes the simulation log file to identify losing trades and patterns.

    Args:
        log_file (str): The path to the log file.
    """
    with open(log_file, 'r', encoding='utf-8') as f:
        log_content = f.read()

    # Regex to find closed trades
    closed_trade_pattern = re.compile(r"📉 Position closed: (.*?) P&L: \$(.*)")
    llm_closed_trade_pattern = re.compile(r"🔹 Trade closed by LLM: (.*?) P&L: \$(.*)")

    closed_trades = []

    for match in closed_trade_pattern.finditer(log_content):
        symbol = match.group(1).strip()
        pnl = float(match.group(2).strip())
        closed_trades.append({'symbol': symbol, 'pnl': pnl, 'closed_by': 'Stop Loss/Take Profit/Time'})

    for match in llm_closed_trade_pattern.finditer(log_content):
        symbol = match.group(1).strip()
        pnl = float(match.group(2).strip())
        closed_trades.append({'symbol': symbol, 'pnl': pnl, 'closed_by': 'LLM'})


    if not closed_trades:
        print("No closed trades found in the log file.")
        return

    df = pd.DataFrame(closed_trades)

    print(df.groupby('symbol')['pnl'].sum())


if __name__ == '__main__':
    analyze_log_file('full_day_simulation_20250804.txt')
