# Weekly Investor Views via vidIQ

A weekly AI portfolio example for fully paid US stocks and ETFs. One researcher
uses vidIQ MCP and complete available captions; one sole trader chooses holdings,
weights, leverage and orders. Python supplies scheduling and saved state.

This is an aggressive strategy. Leveraged ETFs reset daily and can suffer large
losses; returns over several days need not equal a fixed multiple of an index.
An investor view does not mean that investor endorsed the ETF selected here.

## Behavior

- Review open Mondays at or after 10 a.m. America/New_York, using the preceding
  30 calendar days. Search the current window each Monday. Older cached sources
  may explain an existing holding as dated background, not current evidence.
- Hold between reviews. Pending execution can continue that Monday with its
  original cutoff, retained research and exact order IDs.
- Invest available capital, including affordable supported top-ups. Leave only
  actual fees, working commitments and unavoidable execution/whole-share cash.
- Often use supported leveraged ETFs, normally 2x. The AI may choose less leverage
  when the evidence or risk assessment warrants it. No borrowing, shorts or options.
- Reconcile actual fills, positions and cash before declaring completion.

Default risk limits are 25% NAV per position, 50% in leveraged funds, 15% in 3x
funds, 170% gross underlying exposure and 40% combined direct/single-company
leveraged exposure. These are disclosed strategy defaults, not investor quotes.
The active sibling rules.json is the policy ledger used by both agents.

## Setup

Keep main.py and rules.json together. This entrypoint uses BotSpot's standard
runner; BotSpot supplies broker configuration, dates, budget and data connection.

1. Configure an account that supports the selected fully paid stocks and ETFs.
   Check the exact account and instrument eligibility before starting.
2. Obtain a read-only MCP key from https://app.vidiq.com/account/settings/mcp and
   save it as VIDIQ_API_KEY through the normal secret settings. Never put it in
   code or a public file. The configured endpoint is https://mcp.vidiq.com/mcp.
3. Choose the runtime AI funding and model explicitly. The model parameter is
   configurable. An openai/ model on BotSpot uses its managed funding contract;
   an existing local ChatGPT login is not automatically a hosted grant.
4. Use a compatible LumiBot AI/MCP runtime. Local qualification is pinned to
   source `8ec8b9280a036f9d4049d2b58a5462f958f36cde`. LumiBot 4.6.52 is
   now published; check the actual package installed by the selected host.
   Source qualification alone does not prove the version installed on a host.
5. Review the saved code, Rules, connection, schedule and funding before using
   the normal start workflow. Copying this example does not mirror an account.

A Marketplace listing and bot start do not require a hosted BotSpot backtest.
Before any live start, state the selected AI funding and estimated dollars/month.
No live bot or broker order was started during the local qualification below.

## Local qualification checkpoint

November 11, 2026: the current source completed October 19 and 26 in a local
LumiBot simulation. Five fills bought SSO35, SPY3, QQQ3, MSFT4 and SCHB32.
Cash remaining was $26.1493 after $9.9639 in assumed fees (0.1% per side);
ending account value was $9,961.9662 from $10,000, a 0.38% loss. Independent
cash, position, exposure, affordable-held-share and weekly research-date/count
audits passed. Historical quotes lack an executable ask, so affordability is a
disclosed reference-price approximation. The final October 1 through 30 local run also passed its accounting, exposure and
research date/count audits: seven simulated fills, $10.0888 assumed fees, $43.0521
cash and $9,353.8824 ending account value, a **6.46% loss**. All four Monday
reviews completed. No leveraged ETF was held in the month; the shorter study
separately exercised SSO. These results do not establish profitability.

A separate recorded overweight-state continuation sold one IWM share, confirmed
its fill and bought nine SCHB shares. Fees and cash reconciled; ending cash was
$20.3489 and all positions were within the cap. That is a controlled trader check,
not an additional full weekly cycle, customer journey or live broker proof.
Build and edit journeys execute strategies saved by the real BotSpot Agent and
are qualified before Marketplace publication. They are separate from historical
trading or performance evidence.

Prices in the historical strategy study are real recorded five-minute bars.
Research replays genuine vidIQ responses originally retrieved October 30 with
partial coverage. Modern issuer documents establish stable fund mechanics only.
This is approximate historical research using a modern model, with hindsight
limitations. It is not an original-vintage study, fresh provider access, hosted
BotSpot execution, live broker proof or a return forecast. Raw captions stay private.

Local inference uses the existing three-account Login with ChatGPT pool, with
$0 per-call API cash cost and $0 incremental monthly API billing. Existing plan
subscriptions remain separate fixed costs. Hosted ChatGPT plan funding remains
pending its owner as of November 11; do not assume free hosted inference. vidIQ
normally uses at most 55 existing credits per weekly review; no credits are bought.

At November 11 advertised Luna Standard pricing, the month's recorded 92 model
requests correspond to about $0.36 provider cost, or $0.72 in BotSpot credits
at its source-default 2x markup for four Monday cycles. This is an illustration,
not a production bill, ceiling or verified served pricing policy. Cache behavior,
retry counts, selected tier and five-Monday months can change it. The BotSpot
plan, broker charges and existing vidIQ subscription are separate.
