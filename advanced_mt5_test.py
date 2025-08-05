import datetime
import configparser
import os

print("=" * 60)
print("ADVANCED MT5 CONNECTION TEST")
print("=" * 60)

try:
    import MetaTrader5 as mt5
    print("✅ MT5 library imported successfully")
    print(f"   MT5 version: {mt5.version()}")
except ImportError as e:
    print(f"❌ MT5 library import failed: {e}")
    exit(1)

# Load configuration
try:
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config', 'config.ini')
    config.read(config_path)
    
    login = int(config['mt5']['login'])
    password = config['mt5']['password']
    server = config['mt5']['server']
    path = config['mt5']['path']
    
    print(f"\n📋 Configuration:")
    print(f"   Login: {login}")
    print(f"   Server: {server}")
    print(f"   Path exists: {os.path.exists(path)}")
except Exception as e:
    print(f"❌ Config error: {e}")
    exit(1)

# Test different connection methods
print(f"\n🔌 Testing different connection methods...")

# Method 1: Initialize without parameters (use running terminal)
print(f"\n1️⃣ Method 1: Initialize without parameters (use running terminal)")
try:
    if mt5.initialize():
        print("   ✅ Initialization successful")
        
        # Check current login
        account_info = mt5.account_info()
        if account_info:
            print(f"   📊 Currently connected to:")
            print(f"      Login: {account_info.login}")
            print(f"      Server: {account_info.server}")
            print(f"      Company: {account_info.company}")
            
            # Try to login with our credentials
            print(f"   🔐 Trying to login with our credentials...")
            login_result = mt5.login(login, password, server)
            if login_result:
                print("   ✅ Login successful!")
                
                # Test data retrieval
                print(f"   📈 Testing data retrieval...")
                rates = mt5.copy_rates_from_pos("EURUSD", mt5.TIMEFRAME_M1, 0, 1)
                if rates is not None and len(rates) > 0:
                    print(f"   ✅ Data retrieval successful: EURUSD = {rates[0]['close']:.5f}")
                else:
                    print(f"   ⚠️ No data for EURUSD: {mt5.last_error()}")
                    
                    # Try with -ECN suffix
                    rates = mt5.copy_rates_from_pos("EURUSD-ECN", mt5.TIMEFRAME_M1, 0, 1)
                    if rates is not None and len(rates) > 0:
                        print(f"   ✅ Data retrieval successful: EURUSD-ECN = {rates[0]['close']:.5f}")
                    else:
                        print(f"   ⚠️ No data for EURUSD-ECN: {mt5.last_error()}")
                
            else:
                print(f"   ❌ Login failed: {mt5.last_error()}")
        else:
            print("   ❌ No account info available")
        
        mt5.shutdown()
    else:
        print(f"   ❌ Initialization failed: {mt5.last_error()}")
except Exception as e:
    print(f"   ❌ Exception in method 1: {e}")

# Method 2: Initialize with path
print(f"\n2️⃣ Method 2: Initialize with path")
try:
    if mt5.initialize(path=path):
        print("   ✅ Initialization with path successful")
        
        # Try login
        login_result = mt5.login(login, password, server)
        if login_result:
            print("   ✅ Login successful!")
        else:
            print(f"   ❌ Login failed: {mt5.last_error()}")
        
        mt5.shutdown()
    else:
        print(f"   ❌ Initialization with path failed: {mt5.last_error()}")
except Exception as e:
    print(f"   ❌ Exception in method 2: {e}")

# Method 3: Initialize with all parameters
print(f"\n3️⃣ Method 3: Initialize with all parameters")
try:
    if mt5.initialize(path=path, login=login, password=password, server=server):
        print("   ✅ Full initialization successful")
        
        # Test data retrieval
        rates = mt5.copy_rates_from_pos("EURUSD-ECN", mt5.TIMEFRAME_M1, 0, 1)
        if rates is not None and len(rates) > 0:
            print(f"   ✅ Data retrieval successful: EURUSD-ECN = {rates[0]['close']:.5f}")
        else:
            print(f"   ⚠️ No data: {mt5.last_error()}")
        
        mt5.shutdown()
    else:
        print(f"   ❌ Full initialization failed: {mt5.last_error()}")
except Exception as e:
    print(f"   ❌ Exception in method 3: {e}")

# Check available symbols
print(f"\n4️⃣ Method 4: Check available symbols")
try:
    if mt5.initialize():
        print("   ✅ Connected for symbol check")
        
        # Get all symbols
        symbols = mt5.symbols_get()
        if symbols:
            print(f"   📊 Found {len(symbols)} symbols")
            
            # Look for EUR symbols
            eur_symbols = [s.name for s in symbols if 'EUR' in s.name][:10]
            if eur_symbols:
                print(f"   💶 EUR symbols found: {', '.join(eur_symbols)}")
            
            # Look for ECN symbols
            ecn_symbols = [s.name for s in symbols if 'ECN' in s.name][:10]
            if ecn_symbols:
                print(f"   🏢 ECN symbols found: {', '.join(ecn_symbols)}")
            
        else:
            print(f"   ❌ No symbols found: {mt5.last_error()}")
        
        mt5.shutdown()
    else:
        print(f"   ❌ Connection failed: {mt5.last_error()}")
except Exception as e:
    print(f"   ❌ Exception in method 4: {e}")

print(f"\n" + "=" * 60)
print("ADVANCED TEST COMPLETED")
print("=" * 60)
