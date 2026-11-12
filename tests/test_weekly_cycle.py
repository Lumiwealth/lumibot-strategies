"""Native scheduling contracts, not model evals or simulated trading proof."""
import ast
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from zoneinfo import ZoneInfo


ENTRYPOINT = Path(__file__).parents[1] / "strategies/weekly_investor_views_vidiq/main.py"


class Vars(dict):
    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value


def result(state="complete", *, completed=True):
    return SimpleNamespace(
        summary="Recorded actor result", tool_results=[],
        parsed={"execution_state": state, "pending_order_ids": ["order-1"] if state == "pending" else [],
                "cash_remaining": 0, "cash_reason": "Scheduling fixture", "exposure": "Scheduling fixture",
                "actions": "Scheduling fixture"} if completed else None,
        payload={"execution_outcome": {"decision_completed": completed}},
    )


class Actor:
    def __init__(self, research=False):
        self.calls = []
        self.answers = []
        self.research = research

    def run(self, **kwargs):
        self.calls.append(kwargs)
        if self.answers:
            return self.answers.pop(0)
        answer = result()
        if self.research:
            answer.parsed = {"status": "ready", "packet": "Reviewed evidence", "search_attempts": 1, "caption_requests": 1}
        return answer


def strategy(vars_=None):
    # Load the saved strategy's class without importing brokers or providers.
    tree = ast.parse(ENTRYPOINT.read_text())
    tree.body = [node for node in tree.body if isinstance(node, (ast.Assign, ast.ClassDef))]
    scope = {"Strategy": object, "Path": Path, "ZoneInfo": ZoneInfo}
    exec(compile(tree, str(ENTRYPOINT), "exec"), scope)
    bot = scope["BotSpotStrategy"]()
    bot.vars = Vars() if vars_ is None else vars_
    bot.agents = {"investor_researcher": Actor(research=True), "portfolio_risk_trader": Actor()}
    bot.clock = datetime(2026, 10, 19, 10, 0, tzinfo=ZoneInfo("America/New_York"))
    bot.get_datetime = lambda: bot.clock
    return bot


def test_incomplete_week_can_resume():
    bot = strategy()
    bot.agents["portfolio_risk_trader"].answers = [result(completed=False), result()]
    bot.on_trading_iteration()
    assert bot.vars.get("weekly_last_completed") is None
    bot.on_trading_iteration()
    assert len(bot.agents["investor_researcher"].calls) == 2
    assert len(bot.agents["portfolio_risk_trader"].calls) == 2
    assert bot.vars.weekly_last_completed == "2026-10-19"


def test_monday_clock_preserves_the_review_window():
    bot = strategy()
    for day, hour in [(19, 9), (20, 10), (23, 15)]:
        bot.clock = bot.clock.replace(day=day, hour=hour)
        bot.on_trading_iteration()
    assert not bot.agents["investor_researcher"].calls
    assert not bot.agents["portfolio_risk_trader"].calls


def test_completed_week_does_not_repeat():
    bot = strategy()
    bot.on_trading_iteration()
    bot.on_trading_iteration()
    assert len(bot.agents["portfolio_risk_trader"].calls) == 1


def test_pending_execution_survives_restart_and_reuses_the_cutoff():
    bot = strategy()
    bot.agents["portfolio_risk_trader"].answers = [result("pending")]
    bot.on_trading_iteration()
    assert bot.vars.get("weekly_last_completed") is None
    restored = strategy(Vars(bot.vars))
    restored.clock = restored.clock.replace(hour=11)
    restored.on_trading_iteration()
    context = restored.agents["portfolio_risk_trader"].calls[0]["context"]
    assert context["decision_datetime"].endswith("10:00:00-04:00")
    assert context["previous_execution"]["answer"]["pending_order_ids"] == ["order-1"]
    assert restored.vars.weekly_last_completed == "2026-10-19"


def test_blocked_week_stops_polling_without_claiming_completion():
    bot = strategy()
    bot.agents["portfolio_risk_trader"].answers = [result("blocked")]
    bot.on_trading_iteration()
    bot.on_trading_iteration()
    assert bot.vars.get("weekly_last_completed") is None
    assert len(bot.agents["portfolio_risk_trader"].calls) == 1


def test_failed_research_is_handed_to_the_trader_without_false_completion():
    bot = strategy()
    bot.agents["investor_researcher"].answers = [result(completed=False)]
    bot.on_trading_iteration()
    assert len(bot.agents["portfolio_risk_trader"].calls) == 1
    assert not bot.agents["portfolio_risk_trader"].calls[0]["context"]["research_outcome"]["decision_completed"]
    assert bot.vars.get("weekly_last_completed") is None


def test_missing_structured_answer_does_not_claim_completion():
    bot = strategy()
    answer = result()
    answer.parsed = None
    bot.agents["portfolio_risk_trader"].answers = [answer]
    bot.on_trading_iteration()
    assert bot.vars.get("weekly_last_completed") is None


def test_reviewed_research_with_source_gaps_can_finish():
    bot = strategy()
    research = result(completed=False)
    research.parsed = {"status": "ready", "packet": "Reviewed source; another source was unavailable.",
                       "search_attempts": 2, "caption_requests": 1}
    research.payload["execution_outcome"].update(status="tool_error", fallback_used=False)
    bot.agents["investor_researcher"].answers = [research]
    bot.on_trading_iteration()
    assert len(bot.agents["portfolio_risk_trader"].calls) == 1
    assert bot.vars.weekly_last_completed == "2026-10-19"
