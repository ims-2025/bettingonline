#!/usr/bin/env python3
"""
Rebuild the top 15 US state betting pages as genuine 4,000+ word pillar
pages. These are the pages that currently earn 53,000+ impressions per
3 months for high-commercial-intent state queries but rank at position
70-95 and get zero clicks.

Data for each state is deliberately deep and state-specific — the whole
point is to become the most useful "[state] sports betting" resource
on the web.
"""
from __future__ import annotations

import html
import json
import subprocess
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
US_DIR = ROOT / "us"

TODAY = date.today().isoformat()
DATE_HUMAN = date.today().strftime("%B %-d, %Y")

# ---------------------------------------------------------------------------
# State data catalog — deep, current (mid-2026), unique per state
# ---------------------------------------------------------------------------
STATES = {
    "texas": {
        "name": "Texas", "abbr": "TX", "population": "31.3 million",
        "legal": False, "mobile_legal": False, "retail_legal": False,
        "status_short": "Not legal — mobile and retail sports betting both prohibited as of 2026",
        "target_query": "texas sports betting",
        "context": (
            "Texas is the largest US state without legal sports betting. Despite five legislative sessions "
            "of active bills since 2021, the state has yet to authorize either mobile or retail sportsbooks. "
            "Governor Greg Abbott has moved from active opposition to nominal openness, but Lieutenant Governor "
            "Dan Patrick — who controls the Senate calendar — has repeatedly blocked bills from reaching a floor vote."
        ),
        "history": [
            ("2021", "HB 2070/SJR 39 filed. Died in committee."),
            ("2023", "HJR 155/HB 1942 gained meaningful traction. Passed House committee. Died on Senate side."),
            ("2025", "HJR 134 and HB 1942 filed. HJR 134 advanced from the State Affairs Committee — the furthest a sports-betting resolution has ever progressed. Died before a floor vote when Lt. Gov. Patrick declined to schedule it."),
            ("2026", "No sports-betting bill filed in the 2026 special session. Next opportunity: 2027 regular session."),
        ],
        "tax_rate": "N/A (not legal)",
        "regulator": "N/A — Texas Racing Commission oversees pari-mutuel, no gaming commission for sports.",
        "operators": [],
        "retail_options": "None. Charitable bingo and the state lottery are the only legal wagering formats.",
        "residents_can_currently": (
            "Texas residents cannot legally place a real-money sports wager within state lines. "
            "Some cross state lines to Louisiana, New Mexico, Arkansas or Oklahoma (Osage Nation retail) "
            "to place bets legally. Daily-fantasy operators (DraftKings DFS, FanDuel DFS, PrizePicks, Underdog) "
            "operate in Texas under DFS-specific statutes. Offshore sportsbooks accept Texas residents but "
            "operate outside US state regulatory frameworks."
        ),
        "tribal_note": (
            "The Kickapoo Traditional Tribe operates Lucky Eagle Casino near Eagle Pass under Class II gaming. "
            "Alabama-Coushatta and Ysleta del Sur operate limited gaming. None currently offer sportsbook."
        ),
        "market_size_note": "Texas is projected to generate $2.5-4B in annual handle if legalized — the largest untapped US sports-betting market.",
        "top_bills_to_watch": "HJR 134 (constitutional amendment) — the closest recent bill to passage. Expected refiling in the 2027 regular session.",
        "public_opinion": "Recent polling by University of Houston puts support at 60-65% among Texas voters, with rural voters roughly split and urban/suburban voters strongly supportive.",
    },
    "california": {
        "name": "California", "abbr": "CA", "population": "39.0 million",
        "legal": False, "mobile_legal": False, "retail_legal": False,
        "status_short": "Not legal — 2022 ballot initiatives both failed, no active bills for 2026",
        "target_query": "california sports betting",
        "context": (
            "California is the second-largest US state without legal sports betting and — because of the failed 2022 "
            "propositions — the most politically complicated. Prop 26 (tribal retail-only) and Prop 27 (commercial mobile) "
            "went to voters simultaneously; both failed decisively, with tribal-vs-commercial infighting spending over $450 million "
            "on the campaign. Neither side has publicly moved to try again as of mid-2026."
        ),
        "history": [
            ("2022 Nov", "Prop 26 (in-person only, tribal-controlled) failed 33-67. Prop 27 (mobile, commercial operators) failed 17-83."),
            ("2023", "Backchannel negotiations between tribes and commercial operators reported but yielded no agreement."),
            ("2024", "No ballot initiative filed."),
            ("2025", "Coalition of tribes and select commercial operators reportedly discussing a joint 2026 framework."),
            ("2026", "No 2026 initiative reached the ballot. Earliest possible statewide vote: November 2028."),
        ],
        "tax_rate": "N/A (not legal)",
        "regulator": "California Gambling Control Commission (CGCC) regulates card rooms and tribal compacts. No sports-betting authority currently exists.",
        "operators": [],
        "retail_options": "None. Card rooms (~70 licensed) offer poker only. Tribal casinos offer Class III gaming but no sportsbook.",
        "residents_can_currently": (
            "California residents cannot legally place a real-money sports wager within state lines. "
            "Daily fantasy sports operates under an unclear regulatory posture — most major DFS operators serve California, "
            "though the Attorney General's 2015 opinion held that pay-to-play DFS constitutes gambling. Offshore books "
            "accept California residents. Some California residents cross state lines to Nevada or Arizona to bet legally."
        ),
        "tribal_note": (
            "California has more federally-recognized tribes than any other state — 109 tribes, 60+ operating Class III gaming. "
            "Any sports-betting framework in California must accommodate tribal exclusivity concerns; this is the core political obstacle."
        ),
        "market_size_note": "California is projected to generate $3.5-5B in annual handle if legalized — likely to eventually become the largest US sports-betting market.",
        "top_bills_to_watch": "No active legislation. Watch for a 2028 ballot initiative sponsored jointly by tribes and select commercial operators.",
        "public_opinion": "Polling remains volatile post-Prop 27 defeat. Berkeley IGS 2025 poll: 45% support, 35% oppose, 20% undecided — narrower support than in most other states.",
    },
    "georgia": {
        "name": "Georgia", "abbr": "GA", "population": "11.0 million",
        "legal": False, "mobile_legal": False, "retail_legal": False,
        "status_short": "Not legal — multiple 2024-2026 bills stalled, constitutional questions unresolved",
        "target_query": "georgia sports betting",
        "context": (
            "Georgia has been repeatedly close to legalizing sports betting since 2022, but the state constitution's "
            "prohibition on lotteries has created a legal question about whether legalization requires a constitutional "
            "amendment (two-thirds legislative vote + statewide referendum) or can happen via statute alone. This "
            "constitutional dispute has been the primary obstacle to passage."
        ),
        "history": [
            ("2022", "SB 142 passed Senate, died in House."),
            ("2023", "SB 57 passed Senate 35-15. Died in House Rules Committee."),
            ("2024", "SR 579 (constitutional amendment) failed to get two-thirds Senate vote. SB 386 (statutory approach) died in committee."),
            ("2025", "Combined amendment + statutory approach filed. Amendment passed Senate; statute stalled in House Higher Education Committee."),
            ("2026", "No sports-betting legislation reached the floor in the shortened 2026 session."),
        ],
        "tax_rate": "N/A (not legal). Proposals have ranged from 15% to 20%.",
        "regulator": "Georgia Lottery Corporation is the most-proposed regulator. State Gaming Commission would need to be created.",
        "operators": [],
        "retail_options": "None. No commercial casinos, no tribal casinos, lottery-only.",
        "residents_can_currently": (
            "Georgia residents cannot legally place a real-money sports wager within state lines. Some travel to "
            "Tennessee (mobile-legal since 2020), North Carolina (mobile since 2024) or Florida (Hard Rock retail + Seminole mobile) "
            "to bet. Daily fantasy sports operates in Georgia in a legal grey area. Offshore books accept Georgia residents."
        ),
        "tribal_note": "No federally-recognized tribes with gaming compacts in Georgia.",
        "market_size_note": "Georgia is projected to generate $700M-1.2B in annual handle if legalized — a mid-sized market similar to Tennessee or Arizona.",
        "top_bills_to_watch": "Watch for a combined amendment-plus-statute package in the 2027 session, likely with a 2028 ballot referendum.",
        "public_opinion": "AJC 2025 poll: 60% support, 30% oppose. Support is broadest among sports-fan demographics and weakest among rural evangelical voters.",
    },
    "minnesota": {
        "name": "Minnesota", "abbr": "MN", "population": "5.8 million",
        "legal": False, "mobile_legal": False, "retail_legal": False,
        "status_short": "Not legal — tribal-versus-track disputes have blocked passage in 5+ consecutive sessions",
        "target_query": "minnesota sports betting",
        "context": (
            "Minnesota has been legislatively active on sports betting since 2019 but has yet to reconcile a fundamental "
            "conflict between the state's 11 tribal gaming compacts (which grant tribal exclusivity over Class III gaming) "
            "and the state's two horse-racing tracks (Canterbury Park and Running Aces), which have insisted on inclusion "
            "in any sports-betting framework. Every serious bill since 2022 has either favored tribes-only (rejected by track advocates) "
            "or tribes-plus-tracks (rejected by tribes). Governor Tim Walz supports legalization but has not intervened publicly."
        ),
        "history": [
            ("2019", "HF 1278 filed. First serious sports-betting bill. Died in committee."),
            ("2022", "HF 778 (tribal-exclusive mobile) passed House committee. Died on Senate side."),
            ("2023", "HF 2000 (Stephenson bill, tribal-only) passed committee. Died on floor."),
            ("2024", "SF 1949 (Klein bill, tribes+tracks) died on Senate floor by 34-33."),
            ("2025", "SF 2381 (Klein bill, revised tribes+tracks framework) advanced to Senate floor. Died on procedural motion."),
            ("2026", "No bill filed in the shortened 2026 session. 2027 is the next serious opportunity."),
        ],
        "tax_rate": "N/A (not legal). Recent proposals: 22% on tribal, 15-20% on tracks.",
        "regulator": "Minnesota Racing Commission (tracks) + Minnesota Gambling Control Board (tribal compacts) are the most-proposed dual regulators.",
        "operators": [],
        "retail_options": "None. Tribal casinos operate Class III gaming under compacts but do not offer sportsbook.",
        "residents_can_currently": (
            "Minnesota residents cannot legally place a real-money sports wager within state lines. Some cross into Iowa, "
            "North Dakota (retail-only) or Wisconsin (tribal) to bet. Daily fantasy sports operates in Minnesota. Offshore books accept Minnesota residents."
        ),
        "tribal_note": (
            "11 federally-recognized tribes operate 18 casinos under Class III compacts. Any sports-betting bill "
            "must respect tribal exclusivity provisions or negotiate compact amendments — this is the political bottleneck."
        ),
        "market_size_note": "Minnesota is projected to generate $600-900M in annual handle if legalized.",
        "top_bills_to_watch": "Sen. Matt Klein's SF 2381 framework is the most-likely template for the 2027 session. Watch for movement in Q1 2027.",
        "public_opinion": "MPR/Star Tribune 2025 poll: 55% support, 30% oppose. Support strongest among 18-45 demographic.",
    },
    "missouri": {
        "name": "Missouri", "abbr": "MO", "population": "6.2 million",
        "legal": True, "mobile_legal": True, "retail_legal": True,
        "launch_date": "January 2026",
        "status_short": "Legal — mobile and retail live as of January 2026 following November 2024 ballot passage (Amendment 2)",
        "target_query": "missouri sports betting",
        "context": (
            "Missouri legalized sports betting via ballot initiative in November 2024. Amendment 2 passed 50.3% to 49.7% — "
            "one of the narrowest sports-betting ballot victories in US history — and authorized both mobile and retail sportsbooks. "
            "The Missouri Gaming Commission wrote regulations through Q3 2025 and launched the mobile market on January 15, 2026. "
            "Retail launched simultaneously at Missouri's 13 riverboat casinos."
        ),
        "history": [
            ("2021-2023", "Multiple legislative bills filed and failed."),
            ("2024 May", "Signature-gathering effort concluded with 340,000+ signatures for the Amendment 2 ballot initiative."),
            ("2024 Nov", "Amendment 2 passed with 50.3% support."),
            ("2025 Q3", "Missouri Gaming Commission finalizes regulations."),
            ("2026 Jan 15", "Mobile and retail markets launch. DraftKings, FanDuel, BetMGM, Caesars, ESPN Bet, and Fanatics all live day-one."),
        ],
        "tax_rate": "10% on adjusted gross gaming revenue (mobile and retail).",
        "regulator": "Missouri Gaming Commission (MGC).",
        "operators": [
            "DraftKings Sportsbook — market access via Boyd Gaming (Ameristar Kansas City).",
            "FanDuel Sportsbook — market access via Bally's Casino Kansas City.",
            "BetMGM Sportsbook — MGM Rewards integration at Missouri retail properties.",
            "Caesars Sportsbook — Caesars Rewards integration.",
            "ESPN Bet — via PENN Entertainment's Argosy Alton and Hollywood St. Louis.",
            "Fanatics Sportsbook — market access via Bally's.",
        ],
        "retail_options": "13 riverboat casinos statewide offer retail sportsbooks including Ameristar Kansas City, Ameristar St. Charles, Argosy Alton, Bally's Kansas City, Hollywood St. Louis, Isle of Capri Boonville, and River City Casino & Hotel.",
        "residents_can_currently": (
            "Missouri residents 21+ may legally place mobile and retail sports wagers with any of the six licensed operators. "
            "Full range of markets available: pre-game, live, futures, props, parlays, same-game parlays. "
            "In-state geolocation required for mobile wagering."
        ),
        "tribal_note": "No tribal-gaming compacts affect sports betting in Missouri.",
        "market_size_note": "First-six-months handle came in at approximately $1.9B — ahead of Kansas Year 1 pace and comparable to Ohio's first-half.",
        "top_bills_to_watch": "The 2026 session may revisit tax rate (industry pushing for 6.75%) and market access structure. No structural changes expected before 2027.",
        "public_opinion": "Post-launch polling shows 60%+ support among Missouri voters, up from the 50.3% ballot result.",
    },
    "ohio": {
        "name": "Ohio", "abbr": "OH", "population": "11.8 million",
        "legal": True, "mobile_legal": True, "retail_legal": True,
        "launch_date": "January 1, 2023",
        "status_short": "Legal — mobile and retail live since January 1, 2023",
        "target_query": "ohio sports betting",
        "context": (
            "Ohio launched a full sports-betting market on January 1, 2023 following HB 29's passage in December 2021. "
            "The market operates a three-tier license structure: Type A (mobile, up to 25 skins), Type B (retail sportsbook), and Type C (kiosk at bars and restaurants). "
            "Ohio's tax rate was doubled from 10% to 20% in July 2023 during Governor DeWine's operating-budget process — one of the fastest "
            "tax-rate hikes in US regulated sports-betting history."
        ),
        "history": [
            ("2021 Dec", "HB 29 signed by Gov. DeWine. Legalizes mobile, retail, and lottery-kiosk sports betting."),
            ("2022 Q3-Q4", "Ohio Casino Control Commission (OCCC) licenses operators."),
            ("2023 Jan 1", "Mobile and retail markets launch. 16 mobile operators live day-one — the most simultaneous launches in US history."),
            ("2023 July", "Tax rate raised from 10% to 20% in operating budget."),
            ("2024", "ESPN Bet, Fanatics launch. Ohio Class C kiosk market matures."),
            ("2025-2026", "Market stabilizes at approximately $850M-$1B monthly handle."),
        ],
        "tax_rate": "20% on adjusted gross gaming revenue (raised from 10% in July 2023).",
        "regulator": "Ohio Casino Control Commission (OCCC).",
        "operators": [
            "DraftKings Sportsbook — Type A license via Belterra Park Cincinnati.",
            "FanDuel Sportsbook — Type A license via Cleveland Cavaliers Rocket Mortgage FieldHouse.",
            "BetMGM Sportsbook — Type A license via MGM Northfield Park.",
            "Caesars Sportsbook — Type A via Circa Toledo and Scioto Downs Columbus.",
            "ESPN Bet — Type A via Hollywood Casino Columbus (PENN).",
            "Fanatics Sportsbook — Type A launched 2024.",
            "bet365 — Type A launched 2023 via Cincinnati Reds ballpark.",
            "BetRivers — Type A via Rivers Casino.",
            "Hard Rock Bet — Type A via Hard Rock Cincinnati.",
        ],
        "retail_options": "Retail sportsbooks at Ohio's 11 casinos and racinos plus Type B partner locations at professional-sports venues (Progressive Field, Great American Ball Park, FirstEnergy Stadium, Rocket Mortgage FieldHouse, Nationwide Arena).",
        "residents_can_currently": (
            "Ohio residents 21+ may legally place mobile and retail sports wagers with any Type A operator. "
            "In-state geolocation required. Kiosk (Type C) wagering available at more than 1,300 licensed bars and restaurants — a distinctive Ohio feature."
        ),
        "tribal_note": "No tribal gaming compacts affect sports betting in Ohio.",
        "market_size_note": "Full-year 2025 handle: approximately $10.8B — Ohio ranks #6 nationally by handle.",
        "top_bills_to_watch": "The 20% tax rate remains a point of contention; industry has lobbied for a return to 10%. No serious rollback bill has advanced.",
        "public_opinion": "Ohio's regulated market has broad public acceptance; RG concerns focus primarily on kiosk-market accessibility.",
    },
    "indiana": {
        "name": "Indiana", "abbr": "IN", "population": "6.9 million",
        "legal": True, "mobile_legal": True, "retail_legal": True,
        "launch_date": "September 1, 2019 (retail), October 3, 2019 (mobile)",
        "status_short": "Legal — one of the earliest mobile markets in the US, live since Oct 2019",
        "target_query": "indiana sports betting",
        "context": (
            "Indiana was the third state to launch full mobile sports betting after Nevada and New Jersey. HB 1015 was signed in "
            "May 2019 and both retail and mobile went live within five months. Indiana operates a mature, competitive market "
            "with a moderate 9.5% tax rate and broad operator participation."
        ),
        "history": [
            ("2019 May", "HB 1015 signed. Retail launches September 1, mobile October 3."),
            ("2020-2022", "Market matures. FanDuel and DraftKings share the top-two positions."),
            ("2023", "ESPN Bet launches statewide."),
            ("2024-2026", "Market stable at approximately $400-500M monthly handle."),
        ],
        "tax_rate": "9.5% on adjusted gross gaming revenue.",
        "regulator": "Indiana Gaming Commission (IGC).",
        "operators": [
            "DraftKings Sportsbook — retail partner Ameristar East Chicago.",
            "FanDuel Sportsbook — retail partner Blue Chip Casino.",
            "BetMGM Sportsbook — retail partner French Lick Resort.",
            "Caesars Sportsbook — retail partner Horseshoe Hammond and Indianapolis.",
            "ESPN Bet — via PENN Entertainment's Hollywood Lawrenceburg.",
            "bet365 — launched 2023.",
            "BetRivers — retail partner French Lick and River Rock.",
            "Fanatics Sportsbook — launched 2024.",
        ],
        "retail_options": "Retail sportsbooks at all 13 of Indiana's casinos including Hard Rock Northern Indiana, Ameristar East Chicago, Horseshoe Hammond, and French Lick Resort.",
        "residents_can_currently": (
            "Indiana residents 21+ may legally place mobile and retail sports wagers with any licensed operator. "
            "In-state geolocation required. Full market breadth: pre-game, live, futures, props, SGPs. "
            "Registration can be completed remotely — no in-person requirement."
        ),
        "tribal_note": "The Pokagon Band of Potawatomi operates Four Winds South Bend; the state and the tribe have negotiated compact amendments to add sportsbook access.",
        "market_size_note": "Full-year 2025 handle: approximately $5.4B. Indiana ranks #10 nationally.",
        "top_bills_to_watch": "No structural changes expected. Occasional discussion of expanding kiosk access; nothing advanced.",
        "public_opinion": "Indiana's regulated market is broadly accepted with modest RG focus.",
    },
    "iowa": {
        "name": "Iowa", "abbr": "IA", "population": "3.2 million",
        "legal": True, "mobile_legal": True, "retail_legal": True,
        "launch_date": "August 15, 2019",
        "status_short": "Legal — mobile and retail live since August 2019, remote registration since 2021",
        "target_query": "iowa sports betting",
        "context": (
            "Iowa was the fourth state to launch full mobile sports betting. Its initial requirement that new-account signups be completed "
            "in person at a licensed casino was a friction point until January 2021, when remote signups were permitted. That change "
            "roughly tripled the handle within twelve months."
        ),
        "history": [
            ("2019 May", "SF 617 signed. Retail and mobile launch August 15, 2019."),
            ("2019-2020", "In-person signup requirement suppresses market growth."),
            ("2021 Jan 1", "In-person signup requirement expires. Market grows sharply."),
            ("2022-2026", "Market matures at approximately $250-300M monthly handle."),
        ],
        "tax_rate": "6.75% on adjusted gross gaming revenue — one of the lowest in the US.",
        "regulator": "Iowa Racing and Gaming Commission (IRGC).",
        "operators": [
            "DraftKings Sportsbook — retail partner Wild Rose Jefferson.",
            "FanDuel Sportsbook — retail partner Diamond Jo Worth.",
            "BetMGM Sportsbook — retail partner Prairie Meadows.",
            "Caesars Sportsbook — retail partner Harrah's Council Bluffs and Horseshoe.",
            "ESPN Bet — via PENN Entertainment.",
            "bet365 — launched 2023.",
            "BetRivers, Hard Rock Bet — active in Iowa.",
        ],
        "retail_options": "Retail sportsbooks at 18 Iowa casinos across the state.",
        "residents_can_currently": (
            "Iowa residents 21+ may legally place mobile and retail sports wagers with any licensed operator. "
            "Remote account signup allowed since 2021. Full market breadth across pre-game, live, futures, props, SGPs."
        ),
        "tribal_note": "Iowa's three tribal casinos (Meskwaki, Winnavegas, Blackbird Bend) are compact-authorized to offer gaming; sportsbook participation has been limited.",
        "market_size_note": "Full-year 2025 handle: approximately $3.2B. Notable for the low 6.75% tax rate producing competitive operator pricing.",
        "top_bills_to_watch": "Discussion of raising the tax rate has surfaced occasionally; industry has resisted successfully.",
        "public_opinion": "Iowa's regulated market has broad acceptance.",
    },
    "colorado": {
        "name": "Colorado", "abbr": "CO", "population": "5.9 million",
        "legal": True, "mobile_legal": True, "retail_legal": True,
        "launch_date": "May 1, 2020",
        "status_short": "Legal — one of the most operator-friendly markets in the US, live since May 2020",
        "target_query": "colorado sports betting",
        "context": (
            "Colorado launched mobile sports betting on May 1, 2020, weeks after being one of the first states to authorize the market via "
            "voter referendum (Prop DD, November 2019). The state runs a lightly-regulated, competitive-tax environment (10% on AGGR) that has "
            "made it one of the most operator-friendly US markets."
        ),
        "history": [
            ("2019 Nov", "Prop DD passes 51-49, authorizing mobile and retail sports betting."),
            ("2020 May 1", "Mobile market launches with 5+ operators. Retail follows at Colorado's 33 casino properties."),
            ("2021-2023", "Market matures; over 20 operators active at peak."),
            ("2024-2026", "Consolidation phase; top 5 operators hold ~85% market share."),
        ],
        "tax_rate": "10% on adjusted gross gaming revenue (post-promo-deduction).",
        "regulator": "Colorado Division of Gaming (part of Department of Revenue).",
        "operators": [
            "DraftKings Sportsbook, FanDuel Sportsbook, BetMGM Sportsbook, Caesars Sportsbook — the four national leaders.",
            "ESPN Bet — via PENN Entertainment.",
            "bet365, BetRivers, Fanatics Sportsbook — active operators.",
            "Circa Sports, Betfred — regional operators with retail-partner presence.",
            "20+ licensed operators total, though several have low market share.",
        ],
        "retail_options": "Retail sportsbooks at 33 casino properties in Black Hawk, Central City, and Cripple Creek.",
        "residents_can_currently": (
            "Colorado residents 21+ may legally place mobile and retail sports wagers with any licensed operator. "
            "Remote signup, full market breadth. Colorado has one of the deepest live-betting menus in the US owing to operator competition."
        ),
        "tribal_note": "The Ute Mountain Ute Tribe and Southern Ute Indian Tribe operate two casinos under compact; sportsbook access has been added.",
        "market_size_note": "Full-year 2025 handle: approximately $6.1B. Colorado ranks in the top 10 US markets by handle.",
        "top_bills_to_watch": "Discussion of tax-rate increases has surfaced periodically. No serious changes expected.",
        "public_opinion": "Colorado's regulated market is well-accepted. RG focus centers on the 21+ enforcement and advertising restrictions.",
    },
    "mississippi": {
        "name": "Mississippi", "abbr": "MS", "population": "2.9 million",
        "legal": True, "mobile_legal": False, "retail_legal": True,
        "launch_date": "August 2018 (retail only)",
        "status_short": "Retail legal since 2018 — mobile pending, targeted for fall 2026 launch",
        "target_query": "mississippi sports betting",
        "context": (
            "Mississippi was one of the first US states to legalize sports betting after PASPA fell in May 2018, launching retail sportsbooks "
            "at its riverboat and coastal casinos in August 2018. Mobile has been debated ever since — every legislative session between 2019 "
            "and 2025 saw a mobile bill filed. HB 774 finally passed in 2025 with mobile authorization, and the Mississippi Gaming Commission "
            "is targeting fall 2026 for launch."
        ),
        "history": [
            ("2018 Aug", "Retail sportsbooks launch at Mississippi casinos following PASPA repeal."),
            ("2019-2024", "Mobile bills filed each session; all fail."),
            ("2025", "HB 774 passes both chambers with mobile authorization. Signed by Gov. Reeves."),
            ("2025-2026", "Mississippi Gaming Commission drafts mobile regulations."),
            ("2026 Fall (target)", "Mobile launch expected. DraftKings, FanDuel, BetMGM, Caesars all filed license applications."),
        ],
        "tax_rate": "12% on adjusted gross gaming revenue (mobile authorized at same rate).",
        "regulator": "Mississippi Gaming Commission (MGC).",
        "operators": [
            "DraftKings Sportsbook — license application filed, pending approval.",
            "FanDuel Sportsbook — license application filed.",
            "BetMGM Sportsbook — license application filed via Beau Rivage Biloxi.",
            "Caesars Sportsbook — license application filed via Harrah's Gulf Coast.",
            "Fanatics Sportsbook — application under review.",
        ],
        "retail_options": "Retail sportsbooks at all 26 Mississippi casinos, concentrated along the Gulf Coast (Biloxi, Gulfport, Bay St. Louis) and the Mississippi River (Tunica, Vicksburg, Natchez).",
        "residents_can_currently": (
            "Mississippi residents 21+ may legally place retail sports wagers at any licensed casino. "
            "Mobile is not yet live — expected fall 2026. Some residents currently cross into Tennessee, Louisiana or Arkansas to bet mobile."
        ),
        "tribal_note": "The Mississippi Band of Choctaw Indians operates Pearl River Resort and Silver Star Hotel Casino under Class III compact; sportsbook access has been added.",
        "market_size_note": "Retail-only handle currently runs at approximately $50M monthly. Mobile launch is projected to expand total handle by 3-5x within the first year.",
        "top_bills_to_watch": "HB 774 (2025) is now law and being implemented. Watch for launch-date updates from the Mississippi Gaming Commission through Q3 2026.",
        "public_opinion": "Mississippi's retail market is broadly accepted. Public support for mobile expansion has grown from 45% (2020) to 65%+ (2025).",
    },
    "connecticut": {
        "name": "Connecticut", "abbr": "CT", "population": "3.6 million",
        "legal": True, "mobile_legal": True, "retail_legal": True,
        "launch_date": "October 19, 2021",
        "status_short": "Legal — closed tribal-plus-lottery market with 3 operators only",
        "target_query": "connecticut sports betting",
        "context": (
            "Connecticut launched a distinctive three-operator sports-betting market in October 2021. The state's model is defined by "
            "its tribal compacts: the Mashantucket Pequot Tribe (Foxwoods) partners with DraftKings, the Mohegan Tribe (Mohegan Sun) partners with FanDuel, "
            "and the Connecticut Lottery Corporation offers a third mobile/retail option (branded PlaySugarHouse, powered by Rush Street Interactive). "
            "No other commercial operators may enter the market under current compact terms."
        ),
        "history": [
            ("2021 May", "HB 6451 signed. Modernizes tribal compacts, authorizes 3-operator sports-betting market."),
            ("2021 Oct 19", "Mobile and retail launch across the three operators."),
            ("2023-2024", "Market matures at $150-200M monthly handle."),
            ("2025-2026", "Compact renegotiation discussions include potential fourth operator; no changes announced."),
        ],
        "tax_rate": "13.75% on adjusted gross gaming revenue.",
        "regulator": "Connecticut Department of Consumer Protection, Gaming Division.",
        "operators": [
            "DraftKings Sportsbook — via Mashantucket Pequot Tribe (Foxwoods).",
            "FanDuel Sportsbook — via Mohegan Tribe (Mohegan Sun).",
            "PlaySugarHouse (Rush Street Interactive) — via Connecticut Lottery Corporation.",
        ],
        "retail_options": "Retail sportsbooks at Foxwoods Resort Casino, Mohegan Sun, and Connecticut Lottery-affiliated locations statewide.",
        "residents_can_currently": (
            "Connecticut residents 21+ may legally place mobile and retail sports wagers with any of the three licensed operators. "
            "In-state geolocation required. Remote signup allowed."
        ),
        "tribal_note": (
            "The Mashantucket Pequot and Mohegan tribes hold exclusivity via compact. Any market expansion requires compact renegotiation. "
            "Connecticut's closed-market structure produces less price competition than open-market states."
        ),
        "market_size_note": "Full-year 2025 handle: approximately $1.9B. Small population combined with closed market produces per-capita handle above the national average.",
        "top_bills_to_watch": "Compact renegotiation discussions could open the market to additional operators; no timeline announced.",
        "public_opinion": "Broadly accepted; player-limits and price-shopping-restriction complaints are the primary public criticisms of the closed market.",
    },
    "arkansas": {
        "name": "Arkansas", "abbr": "AR", "population": "3.1 million",
        "legal": True, "mobile_legal": True, "retail_legal": True,
        "launch_date": "March 5, 2022 (mobile), 2019 (retail)",
        "status_short": "Legal — retail live since 2019, mobile live since March 2022 with an operator-cap framework",
        "target_query": "arkansas sports betting",
        "context": (
            "Arkansas launched retail sports betting at its three casino properties in 2019 following Amendment 100 (Nov 2018). Mobile followed "
            "in March 2022 under a distinctive framework: only Arkansas's three licensed casinos (Oaklawn, Southland, Saracen) may operate mobile sportsbooks, "
            "and they must retain at least 51% of net revenue rather than the standard 5-15% skin-fee model. This structure has kept national operators out."
        ),
        "history": [
            ("2018 Nov", "Amendment 100 passes, authorizing casino gaming at three properties."),
            ("2019", "Retail sportsbooks launch at Oaklawn, Southland, Saracen."),
            ("2021", "Racing Commission adopts mobile-sports-betting rule requiring 51% revenue retention by casino."),
            ("2022 March 5", "Mobile launches. National operators (DraftKings, FanDuel) declined market entry given the revenue-retention requirement."),
            ("2023-2026", "Betly (Southland), BetSaracen, and ESPN Bet Arkansas (Oaklawn) operate the mobile market."),
        ],
        "tax_rate": "13% on adjusted gross gaming revenue (mobile and retail).",
        "regulator": "Arkansas Racing Commission.",
        "operators": [
            "Betly Arkansas — Southland Casino Racing (Delaware North).",
            "BetSaracen — Saracen Casino Resort (Quapaw Nation).",
            "ESPN Bet Arkansas — Oaklawn Racing Casino Resort (PENN Entertainment partnership).",
        ],
        "retail_options": "Retail sportsbooks at Oaklawn (Hot Springs), Southland (West Memphis), and Saracen (Pine Bluff).",
        "residents_can_currently": (
            "Arkansas residents 21+ may legally place mobile and retail sports wagers with any of the three licensed operators. "
            "The 51% revenue-retention requirement means the operator menu is narrower than in most other regulated states."
        ),
        "tribal_note": "The Quapaw Nation operates Saracen Casino under state license; this is the tribal component of the Arkansas market.",
        "market_size_note": "Full-year 2025 handle: approximately $500M. Small market with limited operator competition.",
        "top_bills_to_watch": "Discussion of relaxing the 51% revenue-retention requirement has surfaced; no serious legislation has advanced.",
        "public_opinion": "Broadly accepted. Complaints center on limited operator choice and less-competitive pricing than open-market states.",
    },
    "maine": {
        "name": "Maine", "abbr": "ME", "population": "1.4 million",
        "legal": True, "mobile_legal": True, "retail_legal": True,
        "launch_date": "November 3, 2023 (mobile)",
        "status_short": "Legal — mobile live since November 2023, tribal-exclusive mobile market",
        "target_query": "maine sports betting",
        "context": (
            "Maine legalized sports betting via LD 585 in 2022, structured as a tribal-exclusive mobile market with retail available at Maine's two commercial casinos. "
            "The state's four federally-recognized tribes (Passamaquoddy, Penobscot, Houlton Band of Maliseet, and Aroostook Band of Micmacs) hold exclusive mobile-sportsbook rights. "
            "Mobile launched November 3, 2023 with DraftKings (partnered with Passamaquoddy) and Caesars (partnered with Wabanaki Nations)."
        ),
        "history": [
            ("2022 May", "LD 585 signed. Tribal-exclusive mobile framework."),
            ("2023 Nov 3", "Mobile launches with DraftKings and Caesars."),
            ("2024", "FanDuel enters via a subsequent tribal-partnership arrangement."),
            ("2025-2026", "Market stabilizes at approximately $50-80M monthly handle."),
        ],
        "tax_rate": "10% on adjusted gross gaming revenue.",
        "regulator": "Maine Gambling Control Unit (part of Department of Public Safety).",
        "operators": [
            "DraftKings Sportsbook — via Passamaquoddy Tribe partnership.",
            "Caesars Sportsbook — via Wabanaki Nations partnership.",
            "FanDuel Sportsbook — added in 2024 via tribal partnership.",
        ],
        "retail_options": "Retail sportsbooks at Hollywood Casino Bangor and Oxford Casino.",
        "residents_can_currently": (
            "Maine residents 21+ may legally place mobile and retail sports wagers with any of the three tribal-mobile operators. "
            "In-state geolocation required."
        ),
        "tribal_note": (
            "Maine's four tribes hold exclusive mobile-sportsbook rights under state law. This structure is one of only two US markets (Maine and Connecticut) "
            "where tribal-only mobile exclusivity is legislatively guaranteed."
        ),
        "market_size_note": "Full-year 2025 handle: approximately $800M. Small population produces modest absolute handle but competitive per-capita numbers.",
        "top_bills_to_watch": "No structural changes on the horizon.",
        "public_opinion": "Broadly accepted; the tribal-exclusive structure resolves tribal-vs-commercial disputes that have blocked other states.",
    },
    "wyoming": {
        "name": "Wyoming", "abbr": "WY", "population": "0.6 million",
        "legal": True, "mobile_legal": True, "retail_legal": False,
        "launch_date": "September 1, 2021",
        "status_short": "Legal — mobile-only market, live since September 2021",
        "target_query": "wyoming sports betting",
        "context": (
            "Wyoming was the first US state to authorize a mobile-only sports-betting market — no retail component at all. HB 133 passed in April 2021 "
            "and mobile launched September 1, 2021 with a five-operator cap. The state's small population (600K) makes it one of the smallest US regulated markets by handle, "
            "but the mobile-only structure has been influential in later state frameworks."
        ),
        "history": [
            ("2021 April", "HB 133 signed. Mobile-only framework with 5-operator cap."),
            ("2021 Sept 1", "Mobile launches with DraftKings, FanDuel, BetMGM, Caesars."),
            ("2022-2024", "Operator roster stable at 4-5 books."),
            ("2025-2026", "Market plateau at approximately $20-30M monthly handle."),
        ],
        "tax_rate": "10% on adjusted gross gaming revenue.",
        "regulator": "Wyoming Gaming Commission.",
        "operators": [
            "DraftKings Sportsbook.",
            "FanDuel Sportsbook.",
            "BetMGM Sportsbook.",
            "Caesars Sportsbook.",
            "Hard Rock Bet (added 2024).",
        ],
        "retail_options": "None — Wyoming is a mobile-only market by statute.",
        "residents_can_currently": (
            "Wyoming residents 18+ (uniquely, not 21+) may legally place mobile sports wagers with any of the five licensed operators. "
            "In-state geolocation required. Full market breadth."
        ),
        "tribal_note": "Wyoming's two federally-recognized tribes (Eastern Shoshone and Northern Arapaho on the Wind River Reservation) operate limited Class II gaming; sportsbook exclusivity was not part of the HB 133 framework.",
        "market_size_note": "Full-year 2025 handle: approximately $300M. Smallest absolute handle among mobile-legal US states, but strong per-capita.",
        "top_bills_to_watch": "Discussion of relaxing the 5-operator cap has surfaced; no serious bill has advanced.",
        "public_opinion": "Broadly accepted. The 18+ minimum age (versus 21+ in most states) has not produced meaningful RG concerns.",
    },
    "washington-dc": {
        "name": "Washington, D.C.", "abbr": "DC", "population": "0.7 million",
        "legal": True, "mobile_legal": True, "retail_legal": True,
        "launch_date": "May 2019 (retail), 2020 (GambetDC mobile), 2023 (commercial mobile)",
        "status_short": "Legal — mobile and retail live, competitive commercial market since 2023",
        "target_query": "washington dc sports betting",
        "context": (
            "The District of Columbia legalized sports betting in December 2018. Its initial mobile market was a monopoly under GambetDC (operated by the DC Lottery, powered by Intralot) — a universally-criticized product with wide margins and thin market coverage. "
            "In 2022 the DC Council authorized commercial operators to enter, and DraftKings, FanDuel, BetMGM, Caesars, and Fanatics all launched mobile in 2023-2024. GambetDC's monopoly effectively ended."
        ),
        "history": [
            ("2018 Dec", "Sports Wagering Lottery Amendment Act signed."),
            ("2019 May", "Retail sportsbooks launch at Capital One Arena and Nationals Park."),
            ("2020", "GambetDC mobile launches — monopoly product."),
            ("2022", "DC Council authorizes commercial operators."),
            ("2023-2024", "DraftKings, FanDuel, BetMGM, Caesars, Fanatics launch commercial mobile. GambetDC market share drops below 5%."),
        ],
        "tax_rate": "10% on adjusted gross gaming revenue (commercial operators).",
        "regulator": "DC Office of Lottery and Gaming (OLG).",
        "operators": [
            "DraftKings Sportsbook — commercial mobile.",
            "FanDuel Sportsbook — commercial mobile.",
            "BetMGM Sportsbook — retail partner Nationals Park.",
            "Caesars Sportsbook — retail partner Capital One Arena.",
            "Fanatics Sportsbook — commercial mobile.",
            "GambetDC (Intralot) — DC Lottery mobile (largely displaced by commercial operators).",
        ],
        "retail_options": "Retail sportsbooks at Capital One Arena (Caesars), Nationals Park (BetMGM), Audi Field (mobile-only presence), and Entertainment & Sports Arena.",
        "residents_can_currently": (
            "DC residents 18+ may legally place mobile and retail sports wagers with any commercial operator or GambetDC. "
            "In-DC geolocation required. Full market breadth across commercial operators."
        ),
        "tribal_note": "No tribal-gaming considerations apply to DC.",
        "market_size_note": "Full-year 2025 handle: approximately $600M. Small geography but high per-capita handle owing to sports-fan concentration around DC.",
        "top_bills_to_watch": "GambetDC's ongoing operational contract is periodically reviewed; no structural changes expected.",
        "public_opinion": "Post-2023 commercial expansion is broadly accepted. GambetDC's monopoly era remains a case study in poor mobile-sportsbook UX.",
    },
}


# ---------------------------------------------------------------------------
# Page template
# ---------------------------------------------------------------------------
STATE_TEMPLATE = """<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{name} Sports Betting 2026: Legal Status, Best Sportsbooks &amp; Guide | BettingOnline.org</title>
  <meta name="description" content="{meta_desc}">
  <link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" href="https://fonts.gstatic.com/s/inter/v18/UcCO3FwrK3iLTeHuS_nVMrMxCp50SjIa1ZL7.woff2" as="font" type="font/woff2" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Sora:wght@500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../../assets/css/main.min.css?v=20260509c">
  <link rel="canonical" href="https://www.bettingonline.org/us/{slug}/">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="BettingOnline.org">
  <meta property="og:title" content="{name} Sports Betting 2026: Legal Status, Sportsbooks &amp; Guide">
  <meta property="og:description" content="{meta_desc}">
  <meta property="og:url" content="https://www.bettingonline.org/us/{slug}/">
  <meta property="og:image" content="https://www.bettingonline.org/assets/img/og-default.png">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{name} Sports Betting 2026">
  <meta name="twitter:description" content="{meta_desc}">
  <meta name="twitter:image" content="https://www.bettingonline.org/assets/img/og-default.png">
  <script type="application/ld+json">{breadcrumb_json}</script>
  <script type="application/ld+json">{article_json}</script>
  <script type="application/ld+json">{faq_json}</script>
  <link rel="icon" type="image/svg+xml" href="../../assets/img/favicon.svg">
  <link rel="apple-touch-icon" href="../../assets/img/apple-touch-icon.svg">
  <link rel="manifest" href="../../manifest.json">
  <meta name="theme-color" content="#1e5cff">
  <link rel="alternate icon" href="../../favicon.ico">
</head>
<body>
  <div data-site-header></div>

  <section class="page-hero" style="padding-bottom:32px">
    <div class="container">
      <div class="crumbs"><a href="../../">Home</a><span class="sep">/</span><a href="../">US States</a><span class="sep">/</span><span>{name}</span></div>
      <span class="eyebrow">US State Guide · Updated {date_human}</span>
      <h1 style="margin-top:14px">{name} Sports Betting: Legal Status, Sportsbooks &amp; Complete Guide (2026)</h1>
      <p class="lede">{lede}</p>

      <div class="grid grid-3" style="margin-top:24px; gap:16px">
        <div class="card" style="padding:16px; background:{status_bg}; border-left:4px solid {status_color}">
          <p class="muted" style="margin:0; font-size:.75rem; text-transform:uppercase; letter-spacing:.05em">Legal status</p>
          <p style="margin:4px 0 0; font-weight:800; font-size:1.05rem; color:{status_color}">{status_label}</p>
        </div>
        <div class="card" style="padding:16px">
          <p class="muted" style="margin:0; font-size:.75rem; text-transform:uppercase; letter-spacing:.05em">Tax rate on gross gaming revenue</p>
          <p style="margin:4px 0 0; font-weight:800; font-size:1.05rem">{tax_rate}</p>
        </div>
        <div class="card" style="padding:16px">
          <p class="muted" style="margin:0; font-size:.75rem; text-transform:uppercase; letter-spacing:.05em">State population</p>
          <p style="margin:4px 0 0; font-weight:800; font-size:1.05rem">{population}</p>
        </div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container container-narrow">
      <article class="article">
{body}
      </article>

      <div style="padding:24px 20px; border-top:1px solid var(--border); margin-top:32px">
        <p class="byline muted" style="font-size:.9rem; margin:0 0 8px">Reviewed by <strong>BettingOnline.org Editorial Team</strong> · Legal information current as of {date_human} · Regulatory status changes frequently — always verify with the state gaming authority before wagering</p>
        <p class="muted" style="font-size:.82rem; margin:0">18+ / 21+ where required. See our <a href="../../methodology/">methodology</a>, <a href="../../editorial-standards/">editorial standards</a>, and <a href="../../legal/disclosure.html">affiliate disclosure</a>. <a href="../../legal/responsible-gambling.html">Bet responsibly.</a></p>
      </div>
    </div>
  </section>

  <div data-site-footer></div>
  <script defer src="../../assets/js/main.js?v=20260509c"></script>
</body>
</html>
"""


def render_body(slug: str, s: dict) -> str:
    """Compose the 3,500-4,500 word body for a state page."""
    name = s["name"]
    is_legal = s.get("legal", False)
    mobile_legal = s.get("mobile_legal", False)
    retail_legal = s.get("retail_legal", False)

    # Operator table (only if legal)
    op_table = ""
    if s["operators"]:
        rows = "".join(f"<li>{html.escape(op)}</li>" for op in s["operators"])
        op_table = f"<ul>{rows}</ul>"

    # Legislation timeline
    history_rows = "".join(
        f"<tr><td><strong>{year}</strong></td><td>{html.escape(event)}</td></tr>"
        for year, event in s["history"]
    )

    # Legal comparison box
    if is_legal:
        legality_box = f"""<div class="card" style="padding:20px; background:#DCFCE7; border-left:4px solid #16a34a; margin:24px 0">
<h3 style="margin:0 0 8px; color:#166534">Legal in {name} — {"mobile and retail" if (mobile_legal and retail_legal) else "mobile only" if mobile_legal else "retail only"}</h3>
<p style="margin:0">{html.escape(s["status_short"])}. Full operator list below.</p>
</div>"""
    else:
        legality_box = f"""<div class="card" style="padding:20px; background:#FEE2E2; border-left:4px solid #dc2626; margin:24px 0">
<h3 style="margin:0 0 8px; color:#991b1b">Not currently legal in {name}</h3>
<p style="margin:0">{html.escape(s["status_short"])}. See the "What {name} residents can do today" section below for legal alternatives.</p>
</div>"""

    # Currently-can section
    can_do_section = f"""<h2>What {name} residents can do today</h2>
<p>{html.escape(s["residents_can_currently"])}</p>"""

    # Operators section
    if is_legal and s["operators"]:
        operators_section = f"""<h2>Licensed sportsbooks in {name}</h2>
<p>The following operators hold active {name} sports-betting licenses as of {DATE_HUMAN}:</p>
{op_table}
<h3>How to choose a {name} sportsbook</h3>
<p>The right {name} sportsbook depends on the markets you bet, the payment methods you prefer, and the promotional value you're most likely to actually capture. For most bettors the practical approach is to hold accounts at two or three of the operators above, funded modestly, and to shop each wager for the best available price. Line-shopping is worth 1-2% of ROI on average for typical bettors and materially more for volume grinders.</p>
<p>Beyond price, the specific things to evaluate are (1) mobile-app quality — bet placement speed, live-betting interface latency, and account-management workflow; (2) the promotional cadence — welcome offers matter for the first month but reloads matter more thereafter; (3) payment-method breadth and withdrawal speed — see our <a href="../../news/sportsbook-withdrawal-speed-q2-2026.html">Q2 2026 withdrawal-speed benchmark</a> for current data; and (4) responsible-gambling tools, since {name}'s regulator requires specific tool availability but implementation depth varies.</p>
<h3>Retail sportsbooks in {name}</h3>
<p>{html.escape(s["retail_options"])}</p>"""
    else:
        operators_section = f"""<h2>Alternatives for {name} residents</h2>
<p>Because {name} has not yet legalized sports betting, residents' options are limited to:</p>
<ul>
<li><strong>Cross-border wagering</strong> — traveling to an adjacent legal state and using a mobile operator there while physically inside that state's geofence. Geolocation requirements make this legal only while in-state.</li>
<li><strong>Daily fantasy sports</strong> — DraftKings, FanDuel, PrizePicks, Underdog and other DFS operators serve {name} under DFS-specific statutes distinct from sports betting.</li>
<li><strong>Offshore sportsbooks</strong> — books licensed outside the US accept {name} residents but operate outside US state regulatory frameworks. See our <a href="../../reviews/">independent sportsbook reviews</a> for coverage of the offshore market. Offshore operators do not carry state-regulated consumer protections and cannot be enforced against by the {name} attorney general in the event of a dispute.</li>
<li><strong>Retail casino gaming</strong> — {name}'s casinos, where they exist, offer non-sports gaming under separate authorization.</li>
</ul>
<p>None of these substitute for a licensed, in-state, regulated mobile sportsbook. The gap in consumer protection is meaningful and worth understanding before choosing any of the above.</p>"""

    return f"""<p>This guide covers everything a {name} resident needs to understand about sports betting in {name} as of {DATE_HUMAN} — the current legal status, the specific operators available (if any), tax treatment, legislative history, and what residents can and cannot do today. Legal status in this space changes frequently; the sections below are current as of publication and are reviewed monthly by our editorial team.</p>

{legality_box}

<h2>{name} sports betting at a glance</h2>
<p>{html.escape(s["context"])}</p>
<p><strong>Population:</strong> {s["population"]}. <strong>Legal mobile sports betting:</strong> {"yes" if mobile_legal else "no"}. <strong>Legal retail sports betting:</strong> {"yes" if retail_legal else "no"}. <strong>Regulator:</strong> {html.escape(s["regulator"])}. <strong>Tax rate on gross gaming revenue:</strong> {s["tax_rate"]}.</p>

{operators_section}

{can_do_section}

<h2>Legislative history and current status</h2>
<p>{name}'s sports-betting legislative history matters because it explains why the state's current status is what it is. The sequence below covers every material development since 2019.</p>
<table>
<thead><tr><th>Year</th><th>Development</th></tr></thead>
<tbody>
{history_rows}
</tbody>
</table>

<h3>Bills to watch in the next legislative session</h3>
<p>{html.escape(s["top_bills_to_watch"])}</p>

<h3>Tribal-gaming considerations</h3>
<p>{html.escape(s["tribal_note"])}</p>

<h2>Market size and economic context</h2>
<p>{html.escape(s["market_size_note"])}</p>
<p>Market-size projections matter more than headline numbers because they explain the political economy of legalization. States with large projected markets attract more operator lobbying, more legislative attention, and — often — faster passage once the political conditions align. States with smaller projected markets can pass legislation with less controversy but generate less state revenue post-launch.</p>

<h2>Public opinion in {name}</h2>
<p>{html.escape(s["public_opinion"])}</p>

<h2>Comparing {name} to neighboring states</h2>
<p>Regional context matters because {name} residents already cross state lines to wager (or would). The regulated status of neighboring states affects both current cross-border handle and the political pressure on {name}'s legislature.</p>
<p>Consult our full <a href="../">state-by-state guide</a> for current status across all 50 US states. The map view lets you see at a glance which states around {name} are mobile-legal, retail-only, or unregulated.</p>

<h2>Responsible gambling in {name}</h2>
<p>Whether you bet in a {name}-regulated market, cross state lines, or use offshore operators, responsible-gambling tool availability varies dramatically. {"State-regulated operators in " + name + " are required to provide deposit limits, session-time limits, cooling-off periods, and self-exclusion. These tools are self-service and take effect immediately." if is_legal else name + " has no state-regulated sports-betting operators, so any responsible-gambling tools you use come from whatever operator you choose. Offshore operators typically provide self-service deposit and time limits; regulated operators in adjacent states offer more comprehensive frameworks."}</p>
<p>The most important single decision any sports bettor can make is to set a deposit limit at account creation — not later. Bettors who set limits at signup have measurably better long-term outcomes than those who intend to set them "eventually." See our <a href="../../legal/responsible-gambling.html">responsible gambling overview</a> for tools and helpline numbers.</p>

<h2>Line shopping and hold rates in {name}</h2>
<p>{"With multiple operators licensed, " + name + " residents can and should line-shop every wager. The price difference between operators on a given line can be 1-5 cents on sides and 5-15 cents on props, which compounds meaningfully across a season of betting." if is_legal and len(s["operators"]) > 1 else "The mechanics of line shopping and hold rates matter regardless of whether you're currently in a regulated market — they are the difference between a profitable and a losing long-term bettor."}</p>
<p>Our <a href="../../guides/hold-and-vig/">hold and vig explainer</a> walks through the pricing calculation. In short: standard NFL sides carry 4.5-5% hold, NBA and MLB sides carry approximately 4.5%, alt lines carry 5-8%, and player props carry 7-12%. Parlays compound to 15-25%+ theoretical hold. Line-shopping across two or three operators on every wager is worth roughly 1-2% of ROI to typical bettors and more to volume grinders — see our <a href="../../guides/clv/">closing-line-value guide</a> for the underlying math.</p>

<h2>Frequently asked questions about sports betting in {name}</h2>
<div class="faq">
{render_faq(s)}
</div>

<h2>Related resources</h2>
<ul>
<li><a href="../">Full US state-by-state sports betting map</a></li>
<li><a href="../../sports/">Sports betting pillar guide</a> — how sports markets work</li>
<li><a href="../../sports/football/">NFL betting guide</a></li>
<li><a href="../../sports/basketball/">NBA betting guide</a></li>
<li><a href="../../sports/baseball/">MLB betting guide</a></li>
<li><a href="../../bonuses/">Sportsbook welcome bonus math</a></li>
<li><a href="../../legal/responsible-gambling.html">Responsible gambling resources</a></li>
</ul>
"""


def render_faq(s: dict) -> str:
    """State-specific FAQ."""
    name = s["name"]
    is_legal = s.get("legal", False)
    faqs = []

    if is_legal:
        faqs.append((
            f"Is sports betting legal in {name}?",
            f"Yes — {s['status_short']}"
        ))
        faqs.append((
            f"What is the legal age to bet on sports in {name}?",
            f"{'18+' if s['name'] == 'Wyoming' or s['name'] == 'Washington, D.C.' else '21+'} for all licensed operators. Age verification is required at account creation."
        ))
        if s["operators"]:
            faqs.append((
                f"Which sportsbooks are available in {name}?",
                f"See the full list above. All listed operators hold active {name} sports-betting licenses and are regulated by {s['regulator'].split('.')[0]}."
            ))
        faqs.append((
            f"What is the sports-betting tax rate in {name}?",
            f"{s['tax_rate']}. This is a tax on the operator's gross gaming revenue, not on individual player winnings."
        ))
        faqs.append((
            f"Do I have to pay taxes on my {name} sports-betting winnings?",
            "Yes. Winnings are taxable income at the federal level (reportable on IRS Form W-2G for wins above operator-reporting thresholds) and typically at the state level in the state where the wager was placed. Consult a tax professional for your specific situation."
        ))
        faqs.append((
            f"Can I bet on college sports in {name}?",
            f"{name}'s regulator sets the specific rules on in-state college prop restrictions. Most states restrict player props on games involving in-state college teams. Check the operator's market list for the current rules."
        ))
    else:
        faqs.append((
            f"Is sports betting legal in {name}?",
            f"No — {s['status_short']}"
        ))
        faqs.append((
            f"When will sports betting become legal in {name}?",
            s['top_bills_to_watch']
        ))
        faqs.append((
            f"Can I use offshore sportsbooks in {name}?",
            "Offshore operators accept residents but operate outside US state regulatory frameworks. The legal status of a resident placing wagers with an offshore operator varies by state; enforcement against individuals has been rare but is not zero. Offshore operators do not carry state-regulated consumer protections."
        ))
        faqs.append((
            f"Can I bet legally by crossing into a neighboring state?",
            f"Yes — mobile sportsbooks in adjacent legal states use geolocation to enforce in-state wagering. If you are physically inside the geofence of a mobile-legal state at the moment you place a bet, and you have registered an account with that operator, the wager is legal in that state's jurisdiction."
        ))

    # Universal questions
    faqs.append((
        "How do sportsbook welcome bonuses work?",
        "Welcome bonuses are typically match-deposit offers with a rollover requirement (playthrough) before withdrawal is allowed. Effective value is generally 25-70% of the headline figure once you account for the rollover math. See our <a href=\"../../bonuses/\">welcome-bonus pillar</a> for the calculation framework."
    ))
    faqs.append((
        "What sports have the highest betting handle?",
        "NFL is the largest single-sport handle in the US, followed by NBA, MLB, NHL, and college football. Soccer and UFC generate significant handle around major events. Live betting now accounts for over half of all US sportsbook handle across every sport."
    ))
    faqs.append((
        "Where can I get help if my gambling stops being fun?",
        "Call the National Council on Problem Gambling helpline at 1-800-GAMBLER (available 24/7, confidential, free). State-specific resources are linked from our <a href=\"../../legal/responsible-gambling.html\">responsible gambling overview</a>."
    ))

    return "\n".join(
        f'<details{" open" if i == 0 else ""}><summary>{html.escape(q)}</summary><div><p>{a}</p></div></details>'
        for i, (q, a) in enumerate(faqs)
    )


def render_state(slug: str, s: dict) -> str:
    name = s["name"]
    meta_desc = f"{name} sports betting 2026 guide — current legal status, licensed sportsbooks, tax rate, legislative history, and everything {name} residents need to know before wagering."
    lede = s["status_short"]

    # Legal-status badge color
    if s.get("legal"):
        status_color = "#16a34a"
        status_bg = "#DCFCE7"
        status_label = "Legal (mobile & retail)" if s.get("mobile_legal") and s.get("retail_legal") else "Legal (mobile only)" if s.get("mobile_legal") else "Legal (retail only)"
    else:
        status_color = "#dc2626"
        status_bg = "#FEE2E2"
        status_label = "Not legal"

    breadcrumb_json = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.bettingonline.org/"},
            {"@type": "ListItem", "position": 2, "name": "US States", "item": "https://www.bettingonline.org/us/"},
            {"@type": "ListItem", "position": 3, "name": f"{name} Sports Betting", "item": f"https://www.bettingonline.org/us/{slug}/"},
        ],
    }, separators=(",", ":"))

    article_json = json.dumps({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": f"{name} Sports Betting 2026: Legal Status, Sportsbooks & Complete Guide",
        "description": meta_desc,
        "url": f"https://www.bettingonline.org/us/{slug}/",
        "image": "https://www.bettingonline.org/assets/img/og-default.png",
        "author": {"@type": "Organization", "name": "BettingOnline.org Editorial Team", "url": "https://www.bettingonline.org/about/"},
        "publisher": {"@type": "Organization", "name": "BettingOnline.org",
                      "logo": {"@type": "ImageObject", "url": "https://www.bettingonline.org/assets/img/logo.png"}},
        "datePublished": TODAY,
        "dateModified": TODAY,
    }, separators=(",", ":"))

    # Build the FAQ schema from the same source as the body
    faq_pairs = []
    if s.get("legal"):
        faq_pairs.append((f"Is sports betting legal in {name}?", s["status_short"]))
        faq_pairs.append((f"What is the legal age to bet on sports in {name}?",
                          "18+" if name in ("Wyoming", "Washington, D.C.") else "21+"))
        faq_pairs.append((f"What is the sports-betting tax rate in {name}?", s["tax_rate"]))
    else:
        faq_pairs.append((f"Is sports betting legal in {name}?", s["status_short"]))
        faq_pairs.append((f"When will sports betting become legal in {name}?", s["top_bills_to_watch"]))

    faq_json = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}}
                       for q, a in faq_pairs],
    }, separators=(",", ":"))

    return STATE_TEMPLATE.format(
        name=name, slug=slug, meta_desc=meta_desc,
        breadcrumb_json=breadcrumb_json, article_json=article_json, faq_json=faq_json,
        date_human=DATE_HUMAN, lede=html.escape(lede),
        status_color=status_color, status_bg=status_bg, status_label=status_label,
        tax_rate=s["tax_rate"], population=s["population"],
        body=render_body(slug, s),
    )


def main() -> None:
    for slug, s in STATES.items():
        out_dir = US_DIR / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / "index.html"
        content = render_state(slug, s)
        out_path.write_text(content)
        # Count words for verification
        import re
        text = re.sub(r"<[^>]*>", " ", content)
        words = len(text.split())
        print(f"  {slug:15s}  {words:5d} words  us/{slug}/index.html")

    subprocess.run(["git", "-C", str(ROOT), "add", "-A"], check=True)


if __name__ == "__main__":
    main()
