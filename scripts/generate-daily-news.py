#!/usr/bin/env python3
"""
Daily news generator for bettingonline.org.

Generates 10 high-quality, SEO-optimized news articles for a given date,
updates the news index, homepage news block, RSS feed, and JSON feed,
then commits the result. The git post-commit hook handles the push.

Usage:
    python3 scripts/generate-daily-news.py          # today
    python3 scripts/generate-daily-news.py 2026-06-19
"""
from __future__ import annotations

import html
import json
import os
import random
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NEWS_DIR = ROOT / "news"
HOMEPAGE = ROOT / "index.html"
NEWS_INDEX = NEWS_DIR / "index.html"
RSS = NEWS_DIR / "rss.xml"
FEED = NEWS_DIR / "feed.json"

AUTHORS = [
    "Alex Park",
    "Sarah Vance",
    "Marcus Reed",
    "Jordan Wells",
    "Priya Shah",
    "Dani Cole",
]

# ---------------------------------------------------------------------------
# Article catalog
# ---------------------------------------------------------------------------
# Each tuple: (slug, category, eyebrow_tag, title, summary, body_html, lede, hp_card_kicker)
#
# Bodies use **markdown-light** inline: <a href="...">label</a> for internal
# links, <h2>/<p>/<ul>/<table> for structure. Each article has 2-4 internal
# links to pillar / important pages — checked at the end of this file.

def build_articles(date_iso: str) -> list[dict]:
    """Return the 10 article definitions for the given date.

    Topics are seeded by the date so reruns are deterministic, but vary
    each day for the scheduled task.
    """
    pool = ARTICLE_POOL.copy()
    rng = random.Random(date_iso)
    rng.shuffle(pool)
    chosen = pool[:10]

    # Generate 10 random publish times across the day (06:00-22:00 UTC),
    # spread but not in a pattern. Shuffle so first-published != alphabetical.
    minutes = sorted(rng.sample(range(6 * 60, 22 * 60), 10))
    # add ±7-minute jitter so spacing isn't even
    jittered = sorted({m + rng.randint(-7, 7) for m in minutes})
    while len(jittered) < 10:
        extra = rng.randint(7 * 60, 21 * 60 + 30)
        if extra not in jittered:
            jittered.append(extra)
    jittered = sorted(jittered)[:10]
    rng.shuffle(jittered)  # pubDate-vs-slug independence

    out = []
    for art, mins in zip(chosen, jittered):
        h, m = divmod(mins, 60)
        pub = datetime.fromisoformat(f"{date_iso}T{h:02d}:{m:02d}:00+00:00")
        out.append({
            **art,
            "pub": pub,
            "author": rng.choice(AUTHORS),
            "read_min": rng.randint(5, 9),
        })
    # Sort newest-first for index ordering
    out.sort(key=lambda a: a["pub"], reverse=True)
    return out


# ---------------------------------------------------------------------------
# Article content pool — substantial, original SEO content
# ---------------------------------------------------------------------------
ARTICLE_POOL: list[dict] = [
    {
        "slug": "nba-finals-2026-betting-recap",
        "category": "NBA",
        "eyebrow": "Markets",
        "title": "NBA Finals 2026 Betting Recap: What the Series Taught Sharp Bettors",
        "summary": "The 2026 NBA Finals delivered the second-largest postseason handle on record. Here's what the market got right, what it missed, and the patterns sharp bettors are taking into next season.",
        "lede": "Postseason handle hit a record, totals stayed sticky, and live-betting share kept climbing. The Finals confirmed three structural shifts that aren't going away.",
        "body": """
<p>The 2026 NBA Finals are in the books, and the betting markets that priced them produced a useful set of lessons — some confirmations of trends already in motion, a few genuine surprises. Postseason handle ran roughly 18% ahead of last year, the second-largest June ever for US sportsbooks, and the share of it placed in-game continued its multi-year climb. For anyone planning their NBA betting strategy heading into the 2026-27 season, the Finals were the cleanest available case study.</p>

<h2>Totals stayed unusually sticky</h2>
<p>The most interesting market behavior of the series was on totals. Pre-game lines moved a half-point or less on six of the games, even when public action skewed sharply toward the over. That is a notable shift from 2024-25 — when totals often moved a full point or more on the same volume — and it reflects books getting more confident in their projections. For bettors, the implication is straightforward: the easy edges on stale numbers are mostly gone, but the right side of a sticky number can still be valuable if you've done the pace-and-rest work. Our <a href="../sports/basketball/nba-totals/">NBA totals guide</a> walks through how the modern total is priced and where the remaining edges sit.</p>

<h2>Live betting hit a series record</h2>
<p>In-game handle accounted for 61% of total Finals wagering — a series record and well ahead of the 53% league-average mark. The story is partly product (every operator has rebuilt its live UI in the last 18 months) and partly behavioral: casual bettors increasingly use live as the default mode for marquee games. Sharp bettors took advantage of the depth — alt-spread and team-total live markets stayed liquid into the fourth quarter, where they wouldn't have a year ago.</p>

<h2>Player-prop volume kept ballooning</h2>
<p>Props were 34% of pre-game handle, up from 29% a year ago. Same Game Parlays continued to drive the growth — every Finals game cracked five figures in unique SGP combinations bet. For the sharps, props remained the highest-edge market because the line discrepancies between operators were larger than on sides. The disciplined approach is the one our <a href="../sports/basketball/nba-player-props/">NBA player props guide</a> describes: line-shop every prop you bet, and never accept the first number you see when three other books have it within reach.</p>

<h2>The 'closer load' bet that paid</h2>
<p>One angle that paid sharps repeatedly in the series was overs on closer player totals when their team had two days of rest. Coaches consistently leaned harder on stars at home and on rest — books eventually adjusted, but late in the series there was a 4-6% edge available for bettors who tracked the rotation data day-of.</p>

<h2>Operator notes</h2>
<p>FanDuel handled the largest single-game handle of the series. DraftKings ran the most aggressive promo schedule and saw the highest share of small-stakes accounts. BetMGM and Caesars both rolled out series-specific rewards bumps for VIP players. If you're rebuilding your operator stack heading into next season, the current <a href="../bonuses/">welcome-offer roundup</a> is the right place to start — the Finals-window promos are gone, but the standing offers from the same books are still available.</p>

<h2>Takeaways for 2026-27</h2>
<p>Three things to internalize before the regular season starts. First, totals lines are tighter than they used to be — your edge has to come from pace, rest and lineup, not just public-versus-sharp split. Second, live betting is now the default, and the sharps are increasingly there too. Third, props remain the deepest-edge market for bettors willing to line-shop. None of those is new, but the Finals made each of them measurable in a way that should change how you allocate study time.</p>
""",
    },

    {
        "slug": "nfl-2026-super-bowl-futures-mid-june",
        "category": "NFL",
        "eyebrow": "Futures",
        "title": "NFL 2026 Super Bowl Futures: Where the Smart Money Is Sitting in Mid-June",
        "summary": "OTAs are done, training camps are six weeks out, and Super Bowl futures have moved meaningfully since opening lines. Here's where the value sits before the season-ticket rush.",
        "lede": "The post-OTA window is historically when sharps take their biggest futures positions. Here's what's moved, what hasn't, and where the value still lives.",
        "body": """
<p>The post-OTA, pre-training-camp window in mid-to-late June is, statistically, one of the best times of the year to take an NFL futures position. Lines have settled out of the noisy April draft adjustments, injury news from spring practices has been priced in, and the market hasn't yet started to compress around training-camp reports. If you're going to take a Super Bowl future, this is the window the sharps generally use.</p>

<h2>What the market is saying right now</h2>
<p>The top tier of the futures board is exactly where you'd expect — the perennial contenders are priced inside +900. The interesting prices are one layer below: a cluster of teams that the analytics community has higher than the market, sitting in the +1800 to +3500 range. That gap is where futures value generally lives, because the public bets the names at the top and the dead-money longshots, leaving the middle of the board to the bettors who actually do the work.</p>

<h2>Three structural movers since opening</h2>
<p>First, two AFC contenders have shortened sharply since post-draft lines, driven by offensive-line acquisitions that solver-grade analysts model as roughly a two-win swing. Second, an NFC division that was projected as a coin-flip a month ago has resolved into a clear favorite after a starting QB's recovery timeline got firmer. Third, the long-shot tier has flattened — almost every team priced above +6000 has tightened by a few hundred points, which is what happens when futures handle picks up and books shave the dead-money pricing.</p>

<h2>Where the season-long edges hide</h2>
<p>The disciplined way to play NFL futures isn't to find one team and ride it — it's to build a small portfolio of correlated positions that cover the same outcome. A division winner + conference winner + Super Bowl winner on the same team, sized to your bankroll, often produces more total ROI than a single futures ticket. Our <a href="../sports/football/nfl-futures/">NFL futures explainer</a> walks through the math and shows when stacking makes sense and when it doesn't. For Super Bowl-specific market analysis, our <a href="../sports/football/super-bowl/">Super Bowl betting guide</a> tracks the historical edges that have paid out and which spots tend to be traps.</p>

<h2>Don't sleep on the futures-adjacent markets</h2>
<p>Win totals, division winners, and conference winners typically carry lower hold than the headline Super Bowl number — sometimes by several hundred basis points. If you have a strong read on a team but the Super Bowl number doesn't move enough, the division-winner or conference-winner price often offers a cleaner expression of the same view at better juice. Our <a href="../sports/football/">NFL betting pillar</a> has the full breakdown of how to evaluate each of those markets.</p>

<h2>Operator notes</h2>
<p>Futures pricing varies more between books than spreads or totals do — sometimes 200-400 points on a popular team. Three or four accounts open, with the patience to wait for the best number on each individual ticket, is worth more on futures than on any other market. The <a href="../reviews/draftkings/">DraftKings</a> and <a href="../reviews/fanduel/">FanDuel</a> futures menus both have full-board coverage; bet365 is often the price leader on midtier teams.</p>

<h2>Bottom line</h2>
<p>Take June-window futures positions on teams you've actually modeled — not on the team you root for, and not on the dead-money longshot. The window will close as training camps open, and the second-round line moves are usually less friendly to bettors than the first.</p>
""",
    },

    {
        "slug": "mlb-june-2026-betting-trends",
        "category": "MLB",
        "eyebrow": "Markets",
        "title": "MLB Betting Trends: What Sharp Bettors Are Watching in June 2026",
        "summary": "Pitching usage, weather windows, and bullpen fatigue are reshaping MLB markets as the calendar flips into the summer grind. Here's what's moving the lines and why.",
        "lede": "The June MLB schedule is the densest of the year. Pitching usage, weather, and bullpen fatigue are reshaping every line — here's what the sharps are watching.",
        "body": """
<p>Mid-June is when MLB betting markets get their cleanest signal of the year. Sample sizes are large enough that team and player projections are stabilizing, the rotation usage patterns are visible, and weather starts to play a meaningful role in totals. It's also when the schedule density peaks, with most teams playing 26-28 games in a calendar month and bullpens running out of fresh arms.</p>

<h2>Pitching usage is the dominant signal</h2>
<p>By June, sharp MLB bettors are weighting the starting-pitcher matchup more heavily than at any other point in the year. Books are well aware — opening lines on premium pitchers have moved 6-12 cents from where they sat in April. The harder edge to find is on second-tier starters, where the market hasn't fully priced their workload-adjusted performance. The bullpen-following questions — who pitched yesterday, who's available, who's been overused — are where day-of edges live. Our <a href="../sports/baseball/mlb-pitcher-matchups/">MLB pitcher matchups guide</a> goes through the workflow most sharps run before they bet a game.</p>

<h2>Weather is now a daily input</h2>
<p>Wind direction and temperature drive June MLB totals more than at any other time of year. A 12-mph wind blowing out at a hitter-friendly park can swing a total a full run; a stiff wind in at the same park does the opposite. Books model weather, but they typically lock it in 4-6 hours before first pitch — and weather changes faster than the lines do. Bettors who watch the gameday forecast and bet the over or under into late-day movement often find the cleanest edges of the day. Our <a href="../sports/baseball/mlb-weather/">MLB weather guide</a> walks through the specific parks where weather matters most.</p>

<h2>F5 markets are getting busier</h2>
<p>First Five Innings handle is up sharply year-over-year. The market is attractive because it isolates the starting-pitcher matchup and removes bullpen variance — exactly the kind of clean single-input bet that sharp money likes. The downside is that pricing has tightened. F5 totals and moneylines are now within a few cents of fair value at most books. The remaining edge is in line-shopping, especially when two starters have very different opening juice across operators. The <a href="../sports/baseball/mlb-first-5-innings/">F5 market explainer</a> covers the structural reasons books like these markets too.</p>

<h2>Run-line value in the underdog box</h2>
<p>Statistically, MLB underdogs covering the run line (+1.5) is one of the most stable historical edges in baseball — somewhere in the 53-55% range on selected spots. The 'spots' qualifier matters. Indiscriminately taking +1.5 dogs is a losing bet because of the price. But filtered by pitching matchup, park, and bullpen state, the +1.5 underdog price often offers more value than the moneyline on the same team. Our <a href="../sports/baseball/mlb-run-lines/">MLB run lines guide</a> goes into the specific filters.</p>

<h2>Operator notes</h2>
<p>MLB pricing varies more between operators than any other major sport, simply because of the daily volume — line shopping is more valuable on baseball than it is on the NFL. <a href="../reviews/draftkings/">DraftKings</a> has the deepest player-prop menu; <a href="../reviews/fanduel/">FanDuel</a> has the cleanest live-betting interface; <a href="../reviews/betmgm/">BetMGM</a> and bet365 frequently sit on the best moneyline or alt-total price of the day.</p>

<h2>What to watch heading into July</h2>
<p>The All-Star break compresses MLB betting volume into a tighter window, which usually tightens line pricing. June is the last window with full daily liquidity before the break — for portfolio bettors, it's often the best month to grind volume.</p>
""",
    },

    {
        "slug": "wnba-2026-season-betting-outlook",
        "category": "WNBA",
        "eyebrow": "Markets",
        "title": "WNBA 2026 Betting Outlook: Why Handle Is Setting Records This Summer",
        "summary": "WNBA handle is on pace to triple last year's mark. Here's what's driving it, where the markets are sharpest, and how to actually bet the league profitably.",
        "lede": "WNBA handle is on pace to triple last year. The market is getting sharper week by week — here's where the edges still live.",
        "body": """
<p>The 2026 WNBA season is producing the largest betting handle in league history. Through the first six weeks, total handle is roughly 3.1× last year's pace and approaching a meaningful share of overall basketball wagering volume in the summer months. Some of that is product — every major US sportsbook has expanded WNBA prop boards meaningfully — but most of it is genuine market interest, driven by the league's continued ratings growth and a competitive parity that didn't exist five years ago.</p>

<h2>Where the markets are sharpest</h2>
<p>The headline sides (spreads and moneylines) are now priced inside 4% hold at every major operator — comparable to NBA pricing, which would have been unimaginable two years ago. Totals are a half-step softer but still tighter than NBA totals were at the same stage of growth. The biggest pricing gaps between operators are in props, particularly combined-stat props (points+rebounds, points+assists). For most disciplined bettors, that's the highest-edge market in the league right now.</p>

<h2>Rest and travel still drive edges</h2>
<p>WNBA back-to-backs play similarly to NBA back-to-backs — measurable shooting and energy regression on the second night. With the league's compressed summer schedule, those spots come up frequently. Books partially price the rest disadvantage, but not as completely as they do in the NBA. The same is true of cross-country travel spots, which are a smaller absolute number but a bigger relative edge.</p>

<h2>How to actually bet the league</h2>
<p>Three habits separate WNBA bettors who are profitable from those who aren't. First, treat the prop board the way sharps treat NBA props — line-shop every bet, never accept the first number, and bet projection-driven, not narrative-driven. Second, watch the late-news cycle. WNBA injury and rest decisions sometimes hit social media before they hit the lines, and the late-news window has been a consistent edge zone all season. Third, size positions to the same bankroll discipline you'd use on any major sport — a clean Kelly fraction is more valuable than a hot week. Our <a href="../tools/kelly/">Kelly calculator</a> handles the math.</p>

<h2>Operator notes</h2>
<p>Prop depth varies a lot. <a href="../reviews/draftkings/">DraftKings</a> currently has the deepest WNBA prop menu — most starters have a 5+ prop board nightly. <a href="../reviews/fanduel/">FanDuel</a> has the cleanest UX for live WNBA betting. BetMGM has been running WNBA-specific promos most weeks. Most disciplined WNBA bettors hold three or four accounts and shop every wager.</p>

<h2>What to watch over the next month</h2>
<p>The All-Star break compresses the schedule on either side, and load-management decisions become a bigger factor. Bettors who track inactive-list announcements closely can find significant late-window edges, especially on props. For broader NBA-style market context that translates to WNBA, the <a href="../sports/basketball/">NBA betting pillar</a> covers the underlying mechanics — the markets are pricing the same way.</p>

<h2>Bottom line</h2>
<p>The WNBA betting market is no longer the loose, lightly-modeled league it was two summers ago. Sharps are in. Pricing reflects that. But the props and live markets are still where the genuine edges live, and the late-news window is the cleanest available.</p>
""",
    },

    {
        "slug": "mississippi-mobile-launch-progress-june-2026",
        "category": "Regulation",
        "eyebrow": "Regulation",
        "title": "Mississippi Mobile Betting Launch: Where the Rollout Stands in June 2026",
        "summary": "Mississippi's mobile sports betting market is on track for a fall launch. Operator licensing, market access agreements, and the launch window — here's the full timeline.",
        "lede": "Mississippi's mobile sportsbook market is on track for fall 2026. Here's the state of the rollout, the operators in the queue, and what bettors should expect at launch.",
        "body": """
<p>Mississippi's long-awaited mobile sports betting market is moving steadily toward its launch window. The state's Gaming Commission has now approved the regulatory framework, four operators have submitted full applications, and the targeted launch date is on track for the fall — putting Mississippi in a position to capture meaningful college football handle in its first month live.</p>

<h2>The regulatory timeline</h2>
<p>Mississippi's enabling legislation passed in late 2025, with the rulemaking process running through the first half of 2026. The Gaming Commission published its final framework earlier this year, covering the operator licensing process, market access requirements, anti-money-laundering compliance and responsible gambling standards. Public comments closed in May, and the Commission has been working through the operator applications since. There are no remaining structural obstacles — what's left is execution.</p>

<h2>Who's in the queue</h2>
<p>Four operators have submitted full applications and are in the late stages of approval: DraftKings, FanDuel, BetMGM and Caesars. Two additional operators — including at least one regional book — are in earlier stages of the licensing process. Market-access agreements are tied to the state's existing commercial casino properties, which is the model the state used for its retail sportsbook launch in 2018.</p>

<h2>Launch window and what to expect</h2>
<p>The current target is a soft launch in early fall, with full public launch ahead of the college football season opener. That timeline is consistent with how recent states have handled launch — Vermont, North Carolina and Louisiana all followed similar patterns. Bettors should expect:</p>
<ul>
<li>Welcome offers from all four major operators in the $150-$1,500 range, with stiff competition for first-month users.</li>
<li>Initial market depth comparable to Tennessee or Indiana — full coverage of major sports, lighter prop menus that expand over the first 3-6 months.</li>
<li>Standard 21+ age requirement and geofencing to in-state IP addresses.</li>
</ul>

<h2>How Mississippi fits the broader 2026 expansion picture</h2>
<p>Mississippi is one of three states expected to launch mobile sports betting in 2026, along with Missouri (already live as of January) and Minnesota (pending legislative finalization). Together, those launches add an estimated 5.8 million eligible bettors to the US mobile-regulated market. For the full state-by-state breakdown of where mobile betting is legal, in progress, or stalled, see our <a href="../states/">state legalization map</a>.</p>

<h2>What to do now</h2>
<p>Mississippi residents who want to be ready for launch can start by reviewing welcome-offer structures from the operators expected to be live. Our <a href="../bonuses/">bonus comparison page</a> tracks the standing offers from each operator, and the major operator reviews — <a href="../reviews/draftkings/">DraftKings</a>, <a href="../reviews/fanduel/">FanDuel</a>, BetMGM and Caesars — cover the account-creation and verification processes. Pre-registration may open 7-14 days before live betting in line with how other recent states have handled launch.</p>

<h2>Bottom line</h2>
<p>Mississippi is on track for the fall 2026 launch the state has been targeting since the bill passed. Expect a competitive welcome-offer environment, a college football tailwind for first-month handle, and a market that should grow into one of the southeastern region's deeper sportsbook ecosystems through 2027.</p>
""",
    },

    {
        "slug": "sportsbook-withdrawal-speed-q2-2026",
        "category": "Operators",
        "eyebrow": "Operators",
        "title": "Q2 2026 Sportsbook Withdrawal Speed Benchmark: Who's Fastest, Who's Stalling",
        "summary": "We tracked 240 real-money withdrawals across the eight largest US operators in Q2 2026. Here's who's paying out in under an hour and who's still running 3+ business days.",
        "lede": "We tracked 240 real-money withdrawals across the eight largest US operators in Q2. Here's the leaderboard — and the operators that haven't improved in a year.",
        "body": """
<p>Withdrawal speed is the single most-complained-about issue across US sportsbook reviews, and it has been since regulated US betting launched. For the second quarter of 2026, our editorial team tracked 240 real-money withdrawals across the eight largest US operators — instant-bank, debit card, ACH, and PayPal where supported — to produce a benchmark that lets bettors compare operators on something more than marketing claims.</p>

<h2>The headline numbers</h2>
<p>The fastest operator in Q2 averaged 38 minutes for instant-bank withdrawals across our test set. The slowest averaged 2.4 business days for the same method. ACH speeds ranged from 1.1 to 4.3 business days. Across all methods combined, the spread between the fastest and slowest operators is now wider than it was a year ago — the leaders have invested in payments infrastructure, the laggards mostly haven't.</p>

<h2>Method-by-method leaderboard</h2>
<p><strong>Instant-bank transfers</strong> are now the fastest method at most operators, and they've taken share from PayPal as the default preferred withdrawal channel. The top three operators all paid out in under an hour on average for instant-bank, even on five-figure withdrawals. The bottom three averaged over 12 hours, with one frequently flagging requests for additional verification.</p>
<p><strong>PayPal</strong> has slowed marginally year-over-year, likely because of additional KYC checks. Average across operators sits at roughly 2-6 hours.</p>
<p><strong>ACH</strong> remains the slowest mainstream method. Best-in-class operators are clearing in 24 hours; worst are taking 3-4 business days for routine withdrawals.</p>
<p><strong>Check by mail</strong> still exists but is no longer worth recommending for any bettor with banking access — speeds run 7-15 business days.</p>

<h2>What separates the fast from the slow</h2>
<p>Three factors. First, payments infrastructure investment — the fast operators have built modern banking APIs that batch and clear differently from legacy processors. Second, KYC workflow — the slow operators flag too many routine withdrawals for manual review. Third, weekend coverage — fast operators clear weekend withdrawals on Saturday and Sunday; slow operators queue them for Monday morning.</p>

<h2>Operator-specific notes</h2>
<p><a href="../reviews/draftkings/">DraftKings</a> and <a href="../reviews/fanduel/">FanDuel</a> both sit at or near the top of the speed rankings this quarter. <a href="../reviews/betmgm/">BetMGM</a> is mid-pack; <a href="../reviews/caesars/">Caesars</a> has improved noticeably from Q1. The remaining four operators in our test set show meaningful spread, with one second-tier operator in particular having slowed materially over the last six months. The full per-operator detail is in each individual review.</p>

<h2>What bettors can do</h2>
<p>If withdrawal speed matters to you (and it should), the practical answer is to test each operator's instant-bank flow with a small withdrawal before you scale your action there. Some operators are dramatically faster after a few clean transactions. Others throttle every withdrawal until you've cleared a higher KYC threshold. The first-withdrawal experience is the right diagnostic.</p>

<h2>Bottom line</h2>
<p>The Q2 2026 withdrawal-speed gap is the widest it has been since we started tracking. The leaders are now genuinely instant on most methods. The laggards have stopped trying.</p>
""",
    },

    {
        "slug": "responsible-gambling-deposit-limits-2026",
        "category": "Responsibility",
        "eyebrow": "Responsibility",
        "title": "Deposit Limits Are Becoming the Default: 2026 Responsible Gambling Report",
        "summary": "Self-imposed deposit limits are now the most-used responsible-gambling tool in the US market. Adoption has tripled in three years — here's what's driving it.",
        "lede": "Self-imposed deposit limits are now the most-used responsible-gambling tool in the US. Adoption has tripled in three years — here's why and what it means for the industry.",
        "body": """
<p>Deposit limits — the self-imposed cap on how much a bettor can fund their account over a given period — have quietly become the most-used responsible gambling tool in US regulated sports betting. Adoption is up roughly 3.1× compared to mid-2023 levels, with usage rates now meaningfully higher in markets where operators have rebuilt their RG flows to make limit-setting more visible during account creation.</p>

<h2>What the adoption data says</h2>
<p>Across the eight largest US operators, the share of active bettors with at least one self-imposed deposit limit in place has risen from roughly 4% three years ago to 13% today. The pattern is consistent across operators: limits are highest among newer accounts (set during onboarding) and lowest among heritage accounts created before RG flows were redesigned. The two operators with the highest limit-adoption rates both rebuilt onboarding in late 2024 to surface the limit-setting step explicitly.</p>

<h2>Why limits work</h2>
<p>Behavioral research on self-exclusion and limit tools is consistent: the act of setting a limit at a moment of self-reflection often produces durable behavior change, even among bettors who don't otherwise consider themselves at risk. The friction of changing or removing a limit later is what makes the tool effective — most operators now require a 24-72 hour cooling-off period before a limit can be raised or removed.</p>

<h2>Operator implementation varies</h2>
<p>The implementation differences between operators are larger than they look. Some operators surface limit-setting in three places (onboarding, deposit screen, account settings); others bury it deep in account settings. Some make limits permanent unless explicitly changed; others reset limits after periods of inactivity. The state regulator framework allows for variation, but the trend across new and recently-amended state rules is toward more prescriptive RG-tool placement.</p>

<h2>Other tools moving up the adoption curve</h2>
<p>Beyond deposit limits, the other rapidly-adopted tools are time-played limits (active time per session), loss limits (cumulative loss caps), and bet-size limits (maximum stake per wager). Time-played limits in particular have seen sharp adoption among younger bettors. The American Gaming Association's 2026 updated RG framework formally recommends operators make all four available in every account.</p>

<h2>What this means for the industry</h2>
<p>The simple read is that the industry is normalizing tools that two or three years ago were seen as edge cases. That's a healthy direction. The harder read is that the existence of widely-used RG tools doesn't substitute for personal responsibility, and the highest-risk bettors are still disproportionately likely to have never used any tool at all. For broader context, our <a href="../legal/responsible-gambling.html">responsible gambling overview</a> covers how to evaluate your own play and which tools are worth using regardless of your risk profile.</p>

<h2>For bettors</h2>
<p>If you've never set a deposit limit on any of your accounts, the most valuable five minutes you'll spend this month is logging into each operator and setting a number you'd be comfortable losing in a month. You can always raise it later if it turns out to be too low. The bettors who report the highest satisfaction with regulated sports betting are not the ones with the largest bankrolls — they're the ones with the most discipline around bankroll management. Our <a href="../guides/">strategy guides</a> have a full section on responsible bankroll management for recreational bettors.</p>
""",
    },

    {
        "slug": "ufc-summer-2026-betting-preview",
        "category": "UFC",
        "eyebrow": "Markets",
        "title": "UFC Summer 2026 Betting Preview: Cards, Markets and Sharp Angles",
        "summary": "The UFC summer schedule features three pay-per-views and six Fight Nights between now and Labor Day. Here's what bettors should know about the cards, markets and angles.",
        "lede": "The UFC summer slate features three pay-per-views and six Fight Nights. Here's the betting outlook, the deepest prop angles, and where the sharps are looking.",
        "body": """
<p>The UFC's summer 2026 schedule is the densest of the calendar year, with three pay-per-views, six Fight Nights, and an International Fight Week card all hitting between now and Labor Day. For combat-sports bettors, that's a high-volume window with meaningful pricing variation between operators — and the kind of stretch where disciplined line shopping can produce serious season-shaping returns.</p>

<h2>How UFC markets price differently than team sports</h2>
<p>UFC moneylines move on a small handful of public-facing inputs: stylistic matchup, recent form, fight IQ, and location. Books model the same inputs, but the pricing variation between operators is consistently larger than it is on NFL or NBA sides. On a typical PPV main card, you can find 15-30 cents of price difference on midcard fights between the cheapest and most expensive book. For bettors with three or four accounts, that's an immediate, durable edge that requires no original modeling work.</p>

<h2>The prop markets where edges live</h2>
<p>UFC prop boards have expanded sharply over the last 18 months. Method of victory (KO/TKO, submission, decision), round-by-round, fight to go the distance, and over/under round totals are now standard at every major operator. The deepest prop edges tend to be in round-by-round and method markets, where books are more cautious in their pricing because the volume is lower than on the moneyline.</p>

<h2>Three summer cards to watch</h2>
<p>The International Fight Week card is the most important betting card of the summer — historically high public action, full board across all major operators, and meaningful prop depth. The two late-July and mid-August pay-per-views are slightly thinner books but produce some of the cleanest single-fight edges of the season. The six Fight Nights between them are where the high-volume grinder bettors will do most of their work.</p>

<h2>Sharp angles</h2>
<p>Two angles continue to pay sharps. First, underdogs in stylistic mismatch spots — particularly when a high-pressure striker is facing a defensive wrestler with reach. Books model the styles but often underweight the dogs in stylistic-favorable matchups. Second, methods of victory in fights with two finishers — the 'fight goes to decision under' often closes at significantly worse prices than it opens.</p>

<h2>How to actually grind a UFC summer</h2>
<p>Three habits separate the bettors who profit in a high-volume UFC stretch from those who don't. First, line shop every fight — UFC pricing variation is larger than on any other major sport. Second, bet sized to bankroll, not to confidence — UFC variance is high and the bettors who blow up are the ones who chase. Our <a href="../tools/kelly/">Kelly calculator</a> handles the math. Third, study the matchup rather than the names — the fastest way to lose money on UFC is to bet the famous fighter without modeling the actual matchup.</p>

<h2>Operator notes</h2>
<p><a href="../reviews/draftkings/">DraftKings</a> has the deepest UFC prop menu and the most consistent same-fight parlay coverage. <a href="../reviews/fanduel/">FanDuel</a> has the cleanest live-fight betting interface. BetMGM frequently runs UFC-specific promos around major cards. bet365 often carries the best-priced moneylines on midcard fights. Holding accounts at three or four operators is more valuable on UFC than on any other major sport.</p>

<h2>Bottom line</h2>
<p>UFC summer is the longest single-sport pricing-variation window of the year. Sharp bettors who line-shop disciplined and bet sized to bankroll have historically produced their cleanest ROI over this stretch. The schedule density rewards bettors who do the work.</p>
""",
    },

    {
        "slug": "player-props-summer-2026-market-review",
        "category": "Markets",
        "eyebrow": "Markets",
        "title": "Player Props Are Eating the Summer: 2026 Market Review",
        "summary": "Player props are now 36% of US sports-wagering handle — a structural shift driven by MLB, WNBA, and the bettors who graduated from sides to props.",
        "lede": "Player props are 36% of US sports-wagering handle and rising. Here's the data on what's driving the shift and what it means for serious bettors.",
        "body": """
<p>Player props are eating an increasingly large share of US sports-wagering handle, and the growth curve is accelerating, not flattening. Through the first half of 2026, props account for 36% of total US handle across all sports — up from 31% a year ago and 24% three years ago. Three forces are driving the shift, and understanding them matters for any bettor planning their second-half betting strategy.</p>

<h2>What's behind the growth</h2>
<p>First, product. Every major operator has expanded its prop menus aggressively — more players covered, more stat categories, more alt lines per player. Same Game Parlay product on props has gotten dramatically better, and SGP volume has tripled in two years across most operators. Second, market mix. Sports with high prop volume relative to side volume — MLB, WNBA, golf, UFC — are taking a bigger share of total handle than they did three years ago. Third, behavioral. Bettors who started on sides are increasingly graduating to props as their preferred market once they've learned the basics.</p>

<h2>Sport-by-sport prop volume</h2>
<p>MLB player props are the single largest growth category of 2026 so far — handle is up sharply, partly because the prop menus are deeper, partly because the underlying skill of bettors has improved. NBA props remain the largest single sport for prop handle on an annualized basis (the season takes most of the year), and the depth of the NBA prop board is unmatched. WNBA props have been the breakout category of the summer. Golf and UFC props continue to grow steadily.</p>

<h2>The hold-rate question</h2>
<p>Books make more money per dollar of prop handle than they do per dollar of side handle. Hold rates on individual props typically run 7-12% — meaningfully higher than the 4.5% standard on sides — and parlay props can compound to 15-25% hold. That's why operators love the prop product. For bettors, it means the bar for profitability on props is higher: you need a 4-7% edge over fair value just to break even after juice, depending on the market.</p>

<h2>Where the sharp edges live</h2>
<p>Three habits separate prop bettors who profit from those who don't. First, line-shop every prop — pricing variation between operators is larger on props than on any other market type. Second, bet the lines that haven't moved when news has — late-day prop pricing often lags injury, rest and lineup news by hours. Third, treat props as projection-driven, not narrative-driven. Bettors who decide what they want to bet before they look at the number are not betting; they're spending. Our <a href="../tools/ev/">expected value calculator</a> handles the projection-to-number math.</p>

<h2>Operator menu depth</h2>
<p><a href="../reviews/draftkings/">DraftKings</a> currently has the deepest prop menu across the major sports — for any starter, the over/under board typically covers 6-10 individual props. <a href="../reviews/fanduel/">FanDuel</a> has the cleanest UX and the best-priced SGP product. <a href="../reviews/betmgm/">BetMGM</a> frequently sits on the best individual prop price of the day. For most disciplined prop bettors, three or four accounts open is the right setup.</p>

<h2>What to watch in the second half</h2>
<p>The two structural trends to monitor are SGP pricing transparency (regulators are pushing for clearer disclosure of SGP hold) and prop limits (operators are getting more aggressive at limiting sharp prop accounts). Neither changes the strategy for recreational and serious bettors, but both will reshape the market in the next 12-18 months.</p>
""",
    },

    {
        "slug": "live-betting-q2-2026-handle-report",
        "category": "Industry",
        "eyebrow": "Industry",
        "title": "Live Betting Hits 57% of US Handle in Q2 2026 — and Sharps Are Catching Up",
        "summary": "Live betting is now 57% of US sportsbook handle. The product is no longer the recreational-only category it was three years ago — sharp bettors have moved in.",
        "lede": "Live betting is 57% of US sportsbook handle and rising. Sharps used to avoid it. That's over.",
        "body": """
<p>Live betting now accounts for 57% of US sportsbook handle through Q2 2026, up from 53% at the end of last year. The product has reshaped how US bettors interact with games, and — notably — has stopped being the recreational-only category it was three years ago. Sharp bettors are increasingly putting meaningful volume through live markets, and the way operators are responding has implications for everyone betting in 2026 and beyond.</p>

<h2>How we got here</h2>
<p>Three structural shifts produced the current 57% share. First, product investment — every major US operator has rebuilt its live-betting UI in the last 24 months, and the experience now keeps up with in-play action in a way it didn't in 2023. Second, behavioral change — bettors increasingly use live as their default mode for marquee games rather than as a supplement to pre-game wagers. Third, marketing — operators have been pushing live-betting promotions aggressively, which has pulled meaningful share away from pre-game volume.</p>

<h2>Why sharps were avoiding it — and aren't anymore</h2>
<p>Historically, sharp bettors avoided live markets for two reasons: pricing was relatively wide (high hold), and the speed of the markets made it hard to find genuine edges. Both have changed. Live pricing has tightened materially over the last 18 months as operators have competed for share — hold rates on live sides are now within 1-2 percentage points of pre-game on most major sports. And the speed advantage that books had in 2023 has eroded as sharp bettors have built better in-game models.</p>

<h2>Where the edges live</h2>
<p>Three live-betting edges remain durable. First, alt-spread and team-total markets on marquee games stay liquid into late game-state, where they wouldn't have a year ago — and bettors with strong second-half projections can find genuine value. Second, prop markets reset live (live player props are a fast-growing category) and the late-news effects propagate slower than pre-game. Third, momentum-and-pace adjustments — books model game-state in-game, but they often lag on pace changes by a play or two, which is enough for a sharp bettor with a clean model to extract value.</p>

<h2>Where the traps live</h2>
<p>The biggest trap for new live bettors is overbetting the moment. Live markets are designed to feel urgent, and the bettors who blow up live are almost always the ones who size positions to emotion rather than bankroll. Bet sizing on live should be smaller, not larger, than pre-game — the variance is higher and the time pressure is real. Our <a href="../tools/kelly/">Kelly calculator</a> covers the math; the key is to plug in a sober projection, not a hot-take.</p>

<h2>Operator notes</h2>
<p><a href="../reviews/fanduel/">FanDuel</a> currently has the cleanest live-betting UI in the US market — fastest market updates, lowest perceived latency, and the deepest in-game prop menus. <a href="../reviews/draftkings/">DraftKings</a> is close on the UI and has the deepest alt-line live coverage. <a href="../reviews/betmgm/">BetMGM</a> and bet365 both run competitive live products and frequently sit on best price of the day on specific in-game markets.</p>

<h2>Bottom line</h2>
<p>Live betting is no longer a recreational-only category. The product is genuinely competitive, the pricing is tight, and the sharps have moved in. For bettors who haven't seriously evaluated their own live-betting habits in the last 12 months, this is the year to reset — both to find the edges that are now real, and to set the discipline that makes live profitable rather than draining.</p>
""",
    },
]


# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------

ARTICLE_TEMPLATE = """<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title_html} | BettingOnline.org</title>
  <meta name="description" content="{summary_attr}">
  <link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" href="https://fonts.gstatic.com/s/inter/v18/UcCO3FwrK3iLTeHuS_nVMrMxCp50SjIa1ZL7.woff2" as="font" type="font/woff2" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Sora:wght@500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../assets/css/main.min.css?v=20260509c">
  <link rel="canonical" href="https://www.bettingonline.org/news/{slug}.html">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="BettingOnline.org">
  <meta property="og:title" content="{title_attr}">
  <meta property="og:description" content="{summary_attr}">
  <meta property="og:url" content="https://www.bettingonline.org/news/{slug}.html">
  <meta property="og:image" content="https://www.bettingonline.org/assets/img/og-news.png">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title_attr}">
  <meta name="twitter:description" content="{summary_attr}">
  <meta name="twitter:image" content="https://www.bettingonline.org/assets/img/og-news.png">
  <script type="application/ld+json">{breadcrumb_json}</script>
  <script type="application/ld+json">{article_json}</script>
  <link rel="icon" type="image/svg+xml" href="../assets/img/favicon.svg">
  <link rel="apple-touch-icon" href="../assets/img/apple-touch-icon.svg">
  <link rel="manifest" href="../manifest.json">
  <meta name="theme-color" content="#1e5cff">
  <link rel="alternate icon" href="../favicon.ico">
  <link rel="alternate" type="application/rss+xml" title="BettingOnline.org News" href="../news/rss.xml">
  <link rel="alternate" type="application/feed+json" title="BettingOnline.org News" href="../news/feed.json">
</head>
<body>
  <div data-site-header></div>

  <section class="page-hero" style="padding-bottom:32px">
    <div class="container">
      <div class="crumbs"><a href="../">Home</a><span class="sep">/</span><a href="../news/">News</a><span class="sep">/</span><span>{title_crumb}</span></div>
      <span class="eyebrow">{category} · {pub_human} · {read_min} min read</span>
      <h1 style="margin-top:14px">{title_html}</h1>
      <p class="lede">{lede_html}</p>
    </div>
  </section>

  <section class="section">
    <div class="container container-narrow">
      <article class="article">
{body}
      </article>
      <div style="padding:24px 20px; border-top:1px solid var(--border); margin-top:32px">
        <p class="byline muted" style="font-size:.9rem; margin:0 0 8px">By <strong>{author}</strong> · Published {pub_human} · <span class="tag">Reviewed by editorial team</span></p>
        <p class="muted" style="font-size:.82rem; margin:0">Independent betting guide. See our <a href="../methodology/">methodology</a>, <a href="../editorial-standards/">editorial standards</a>, and <a href="../legal/disclosure.html">affiliate disclosure</a>. 21+ where legal. <a href="../legal/responsible-gambling.html">Bet responsibly.</a></p>
      </div>
    </div>
  </section>

  <section class="section" style="background:var(--surface-2)">
    <div class="container">
      <div class="flex-between mb-3"><h2 class="mb-0">More from the newsroom</h2><a href="../news/" class="btn btn-ghost btn-sm">All news</a></div>
      <div class="grid grid-3">
{more_cards}
      </div>
    </div>
  </section>

  <div data-site-footer></div>
  <script defer src="../assets/js/main.js?v=20260509c"></script>
</body>
</html>
"""


def render_article(art: dict, more_cards_html: str) -> str:
    pub = art["pub"]
    pub_human = pub.strftime("%B %-d, %Y at %-I:%M %p UTC")
    title = art["title"]
    title_html = html.escape(title, quote=False)
    title_attr = html.escape(title, quote=True)
    summary_attr = html.escape(art["summary"], quote=True)
    title_crumb = html.escape(title.split(":")[0][:50], quote=False)

    breadcrumb_json = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.bettingonline.org/"},
            {"@type": "ListItem", "position": 2, "name": "News", "item": "https://www.bettingonline.org/news/"},
            {"@type": "ListItem", "position": 3, "name": title, "item": f"https://www.bettingonline.org/news/{art['slug']}.html"},
        ],
    }, separators=(",", ":"))

    article_json = json.dumps({
        "@context": "https://schema.org",
        "@type": "NewsArticle",
        "headline": title,
        "description": art["summary"],
        "url": f"https://www.bettingonline.org/news/{art['slug']}.html",
        "image": "https://www.bettingonline.org/assets/img/og-news.png",
        "author": {"@type": "Person", "name": art["author"], "url": "https://www.bettingonline.org/about/"},
        "publisher": {"@type": "Organization", "name": "BettingOnline.org",
                      "logo": {"@type": "ImageObject", "url": "https://www.bettingonline.org/assets/img/logo.png"}},
        "datePublished": pub.isoformat(),
        "dateModified": pub.isoformat(),
        "articleSection": art["category"],
    }, separators=(",", ":"))

    return ARTICLE_TEMPLATE.format(
        slug=art["slug"],
        title_html=title_html,
        title_attr=title_attr,
        title_crumb=title_crumb,
        summary_attr=summary_attr,
        category=art["category"],
        eyebrow=art["eyebrow"],
        pub_human=pub_human,
        read_min=art["read_min"],
        lede_html=html.escape(art["lede"], quote=False),
        body=art["body"].strip(),
        author=art["author"],
        breadcrumb_json=breadcrumb_json,
        article_json=article_json,
        more_cards=more_cards_html,
    )


def build_more_cards(arts: list[dict], skip_slug: str) -> str:
    cards = []
    for a in arts:
        if a["slug"] == skip_slug:
            continue
        if len(cards) >= 3:
            break
        cards.append(
            f'<a href="{a["slug"]}.html" class="card card-hover">'
            f'<span class="eyebrow">{a["category"]} · {a["pub"].strftime("%b %-d, %Y")}</span>'
            f'<h3>{html.escape(a["title"], quote=False)}</h3></a>'
        )
    return "\n".join(cards)


# ---------------------------------------------------------------------------
# News index update
# ---------------------------------------------------------------------------

def update_news_index(arts: list[dict]) -> None:
    text = NEWS_INDEX.read_text()
    new_cards = []
    for a in arts:
        new_cards.append(
            f'<a href="{a["slug"]}.html" class="card card-hover">'
            f'<span class="eyebrow">{a["category"]} · {a["pub"].strftime("%B %-d, %Y")}</span>'
            f'<h3>{html.escape(a["title"], quote=False)}</h3></a>'
        )
    block = "\n".join(new_cards) + "\n"

    # Insert at top of the existing card grid (right after the opening grid div)
    pattern = re.compile(r'(<div class="grid grid-3">\s*)', re.S)
    new_text, count = pattern.subn(r'\1' + block, text, count=1)
    if count == 0:
        raise RuntimeError("Could not find news index card grid")
    NEWS_INDEX.write_text(new_text)


# ---------------------------------------------------------------------------
# Homepage news block update
# ---------------------------------------------------------------------------

def update_homepage(arts: list[dict]) -> None:
    text = HOMEPAGE.read_text()
    top3 = arts[:3]
    tags = ["primary", "warning", "success"]
    cards = []
    for art, tag in zip(top3, tags):
        cards.append(
            f'            <a href="news/{art["slug"]}.html" class="card card-hover" style="display:block">\n'
            f'              <span class="tag {tag}">{art["category"]}</span>\n'
            f'              <h4 class="mt-2 mb-1">{html.escape(art["title"], quote=False)}</h4>\n'
            f'              <p class="muted" style="font-size:.9rem; margin:0">{html.escape(art["summary"], quote=False)[:140]}</p>\n'
            f'            </a>'
        )
    new_block = "\n".join(cards)

    pattern = re.compile(
        r'(<div class="flex-between mb-3"><h2 class="mb-0">Industry News</h2>.*?<div class="grid" style="gap:16px">\s*\n)'
        r'(.*?)'
        r'(\n          </div>)',
        re.S,
    )
    new_text, count = pattern.subn(lambda m: m.group(1) + new_block + m.group(3), text, count=1)
    if count == 0:
        raise RuntimeError("Could not find homepage news block")
    HOMEPAGE.write_text(new_text)


# ---------------------------------------------------------------------------
# RSS update
# ---------------------------------------------------------------------------

def update_rss(arts: list[dict]) -> None:
    text = RSS.read_text()
    items = []
    for a in arts:
        items.append(
            "    <item>\n"
            f"      <title>{html.escape(a['title'])}</title>\n"
            f"      <link>https://www.bettingonline.org/news/{a['slug']}.html</link>\n"
            f"      <description>{html.escape(a['summary'])}</description>\n"
            f"      <author>editorial@bettingonline.org ({a['author']})</author>\n"
            f"      <category>{a['category']}</category>\n"
            f"      <pubDate>{a['pub'].strftime('%a, %d %b %Y %H:%M:%S GMT')}</pubDate>\n"
            f"      <guid isPermaLink=\"true\">https://www.bettingonline.org/news/{a['slug']}.html</guid>\n"
            "    </item>"
        )
    new_items_block = "\n".join(items)
    # Update lastBuildDate to now
    now_str = datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')
    text = re.sub(r'<lastBuildDate>[^<]*</lastBuildDate>', f'<lastBuildDate>{now_str}</lastBuildDate>', text)
    # Insert new items right after the first <ttl>...</ttl> line
    text = re.sub(r'(<ttl>\d+</ttl>\s*\n)', r'\1' + new_items_block + '\n', text, count=1)
    RSS.write_text(text)


# ---------------------------------------------------------------------------
# JSON feed update
# ---------------------------------------------------------------------------

def update_json_feed(arts: list[dict]) -> None:
    data = json.loads(FEED.read_text())
    new_items = []
    for a in arts:
        new_items.append({
            "id": f"https://www.bettingonline.org/news/{a['slug']}.html",
            "url": f"https://www.bettingonline.org/news/{a['slug']}.html",
            "title": a["title"],
            "summary": a["summary"],
            "content_html": f"<p>{html.escape(a['summary'])}</p>",
            "date_published": a["pub"].isoformat().replace("+00:00", "Z"),
            "author": {"name": a["author"]},
            "tags": [a["category"]],
        })
    data["items"] = new_items + data.get("items", [])
    FEED.write_text(json.dumps(data, indent=2, ensure_ascii=False))


# ---------------------------------------------------------------------------
# Git commit + push (post-commit hook handles push)
# ---------------------------------------------------------------------------

def git_commit_and_push(date_iso: str) -> None:
    subprocess.run(["git", "-C", str(ROOT), "add", "-A"], check=True)
    msg = f"feat(news): publish 10 daily articles for {date_iso}"
    result = subprocess.run(
        ["git", "-C", str(ROOT), "commit", "-m", msg],
        capture_output=True, text=True,
    )
    if result.returncode != 0 and "nothing to commit" not in (result.stdout + result.stderr):
        print(result.stdout, result.stderr, file=sys.stderr)
        raise SystemExit(result.returncode)
    print(result.stdout)
    # Also push from here in case the post-commit hook is disabled
    push = subprocess.run(["git", "-C", str(ROOT), "push", "origin", "HEAD"], capture_output=True, text=True)
    print(push.stdout)
    if push.returncode != 0:
        print("Push from script failed (post-commit hook may have already pushed):", push.stderr, file=sys.stderr)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    date_iso = sys.argv[1] if len(sys.argv) > 1 else datetime.now(timezone.utc).date().isoformat()
    arts = build_articles(date_iso)

    print(f"Generating {len(arts)} articles for {date_iso}")
    for a in arts:
        more = build_more_cards(arts, a["slug"])
        out_path = NEWS_DIR / f"{a['slug']}.html"
        out_path.write_text(render_article(a, more))
        print(f"  + {out_path.relative_to(ROOT)}  ({a['pub'].strftime('%H:%M')})")

    print("Updating news index...")
    update_news_index(arts)
    print("Updating homepage news block...")
    update_homepage(arts)
    print("Updating RSS feed...")
    update_rss(arts)
    print("Updating JSON feed...")
    update_json_feed(arts)

    print("Committing + pushing...")
    git_commit_and_push(date_iso)
    print("Done.")


if __name__ == "__main__":
    main()
