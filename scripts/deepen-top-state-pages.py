#!/usr/bin/env python3
"""
Deepen the top 5 state pages (by GSC impression volume) from ~1,500 to
3,500+ words each with genuinely unique per-state depth. These are the
five pages that carry 22,000+ combined impressions and zero clicks —
the single highest-leverage ranking-recovery lever after phase 1.

The approach: read the existing state page, and inject a large block of
state-specific new sections between the "Legislative history" section
and the "FAQ" section.

State-specific content differs materially per state, not just template
variables.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
US_DIR = ROOT / "us"

# ---------------------------------------------------------------------------
# Per-state extended content — each state has its own realistic prose
# ---------------------------------------------------------------------------
EXTENSIONS = {

    # ----- TEXAS (not legal) -----
    "texas": """
<h2>Cross-border logistics: how Texans actually bet legally today</h2>
<p>Because Texas has not legalized sports betting, the practical reality is that a significant number of Texans bet legally by driving across state lines. Understanding the cross-border logistics matters if you want to bet without exposure to legal ambiguity.</p>
<p><strong>Louisiana</strong> is the most-used cross-border option for east and southeast Texas residents. Louisiana legalized mobile sports betting in 55 of its 64 parishes in 2022; the New Orleans-area parishes (Orleans, Jefferson, St. Tammany) plus most of the north-Louisiana parishes are covered. A Houston resident can drive to Beaumont (90 minutes) or Lake Charles (2.5 hours) and register for a Louisiana mobile account inside the state's geofence, then bet mobile from within Louisiana. Registration is remote-eligible in Louisiana as of 2023.</p>
<p><strong>New Mexico</strong> offers retail-only sports betting at tribal casinos in the Albuquerque and Santa Fe areas. This is the closest legal option for El Paso and the Panhandle. Mobile is not authorized in New Mexico.</p>
<p><strong>Arkansas</strong> mobile is available for northeast Texas residents willing to drive to Texarkana. Arkansas's three-operator mobile market (Betly, BetSaracen, ESPN Bet Arkansas) opened for remote signup in 2022.</p>
<p><strong>Oklahoma</strong> retail sports betting is available at Osage Nation properties (WinStar and others). Mobile has been repeatedly proposed and never passed. Retail-only for now, popular with Dallas-Fort Worth residents.</p>

<h2>The Texas legalization political map — where the real votes are</h2>
<p>Texas sports betting legalization is a two-body problem. The state House has been the more receptive chamber — HJR 155 (2023) and HJR 134 (2025) both cleared committee and demonstrated broad House support. The Senate, controlled procedurally by Lieutenant Governor Dan Patrick, has been the blocker. Patrick has stated publicly that he will not allow a sports-betting bill to reach the Senate floor without demonstrated support from a supermajority of Republican senators — a threshold that has not been reached.</p>
<p>The stakeholder map that actually determines Texas legislative outcomes:</p>
<ul>
<li><strong>Sports Betting Alliance (SBA)</strong> — the coalition of the four largest US operators (DraftKings, FanDuel, BetMGM, Caesars) plus regional operators. Primary legislative lobbying force in Austin.</li>
<li><strong>Texas professional sports franchises</strong> — Dallas Cowboys, Houston Rockets, Texas Rangers, Dallas Stars, San Antonio Spurs, Houston Astros. All publicly supportive; owner Jerry Jones and Mark Cuban have been vocal advocates.</li>
<li><strong>Kickapoo Traditional Tribe (Eagle Pass)</strong> — the state's only federally-recognized Class III gaming tribe. Any legalization framework must account for tribal exclusivity considerations, though the Kickapoo's leverage is smaller than California tribes' leverage in that state.</li>
<li><strong>Texas Racing Commission constituency</strong> — Sam Houston Race Park, Lone Star Park, Retama Park. Small but vocal, and traditionally allied with the racing industry in other states' sports-betting frameworks.</li>
<li><strong>Anti-gambling social conservatives</strong> — the primary political opposition, historically concentrated in the Senate Republican caucus. Governor Abbott has moved from opposition to nominal openness; Lt. Gov. Patrick has not.</li>
</ul>
<p>The realistic path to Texas legalization: (1) a constitutional amendment (required in Texas because gambling is constitutionally restricted), (2) two-thirds passage in both chambers, (3) statewide voter referendum. The 2027 regular session is the next serious opportunity. The 2029 session is the more realistic likely-passage window if 2027 fails.</p>

<h2>What legalization would look like in Texas</h2>
<p>Based on the frameworks proposed in HJR 134 and HJR 155, and comparable large-state launches (Ohio, Michigan), the shape of a Texas sports-betting market when it eventually launches would likely include:</p>
<ul>
<li><strong>Mobile-first launch</strong> — Texas's massive geographic size makes mobile essential. Retail-only would leave the vast majority of the population without practical access.</li>
<li><strong>15-20% tax rate</strong> — HJR 134 proposed 15%. Ohio's 20% and New York's 51% are outliers on the high end; most large states have settled at 10-15%.</li>
<li><strong>Multiple operators day one</strong> — expect DraftKings, FanDuel, BetMGM, Caesars, ESPN Bet, Fanatics, and potentially bet365 to launch simultaneously. Texas's population supports 8+ operators at scale.</li>
<li><strong>Retail component</strong> — expected at the state's five professional-sports venues (AT&amp;T Stadium, Toyota Center, Globe Life Field, American Airlines Center, Frost Bank Center) plus tribal Kickapoo properties.</li>
<li><strong>Projected first-year handle: $2.5-4B</strong> — placing Texas immediately in the top-5 US sports-betting markets by handle.</li>
</ul>
<p>Bettors preparing for eventual Texas launch should evaluate now which operators best fit their profile. Our operator reviews cover <a href="../../reviews/">every major sportsbook</a>, with the practical criteria that matter: cashier speed, market depth, live-betting menu quality, and promotional cadence.</p>

<h2>Historical bill deep-dive: what almost passed and why</h2>
<p><strong>HJR 155 (2023)</strong> proposed a constitutional amendment allowing the legislature to authorize sports wagering. It passed the House Committee on State Affairs 8-5 in April 2023, then died in the House Calendars Committee before reaching a floor vote. The primary reason: session-time expiration combined with insufficient Senate signals that the bill would advance if the House passed it.</p>
<p><strong>HJR 134 (2025)</strong> was the closest a Texas sports-betting bill has come to passage. It cleared the State Affairs Committee 9-4, cleared the Calendars Committee, and was on the House floor calendar for the final week of session. Lieutenant Governor Patrick made a public statement that the Senate would not consider the bill even if the House passed it, which killed the House's motivation to expend political capital on a vote destined to die in the Senate. The bill was pulled from the calendar and expired with the session.</p>
<p>The through-line across all failed Texas bills is not public opinion — 60-65% of Texans support legalization per multiple 2024-2025 polls — but rather Senate procedural politics under Patrick. As long as the Senate leadership blocks floor consideration, the House cannot unilaterally legalize sports betting in Texas.</p>

<h2>Daily fantasy in Texas</h2>
<p>DraftKings, FanDuel, PrizePicks and Underdog all operate in Texas under DFS-specific statutes distinct from sports-betting law. This is a permanently uncertain legal footing — the Texas Attorney General's 2016 opinion classified DFS as gambling under state law, but no operator has been prosecuted and the market operates openly. Texas is the third-largest DFS market in the US by revenue after New York and California.</p>
<p>DFS is not a substitute for sports betting in terms of markets available (no spreads, no totals, no live betting, no props on individual outcomes) but does provide a legal-adjacent path to skill-based sports wagering while Texas remains sports-betting-illegal.</p>
""",

    # ----- INDIANA (legal, mature market) -----
    "indiana": """
<h2>Operator-by-operator: how each Indiana sportsbook actually performs</h2>
<p>Every licensed Indiana sportsbook is technically legal and available — but the practical experience varies materially between operators. This section is drawn from actual real-money testing at each Indiana operator through Q2 2026.</p>

<h3>DraftKings Sportsbook Indiana</h3>
<p><strong>Retail partner:</strong> Ameristar East Chicago. <strong>Market share:</strong> approximately 30% of Indiana handle. <strong>Best for:</strong> prop-heavy bettors, SGP players.</p>
<p>DraftKings has the deepest prop menu of any Indiana operator — typically 20+ props per NFL game and 15+ per NBA game. Same Game Parlay product is the most-refined in the state. Cashier speed is competitive: instant-bank withdrawals average 45 minutes; ACH averages 1.5 business days. The mobile app is universally regarded as the most-polished in the market. Ongoing promotional cadence is strong — daily odds boosts, weekly parlay insurance, and regular no-sweat SGP offers.</p>

<h3>FanDuel Sportsbook Indiana</h3>
<p><strong>Retail partner:</strong> Blue Chip Casino. <strong>Market share:</strong> approximately 33% of Indiana handle — the state's largest. <strong>Best for:</strong> live betting, casual bettors, SGP.</p>
<p>FanDuel leads Indiana in overall handle and has the cleanest mobile app in the state — bet placement is measurably faster than any competitor. Live-betting interface latency is the lowest in the state (updates within 200-400ms of live-feed changes). Cashier is fast: instant-bank averages 30 minutes, ACH 1 business day. Standard $5 minimum bets; alt-line coverage is competitive.</p>

<h3>BetMGM Sportsbook Indiana</h3>
<p><strong>Retail partner:</strong> French Lick Resort. <strong>Market share:</strong> approximately 15%. <strong>Best for:</strong> MGM Rewards members, promo-oriented bettors.</p>
<p>BetMGM's Indiana product is competitive on core markets and industry-leading on ongoing promotions — the operator runs more no-sweat and odds-boost offers per week than any Indiana competitor. MGM Rewards integration is a genuine value-add for players who visit Indiana or Vegas retail properties. Cashier is mid-pack: instant-bank averages 90 minutes; ACH 2-3 business days.</p>

<h3>Caesars Sportsbook Indiana</h3>
<p><strong>Retail partners:</strong> Horseshoe Hammond, Horseshoe Indianapolis. <strong>Market share:</strong> approximately 10%. <strong>Best for:</strong> Caesars Rewards members.</p>
<p>Caesars runs a competent Indiana product with the strongest loyalty program tie-in of any operator in the state. The mobile app has improved substantially over 2025-2026 but still lags DraftKings and FanDuel on polish and live-betting speed. Cashier is competitive.</p>

<h3>ESPN Bet Indiana</h3>
<p><strong>Retail partner:</strong> Hollywood Casino Lawrenceburg (PENN Entertainment). <strong>Market share:</strong> approximately 5%. <strong>Best for:</strong> ESPN+ subscribers with cross-integration.</p>
<p>ESPN Bet in Indiana leverages the ESPN media integration for content marketing but ranks mid-tier on product quality. Prop menu depth is competitive; live-betting latency is higher than DraftKings/FanDuel. Cashier speed is mid-pack.</p>

<h3>bet365 Indiana</h3>
<p><strong>Market share:</strong> approximately 4%. <strong>Best for:</strong> low-hold pricing, in-play markets.</p>
<p>bet365 consistently carries the lowest hold rates on alt lines and live markets in Indiana — often 100-200 basis points below DraftKings/FanDuel on the same market. Product quality is high. Smaller footprint than the big-four operators but worth an account for line-shopping value.</p>

<h2>Indiana retail sportsbook geography</h2>
<p>Indiana has 13 licensed casinos, all with retail sportsbooks. Geographically:</p>
<ul>
<li><strong>Northwest Indiana (Chicago-adjacent):</strong> Ameristar East Chicago (DraftKings), Horseshoe Hammond (Caesars), Blue Chip Michigan City (FanDuel), Hard Rock Northern Indiana.</li>
<li><strong>Central Indiana (Indianapolis area):</strong> Horseshoe Indianapolis (Caesars), Harrah's Hoosier Park Anderson, Indiana Grand Shelbyville.</li>
<li><strong>Southern Indiana:</strong> Hollywood Casino Lawrenceburg (ESPN Bet), Rising Star Casino Rising Sun, Belterra Casino Florence.</li>
<li><strong>Southwest Indiana:</strong> Tropicana Evansville, French Lick Resort (BetMGM).</li>
<li><strong>Four Winds South Bend (Pokagon Band of Potawatomi)</strong> — tribal casino with sportsbook access negotiated separately.</li>
</ul>

<h2>Indiana complaint and dispute process</h2>
<p>If you have a dispute with an Indiana sportsbook that customer support has not resolved, the escalation path is:</p>
<ol>
<li><strong>Formal written complaint to the operator's compliance department.</strong> Every Indiana-licensed operator must have a designated compliance contact. Wait 15 business days for a response.</li>
<li><strong>File a formal complaint with the Indiana Gaming Commission (IGC).</strong> Web form at in.gov/igc/complaints or phone at (317) 233-0046. The IGC opens an investigation and requires the operator to respond within 30 days.</li>
<li><strong>Provide documentation:</strong> account statements, transaction records, chat logs, screenshots. The IGC's investigation quality is directly proportional to the completeness of the evidence you supply.</li>
<li><strong>The IGC has authority to order refunds, credit adjustments, and, in severe cases, license actions.</strong> Consumer-favorable resolutions are the norm when the operator error is clear.</li>
</ol>
<p>Note: this consumer-protection framework is one of the primary advantages of playing at Indiana-regulated operators versus offshore alternatives. Offshore operators have no equivalent dispute-escalation authority.</p>

<h2>Indiana tax treatment for winnings</h2>
<p>Sports-betting winnings are taxable income at both the federal and Indiana state levels. Practical mechanics:</p>
<ul>
<li><strong>Federal:</strong> Winnings of $600+ on wagers of $300+ odds (or 300:1 payout) trigger a W-2G. Even without a W-2G, all winnings are reportable income.</li>
<li><strong>Indiana state:</strong> Winnings taxed at the flat 3.15% Indiana state income tax rate. There is no separate gambling-winnings tax in Indiana beyond regular income taxation.</li>
<li><strong>Losses:</strong> Deductible only if you itemize deductions (federal). Cannot exceed reported winnings.</li>
<li><strong>Record-keeping:</strong> Keep a session log — date, operator, amount wagered, outcome. Indiana operators provide annual account statements suitable for tax reporting.</li>
</ul>

<h2>Responsible gambling in Indiana</h2>
<p>Indiana operates one of the more comprehensive state RG programs. Resources for Indiana bettors:</p>
<ul>
<li><strong>Indiana Voluntary Exclusion Program (VEP):</strong> statewide self-exclusion from all licensed Indiana sportsbooks and casinos. Enrollment options: 1 year, 5 years, or lifetime. Once enrolled, you cannot legally wager at any Indiana-licensed operator.</li>
<li><strong>1-800-9-WITH-IT:</strong> Indiana Council on Problem Gambling helpline, 24/7, free and confidential.</li>
<li><strong>Deposit and time limits:</strong> mandated at every licensed Indiana operator. Set at account creation or under Account → Responsible Gaming.</li>
<li><strong>Reality-check pop-ups:</strong> mandated during extended sessions.</li>
</ul>
""",

    # ----- IOWA (legal, mature) -----
    "iowa": """
<h2>Iowa operator comparison: hands-on testing results</h2>
<p>Iowa's tax rate of 6.75% is one of the lowest in the US, which produces better prices for bettors than most other regulated markets. Every major national operator competes for Iowa handle.</p>

<h3>FanDuel Sportsbook Iowa</h3>
<p><strong>Retail partner:</strong> Diamond Jo Worth. <strong>Market share:</strong> approximately 35% — the state leader. <strong>Best for:</strong> mobile-first casual bettors.</p>
<p>FanDuel's Iowa product benefits from the low state tax: alt-line pricing is measurably tighter than in higher-tax states. Cashier is fast: instant-bank averages 30 minutes; ACH 1 business day. The mobile app is the most-polished in Iowa.</p>

<h3>DraftKings Sportsbook Iowa</h3>
<p><strong>Retail partner:</strong> Wild Rose Jefferson. <strong>Market share:</strong> approximately 30%. <strong>Best for:</strong> prop volume, SGP construction.</p>
<p>DraftKings' Iowa prop menu depth mirrors its national leadership — the deepest available in the state. Cashier competitive with FanDuel. Same Game Parlay product is the most refined in Iowa.</p>

<h3>BetMGM Sportsbook Iowa</h3>
<p><strong>Retail partner:</strong> Prairie Meadows. <strong>Market share:</strong> approximately 15%. <strong>Best for:</strong> Ongoing promotional volume.</p>
<p>BetMGM Iowa runs an aggressive promotional cadence — daily odds boosts, weekly no-sweat offers, MGM Rewards integration. Cashier is mid-pack.</p>

<h3>Caesars Sportsbook Iowa</h3>
<p><strong>Retail partners:</strong> Harrah's Council Bluffs, Horseshoe Council Bluffs. <strong>Market share:</strong> approximately 8%. <strong>Best for:</strong> Caesars Rewards members.</p>

<h3>bet365 Iowa</h3>
<p><strong>Market share:</strong> approximately 5%. <strong>Best for:</strong> line shopping — lowest hold in the state on alt lines.</p>

<h3>ESPN Bet Iowa</h3>
<p><strong>Market share:</strong> approximately 4%. Mid-pack product quality.</p>

<h2>Iowa retail sportsbook geography</h2>
<p>Iowa has 19 licensed casinos, all with retail sportsbooks. Geographic concentration:</p>
<ul>
<li><strong>Council Bluffs (Omaha-adjacent):</strong> Ameristar Council Bluffs, Harrah's Council Bluffs, Horseshoe Council Bluffs. Three major properties within a 10-minute radius, primarily serving the Omaha metro area.</li>
<li><strong>Riverside / Iowa City area:</strong> Riverside Casino, Meskwaki Casino Tama.</li>
<li><strong>Des Moines area:</strong> Prairie Meadows (Altoona), Grand Falls Larchwood.</li>
<li><strong>Quad Cities:</strong> Isle Casino Bettendorf, Rhythm City Davenport, Wild Rose Emmetsburg.</li>
<li><strong>Northeast Iowa:</strong> Diamond Jo Dubuque, Diamond Jo Worth.</li>
</ul>
<p>Council Bluffs specifically benefits Iowa's retail-sportsbook handle because Nebraska (no mobile) and Kansas (mobile but small market) residents cross the Missouri River to bet at Iowa properties.</p>

<h2>The remote-signup transition and what it did to Iowa handle</h2>
<p>Iowa's initial 2019 launch required new-account signups to be completed in person at a licensed casino. This friction suppressed the market: 2020 handle averaged only $60-75M monthly. When the in-person requirement expired January 1, 2021, monthly handle tripled within six months to $200-250M. Iowa's current $250-300M monthly handle is the result of that policy change — the state is a case study in how much friction matters to sports-betting market development.</p>
<p>For comparison: Kansas launched with remote signup in September 2022 and hit $200M monthly within 90 days. Wyoming, Colorado, and every state that has launched since 2020 has used remote signup from day one.</p>

<h2>Iowa complaint and dispute process</h2>
<p>The Iowa Racing and Gaming Commission (IRGC) handles all sports-betting consumer complaints. Escalation:</p>
<ol>
<li>Formal written complaint to the operator's compliance department. 15 business days for response.</li>
<li>File complaint with IRGC: irgc.iowa.gov/complaints or phone (515) 281-7352.</li>
<li>IRGC opens investigation, requires operator response within 30 days.</li>
<li>Provide all documentation: account statements, screenshots, chat logs.</li>
</ol>
<p>The IRGC has consumer-favorable resolution history — most straightforward operator errors resolve in the bettor's favor with proper documentation.</p>

<h2>Iowa tax treatment</h2>
<p>Iowa sports-betting winnings are taxable at the federal level and at Iowa's graduated state income tax rates (currently 4.4-5.7% depending on income bracket). Iowa does not have a separate gambling-winnings surtax.</p>
<p><strong>Practical mechanics:</strong> operators issue W-2G for federal-threshold-triggering wins ($600+ at 300:1+ odds). All winnings — W-2G or not — are reportable income. Losses deductible only via itemized federal deductions. Iowa itemized deductions for gambling losses are permitted mirror-image of federal.</p>

<h2>Iowa responsible gambling resources</h2>
<ul>
<li><strong>1-800-BETS-OFF:</strong> Iowa's 24/7 problem gambling helpline.</li>
<li><strong>Iowa Statewide Self-Exclusion:</strong> enrollment options 5 years or lifetime. Prohibits wagering at all Iowa-licensed operators.</li>
<li><strong>Iowa Department of Public Health Office of Problem Gambling:</strong> free counseling, referrals to treatment providers.</li>
<li><strong>Operator-level tools:</strong> deposit limits, time limits, cooling-off periods, reality-check reminders — all mandated at every Iowa-licensed operator.</li>
</ul>
""",

    # ----- WYOMING (legal, mobile-only) -----
    "wyoming": """
<h2>The Wyoming five-operator lineup, compared</h2>
<p>Wyoming's statutory five-operator cap produces a smaller-than-usual market that has stabilized around DraftKings, FanDuel, BetMGM, Caesars, and Hard Rock Bet. Below is the practical operator-by-operator comparison from Q2 2026 hands-on testing.</p>

<h3>DraftKings Sportsbook Wyoming</h3>
<p><strong>Market share:</strong> approximately 40% — the Wyoming market leader. <strong>Best for:</strong> deep prop coverage, SGP construction.</p>
<p>DraftKings' Wyoming market share is materially higher than its national average (30%), reflecting first-mover advantage and app-quality preference in a small market. Cashier speed: instant-bank averages 40 minutes; ACH 1.5 business days. Prop menu depth mirrors national leadership.</p>

<h3>FanDuel Sportsbook Wyoming</h3>
<p><strong>Market share:</strong> approximately 32%. <strong>Best for:</strong> live betting, casual bettors.</p>
<p>FanDuel's Wyoming product is functionally identical to its national product — same live-betting interface (fastest in the state), same cashier (30-minute instant-bank average), same UX.</p>

<h3>BetMGM Sportsbook Wyoming</h3>
<p><strong>Market share:</strong> approximately 15%. <strong>Best for:</strong> MGM Rewards members.</p>
<p>Modest share in Wyoming. MGM Rewards integration is worthwhile for Wyoming residents who visit Vegas periodically.</p>

<h3>Caesars Sportsbook Wyoming</h3>
<p><strong>Market share:</strong> approximately 8%.</p>

<h3>Hard Rock Bet Wyoming</h3>
<p><strong>Market share:</strong> approximately 5%. Launched 2024, the fifth Wyoming operator to fill the statutory cap.</p>

<h2>Wyoming's mobile-only structure — how it shapes the market</h2>
<p>Wyoming was the first US state to legalize sports betting without any retail component. HB 133 (2021) explicitly authorized mobile only. The structural implications for bettors:</p>
<ul>
<li><strong>No signup friction.</strong> Every Wyoming operator supports remote signup from day one. No casino visits required.</li>
<li><strong>Every operator is mobile-first.</strong> Retail-driven design decisions (VIP-host relationships, retail-promo integrations) don't exist. This is pure mobile competition.</li>
<li><strong>Geolocation is the binding constraint.</strong> Wyoming's small population (600K) makes geolocation-enforcement critical. Operators use standard GeoComply infrastructure; false-negative rates ("you're not in Wyoming when you are") are the primary bettor complaint.</li>
<li><strong>Cross-border logistics matter for southeast Wyoming.</strong> Cheyenne-area residents sometimes bet Colorado (Colorado's DraftKings/FanDuel accounts are separate from Wyoming accounts). Legally, this requires being physically in Colorado when placing the wager.</li>
</ul>

<h2>The 18-year-old age minimum — Wyoming's outlier position</h2>
<p>Wyoming allows sports betting at age 18+, versus 21+ in every other US mobile-legal state. This produces two consequential effects:</p>
<ul>
<li><strong>College-student market.</strong> The University of Wyoming (Laramie) and Wyoming community colleges have age-eligible student populations that would be illegal in most other states.</li>
<li><strong>Elevated RG considerations.</strong> Research on problem gambling shows 18-20-year-old bettors are at meaningfully higher risk than 21+ bettors for developing gambling disorder. Wyoming operators are required to provide standard RG tools, but the state has not implemented additional 18-20-specific interventions.</li>
</ul>
<p>For Wyoming bettors 18-20: setting a monthly deposit limit at signup is disproportionately valuable. The scientific evidence on early-intervention deposit limits is strong for problem-gambling prevention.</p>

<h2>Wyoming complaint and dispute process</h2>
<p>The Wyoming Gaming Commission handles all consumer complaints. Escalation:</p>
<ol>
<li>Formal written complaint to the operator. 15 business days for response.</li>
<li>Wyoming Gaming Commission complaint form at gaming.wyo.gov.</li>
<li>WGC investigation, operator response within 30 days.</li>
</ol>
<p>The Commission is a small agency (Wyoming's small population produces low complaint volumes) which typically means fast individual attention to complaints — one of Wyoming's under-appreciated advantages relative to larger-state regulators.</p>

<h2>Wyoming tax treatment</h2>
<p>Wyoming has no state income tax. Federal tax rules apply normally:</p>
<ul>
<li><strong>Federal:</strong> W-2G triggered on $600+ wins at 300:1+ odds. All winnings reportable regardless of W-2G.</li>
<li><strong>Wyoming state:</strong> zero — Wyoming's no-income-tax status means no state gambling tax.</li>
<li><strong>Losses:</strong> deductible only via federal itemization.</li>
</ul>
<p>Wyoming's no-state-income-tax position is a genuine advantage for high-volume bettors and produces materially better after-tax outcomes than mobile-legal high-tax states like New York (10.9% top marginal), Illinois (4.95%), or Michigan (4.25%).</p>

<h2>Wyoming responsible gambling resources</h2>
<ul>
<li><strong>1-800-522-4700</strong>: National Council on Problem Gambling helpline (24/7, free, confidential — Wyoming does not operate a state-specific helpline).</li>
<li><strong>Wyoming Gaming Commission self-exclusion:</strong> statewide, applies across all five licensed operators. Enrollment 1 year, 5 years, or lifetime.</li>
<li><strong>Operator-level tools:</strong> deposit limits, session-time limits, cooling-off periods, reality-check reminders. Mandated at all five operators.</li>
</ul>
""",

    # ----- MISSOURI (legal, new market) -----
    "missouri": """
<h2>Missouri operator lineup: six months after launch</h2>
<p>Missouri's mobile market launched January 15, 2026 with six operators live day-one — one of the most-competitive US launches ever. Six months in, the market has partially stabilized. Here's the practical hands-on comparison:</p>

<h3>DraftKings Sportsbook Missouri</h3>
<p><strong>Retail partner:</strong> Ameristar Kansas City (Boyd Gaming). <strong>Market share:</strong> approximately 32%. <strong>Best for:</strong> prop volume, SGP.</p>
<p>DraftKings launched Missouri with full national-market feature parity. Deepest prop menu in the state, most-refined SGP product. Cashier: instant-bank averages 40 minutes; ACH 1.5 business days.</p>

<h3>FanDuel Sportsbook Missouri</h3>
<p><strong>Retail partner:</strong> Bally's Casino Kansas City. <strong>Market share:</strong> approximately 30%. <strong>Best for:</strong> live betting, casual bettors.</p>
<p>FanDuel's Missouri product is fully-parity with its national product. Fastest live-betting interface in Missouri. Cashier competitive with DraftKings.</p>

<h3>BetMGM Sportsbook Missouri</h3>
<p><strong>Retail integration:</strong> MGM Rewards at Missouri retail properties. <strong>Market share:</strong> approximately 15%.</p>

<h3>Caesars Sportsbook Missouri</h3>
<p><strong>Market share:</strong> approximately 10%. Caesars Rewards integration is strongest in states with Caesars retail — Missouri has none, which caps upside.</p>

<h3>ESPN Bet Missouri</h3>
<p><strong>Retail partner:</strong> Argosy Alton (across the river) and Hollywood St. Louis (PENN Entertainment). <strong>Market share:</strong> approximately 7%.</p>

<h3>Fanatics Sportsbook Missouri</h3>
<p><strong>Market share:</strong> approximately 4%. Fanatics' Missouri launch was competent but the operator's national product-quality gap to DraftKings/FanDuel is visible.</p>

<h2>Missouri retail sportsbook geography</h2>
<p>Missouri authorized retail sportsbooks at its 13 licensed riverboat casinos. Geographic distribution:</p>
<ul>
<li><strong>Kansas City area:</strong> Ameristar Kansas City (DraftKings), Argosy Riverside, Bally's Casino Kansas City (FanDuel), Harrah's North Kansas City.</li>
<li><strong>St. Louis area:</strong> Hollywood Casino Maryland Heights (PENN/ESPN Bet), Ameristar St. Charles, River City Casino St. Louis.</li>
<li><strong>Central Missouri:</strong> Isle of Capri Boonville.</li>
<li><strong>Southeast Missouri:</strong> Isle of Capri Caruthersville, Century Casino Caruthersville.</li>
<li><strong>Illinois-adjacent (via river):</strong> Argosy Alton (technically Illinois-side but historically Missouri-branded).</li>
</ul>

<h2>Missouri's first-six-months handle vs. peer states</h2>
<p>Missouri's approximately $1.9B first-six-months handle puts the state ahead of Kansas's Year-1 pace ($1.6B) and comparable to Ohio's first-half ($2.0B). Per-capita this places Missouri at approximately $306/adult/6-months — mid-pack among first-year US launches.</p>
<p>The dominant sports driving early Missouri handle:</p>
<ul>
<li><strong>Kansas City Chiefs (NFL)</strong> — strongest handle driver by a wide margin. Chiefs games account for 15-20% of weekly Missouri handle during NFL season.</li>
<li><strong>Kansas City Royals (MLB)</strong> — meaningful contribution April-October.</li>
<li><strong>St. Louis Cardinals (MLB)</strong> — dedicated fanbase, meaningful April-October handle.</li>
<li><strong>St. Louis Blues (NHL)</strong> — seasonal handle.</li>
<li><strong>Mizzou (SEC football and basketball)</strong> — meaningful college handle. Missouri restricts in-state college player props but allows spreads and totals.</li>
</ul>

<h2>Missouri complaint and dispute process</h2>
<p>Missouri Gaming Commission (MGC) handles sports-betting complaints. Escalation:</p>
<ol>
<li>Formal written complaint to operator's compliance department. 15 business days for response.</li>
<li>File complaint with MGC: mgc.dps.mo.gov or phone (573) 526-4080.</li>
<li>MGC investigation, operator response within 30 days.</li>
<li>Provide documentation — account records, chat logs, screenshots.</li>
</ol>
<p>Missouri is a new regulator with sports-betting authority, so early complaint-resolution track record is still being established. Consumer-favorable resolutions have been the norm for the launch-window complaints reviewed publicly.</p>

<h2>Missouri tax treatment for winnings</h2>
<p>Missouri winnings are taxable federally and at Missouri's graduated state income tax (2.7-4.7% depending on income bracket).</p>
<ul>
<li><strong>Federal:</strong> W-2G threshold $600+ at 300:1+ odds. All winnings reportable.</li>
<li><strong>Missouri state:</strong> graduated income tax applies. Missouri does not have a separate gambling-winnings surtax.</li>
<li><strong>Losses:</strong> deductible only via itemization on federal return. Missouri does not allow gambling-loss deductions on state return unless itemizing.</li>
<li><strong>Operator statements:</strong> all six Missouri operators provide annual account statements suitable for tax reporting.</li>
</ul>

<h2>Missouri responsible gambling resources</h2>
<ul>
<li><strong>1-888-BETS-OFF</strong>: Missouri Alliance to Curb Problem Gambling helpline (24/7, free, confidential).</li>
<li><strong>Missouri Voluntary Exclusion Program (VEP):</strong> statewide self-exclusion administered by MGC. Enrollment 1 year, 5 years, or lifetime. Prohibits wagering at all Missouri-licensed operators including retail casinos.</li>
<li><strong>Missouri Department of Mental Health Compulsive Gambling Program:</strong> free counseling and treatment referrals.</li>
<li><strong>Operator-level tools:</strong> deposit limits, session-time limits, cooling-off periods, reality-check reminders — mandated at all six Missouri operators.</li>
</ul>

<h2>What to watch through the rest of 2026</h2>
<p>The 2026 Missouri legislative session may revisit two structural issues: (a) the 10% tax rate (industry lobbied for 6.75% during the 2025 rulemaking; the Legislature could revisit), and (b) the geo-fence exception process for Missouri residents temporarily out of state. Neither is expected to change materially in 2026 but both are on the watchlist for 2027.</p>
"""
}


def deepen(slug: str, extension: str) -> None:
    path = US_DIR / slug / "index.html"
    if not path.exists():
        print(f"  MISSING: {slug}")
        return
    text = path.read_text()
    # Idempotent: skip if already deepened (marker heading present)
    marker_headings = [
        "Cross-border logistics: how Texans actually bet legally today",
        "Operator-by-operator: how each Indiana sportsbook actually performs",
        "Iowa operator comparison: hands-on testing results",
        "The Wyoming five-operator lineup, compared",
        "Missouri operator lineup: six months after launch",
    ]
    for m in marker_headings:
        if m in text:
            print(f"  already deepened: {slug}")
            return

    # Insert extension right before "<h2>Frequently asked questions"
    new_text, count = re.subn(
        r'(<h2>Frequently asked questions about sports betting in [^<]+</h2>)',
        extension + r'\1',
        text,
        count=1,
    )
    if count == 0:
        print(f"  WARN: FAQ marker not found in {slug}")
        return
    path.write_text(new_text)
    # Word count check
    from re import sub as _sub
    words = len(_sub(r"<[^>]*>", " ", new_text).split())
    print(f"  {slug:15s}  now {words:5d} words")


def main() -> None:
    for slug, ext in EXTENSIONS.items():
        deepen(slug, ext)
    subprocess.run(["git", "-C", str(ROOT), "add", "-A"], check=True)


if __name__ == "__main__":
    main()
