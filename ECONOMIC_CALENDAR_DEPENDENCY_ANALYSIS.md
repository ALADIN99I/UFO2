# Economic Calendar Feature - Complete Dependency Analysis
## Root to Stem to Branch to Leaves to Fruit

**Analysis Date**: 2025-08-02 Saturday  
**Current Week**: 2025-W31  
**Current Cache**: 2025-W31 (101 records, retrieved today)

---

## 🌱 ROOT: Project Entry Point

### **main.py** (Application Root)
```python
def main():
    config = configparser.ConfigParser()
    config_path = os.path.join(script_dir, 'config', 'config.ini')
    config.read(config_path)
    
    live_trader = LiveTrader(config)
    live_trader.run()  # ← Entry point to trading loop
```

**Status**: ✅ **VERIFIED** - Main entry initializes LiveTrader and starts trading loop

---

## 🌿 STEM: Core Trading Engine

### **LiveTrader.run()** (Primary Trading Loop)
**File**: `src/live_trader.py`  
**Lines**: 47-311

```python
def run(self):
    while True:  # Main trading loop
        # ... UFO analysis and position management ...
        
        # Line 154: Economic calendar retrieval 
        economic_events = self.agents['data_analyst'].execute({'source': 'economic_calendar'})
        
        # Line 162: Pass to market researcher
        research_result = self.agents['researcher'].execute(ufo_data, economic_events)
```

**Key Details**:
- **Execution Frequency**: Every 40 minutes (2400 seconds) - Line 302
- **Economic Calendar Call**: Line 154 - Called EVERY trading cycle
- **No Special Monday Logic**: Economic calendar is fetched every 40 minutes regardless of day

**Status**: ✅ **VERIFIED** - Economic calendar retrieved every 40 minutes, not specifically on Mondays

---

## 🌳 BRANCH: Agent Architecture

### **DataAnalystAgent** (Data Collection Layer)
**File**: `src/agents/data_analyst_agent.py`  
**Lines**: 5-36

```python
class DataAnalystAgent(Agent):
    def __init__(self, name, mt5_collector):
        self.economic_calendar_collector = EconomicCalendarCollector()  # ← Creates collector
    
    def execute(self, task):
        if task['source'] == 'economic_calendar':
            return self.economic_calendar_collector.get_economic_calendar()  # ← Direct call
```

**Status**: ✅ **VERIFIED** - Agent creates collector instance and calls it when requested

### **MarketResearcherAgent** (Analysis Layer)
**File**: `src/agents/market_researcher_agent.py`  
**Lines**: 3-42

```python
def execute(self, ufo_data, economic_events):
    economic_events_str = economic_events.to_string() if economic_events is not None and not economic_events.empty else "No upcoming economic events."
    
    analysis_prompt = (
        # ... UFO analysis prompt ...
        f"Upcoming Economic Events:\n{economic_events_str}\n\n"  # ← Economic events included in LLM prompt
    )
```

**Status**: ✅ **VERIFIED** - Economic events are integrated into LLM analysis for trading decisions

---

## 🍃 LEAVES: Economic Calendar Implementation

### **EconomicCalendarCollector** (Core Implementation)
**File**: `src/data_collector.py`  
**Lines**: 147-287

#### **Weekly Caching Logic**:
```python
def _get_current_week_key(self):
    """Returns a unique key for the current week (year-week format)."""
    now = datetime.datetime.now()
    year, week, _ = now.isocalendar()
    return f"{year}-W{week:02d}"  # Format: "2025-W31"

def _is_cache_valid(self):
    """Checks if the cached data is from the current week."""
    cached_week = metadata.get('week_key')
    current_week = self._get_current_week_key()
    return cached_week == current_week  # ← Week-based validation
```

#### **Cache Update Mechanism**:
```python
def get_economic_calendar(self):
    # Check if we have valid cache for current week
    if self._is_cache_valid():
        return self._load_cache()  # ← Return cached data if same week
    
    # Cache is either missing or from previous week - clean up old data
    self._cleanup_old_cache()  # ← Remove old cache files
    
    # Fetch fresh data from API
    response = requests.get(self.url, timeout=10)  # ← API call to faireconomy.media
    data = pd.DataFrame(response.json())
    
    if not data.empty:
        self._save_cache(data)  # ← Save new cache with current week key
```

#### **API Details**:
- **URL**: `https://nfs.faireconomy.media/ff_calendar_thisweek.json`
- **Data Source**: ForexFactory calendar (thisweek endpoint)
- **Update Frequency**: When week key changes (Monday at 00:00)

**Status**: ✅ **VERIFIED** - Cache refreshes when week changes, not specifically on Monday

---

## 🍎 FRUIT: Actual Behavior Analysis

### **Current State** (As of 2025-08-02 Saturday):
- **Cache Week**: 2025-W31 
- **Cache Status**: Valid (current week)
- **Records**: 101 economic events
- **Last Updated**: 2025-08-02 01:04:59 (today)

### **When Cache Updates**:

| Day | Week Key | Cache Behavior | API Call |
|-----|----------|----------------|----------|
| **Monday** | Changes to new week | ❌ Invalid → Fresh fetch | ✅ YES |
| **Tuesday-Sunday** | Same week | ✅ Valid → Use cache | ❌ NO |

### **Example Week Transition**:
```
2025-08-03 Sunday   → Week 2025-W31 → Cache Valid   → No API call
2025-08-04 Monday   → Week 2025-W32 → Cache Invalid → API CALL + Cache Update
2025-08-05 Tuesday  → Week 2025-W32 → Cache Valid   → No API call
...
2025-08-10 Sunday   → Week 2025-W32 → Cache Valid   → No API call
2025-08-11 Monday   → Week 2025-W33 → Cache Invalid → API CALL + Cache Update
```

**Status**: ✅ **VERIFIED** - Economic calendar updates automatically on week transitions (typically Monday)

---

## 🔄 Complete Data Flow Chain

### **1. ROOT ACTIVATION**
```
main.py → LiveTrader(config) → live_trader.run()
```

### **2. TRADING LOOP CYCLE** (Every 40 minutes)
```
LiveTrader.run() → Line 154: economic_events = self.agents['data_analyst'].execute({'source': 'economic_calendar'})
```

### **3. AGENT DELEGATION**
```
DataAnalystAgent.execute() → self.economic_calendar_collector.get_economic_calendar()
```

### **4. CACHE LOGIC**
```
EconomicCalendarCollector.get_economic_calendar():
├── _is_cache_valid() → Check if current week matches cached week
├── IF VALID: _load_cache() → Return cached data
├── IF INVALID: 
    ├── _cleanup_old_cache() → Remove old files
    ├── requests.get(API_URL) → Fetch fresh data
    └── _save_cache() → Store with new week key
```

### **5. INTEGRATION**
```
MarketResearcherAgent.execute(ufo_data, economic_events) → LLM Analysis → Trading Decisions
```

---

## 🔍 Dependencies Verification

### **External Dependencies**:
- ✅ **requests** - HTTP calls to API
- ✅ **pandas** - Data manipulation
- ✅ **datetime** - Week calculations
- ✅ **json** - Cache file handling
- ✅ **pathlib** - File system operations

### **Internal Dependencies**:
- ✅ **config/config.ini** - Not used by economic calendar
- ✅ **cache/** directory - Auto-created if missing
- ✅ **API Endpoint** - `https://nfs.faireconomy.media/ff_calendar_thisweek.json`

### **Network Dependency Test**:
```bash
curl -s "https://nfs.faireconomy.media/ff_calendar_thisweek.json" | head -n 5
# ✅ TESTED: API accessible, returns JSON data
```

---

## ⚠️ Issues Identified

### **1. TIMING DISCREPANCY**
- **Expected**: Updates "every week at Monday"
- **Actual**: Updates when week key changes (can be any time Monday 00:00-23:59)
- **Issue**: Week boundary is based on system time, not market open times

### **2. NO EXPLICIT MONDAY LOGIC**
- **Current**: Week-based caching with ISO week calculation
- **Missing**: Explicit Monday detection or market-calendar awareness
- **Impact**: May update mid-Monday instead of at market open

### **3. TIMEZONE CONSIDERATIONS**
- **System Time**: Uses local system datetime
- **Market Time**: No timezone conversion for forex market hours
- **Risk**: Week boundaries may not align with trading week start

### **4. API DEPENDENCY**
- **Single Point of Failure**: Only one API endpoint
- **No Fallback**: If API fails, returns empty DataFrame
- **No Retry Logic**: Single attempt per week

---

## 🔧 Recommended Fixes

### **1. Add Explicit Monday Detection**
```python
def should_fetch_fresh_data(self):
    """Enhanced logic for Monday-specific updates"""
    if not self._is_cache_valid():
        return True
    
    # Check if it's Monday and we haven't updated today
    now = datetime.datetime.now()
    if now.weekday() == 0:  # Monday
        last_update = self._get_last_update_date()
        if last_update.date() != now.date():
            return True
    return False
```

### **2. Add Market Timezone Support**
```python
import pytz

def _get_current_week_key(self):
    """Use forex market timezone for week calculations"""
    market_tz = pytz.timezone('Europe/London')  # Forex market reference
    now = datetime.datetime.now(market_tz)
    year, week, _ = now.isocalendar()
    return f"{year}-W{week:02d}"
```

### **3. Add Fallback API Sources**
```python
BACKUP_APIS = [
    "https://nfs.faireconomy.media/ff_calendar_thisweek.json",
    "https://api.forexfactory.com/calendar",  # If available
    # Add more backup sources
]
```

---

## 📊 Current Feature Status

| Component | Status | Issues | Dependency Met |
|-----------|--------|--------|----------------|
| **Root (main.py)** | ✅ Working | None | ✅ |
| **Stem (LiveTrader)** | ✅ Working | Calls every 40min, not just Monday | ⚠️ |
| **Branch (Agents)** | ✅ Working | None | ✅ |
| **Leaves (Collector)** | ✅ Working | Week-based, not Monday-specific | ⚠️ |
| **Fruit (Cache)** | ✅ Working | Timezone agnostic | ⚠️ |
| **API Integration** | ✅ Working | Single point of failure | ⚠️ |
| **Monday Updates** | ⚠️ Partial | Updates on week change, not explicit Monday | ❌ |

---

## 🎯 Summary for Senior

**What Works**:
- ✅ Economic calendar data is retrieved and cached
- ✅ Weekly caching prevents excessive API calls
- ✅ Data flows correctly through agent architecture
- ✅ Integration with LLM analysis is functional

**What Needs Fixing**:
- ❌ No explicit Monday morning update logic
- ❌ System timezone instead of market timezone
- ❌ No fallback for API failures
- ❌ Updates can happen any time during Monday, not at specific time

**Mechanism Verification**:
- 📡 **API Call**: Every week boundary change (Monday 00:00 system time)
- 🔄 **Cache Logic**: ISO week-based validation
- 🏗️ **Architecture**: Agent-based delegation working correctly
- 🌐 **Dependencies**: All external dependencies satisfied

**Recommendation**: Implement explicit Monday market-time logic and timezone awareness for proper forex market alignment.

---
**Analysis Complete**: 2025-08-02  
**Files Examined**: 8 core files  
**Dependencies Traced**: Root → Stem → Branch → Leaves → Fruit  
**Status**: Feature works but needs Monday-specific enhancements
