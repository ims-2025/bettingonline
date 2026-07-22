#!/usr/bin/env python3
"""Second-pass cleanup on bonuses/index.html — replace old-brand examples in
educational sections and the JSON-LD schema with our promoted brands.
"""
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BONUSES = ROOT / "bonuses" / "index.html"

text = BONUSES.read_text()

# ---------------------------------------------------------------------------
# 1) JSON-LD FAQPage schema — replace the old-brand FAQ answers
# ---------------------------------------------------------------------------
old_faq_1 = ('{"@type":"Question","name":"What is the best online sports betting welcome bonus in 2026?",'
             '"acceptedAnswer":{"@type":"Answer","text":"The best welcome bonus depends on your typical bet size. '
             'For small first bets, the Caesars Wager $1 Get $300 in bonus bets offer is exceptional value because '
             'it pays the same regardless of outcome. For higher-confidence first bets, FanDuel\'s Bet $5, Get $150 '
             'If Your Bet Wins pays $150 in Bonus Bets when the first wager wins (no refund if it loses). For maximum '
             'upside, BetMGM\'s First Bet Offer up to $1,500 has the highest cap."}}')

new_faq_1 = ('{"@type":"Question","name":"What is the best online sports betting welcome bonus in 2026?",'
             '"acceptedAnswer":{"@type":"Answer","text":"The best welcome bonus depends on your deposit size and '
             'preferred cashier method. For a large crypto deposit, BetUS\'s 125% match up to $3,125 has the highest '
             'headline value. For an all-around 50% match with strong crypto reloads and cross-vertical account access, '
             'BetOnline is the top pick. For a second-book account with a distinct reload calendar, Sportsbetting.ag is '
             'the natural pair with BetOnline."}}')

text = text.replace(old_faq_1, new_faq_1)

old_faq_2 = ('{"@type":"Question","name":"What is the difference between a no-deposit bonus and a free bet?",'
             '"acceptedAnswer":{"@type":"Answer","text":"A no-deposit bonus credits funds to your account just for '
             'registering — no deposit required. These are rare in US sports betting (888 Poker is one of the few). '
             'A free bet (or bonus bet) requires a qualifying deposit and/or wager, then credits a single-use betting token."}}')

new_faq_2 = ('{"@type":"Question","name":"What is the difference between a no-deposit bonus and a free bet?",'
             '"acceptedAnswer":{"@type":"Answer","text":"A no-deposit bonus credits funds to your account just for '
             'registering — no deposit required. These are rare in US-facing sports betting. A free bet (or bonus bet) '
             'requires a qualifying deposit and/or wager, then credits a single-use betting token."}}')

text = text.replace(old_faq_2, new_faq_2)


# ---------------------------------------------------------------------------
# 2) Educational sections — swap brand-example references for generic or
#    promoted-brand examples.
# ---------------------------------------------------------------------------

# Line ~281 "today's largest first-bet offer is BetMGM at $1,500"
text = text.replace(
    "today's largest first-bet offer is BetMGM at $1,500",
    "the largest first-bet offers in the regulated US market now cap at $1,500",
)

# Line ~290 "Deposit matches are dominant in casino welcome offers (BetMGM Casino $1,000, Caesars Palace Online $2,500)"
text = text.replace(
    "Deposit matches are dominant in casino welcome offers (BetMGM Casino $1,000, Caesars Palace Online $2,500)",
    "Deposit matches are dominant in casino welcome offers (offshore casino welcomes commonly run 100% up to $3,000 across the first three deposits, e.g., BetOnline Casino)",
)

# Line ~294 "FanDuel's prior No-Sweat First Bet up to $1,000 was the canonical example; FanDuel has since migrated..."
text = re.sub(
    r"FanDuel's prior No-Sweat First Bet up to \$1,000 was the canonical example; FanDuel has since migrated "
    r'to a win-conditional \\"Bet \$5, Get \$150 If Your Bet Wins\\" structure, while BetMGM\'s First Bet Offer up to \$1,500 still carries the refund-on-loss mechanic\. ',
    "The refund-on-loss mechanic is standard across regulated US operators at first-bet caps of $500-$1,500. ",
    text,
)

# Line ~298 "DraftKings' 'Bet $5, Get $100' and Caesars' 'Wager $1, Get $300' are the textbook examples"
text = text.replace(
    'DraftKings\\\' "Bet $5, Get $100" and Caesars\\\' "Wager $1, Get $300" are the textbook examples. '
    'Fast and clean — no math, no protection mechanics, just a small qualifying bet and an instant bonus drop. '
    'The bonus is typically split into multiple smaller tokens (DraftKings: 4 × $25; Caesars: 30 × $10)',
    "Regulated US-market Wager & Get offers are the textbook examples. Fast and clean — no math, no protection "
    "mechanics, just a small qualifying bet and an instant bonus drop. The bonus is typically split into multiple "
    "smaller tokens (e.g., 4 × $25 or 30 × $10)",
)

# Line ~302 "Common in casino welcome packages — BetMGM Casino includes 100 free spins"
text = text.replace(
    "Common in casino welcome packages — BetMGM Casino includes 100 free spins on top of its match bonus.",
    "Common in casino welcome packages — regulated US casino welcome offers often bundle 50-100 free spins on top of a match bonus.",
)

# Line ~306 "888 Poker's $88 free is the standard example in US legal markets"
text = text.replace(
    "888 Poker's $88 free is the standard example in US legal markets. No-deposit bonuses always have meaningful restrictions",
    "No-deposit bonuses are rare in US-facing sports betting. Where they exist (typically in regulated US poker markets), they carry meaningful restrictions",
)

# Line ~318 "Tight 7-day windows (BetMGM bonus bets)"
text = text.replace(
    "Tight 7-day windows (BetMGM bonus bets)",
    "Tight 7-day windows (typical of regulated first-bet-protection offers)",
)

# Line ~335 worked math example — replace Caesars specific
text = re.sub(
    r"<strong>The math example:</strong> Take Caesars' Wager \$1, Get \$300 in 30 × \$10 tokens\. "
    r"If you place each \$10 bonus bet on a \+200 underdog and 35% of them win, you'll realize approximately "
    r"30 × \$10 × 0\.35 × 2 = \$210 in cash winnings — about 70% of the \$300 nominal value\. That's the realistic "
    r"expected outcome for a disciplined user\. A user who sticks tokens on -200 favorites would realize ~\$130 — "
    r"less than half\. Bonus bet selection matters as much as the offer choice\.",
    "<strong>The math example:</strong> Take a $1,000 sportsbook welcome match at 10× rollover (typical at BetOnline "
    "and Sportsbetting.ag). Total rollover required = 10 × ($1,000 deposit + $1,000 bonus) = $20,000. At an average "
    "sportsbook hold of ~5% on sides, expected loss during clearance = $1,000. Net realized value = $1,000 bonus "
    "− $1,000 expected loss = roughly break-even before variance, plus reload access. A bettor with a small edge (say "
    "positive CLV) retains materially more of the bonus; a very casual bettor may retain less. Bonus math is a "
    "framework, not a guarantee.",
    text,
)

# Line ~349 token splitting example
text = text.replace(
    "If a $300 bonus is delivered as 30 × $10 tokens (Caesars), you can't combine them into a single $200 bet. "
    "This forces volume and limits your ability to concentrate the bonus on a high-conviction position. "
    "If a $1,500 bonus arrives as 5 × $300 tokens (BetMGM), each token is a separate single-use bet.",
    "If a bonus is delivered as many small tokens (e.g., 30 × $10), you can't combine them into a single large bet. "
    "This forces volume and limits your ability to concentrate the bonus on a high-conviction position. "
    "Larger-token structures (e.g., 5 × $300) give more per-bet flexibility.",
)

# Line ~361 state availability example
text = text.replace(
    "The Caesars $300 Wager &amp; Get is the standard offer in most states; some states offer enhanced or different "
    "offers depending on regulatory and licensing context.",
    "Regulated operators run distinct welcome-offer variants by state depending on regulatory and licensing context. "
    "Our promoted offshore books offer a single global welcome package — the same offer applies regardless of the "
    "state you deposit from.",
)

# Line ~495 step 2 example
text = text.replace(
    "If you're a small-stakes recreational bettor, the Caesars $1 → $300 offer is more efficient than chasing "
    "FanDuel's $1,000 first-bet protection (which only matters if you bet $300+ on your first wager). Match the "
    "offer structure to your actual betting pattern.",
    "If you're a small-stakes recreational bettor, a smaller deposit-match offer with lower rollover is more efficient "
    "than chasing a large first-bet-protection ceiling you couldn't realistically max out. Match the offer structure "
    "to your actual deposit and betting pattern.",
)

# 3) State-guide reference — this one intentionally mentions regulated brands
# to give informational context. Keep as is.

BONUSES.write_text(text)
print(f"Pass 2 complete on {BONUSES.relative_to(ROOT)}")

subprocess.run(["git", "-C", str(ROOT), "add", "-A"], check=True)
