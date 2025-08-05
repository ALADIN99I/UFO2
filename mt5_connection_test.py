import datetime
import configparser
import os

# Test 1: Check if real MT5 is available
print("=" * 60)
print("MT5 CONNECTION DIAGNOSTIC TEST")
print("=" * 60)

try:
    import MetaTrader5 as mt5
    REAL_MT5 = True
    print("✅ STEP 1: Real MT5 library imported successfully")
except ImportError:
    print("❌ STEP 1: Real MT5 library not available - would use mock")
    REAL_MT5 = False

if not REAL_MT5:
    print("❌ Test failed - MT5 library not available")
    exit(1)

# Test 2: Load configuration
print("\n📋 STEP 2: Loading configuration...")
try:
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config', 'config.ini')
    config.read(config_path)
    
    login = int(config['mt5']['login'])
    password = config['mt5']['password']
    server = config['mt5']['server']
    path = config['mt5']['path']
    
    print(f"✅ Config loaded:")
    print(f"   Login: {login}")
    print(f"   Server: {server}")
    print(f"   Path: {path}")
    print(f"   Password: {'*' * len(password)}")
except Exception as e:
    print(f"❌ Config loading failed: {e}")
    exit(1)

# Test 3: Check if MT5 terminal path exists
print(f"\n📁 STEP 3: Checking MT5 terminal path...")
if os.path.exists(path):
    print(f"✅ MT5 terminal found at: {path}")
else:
    print(f"❌ MT5 terminal NOT found at: {path}")
    print("   Please verify the path in config.ini")

# Test 4: Test MT5 initialization
print(f"\n🔌 STEP 4: Testing MT5 connection...")
try:
    # Try without path first (use default)
    init_result = mt5.initialize()
    if init_result:
        print("✅ MT5 initialized successfully (default path)")
    else:
        print(f"⚠️ Default initialization failed: {mt5.last_error()}")
        print("   Trying with specified path...")
        
        # Try with specified path
        init_result = mt5.initialize(path=path)
        if init_result:
            print("✅ MT5 initialized successfully (specified path)")
        else:
            print(f"❌ Path initialization failed: {mt5.last_error()}")

    if init_result:
        # Test 5: Test login
        print(f"\n🔐 STEP 5: Testing account login...")
        login_result = mt5.login(login, password, server)
        if login_result:
            print("✅ Account login successful")
            
            # Test 6: Get account info
            print(f"\n📊 STEP 6: Getting account information...")
            account_info = mt5.account_info()
            if account_info:
                print("✅ Account info retrieved:")
                print(f"   Login: {account_info.login}")
                print(f"   Server: {account_info.server}")
                print(f"   Balance: ${account_info.balance:.2f}")
                print(f"   Equity: ${account_info.equity:.2f}")
                print(f"   Company: {account_info.company}")
            else:
                print("❌ Failed to get account info")
            
            # Test 7: Test symbol data retrieval
            print(f"\n📈 STEP 7: Testing historical data retrieval...")
            test_symbols = ['EURUSD-ECN', 'GBPUSD-ECN', 'USDJPY-ECN']
            
            for symbol in test_symbols:
                print(f"\n   Testing {symbol}:")
                
                # Test current rates
                rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 1)
                if rates is not None and len(rates) > 0:
                    rate = rates[0]
                    timestamp = datetime.datetime.fromtimestamp(rate['time'])
                    print(f"   ✅ Current rate: {rate['close']:.5f} at {timestamp}")
                else:
                    print(f"   ❌ No current rates for {symbol}: {mt5.last_error()}")
                
                # Test historical rates for August 4, 2025
                target_date = datetime.datetime(2025, 8, 4, 8, 0, 0)
                target_timestamp = int(target_date.timestamp())
                
                historical_rates = mt5.copy_rates_from(symbol, mt5.TIMEFRAME_M5, target_timestamp, 1)
                if historical_rates is not None and len(historical_rates) > 0:
                    rate = historical_rates[0]
                    timestamp = datetime.datetime.fromtimestamp(rate['time'])
                    print(f"   ✅ Historical rate (Aug 4, 2025): {rate['close']:.5f} at {timestamp}")
                else:
                    print(f"   ⚠️ No historical rates for Aug 4, 2025: {mt5.last_error()}")
                    
                    # Try alternative date range
                    today = datetime.datetime.now()
                    week_ago = today - datetime.timedelta(days=7)
                    week_ago_timestamp = int(week_ago.timestamp())
                    
                    alt_rates = mt5.copy_rates_from(symbol, mt5.TIMEFRAME_M5, week_ago_timestamp, 1)
                    if alt_rates is not None and len(alt_rates) > 0:
                        rate = alt_rates[0]
                        timestamp = datetime.datetime.fromtimestamp(rate['time'])
                        print(f"   ✅ Alternative historical rate: {rate['close']:.5f} at {timestamp}")
                    else:
                        print(f"   ❌ No alternative historical rates: {mt5.last_error()}")
            
            # Test 8: Test symbol info
            print(f"\n🔍 STEP 8: Testing symbol information...")
            symbol_info = mt5.symbol_info('EURUSD-ECN')
            if symbol_info:
                print("✅ Symbol info retrieved:")
                print(f"   Spread: {symbol_info.spread}")
                print(f"   Digits: {symbol_info.digits}")
                print(f"   Point: {symbol_info.point}")
            else:
                print(f"❌ No symbol info: {mt5.last_error()}")
            
        else:
            print(f"❌ Account login failed: {mt5.last_error()}")
            print("   Please check your credentials in config.ini")
    
    # Shutdown
    mt5.shutdown()
    print(f"\n🔌 MT5 connection closed")
    
except Exception as e:
    print(f"❌ Unexpected error during MT5 testing: {e}")
    import traceback
    traceback.print_exc()

print(f"\n" + "=" * 60)
print("TEST COMPLETED")
print("=" * 60)
