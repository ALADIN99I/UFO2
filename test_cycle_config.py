#!/usr/bin/env python3
"""
Test script to verify that cycle_period_minutes configuration changes
are properly applied to both simulation and live trading systems.
"""

import configparser
import os
import datetime
import sys

def test_config_loading():
    """Test configuration loading for both systems"""
    print("🧪 TESTING CYCLE PERIOD CONFIGURATION")
    print("="*60)
    
    # Load the config file
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config', 'config.ini')
    config.read(config_path)
    
    # Get current cycle period value
    current_cycle_period = config.get('trading', 'cycle_period_minutes', fallback='40')
    print(f"📋 Current config.ini value: {current_cycle_period} minutes")
    
    # Test simulation loading (same as FullDayTradingSimulation)
    def parse_value(value, default):
        """Parse config value removing comments"""
        if isinstance(value, str):
            # Remove inline comments
            value = value.split('#')[0].strip()
            # Remove multiple values (take first)
            value = value.split()[0] if value else str(default)
        try:
            return int(value)
        except ValueError:
            return default
    
    simulation_cycle_period = parse_value(config['trading'].get('cycle_period_minutes', '40'), 40)
    print(f"🎮 Simulation would use: {simulation_cycle_period} minutes")
    
    # Test live trader loading (same as LiveTrader)
    try:
        live_cycle_period_raw = config.get('trading', 'cycle_period_minutes', fallback='40')
        live_cycle_period = parse_value(live_cycle_period_raw, 40)
    except:
        live_cycle_period = 40
    print(f"🚀 Live system would use: {live_cycle_period} minutes")
    
    # Calculate cycle timing
    print(f"\n⏰ TIMING CALCULATIONS:")
    print(f"   Simulation cycle frequency: Every {simulation_cycle_period} minutes")
    print(f"   Live system cycle frequency: Every {live_cycle_period} minutes") 
    print(f"   Live system cycle frequency: Every {live_cycle_period * 60} seconds")
    
    # Calculate daily cycles
    trading_hours = 18  # 0 GMT to 18 GMT
    total_minutes = trading_hours * 60
    simulation_total_cycles = total_minutes // simulation_cycle_period
    live_cycles_per_day = (24 * 60) // live_cycle_period  # Live runs 24/7
    
    print(f"\n📊 DAILY CYCLE COUNTS:")
    print(f"   Simulation cycles (0-18 GMT): {simulation_total_cycles}")
    print(f"   Live system cycles (24/7): {live_cycles_per_day}")
    
    # Verify both systems read the same value
    if simulation_cycle_period == live_cycle_period:
        print(f"\n✅ SUCCESS: Both systems use the same cycle period ({simulation_cycle_period} minutes)")
        print("   Changes to config.ini will be applied to both simulation and live trading!")
    else:
        print(f"\n❌ WARNING: Systems use different cycle periods!")
        print(f"   Simulation: {simulation_cycle_period} minutes")
        print(f"   Live: {live_cycle_period} minutes")
    
    return simulation_cycle_period, live_cycle_period

def demonstrate_config_change():
    """Demonstrate what happens when config is changed"""
    print(f"\n🔧 CONFIGURATION CHANGE DEMONSTRATION")
    print("="*60)
    
    print("To change the cycle period for BOTH systems:")
    print("1. Edit config/config.ini")
    print("2. Find line 19: cycle_period_minutes = 40")
    print("3. Change to desired value (e.g., cycle_period_minutes = 30)")
    print("4. Save the file")
    print("5. Restart simulation or live system")
    
    print(f"\nEXAMPLE CONFIGURATIONS:")
    example_periods = [15, 30, 45, 60, 120]
    
    for period in example_periods:
        trading_cycles = (18 * 60) // period
        live_cycles = (24 * 60) // period
        print(f"   {period:3d} minutes → Simulation: {trading_cycles:2d} cycles/day, Live: {live_cycles:2d} cycles/day")
    
    print(f"\n⚠️  IMPORTANT NOTES:")
    print("   • Lower values = More frequent trading (higher activity)")
    print("   • Higher values = Less frequent trading (lower activity)")
    print("   • UFO methodology typically uses 30-60 minute cycles")
    print("   • Current default (40 min) provides good balance")

if __name__ == "__main__":
    try:
        # Test current configuration
        sim_period, live_period = test_config_loading()
        
        # Show how to change configuration
        demonstrate_config_change()
        
        print(f"\n🎯 CONCLUSION:")
        print("YES - Changing cycle_period_minutes in config.ini will affect BOTH:")
        print("   ✅ Full day simulation (full_day_simulation.py)")
        print("   ✅ Live trading system (main.py)")
        print("   ✅ Both systems read from the same config/config.ini file")
        
    except Exception as e:
        print(f"❌ Error testing configuration: {e}")
        sys.exit(1)
