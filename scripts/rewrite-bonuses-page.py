#!/usr/bin/env python3
"""
Rewrite /bonuses/index.html so every brand-specific section reflects
only the 13 actually-promoted brands. Educational content is preserved;
promotional / listing / ranking / filter sections are regenerated.

Promoted brands:
  Sportsbooks (3):  BetOnline, Sportsbetting.ag, BetUS
  Casinos    (3):   BetOnline Casino, Sportsbetting.ag Casino, BetUS Casino
  Poker      (7):   Black Chip, ACR, Ya, True, BetOnline Poker,
                    TigerGaming, Sportsbetting.ag Poker
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BONUSES = ROOT / "bonuses" / "index.html"

# ---------------------------------------------------------------------------
# Brand data — matches the promoted brands used in the rest of the site
# ---------------------------------------------------------------------------
TRACKERS = {
    "betonline-sportsbook":     "https://record.betonlineaffiliates.ag/_CZzXr-5WlPe6tyDIijdDK2Nd7ZgqdRLk/2/",
    "sportsbetting-sportsbook": "https://record.sportsbettingaffiliates.ag/_CZzXr-5WlPeh_7RUBh20pWNd7ZgqdRLk/2/",
    "betus-sportsbook":         "https://record.revmasters.com/_B-rumzaR8azUOsjNOfgKeWNd7ZgqdRLk/2/",
    "betonline-casino":         "https://record.betonlineaffiliates.ag/_CZzXr-5WlPfYJMJFEJBL7mNd7ZgqdRLk/3/",
    "sportsbetting-casino":     "https://record.betonlineaffiliates.ag/_CZzXr-5WlPfYJMJFEJBL7mNd7ZgqdRLk/3/",
    "betus-casino":             "https://record.revmasters.com/_B-rumzaR8axhg6WO2I1rgWNd7ZgqdRLk/2/",
    "black-chip-poker":         "https://go.wpnaffiliates.com/visit/?bta=237090&nci=5355",
    "acr-poker":                "https://go.wpnaffiliates.com/visit/?bta=237090&brand=americascardroom",
    "ya-poker":                 "https://go.wpnaffiliates.com/visit/?bta=237090&brand=yapoker",
    "true-poker":               "https://go.wpnaffiliates.com/visit/?bta=237090&brand=truepoker",
    "betonline-poker":          "https://record.betonlineaffiliates.ag/_CZzXr-5WlPfYJMJFEJBL7mNd7ZgqdRLk/3/",
    "tigergaming-poker":        "https://record.betonlineaffiliates.ag/_CZzXr-5WlPfYJMJFEJBL7mNd7ZgqdRLk/3/",
    "sportsbetting-poker":      "https://record.betonlineaffiliates.ag/_CZzXr-5WlPfYJMJFEJBL7mNd7ZgqdRLk/3/",
}


def cta(slug: str, label: str) -> str:
    return (f'<a href="{TRACKERS[slug]}" rel="sponsored nofollow" target="_blank" '
            f'data-affiliate-brand="{slug}" class="btn btn-primary btn-sm">{label}</a>')


# ---------------------------------------------------------------------------
# NEW SECTIONS
# ---------------------------------------------------------------------------

NEW_HERO_TAGS = '''      <div style="margin-top:18px;display:flex;gap:8px;flex-wrap:wrap">
        <span class="tag primary">13 promoted offers</span>
        <span class="tag">$22,000+ in nominal value</span>
        <span class="tag">Updated monthly</span>
        <span class="tag">Independent editorial</span>
      </div>'''


NEW_TOP_TABLES = f'''  <section class="section" style="padding-top:32px">
    <div class="container">
      <h2>At a glance: our promoted sportsbook welcome offers</h2>
      <p class="muted">Independent editorial ranking of the sportsbooks we currently promote. Click a CTA to visit the operator with our affiliate tracking; click Details to see the T&amp;C breakdown.</p>
      <div style="overflow-x:auto;margin-top:18px">
        <table class="bo-quick-table" style="width:100%;min-width:780px">
          <thead><tr><th>Operator</th><th>Offer</th><th>Bonus type</th><th>Rollover</th><th>Regions</th><th></th></tr></thead>
          <tbody>
            <tr>
              <td><strong>BetOnline</strong></td>
              <td>50% up to $1,000 + crypto reloads</td>
              <td>Deposit match</td>
              <td>10× dep+bonus</td>
              <td>US-facing offshore</td>
              <td><div style="display:flex;gap:6px;flex-wrap:wrap">{cta("betonline-sportsbook","Claim →")}<a href="../reviews/betonline-sportsbook/" class="btn btn-ghost btn-sm">Review</a></div></td>
            </tr>
            <tr>
              <td><strong>Sportsbetting.ag</strong></td>
              <td>50% up to $1,000 + crypto reloads</td>
              <td>Deposit match</td>
              <td>10× dep+bonus</td>
              <td>US-facing offshore</td>
              <td><div style="display:flex;gap:6px;flex-wrap:wrap">{cta("sportsbetting-sportsbook","Claim →")}<a href="../reviews/sportsbetting-sportsbook/" class="btn btn-ghost btn-sm">Review</a></div></td>
            </tr>
            <tr>
              <td><strong>BetUS</strong></td>
              <td>125% crypto up to $3,125 (or 100% up to $2,500 card)</td>
              <td>Deposit match</td>
              <td>10× dep+bonus</td>
              <td>US-facing offshore</td>
              <td><div style="display:flex;gap:6px;flex-wrap:wrap">{cta("betus-sportsbook","Claim →")}<a href="../reviews/betus-sportsbook/" class="btn btn-ghost btn-sm">Review</a></div></td>
            </tr>
          </tbody>
        </table>
      </div>

      <h2 style="margin-top:40px">At a glance: our promoted casino welcome offers</h2>
      <div style="overflow-x:auto;margin-top:18px">
        <table class="bo-quick-table" style="width:100%;min-width:780px">
          <thead><tr><th>Operator</th><th>Offer</th><th>Bonus type</th><th>Rollover</th><th>Regions</th><th></th></tr></thead>
          <tbody>
            <tr>
              <td><strong>BetOnline Casino</strong></td>
              <td>100% up to $3,000 across first 3 deposits</td>
              <td>Deposit match</td>
              <td>30× slots / 60× tables</td>
              <td>US-facing offshore</td>
              <td><div style="display:flex;gap:6px;flex-wrap:wrap">{cta("betonline-casino","Claim →")}<a href="../reviews/betonline-casino/" class="btn btn-ghost btn-sm">Review</a></div></td>
            </tr>
            <tr>
              <td><strong>Sportsbetting.ag Casino</strong></td>
              <td>100% up to $3,000 across first 3 deposits</td>
              <td>Deposit match</td>
              <td>30× slots / 60× tables</td>
              <td>US-facing offshore</td>
              <td><div style="display:flex;gap:6px;flex-wrap:wrap">{cta("sportsbetting-casino","Claim →")}<a href="../reviews/sportsbetting-casino/" class="btn btn-ghost btn-sm">Review</a></div></td>
            </tr>
            <tr>
              <td><strong>BetUS Casino</strong></td>
              <td>150% crypto up to $3,000</td>
              <td>Deposit match</td>
              <td>30× slots</td>
              <td>US-facing offshore</td>
              <td><div style="display:flex;gap:6px;flex-wrap:wrap">{cta("betus-casino","Claim →")}<a href="../reviews/betus-casino/" class="btn btn-ghost btn-sm">Review</a></div></td>
            </tr>
          </tbody>
        </table>
      </div>

      <h2 style="margin-top:40px">At a glance: our promoted poker welcome offers</h2>
      <div style="overflow-x:auto;margin-top:18px">
        <table class="bo-quick-table" style="width:100%;min-width:840px">
          <thead><tr><th>Room</th><th>Offer</th><th>Network</th><th>Rakeback</th><th></th></tr></thead>
          <tbody>
            <tr>
              <td><strong>Black Chip Poker</strong></td>
              <td>100% up to $2,000 first deposit</td>
              <td>Winning Poker Network</td>
              <td>Elite Benefits 20-65%</td>
              <td>{cta("black-chip-poker","Claim →")}</td>
            </tr>
            <tr>
              <td><strong>ACR Poker</strong></td>
              <td>100% up to $2,000 + Venom qualifiers</td>
              <td>Winning Poker Network</td>
              <td>Elite Benefits 20-65%</td>
              <td>{cta("acr-poker","Claim →")}</td>
            </tr>
            <tr>
              <td><strong>Ya Poker</strong></td>
              <td>100% up to $2,000 + rakeback rewards</td>
              <td>Winning Poker Network</td>
              <td>Elite Benefits 20-65%</td>
              <td>{cta("ya-poker","Claim →")}</td>
            </tr>
            <tr>
              <td><strong>True Poker</strong></td>
              <td>100% up to $1,000 + WPN promos</td>
              <td>Winning Poker Network</td>
              <td>Elite Benefits 20-65%</td>
              <td>{cta("true-poker","Claim →")}</td>
            </tr>
            <tr>
              <td><strong>BetOnline Poker</strong></td>
              <td>100% up to $1,000 + weekly reloads</td>
              <td>Chico Poker Network</td>
              <td>Rebate 15-35%</td>
              <td>{cta("betonline-poker","Claim →")}</td>
            </tr>
            <tr>
              <td><strong>TigerGaming Poker</strong></td>
              <td>100% up to $1,000 + poker rebates</td>
              <td>Chico Poker Network</td>
              <td>Rebate 15-35%</td>
              <td>{cta("tigergaming-poker","Claim →")}</td>
            </tr>
            <tr>
              <td><strong>Sportsbetting.ag Poker</strong></td>
              <td>100% up to $1,000 + weekly reloads</td>
              <td>Chico Poker Network</td>
              <td>Rebate 15-35%</td>
              <td>{cta("sportsbetting-poker","Claim →")}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>'''


BROWSE_HEADING = '''    <div class="container">
      <h2>Browse all 13 promoted welcome offers</h2>
      <p class="muted">Filter by category and bonus type. Every offer below carries our editorial team's independent review.</p>'''


NEW_BEST_SPORTSBOOK = f'''          <h2 id="best-sportsbook">Best sportsbook welcome offers — ranked and analyzed</h2>

          <p>Our ranking weights realized value (nominal bonus after rollover), cashier speed (how fast you actually see winnings), pricing (hold rates on standard sides), and operator quality. All three sportsbooks below are US-facing offshore books — see our <a href="../trust/">Trust &amp; Transparency</a> page for a full discussion of the offshore-vs-regulated trade-off before choosing.</p>

          <div class="bo-tier-card">
            <h3>1. BetOnline — 50% Welcome Bonus up to $1,000 <span class="tag primary">Best all-around</span></h3>
            <p>The strongest all-around US-facing offshore welcome offer. 50% match up to $1,000 with a friendly 10× (deposit + bonus) rollover on qualifying sports wagers. Crypto deposits unlock a series of reload boosters that continue past the welcome window, which is where BetOnline's total-value calculus pulls clear of most competitors. Cashier is fast (crypto withdrawals typically clear in 1-24 hours), and the account works across sports, casino, and poker with a single login. {cta("betonline-sportsbook","Claim at BetOnline →")}</p>
            <div class="badge-row">
              <span class="tag">Min dep $20 crypto</span><span class="tag">10× rollover</span><span class="tag">30-day expiry</span><span class="tag">Realized value ~$650</span>
            </div>
          </div>

          <div class="bo-tier-card">
            <h3>2. BetUS — 125% Crypto Welcome Bonus up to $3,125 <span class="tag">Largest headline match</span></h3>
            <p>The largest headline welcome match in the US-facing offshore market. Crypto deposits unlock the 125% tier and a $3,125 ceiling; card deposits get a still-strong 100% match up to $2,500. BetUS has been operating since 1994 — one of the longest-tenured brands in offshore — and specializes in NFL and college football depth. The 10× rollover matches BetOnline; realized value depends on volume during the welcome window. {cta("betus-sportsbook","Claim at BetUS →")}</p>
            <div class="badge-row">
              <span class="tag">Min dep $50 crypto</span><span class="tag">10× rollover</span><span class="tag">30-day expiry</span><span class="tag">Realized value cap-dependent</span>
            </div>
          </div>

          <div class="bo-tier-card">
            <h3>3. Sportsbetting.ag — 50% Welcome Bonus up to $1,000 <span class="tag">Best second-book access</span></h3>
            <p>Sister brand to BetOnline on the same underlying Chico platform. Same odds, same cashier, same live-betting menu — but a distinct account and a slightly different reload calendar. Volume bettors typically open both to double the reload-offer surface area. Structurally identical welcome offer. {cta("sportsbetting-sportsbook","Claim at Sportsbetting.ag →")}</p>
            <div class="badge-row">
              <span class="tag">Min dep $20 crypto</span><span class="tag">10× rollover</span><span class="tag">30-day expiry</span><span class="tag">Realized value ~$650</span>
            </div>
          </div>'''


NEW_BEST_CASINO = f'''          <h2 id="best-casino">Best online casino welcome offers</h2>

          <p>Casino welcome offers run on different economics from sportsbook offers. Larger nominal bonuses (100% match up to $3,000) but higher rollover requirements (30-60×) materially reduce realized value. The realized-value framework matters more in casino than in sportsbook welcome offers because the rollover math compounds against you — see our worked example below for real-dollar impact.</p>

          <div class="bo-tier-card">
            <h3>1. BetOnline Casino — 100% Match up to $3,000 (across 3 deposits) <span class="tag primary">Best all-around</span></h3>
            <p>Split across your first three deposits, BetOnline Casino's welcome package tops out at $3,000 in bonus funds. 30× rollover applies to slot play (which contributes 100%); table games contribute 10-20% and carry effectively 60× rollover. Available to US-facing offshore players. Slot library covers 500+ titles from Betsoft, Nucleus, Rival, Dragon, Concept and Fresh Deck; live-dealer floor covers all major game types. {cta("betonline-casino","Claim at BetOnline Casino →")}</p>
            <div class="badge-row">
              <span class="tag">Min dep $25 crypto</span><span class="tag">30× slots</span><span class="tag">30-day expiry</span><span class="tag">Realized value ~$800</span>
            </div>
          </div>

          <div class="bo-tier-card">
            <h3>2. BetUS Casino — 150% Crypto Match up to $3,000 <span class="tag">Largest crypto uplift</span></h3>
            <p>Highest headline match percentage in the US-facing offshore casino segment. Crypto deposits only — card deposits get the standard 100%. Slot library 300+ titles from BetSoft, Real Time Gaming and Nucleus. Progressive jackpots across 10+ titles. 30× rollover on slots. {cta("betus-casino","Claim at BetUS Casino →")}</p>
            <div class="badge-row">
              <span class="tag">Min dep $50 crypto</span><span class="tag">30× slots</span><span class="tag">30-day expiry</span><span class="tag">Realized value ~$700</span>
            </div>
          </div>

          <div class="bo-tier-card">
            <h3>3. Sportsbetting.ag Casino — 100% Match up to $3,000 (across 3 deposits)</h3>
            <p>Sister brand to BetOnline Casino on the same underlying platform. Mirror slot library and live-dealer floor; distinct promotional cadence. Volume casino players benefit from holding both to capture different reload calendars. {cta("sportsbetting-casino","Claim at Sportsbetting.ag Casino →")}</p>
            <div class="badge-row">
              <span class="tag">Min dep $25 crypto</span><span class="tag">30× slots</span><span class="tag">30-day expiry</span><span class="tag">Realized value ~$800</span>
            </div>
          </div>'''


NEW_BEST_POKER = f'''          <h2 id="best-poker">Best online poker welcome offers</h2>

          <p>Poker welcome offers are structured differently from sportsbook and casino — typically a deposit match released incrementally as you play (rake-based clearance) rather than a one-time bonus drop. This means you must play meaningful poker volume to realize the full bonus. Rakeback structures matter more than headline welcome numbers on a lifetime basis. We promote seven rooms across the two major US-facing offshore networks (Winning Poker Network + Chico Poker Network).</p>

          <div class="bo-tier-card">
            <h3>1. ACR Poker — 100% Match up to $2,000 + Venom qualifiers <span class="tag primary">Best for MTT players</span></h3>
            <p>The flagship Winning Poker Network brand. Home of the Venom ($10M+ GTD marquee event), the biggest MTT available to US-based players. Cash-game liquidity is the deepest in offshore poker. Elite Benefits rakeback scales from 20% for casual players to 65% at high volume. Same shared player pool as Black Chip, Ya Poker, and True Poker. {cta("acr-poker","Claim at ACR Poker →")}</p>
            <div class="badge-row">
              <span class="tag">Min dep $25 crypto</span><span class="tag">Rake clearance</span><span class="tag">60-day expiry</span><span class="tag">Elite Benefits 20-65%</span>
            </div>
          </div>

          <div class="bo-tier-card">
            <h3>2. Black Chip Poker — 100% Match up to $2,000 + 27% Elite Benefits <span class="tag">Softest cash tables on WPN</span></h3>
            <p>Same WPN player pool as ACR — but Black Chip's brand positioning attracts a slightly softer cash-game population. Best pick for cash-game specialists who want the WPN liquidity without the tough-reg brand-recognition tax at ACR. Same rakeback structure and same access to Venom qualifiers. {cta("black-chip-poker","Claim at Black Chip Poker →")}</p>
            <div class="badge-row">
              <span class="tag">Min dep $25 crypto</span><span class="tag">Rake clearance</span><span class="tag">60-day expiry</span><span class="tag">Elite Benefits 20-65%</span>
            </div>
          </div>

          <div class="bo-tier-card">
            <h3>3. Ya Poker — 100% Match up to $2,000 + rakeback rewards <span class="tag">Best crypto UX on WPN</span></h3>
            <p>Newer WPN skin with a crypto-first cashier and streamlined lobby. Same shared WPN player pool as ACR and Black Chip. Best crypto-deposit UX among the WPN skins. {cta("ya-poker","Claim at Ya Poker →")}</p>
            <div class="badge-row">
              <span class="tag">Min dep $20 crypto</span><span class="tag">Rake clearance</span><span class="tag">60-day expiry</span><span class="tag">Elite Benefits 20-65%</span>
            </div>
          </div>

          <div class="bo-tier-card">
            <h3>4. True Poker — 100% Match up to $1,000 + WPN promos</h3>
            <p>The WPN's 3D-avatar skin. Same shared player pool as ACR/Black Chip/Ya. Distinctive lounge-style client. Smaller welcome match ($1,000) but same rakeback structure and same MTT schedule access. {cta("true-poker","Claim at True Poker →")}</p>
            <div class="badge-row">
              <span class="tag">Min dep $25 crypto</span><span class="tag">Rake clearance</span><span class="tag">60-day expiry</span><span class="tag">Elite Benefits 20-65%</span>
            </div>
          </div>

          <div class="bo-tier-card">
            <h3>5. BetOnline Poker — 100% Match up to $1,000 + weekly reloads <span class="tag">Best cross-vertical account</span></h3>
            <p>The Chico Poker Network flagship. Smaller player pool than WPN but anonymous tables (better for recreational players) and cross-vertical account access — one login for sports, casino, and poker. Weekly poker reload bonuses continue past the welcome window. {cta("betonline-poker","Claim at BetOnline Poker →")}</p>
            <div class="badge-row">
              <span class="tag">Min dep $20 crypto</span><span class="tag">Rake clearance</span><span class="tag">60-day expiry</span><span class="tag">Rebate 15-35%</span>
            </div>
          </div>

          <div class="bo-tier-card">
            <h3>6. TigerGaming Poker — 100% Match up to $1,000 + poker rebates</h3>
            <p>Chico Poker Network sister to BetOnline. Same shared player pool. Distinct promotional cadence with an aggressive weekly rebate program aimed at volume grinders. {cta("tigergaming-poker","Claim at TigerGaming Poker →")}</p>
            <div class="badge-row">
              <span class="tag">Min dep $20 crypto</span><span class="tag">Rake clearance</span><span class="tag">60-day expiry</span><span class="tag">Rebate 15-35%</span>
            </div>
          </div>

          <div class="bo-tier-card">
            <h3>7. Sportsbetting.ag Poker — 100% Match up to $1,000 + weekly reloads</h3>
            <p>Chico Poker Network sister to BetOnline. Same shared player pool. Distinct account keeps promo calendars separate — volume players hold both. {cta("sportsbetting-poker","Claim at Sportsbetting.ag Poker →")}</p>
            <div class="badge-row">
              <span class="tag">Min dep $20 crypto</span><span class="tag">Rake clearance</span><span class="tag">60-day expiry</span><span class="tag">Rebate 15-35%</span>
            </div>
          </div>'''


NEW_ONGOING_PROMOS = '''          <p>Worth knowing about each promoted operator's ongoing promo profile:</p>
          <ul>
            <li><strong>BetOnline:</strong> weekly crypto reload boosters, live-betting insurance on marquee games, VIP-host access at $10K/month volume, MGM-style Rewards program with cross-vertical earn.</li>
            <li><strong>BetUS:</strong> historical NFL specialist — the strongest weekly reload cadence during football season. Custom high-roller terms negotiable via account host.</li>
            <li><strong>Sportsbetting.ag:</strong> distinct reload calendar from BetOnline (same platform, different cadence). Serious bettors hold both accounts.</li>
            <li><strong>BetOnline / Sportsbetting.ag Casino:</strong> weekly reload matches on both platforms; free-spin drops on featured slots; live-dealer VIP tables at scale.</li>
            <li><strong>BetUS Casino:</strong> aggressive crypto reload structure; rakeback-style cashback on losses for VIPs.</li>
            <li><strong>ACR / Black Chip / Ya / True (WPN):</strong> Elite Benefits rakeback is the primary ongoing lift. Frequent Venom satellite paths at $22-$88. OSS Cub3d series.</li>
            <li><strong>BetOnline / TigerGaming / Sportsbetting Poker (Chico):</strong> weekly poker-specific reloads, freeroll tournament tickets, and the Chico rebate program.</li>
          </ul>'''


NEW_BY_STATE = '''          <p>Because our promoted brands are US-facing offshore books, they accept players from most US states — including states where regulated mobile sports betting is not yet legal (Texas, California, Georgia, Minnesota, etc.). Understand the offshore-vs-regulated trade-off before depositing:</p>

          <ul>
            <li><strong>States with mature regulated markets (NJ, PA, MI, NY, IL, MA, OH, etc.):</strong> regulated operators (DraftKings, FanDuel, BetMGM, Caesars) carry state consumer protections and simpler tax reporting. Our promoted offshore books are still accessible but the trade-off tilts more toward the regulated market.</li>
            <li><strong>States with no legal mobile sports betting (TX, CA, GA, MN, AL, HI, ID, OK, SC, UT, WI, etc.):</strong> our promoted offshore brands are the only mobile-accessible path. Understand jurisdictional context — see the Trust page.</li>
            <li><strong>States with launches in 2026:</strong> Mississippi (fall). See our <a href="../us/">state-by-state guide</a> for launch timing and operator rosters.</li>
            <li><strong>Tribal-exclusive states (FL, ME, CT):</strong> regulated market is tribal-restricted; offshore books are outside that framework.</li>
          </ul>'''


NEW_FAQ = f'''          <div class="faq-item">
            <h3>What is the best online sports betting welcome bonus in 2026?</h3>
            <p>The best welcome bonus depends on your deposit size and preferred cashier method. For a large crypto deposit, BetUS's 125% match up to $3,125 has the highest headline value. For an all-around 50% match with strong crypto reloads and cross-vertical account access, BetOnline is the top pick. For a second-book account with a distinct reload calendar, Sportsbetting.ag is the natural pair with BetOnline.</p>
          </div>

          <div class="faq-item">
            <h3>How does a US-facing offshore welcome bonus differ from a regulated-state welcome bonus?</h3>
            <p>Offshore welcome bonuses are typically deposit-match structures (50-150% up to a cap) with 10× (deposit + bonus) rollover. Regulated welcome bonuses in states like NJ or PA are typically first-bet-protection or wager-and-get structures with lower nominal value but 1× rollover on bonus bets. Realized-value math differs materially between the two structures.</p>
          </div>

          <div class="faq-item">
            <h3>What is the rollover requirement on a deposit-match casino bonus?</h3>
            <p>Rollover (also called playthrough or wagering requirement) is the number of times you must wager the bonus amount before withdrawing winnings. Casino welcome offers at our promoted brands run 30× on slots and 60× on table games. A 30× rollover on a $1,000 bonus means you must place $30,000 in qualifying slot wagers. Slots contribute 100%; table games typically 10-20%.</p>
          </div>

          <div class="faq-item">
            <h3>Are betting bonuses really free money?</h3>
            <p>Welcome bonuses can have positive expected value when used carefully, but they are not free money. The fine print — minimum odds, qualifying wagers, expiry windows, and rollover requirements — typically reduces the nominal bonus value by 25-50%. A $1,000 sportsbook bonus at 10× rollover has an approximate realized value of $650. A $2,000 casino match at 30× rollover has an approximate realized value of $600-$800 depending on game selection.</p>
          </div>

          <div class="faq-item">
            <h3>Can I claim a sportsbook welcome and a casino welcome at the same brand?</h3>
            <p>Yes at our promoted brands. BetOnline and Sportsbetting.ag both let you claim the sportsbook welcome AND the casino welcome as separate offers, provided each is claimed at first deposit into that product line. The two rollover structures track separately.</p>
          </div>

          <div class="faq-item">
            <h3>Do I have to use a bonus code to claim a welcome offer?</h3>
            <p>Clicking through from our tracked affiliate link auto-applies the standard welcome offer at each operator. A few operators occasionally run enhanced offers with specific promo codes — the T&amp;C section of each ranked entry above will note if one applies at the time of writing.</p>
          </div>

          <div class="faq-item">
            <h3>What happens if my qualifying bet pushes or voids?</h3>
            <p>Most offshore welcome offers treat a push or void as if the bet did not occur — the qualifying wager doesn't count toward triggering the bonus, and you'll need to place another. For deposit-match structures, this is less of a concern (the bonus is triggered by the deposit, not the qualifying bet).</p>
          </div>

          <div class="faq-item">
            <h3>How quickly does the welcome bonus credit?</h3>
            <p>For offshore deposit-match welcome offers, the bonus credits within minutes of the qualifying deposit clearing. Crypto deposits credit fastest (usually within 30 minutes). Card deposits can take longer if the operator requires additional KYC.</p>
          </div>

          <div class="faq-item">
            <h3>Can I withdraw my bonus directly?</h3>
            <p>No. Bonus credits cannot be withdrawn directly. You must clear the rollover requirement first — 10× on sportsbook welcomes, 30-60× on casino welcomes. Only after rollover clears does the bonus convert to withdrawable cash.</p>
          </div>

          <div class="faq-item">
            <h3>Are sportsbook bonuses or casino bonuses better value?</h3>
            <p>Sportsbook welcomes are more efficient. 10× rollover on a $1,000 sportsbook match retains ~65% of nominal value ($650). 30× rollover on a $1,000 casino slot match retains ~25-30% of nominal value ($250-300). For volume casino players who would have played the slots anyway, the casino bonus is essentially a play-subsidy — the retention math is less relevant. For occasional players, the sportsbook side is materially better.</p>
          </div>

          <div class="faq-item">
            <h3>What about poker welcome bonuses?</h3>
            <p>Poker welcomes at our seven promoted rooms are rake-clearance based — the bonus releases incrementally as you generate rake through cash-game and MTT play. Realized value depends entirely on your play volume. A player generating $500/month in rake will clear a $1,000 bonus in roughly 10 months; a full-time grinder might clear the same bonus in 3-4 weeks.</p>
          </div>

          <div class="faq-item">
            <h3>Are operators that offer larger bonuses better?</h3>
            <p>No. Headline bonus size is largely a marketing function. Our rankings weight realized value (after rollover), cashier speed, pricing (hold rates), and operator quality. Welcome offers are 15% of our 100-point framework. See our <a href="../how-we-rate/">rating methodology</a> for the full weight breakdown.</p>
          </div>'''


NEW_RELATED_READING = '''          <h2>Related reading</h2>
          <ul>
            <li><a href="../reviews/betonline-sportsbook/">BetOnline Sportsbook — full review</a></li>
            <li><a href="../reviews/sportsbetting-sportsbook/">Sportsbetting.ag Sportsbook — full review</a></li>
            <li><a href="../reviews/betus-sportsbook/">BetUS Sportsbook — full review</a></li>
            <li><a href="../reviews/betonline-casino/">BetOnline Casino — full review</a></li>
            <li><a href="../reviews/betus-casino/">BetUS Casino — full review</a></li>
            <li><a href="../reviews/acr-poker/">ACR Poker — full review</a></li>
            <li><a href="../reviews/black-chip-poker/">Black Chip Poker — full review</a></li>
            <li><a href="../reviews/">All operator reviews</a></li>
            <li><a href="../guides/">All strategy guides</a></li>
            <li><a href="../data/withdrawal-speed-tracker/">Withdrawal speed tracker</a></li>
            <li><a href="../data/hold-rate-tracker/">Hold rate tracker</a></li>
            <li><a href="../how-we-rate/">How we rate operators</a></li>
            <li><a href="../trust/">Trust &amp; Transparency</a></li>
            <li><a href="../legal/disclosure.html">Affiliate disclosure</a></li>
            <li><a href="../legal/responsible-gambling.html">Responsible gambling resources</a></li>
          </ul>'''


# BONUSES filter grid JS array
NEW_BONUSES_JS = f'''    const BONUSES = [
      {{ op:'BetOnline Sportsbook', cat:'sports', type:'match', amount:'$1,000', amountVal:1000, headline:'50% Welcome Bonus up to $1,000 + crypto reloads', desc:'50% match on first sportsbook deposit up to $1,000. 10x rollover on deposit + bonus. Crypto deposits unlock weekly reload boosters.', minDep:20, rollover:'10×', expiry:'30 days', states:'Most US states (offshore)', code:'—', link:'{TRACKERS["betonline-sportsbook"]}' }},
      {{ op:'Sportsbetting.ag Sportsbook', cat:'sports', type:'match', amount:'$1,000', amountVal:1000, headline:'50% Welcome Bonus up to $1,000 + crypto reloads', desc:'Same structure as BetOnline (sister brand on Chico Network). Distinct account and distinct reload calendar.', minDep:20, rollover:'10×', expiry:'30 days', states:'Most US states (offshore)', code:'—', link:'{TRACKERS["sportsbetting-sportsbook"]}' }},
      {{ op:'BetUS Sportsbook', cat:'sports', type:'match', amount:'$3,125', amountVal:3125, headline:'125% Crypto Welcome Bonus up to $3,125 (or 100% up to $2,500 card)', desc:'Largest headline welcome match in the offshore segment. Crypto unlocks 125%; card gets 100% up to $2,500.', minDep:50, rollover:'10×', expiry:'30 days', states:'Most US states (offshore)', code:'—', link:'{TRACKERS["betus-sportsbook"]}' }},
      {{ op:'BetOnline Casino', cat:'casino', type:'match', amount:'$3,000', amountVal:3000, headline:'100% Match up to $3,000 (across first 3 deposits)', desc:'Split across your first three deposits, tops out at $3,000. 30x rollover on slots; 60x on table games. Slot library 500+ titles.', minDep:25, rollover:'30×', expiry:'30 days', states:'Most US states (offshore)', code:'—', link:'{TRACKERS["betonline-casino"]}' }},
      {{ op:'Sportsbetting.ag Casino', cat:'casino', type:'match', amount:'$3,000', amountVal:3000, headline:'100% Match up to $3,000 (across first 3 deposits)', desc:'Sister to BetOnline Casino. Mirror slot library and live-dealer floor; distinct promotional cadence.', minDep:25, rollover:'30×', expiry:'30 days', states:'Most US states (offshore)', code:'—', link:'{TRACKERS["sportsbetting-casino"]}' }},
      {{ op:'BetUS Casino', cat:'casino', type:'match', amount:'$3,000', amountVal:3000, headline:'150% Crypto Match up to $3,000', desc:'Highest headline match percentage in the offshore casino segment. Crypto deposits only. 30x rollover on slots.', minDep:50, rollover:'30×', expiry:'30 days', states:'Most US states (offshore)', code:'—', link:'{TRACKERS["betus-casino"]}' }},
      {{ op:'ACR Poker', cat:'poker', type:'match', amount:'$2,000', amountVal:2000, headline:'100% Match up to $2,000 + Venom qualifiers', desc:'Flagship Winning Poker Network brand. Home of Venom $10M+ GTD marquee. Rake-clearance based release. Elite Benefits 20-65% rakeback.', minDep:25, rollover:'Rake clearance', expiry:'60 days', states:'Most US states (offshore)', code:'—', link:'{TRACKERS["acr-poker"]}' }},
      {{ op:'Black Chip Poker', cat:'poker', type:'match', amount:'$2,000', amountVal:2000, headline:'100% Match up to $2,000 + 27% Elite Benefits rakeback', desc:'Same WPN player pool as ACR. Softer cash-game population. Same rakeback structure.', minDep:25, rollover:'Rake clearance', expiry:'60 days', states:'Most US states (offshore)', code:'—', link:'{TRACKERS["black-chip-poker"]}' }},
      {{ op:'Ya Poker', cat:'poker', type:'match', amount:'$2,000', amountVal:2000, headline:'100% Match up to $2,000 + rakeback rewards', desc:'Newer WPN skin with crypto-first cashier and streamlined lobby. Same WPN pool.', minDep:20, rollover:'Rake clearance', expiry:'60 days', states:'Most US states (offshore)', code:'—', link:'{TRACKERS["ya-poker"]}' }},
      {{ op:'True Poker', cat:'poker', type:'match', amount:'$1,000', amountVal:1000, headline:'100% Match up to $1,000 + WPN promos', desc:'WPN 3D-avatar skin. Same shared player pool. Distinctive lounge-style client.', minDep:25, rollover:'Rake clearance', expiry:'60 days', states:'Most US states (offshore)', code:'—', link:'{TRACKERS["true-poker"]}' }},
      {{ op:'BetOnline Poker', cat:'poker', type:'match', amount:'$1,000', amountVal:1000, headline:'100% Match up to $1,000 + weekly reloads', desc:'Chico Poker Network flagship. Anonymous tables. Cross-vertical account (sports + casino + poker).', minDep:20, rollover:'Rake clearance', expiry:'60 days', states:'Most US states (offshore)', code:'—', link:'{TRACKERS["betonline-poker"]}' }},
      {{ op:'TigerGaming Poker', cat:'poker', type:'match', amount:'$1,000', amountVal:1000, headline:'100% Match up to $1,000 + poker rebates', desc:'Chico Network sister to BetOnline. Aggressive weekly rebate program for volume grinders.', minDep:20, rollover:'Rake clearance', expiry:'60 days', states:'Most US states (offshore)', code:'—', link:'{TRACKERS["tigergaming-poker"]}' }},
      {{ op:'Sportsbetting.ag Poker', cat:'poker', type:'match', amount:'$1,000', amountVal:1000, headline:'100% Match up to $1,000 + weekly reloads', desc:'Chico Network sister to BetOnline. Distinct account keeps promo calendars separate.', minDep:20, rollover:'Rake clearance', expiry:'60 days', states:'Most US states (offshore)', code:'—', link:'{TRACKERS["sportsbetting-poker"]}' }}
    ];'''


# ---------------------------------------------------------------------------
# Apply the rewrite
# ---------------------------------------------------------------------------
def main() -> None:
    text = BONUSES.read_text()

    # 1) Hero tags — the "15 active offers ..." block
    text = re.sub(
        r'      <div style="margin-top:18px;display:flex;gap:8px;flex-wrap:wrap">\s*'
        r'<span class="tag primary">15 active offers</span>.*?</div>',
        NEW_HERO_TAGS,
        text,
        count=1,
        flags=re.S,
    )

    # 2) Replace the entire "At a glance: top 6" section with our 3 new tables
    text = re.sub(
        r'  <section class="section" style="padding-top:32px">\s*<div class="container">\s*'
        r'<h2>At a glance: top 6 sportsbook welcome offers</h2>.*?</section>',
        NEW_TOP_TABLES,
        text,
        count=1,
        flags=re.S,
    )

    # 3) "Browse all 15" heading + intro
    text = re.sub(
        r'    <div class="container">\s*<h2>Browse all 15 active welcome offers</h2>\s*'
        r'<p class="muted">Filter by category, bonus type, and minimum deposit\..*?</p>',
        BROWSE_HEADING,
        text,
        count=1,
        flags=re.S,
    )

    # 4) Best sportsbook welcome offers — replace the whole ranked section
    text = re.sub(
        r'          <h2 id="best-sportsbook">Best sportsbook welcome offers.*?</h2>\s*'
        r'.*?(?=          <h2 id="best-casino">)',
        NEW_BEST_SPORTSBOOK + "\n\n",
        text,
        count=1,
        flags=re.S,
    )

    # 5) Best casino
    text = re.sub(
        r'          <h2 id="best-casino">.*?(?=          <h2 id="best-poker">)',
        NEW_BEST_CASINO + "\n\n",
        text,
        count=1,
        flags=re.S,
    )

    # 6) Best poker
    text = re.sub(
        r'          <h2 id="best-poker">.*?(?=          <h2 id="how-to-claim">)',
        NEW_BEST_POKER + "\n\n",
        text,
        count=1,
        flags=re.S,
    )

    # 7) Ongoing promotions bullet list
    text = re.sub(
        r"          <p>Worth knowing about each operator's ongoing promo profile:</p>\s*<ul>.*?</ul>",
        NEW_ONGOING_PROMOS,
        text,
        count=1,
        flags=re.S,
    )

    # 8) "By state" section — replace the bullet-list content but keep the h2
    text = re.sub(
        r'          <p>State availability is one of the most-overlooked dimensions.*?</p>\s*<ul>.*?</ul>\s*<p>For state-specific operator availability[^<]+<a href="\.\./us/">complete US states guide</a>\.</p>',
        NEW_BY_STATE,
        text,
        count=1,
        flags=re.S,
    )

    # 9) FAQ — replace all the faq-item divs between "<div class=\"faq-item\">" (first) and the "<hr>"
    text = re.sub(
        r'          <div class="faq-item">\s*<h3>What is the best online sports betting welcome bonus.*?</div>\s*(?=          <hr>)',
        NEW_FAQ + "\n\n",
        text,
        count=1,
        flags=re.S,
    )

    # 10) Related reading list
    text = re.sub(
        r'          <h2>Related reading</h2>\s*<ul>.*?</ul>',
        NEW_RELATED_READING,
        text,
        count=1,
        flags=re.S,
    )

    # 11) BONUSES JS array
    text = re.sub(
        r'    const BONUSES = \[.*?\];',
        NEW_BONUSES_JS,
        text,
        count=1,
        flags=re.S,
    )

    # 12) Update the "Showing X of N bonuses" default text — leave the JS math alone

    # 13) Update page-hero eyebrow date
    text = re.sub(
        r'<span class="eyebrow">Welcome offers · Updated April 2026</span>',
        '<span class="eyebrow">Welcome offers · Updated July 2026</span>',
        text,
    )

    # 14) Update byline date
    text = re.sub(
        r'Last updated April 30, 2026',
        'Last updated July 22, 2026',
        text,
    )

    BONUSES.write_text(text)
    print(f"Rewrote {BONUSES.relative_to(ROOT)}")

    subprocess.run(["git", "-C", str(ROOT), "add", "-A"], check=True)


if __name__ == "__main__":
    main()
