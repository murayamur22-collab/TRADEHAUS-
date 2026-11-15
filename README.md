# TRADEHAUS

A pixel-art trading villa for Windows. A crew of AI agents patrol the floor while
a live MetaTrader 5 terminal feeds real quotes, real candles and real orders.
Trade manually, or switch the desk to AUTO and let the bot work the session.

PyGame at a 640×360 logical resolution, scaled ×2 and letterboxed into a
resizable window, with a CRT pass over the whole picture.

## Run

```powershell
.\.venv\Scripts\python.exe main.py
```

The login screen wants your MT5 account number, password, and the trade server
name exactly as the terminal shows it (e.g. `Deriv-Demo`). DEMO is the default;
LIVE needs a confirmed order every time.

Dependencies live in [requirements.txt](requirements.txt). The build script for
a standalone `TRADEHAUS_game` folder is [tools/build_windows.py](tools/build_windows.py).

## Controls

| Input | Does |
|---|---|
| Click an agent | Select it, zoom to 3×, and open its agent file |
| Click the floor | Deselect, back to 2× |
| Right-click the floor | Walk the selected agent there (A\* around the furniture) |
| Mouse wheel | Zoom 1×–3× around the cursor |
| WASD | Move the selected agent, or pan the map when nobody is selected |
| `B` | Toggle the auto trader |
| `F` | Sound effects on/off |
| `C` | Open the closet (outfits per agent) |
| `O` | Slide the MT5 drawer; `Enter` inside it opens the full CRT |
| `M` / `N` | Music on-off / next track |
| `←` `→` | Previous / next symbol |
| Click the clock | Open or close the timezone menu |
| `Esc` | Close panels, twice for the exit prompt |
| `Y` / `N` | Confirm or decline an order, and the exit prompt |

## The auto trader

`B` hands the desk to the bot. It scans one symbol per market tick, and when a
strategy likes what it sees, NOVA calls the setup and BYTE physically walks to
the order station before the order is sent.

- Three strategies in [signals/](signals/): **trend pullback** (EMA 9/21 with an
  RSI turn), **range break** (a close beyond the prior 12 bars), and **fade**
  (RSI exhaustion outside the bands). They vote; if they disagree the desk
  stands aside until the next bar.
- One position at a time. Entries carry an ATR-derived stop and target, and the
  bot closes itself when either is reached.
- DEMO only. Auto refuses a LIVE account; LIVE manual orders still work.
- No stacked vetoes. There is no queue of filters to get through — if a signal
  fires, it trades.

## The hearts

Three hearts, twelve quarters, persisted in `data/tradehaus.sqlite3`.

- A losing closed trade costs one quarter; a winning one earns one back.
- Empty hearts put the house in **REST MODE**: the auto trader stops and the HUD
  goes red. Manual trading stays available, so the game never deadlocks.
- The state survives a restart, so the desk carries its record.

## Sound and ambience

There are no audio files. Every effect is synthesised at start-up from a short
frequency-sweep recipe in [audio/sfx.py](audio/sfx.py) — fills, rejections, wins,
losses, heart changes, confirmation prompts. If the machine has no output device
the bank reports itself unavailable and the game simply runs silent.

Dust motes drift through the room and the wizard's staff twinkles, both driven by
plain maths over elapsed time in [game/ambience.py](game/ambience.py).

## The scoreboard

Every closed trade lands in a session ledger and the CRT prints the running line:
trades, win rate, net, and max drawdown. The ledger is per-session (the hearts are
the persistent record).

## The agent files

Every sprite has a persona and a tally. Click one and the file opens: name, role,
a tagline, a short bio, its favourite strategy, and three live numbers that count
what that person actually did this session — NOVA's calls and hit rate, RHEA's
stops cut and hearts left, SCOUT's scans, BYTE's fills. Click anywhere else, or
press `Esc`, to close it and carry on.

## The chart

The CRT has its own timeframe row (`M5` `M15` `H1` `H4`) and the mouse wheel
zooms the candles from 48 down to 8, so you can read a single setup up close.
The drawer's own controls still work independently.

## Layout

```
main.py                window, event loop, screen flow, exit prompt
screens/               loading, login, trading_floor (the game), CRT, music, theme
agents/character.py    sprite, patrol route, path following, manual movement
game/navigation.py     grid router + walkability
signals/               indicators, strategies, decision engine
trading/               risk_state (hearts), closet (outfits)
mt5/connector.py       the only MT5 surface: quotes, candles, orders, positions
tools/                 asset generation and the Windows build
data/                  SQLite state
```

## Tests

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -t tests
```

`tests/test_music.py` and `tests/test_paper_engine.py` need a writable system
temp directory; everything else runs anywhere. The trading-floor tests use an
in-memory database (`:memory:`), so they leave no files behind.

## Notes

- `.attic/` holds unused files that were removed from the tree, with a manifest.
  Nothing there is needed to run the game.
- `trading/paper_engine.py` and `trading/strategy.py` are not used by the game;
  they are the earlier paper-trading experiment, kept for reference.
