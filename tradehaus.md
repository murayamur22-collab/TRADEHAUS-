# TRADEHAUS – Design Document
**Version 3.1**  
Local MT5-powered trading bot inside a bright, stylish, Gen-Z playboy villa

## 1. Core Fantasy
Welcome to **TRADEHAUS** — a small, sun-drenched, high-vibe villa.  
A crew of quirky AI agents move around the floor, while a static Anon Wizard mascot watches from the upper-left. Manual trades use the MT5 monitor drawer.  
Relaxed, colourful, slightly magical, and permanently fun.

## 2. Branding
- **App Name:** TRADEHAUS
- **Executable:** TRADEHAUS.exe
- **Tagline ideas:**  
  “Trade from the villa.”  
  “Chill. Tick. Profit.”  
  “Anonymous alpha in the Haus.”

## 3. Mascot – The Anon Wizard
- Classic V-for-Vendetta mask
- Relaxed wizard fit: oversized hoodie-robe, tilted pointed hat, glowing price-tick staff
- Personality: calm, slightly smug, occasionally floats, drops dry one-liners
- Static and inanimate in the upper-left of the room; not part of character selection or patrol movement
- Fully modular sprite (easy recolours and seasonal skins)

## 4. Style & Technical
- Resolution: 640×360 or 640×480 (nearest-neighbor)
- Palette: Bright saturated — turquoise, coral, mint, sunny yellow, soft pink, clean white, warm wood, neon accents
- Perspective: Top-down with light isometric tilt
- Mood: Sunny, stylish, chill Gen-Z villa

## 5. Permanent HUD
**Top-Left – Money Widget**
┌─────────────────────────┐
│ $ 12,847.32             │
│ DEMO                    │
└─────────────────────────┘

(Typewriter animation on DEMO/REAL switch)

**Top-Right – Hearts**  
3 chunky pixel hearts (12 quarters total).  
Each losing trade drains ¼ heart.  
All grey = 12-hour REST MODE.

## 6. Villa Layout
Bright scrolling LED ticker across the top.  
Big sunny windows, sunken lounge + beanbags, bar cart, record player, stylish low desks,  
**right-side MT5 monitor drawer** (peek tab, live selected-symbol chart, BUY / SELL controls),  
pixel desk clock with timezone dropdown (Local / NY / London / Asia / EAT Nairobi),  
open closet, neon whiteboard, trophy shelf, lush plants, filing cabinet, manager’s low desk.  
Slim Order Strip slides in from the right → click to expand into pixel CRT terminal.

## 7. Core Systems
- Manual MT5 DEMO/LIVE trade controls in the slide-out monitor
- Live MT5 prices on the ticker
- Timezone-adjustable desk clock
- Order Strip + fullscreen CRT
- 12-heart daily hardcap → REST MODE
- Closet outfit system for all agents + Anon Wizard
- Static, inanimate Anon Wizard mascot at the upper-left of the room
- In-game playlist discovered from supported audio files in the music folder

## 8. requirements.txt
```txt
# TRADEHAUS – Core Dependencies
pygame>=2.5.0
MetaTrader5>=5.0.45
numpy>=1.24.0
pandas>=2.0.0
quantstats>=0.0.62
Pillow>=10.0.0
python-dateutil>=2.8.2

# Optional
pygame-gui>=0.6.9

Recommended Build Order
Project skeleton + bright palette + empty villa
HUD (money + hearts)
Ticker + desk clock
MT5 monitor drawer + manual trade animation
Music folder playlist
Order Strip + CRT
Characters + Anon Wizard
Closet system
Polish, sound, REST MODE

Core Architecture (Local-First)1. MT5 Connection (exactly what you want)
Use the official MetaTrader5 Python package (pip install MetaTrader5). It connects directly to the local MT5 terminal on the same Windows machine (or via Wine/VM bridges on other OSes). No websockets to the broker’s web terminal.Typical flow:User enters Login + Password + Server (dropdown)
Call mt5.initialize(path=...) then mt5.login(login, password, server)
Everything else (ticks, rates, orders, positions, history) goes through the same package.

Useful GitHub helpers around it:Akinzou/MetaTrader5-Python — clean Broker wrapper
Various socket/ZeroMQ/file bridges if you ever need cross-platform later (e.g. huy-bui-tech/mt5_api, macOS file-IPC bridges)

Server dropdown: hardcode popular broker servers or scrape/parse from the terminal’s server list / a local JSON you maintain.2. Game Layer (90s low-res aesthetic)
Pygame is the clear winner for a true local 90s-feeling app:Pixel-art sprites, CRT scanlines, limited color palette, chunky UI
Easy loading screen → login screen → main “trading floor” scene
Hearts system, character animations, particle effects on wins/losses

Visual style suggestions:Agents as tiny 16×16 / 32×32 “Sims-like” or RPG characters (analyst, risk manager, execution bot, news scout, etc.)
They walk around a small office / trading pit, sit at desks, type, high-five on wins, facepalm or explode hearts on losses
Background can be a simple pixel trading floor with floating charts, ticker tape, etc.
Hearts: classic Zelda/Mario style. 3 full hearts = 12 quarters. Each losing trade drains ¼ heart. When all grey → “cooldown” mode (12-hour hard lock). Store state in a local SQLite/JSON file with timestamps.

3. Hearts / Risk Hardcap Logictext

lives = 12   # quarters
on_losing_trade:
    lives -= 1
    update_hearts_display()   # 3 hearts, each with 4 fill states (red → grey)
if lives <= 0:
    lock_trading_until = now + 12 hours
    show "REST MODE – come back later" screen + grey hearts

Reset only after the timer. This is pure local state — no broker dependency.4. Trading Agents + Strategy
Pull real AI/strategy code from GitHub and wrap each as a “character”:Strong starting points:Multi-agent LLM desks: PetteKay/ai-forex-trading-bot (5-agent adversarial), El-Bach/claude-trader (14 agents), Elyounesinho/XAUUSD_AIRoom_Git
ML-heavy: Ezee-Kits/FOREX-TRADING-BOT (LightGBM + Optuna), algrythm-fx/algrythm, HillaryMurimi/mt5-gold-ai-trader
General MT5 AI assistants: jblanked/metatrader-ai, toki-plus/ai-trader-for-mt5

Each agent becomes a sprite with its own “job” animation and speech bubbles (“RSI oversold…”, “Risk veto!”, “Executing market order…”).5. Statistics & Analysis (TradingView-like)
Best pure-Python repo: ranaroussi/quantstats (very popular).
Feed it your equity curve / trade list from MT5 history → get Sharpe, Sortino, drawdown, win rate, monthly heatmaps, tearsheets, etc.
You can render the key numbers and simple charts inside the Pygame UI (or open an HTML tearsheet in a browser window).
Complement with TA-Lib / pandas-ta for live indicator values the agents can “read”.Suggested Project Structure

tradehaus/
├── main.py                 # Pygame entry + game loop
├── screens/
│   ├── loading.py
│   ├── login.py            # MT5-style form
│   └── trading_floor.py    # main scene with agents + hearts
├── mt5/
│   ├── connector.py        # official MetaTrader5 wrapper
│   └── order_manager.py
├── agents/
│   ├── base_agent.py
│   ├── technical.py
│   ├── risk.py
│   └── ...
├── strategy/               # plug in GitHub strategies here
├── stats/
│   └── quantstats_wrapper.py
├── assets/                 # pixel sprites, hearts, fonts, sfx
├── data/                   # local SQLite for lives, trade log, settings
└── requirements.txt

Tech Stack RecommendationUI / Game: Pygame (+ optional pygame-gui or custom pixel widgets)
MT5: official MetaTrader5 package
Data / Stats: pandas, quantstats, TA-Lib or pandas-ta
Persistence: SQLite or just JSON + pickle for the 12-hour timer
Optional: simple local FastAPI if you later want a companion web dashboard

Realistic Build PathGet MT5 login + basic order send working in a plain script.
Build the Pygame loading → login → empty floor screens.
Implement the hearts system and hard lock.
Add one or two agent sprites that react to mock signals.
Plug in a real strategy from one of the GitHub repos.
Wire quantstats for a “Stats” panel or post-session report.
Polish the 90s juice (scanlines, chiptune SFX, speech bubbles, idle animations).
