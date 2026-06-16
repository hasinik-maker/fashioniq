import pandas as pd
import numpy as np
from datetime import datetime
import random

random.seed(42)
np.random.seed(42)

# ── Expanded illegal keywords (drugs, weapons, trafficking etc) ───────────────
ILLEGAL_KEYWORDS = [
    # Counterfeits
    "counterfeit","fake brand","replica","duplicate","pirated","forged","knockoff",
    # Drugs
    "drugs","cocaine","heroin","weed","marijuana","mdma","ecstasy","meth","amphetamine",
    "narcotics","cannabis","opium","fentanyl","ketamine","lsd","psychedelics",
    # Weapons
    "guns","weapons","firearms","pistol","rifle","bullets","ammunition","explosives",
    "bomb","knife sale","illegal weapons","arms dealer",
    # Human trafficking / exploitation
    "child labour","trafficking","smuggled","underage","exploit","slavery","forced labour",
    # Financial crime
    "black market","money laundering","tax evasion","fraud","stolen","embezzlement",
    # Other illegal trade
    "prohibited","banned fabric","illegal dye","smuggling","contraband",
]

def check_illegal_content(text):
    t = text.lower()
    return [kw for kw in ILLEGAL_KEYWORDS if kw in t]

# ── Messages ──────────────────────────────────────────────────────────────────
MESSAGES = [
    {"id":1,"from":"buyer1","to":"seller1","text":"Hi! Interested in 100 units of Baggy Cargo Pants. Best price?","time":"10:32 AM","date":"Today"},
    {"id":2,"from":"seller1","to":"buyer1","text":"Hello Priya! For 100 units we offer ₹295/unit. Delivery in 7 days.","time":"10:45 AM","date":"Today"},
    {"id":3,"from":"buyer1","to":"seller1","text":"Can you do ₹280 if I order 150 units?","time":"11:02 AM","date":"Today"},
    {"id":4,"from":"buyer2","to":"seller2","text":"Do you have Printed Maxi Dresses in plus sizes?","time":"9:15 AM","date":"Today"},
    {"id":5,"from":"seller2","to":"buyer2","text":"Yes! S to 3XL available. MOQ 40 units. Want samples?","time":"9:30 AM","date":"Today"},
]

# ── Trends ────────────────────────────────────────────────────────────────────
TRENDS = [
    {"id":1,"name":"Baggy Cargo Pants","category":"Bottoms","heat":94,
     "direction":"🔥 Viral","city":"Hyderabad","change":"+38%",
     "tags":["streetwear","Gen-Z","unisex"],"urgency":"HIGH",
     "description":"Cargo silhouettes dominating local markets. Demand spike driven by college campuses.",
     "peak_weeks":6,
     "insight":"Your core audience is Gen-Z women aged 18-24. This fits perfectly — stock in S, M, L sizes. Pair with oversized tees for bundle selling."},
    {"id":2,"name":"Pastel Oversized Shirts","category":"Tops","heat":87,
     "direction":"📈 Rising","city":"Hyderabad","change":"+24%",
     "tags":["summer","unisex","casual"],"urgency":"HIGH",
     "description":"Pastel colour-blocked shirts trending on Instagram and Pinterest.",
     "peak_weeks":8,
     "insight":"Best seller for college-going women. Stock pastels — lavender, mint, peach. Avoid whites as they go out of trend faster."},
    {"id":3,"name":"Co-ord Sets (Ethnic Fusion)","category":"Sets","heat":82,
     "direction":"📈 Rising","city":"Hyderabad","change":"+19%",
     "tags":["fusion","women","festive"],"urgency":"MEDIUM",
     "description":"Ethnic-modern fusion co-ords gaining traction pre-festive season.",
     "peak_weeks":10,
     "insight":"Perfect for festive gifting and Diwali prep. Target 25-35 women. Price between ₹1,500-2,000 for best conversion."},
    {"id":4,"name":"Relaxed Linen Trousers","category":"Bottoms","heat":71,
     "direction":"📈 Rising","city":"Hyderabad","change":"+15%",
     "tags":["summer","workwear","sustainable"],"urgency":"MEDIUM",
     "description":"Comfort-work hybrid. Linen in muted earth tones performing well.",
     "peak_weeks":12,
     "insight":"Appeals to working women aged 25-35. Sand, beige, and olive sell best. Great for office-to-casual buyers."},
    {"id":5,"name":"Logo Crop Hoodies","category":"Tops","heat":65,
     "direction":"→ Stable","city":"Hyderabad","change":"+4%",
     "tags":["streetwear","women","casual"],"urgency":"LOW",
     "description":"Holding steady. Good consistent seller but no surge expected.",
     "peak_weeks":16,
     "insight":"Reliable staple but don't overstock. Keep 15-20 units max. Good for bundling with joggers or cargo pants."},
    {"id":6,"name":"Formal Straight-Cut Blazers","category":"Outerwear","heat":38,
     "direction":"📉 Declining","city":"Hyderabad","change":"-12%",
     "tags":["formal","office","classic"],"urgency":"DEAD_STOCK",
     "description":"Post-pandemic formal wear slowing down. Reduce inventory now.",
     "peak_weeks":0,
     "insight":"Your audience does not buy formal wear. This is a category mismatch for your niche. Clear immediately and never restock."},
    {"id":7,"name":"Crochet Mini Skirts","category":"Bottoms","heat":79,
     "direction":"📈 Rising","city":"Hyderabad","change":"+21%",
     "tags":["boho","summer","women"],"urgency":"HIGH",
     "description":"Crochet textures exploding on social. Boutique favourite this season.",
     "peak_weeks":7,
     "insight":"Your highest-margin item. Boho-loving women aged 18-28 are your buyers. Stock white, beige, brown. Peaking in 3 weeks — order NOW."},
    {"id":8,"name":"Printed Maxi Dresses","category":"Dresses","heat":85,
     "direction":"🔥 Viral","city":"Hyderabad","change":"+29%",
     "tags":["summer","women","festive"],"urgency":"HIGH",
     "description":"Bold prints in floral and abstract trending hard this season.",
     "peak_weeks":5,
     "insight":"Perfect for your audience — women 18-34 love this for weddings and outings. Floral prints outperform abstract. Order immediately."},
]

# ── Inventory ─────────────────────────────────────────────────────────────────
INVENTORY = [
    {"sku":"BGC-001","name":"Baggy Cargo Pants - Olive","qty":12,"reorder_point":30,
     "cost":480,"selling_price":1299,"days_of_stock":4,"velocity":"Fast",
     "status":"REORDER NOW","category":"Bottoms","trend_alignment":94,
     "insight":"🔴 CRITICAL: Only 4 days of stock left on your best-selling item. Order 90 units from Rajesh Textiles (₹320/unit = ₹28,800). At current sell rate you need stock by TOMORROW."},
    {"sku":"PST-002","name":"Pastel Oversized Shirt - Blue","qty":8,"reorder_point":25,
     "cost":320,"selling_price":899,"days_of_stock":5,"velocity":"Fast",
     "status":"REORDER NOW","category":"Tops","trend_alignment":87,
     "insight":"🔴 5 days left. Order 75 units from Femina (₹210/unit = ₹15,750). Peaking in 8 weeks — you need to be fully stocked in the next 7 days."},
    {"sku":"CRD-003","name":"Ethnic Co-ord Set - Beige","qty":34,"reorder_point":20,
     "cost":650,"selling_price":1799,"days_of_stock":18,"velocity":"Medium",
     "status":"HEALTHY","category":"Sets","trend_alignment":82,
     "insight":"✅ Stock is healthy. Monitor weekly. Festive season is coming — consider ordering 20 more units in 2 weeks to prepare for the demand surge."},
    {"sku":"LIN-004","name":"Linen Trouser - Sand","qty":45,"reorder_point":15,
     "cost":390,"selling_price":999,"days_of_stock":28,"velocity":"Medium",
     "status":"HEALTHY","category":"Bottoms","trend_alignment":71,
     "insight":"✅ Comfortable stock level. No action needed this week. Re-evaluate in 3 weeks."},
    {"sku":"BLZ-005","name":"Straight Blazer - Black","qty":78,"reorder_point":10,
     "cost":890,"selling_price":1499,"days_of_stock":90,"velocity":"Slow",
     "status":"DEAD STOCK","category":"Outerwear","trend_alignment":38,
     "insight":"⚫ DEAD STOCK: ₹70,620 locked in capital. Your audience doesn't buy formal wear. Run a 30% flash sale this week (₹1,049). Post on Instagram Stories. Never restock this category."},
    {"sku":"CRC-006","name":"Crochet Mini Skirt - White","qty":6,"reorder_point":20,
     "cost":280,"selling_price":799,"days_of_stock":3,"velocity":"Fast",
     "status":"REORDER NOW","category":"Bottoms","trend_alignment":79,
     "insight":"🔴 URGENT: Only 3 days left on your highest-margin item (71% margin). Order 75 units from Femina (₹195/unit = ₹14,625). This peaks in 3 weeks — missing this window costs you big."},
    {"sku":"MAX-007","name":"Printed Maxi Dress - Floral","qty":9,"reorder_point":25,
     "cost":540,"selling_price":1499,"days_of_stock":4,"velocity":"Fast",
     "status":"REORDER NOW","category":"Dresses","trend_alignment":85,
     "insight":"🔴 VIRAL item with only 4 days of stock. Order 120 units from Femina (₹380/unit = ₹45,600). This is peaking in 5 weeks. Every day out of stock = lost revenue."},
    {"sku":"HDD-008","name":"Logo Crop Hoodie - Pink","qty":52,"reorder_point":15,
     "cost":420,"selling_price":999,"days_of_stock":35,"velocity":"Slow",
     "status":"OVERSTOCK","category":"Tops","trend_alignment":65,
     "insight":"🟡 OVERSTOCK: 35 days of stock at current rate. Pause all reorders. Consider bundling with cargo pants at ₹1,799 combo to move stock faster. No urgency but monitor."},
]

# ── Pricing ───────────────────────────────────────────────────────────────────
PRICING = [
    {"product":"Baggy Cargo Pants","your_price":1299,"market_avg":1350,"low":999,"high":1799,
     "suggested":1399,"margin_pct":63,"opportunity":"Price UP ↑",
     "tip":"Your Gen-Z audience will pay ₹1,399 for trending cargo pants. You are ₹51 below market average. Raise price TODAY — you will earn ₹51 extra per unit, which adds up to ₹4,590 on your next 90-unit order."},
    {"product":"Pastel Oversized Shirt","your_price":899,"market_avg":849,"low":699,"high":1199,
     "suggested":949,"margin_pct":64,"opportunity":"Price UP ↑",
     "tip":"You can push to ₹949. At 75 units that is ₹3,750 extra margin for zero additional cost. Your audience sees this as affordable fashion — ₹949 still feels accessible."},
    {"product":"Ethnic Co-ord Set","your_price":1799,"market_avg":1899,"low":1499,"high":2499,
     "suggested":1899,"margin_pct":64,"opportunity":"Price UP ↑",
     "tip":"Your festive-season buyers (women 25-35) expect to pay ₹1,899-2,200 for co-ords. Raise to ₹1,899 — you are currently undervaluing this product by ₹100."},
    {"product":"Crochet Mini Skirt","your_price":799,"market_avg":899,"low":599,"high":1299,
     "suggested":899,"margin_pct":71,"opportunity":"Price UP ↑",
     "tip":"This is your highest-margin item AND you are ₹100 below market. Raise to ₹899 immediately. Boutique buyers pay premium for crochet. ₹899 feels like a steal vs competitors at ₹999+."},
    {"product":"Printed Maxi Dress","your_price":1499,"market_avg":1599,"low":1199,"high":2199,
     "suggested":1649,"margin_pct":66,"opportunity":"Price UP ↑",
     "tip":"Viral item = price power. Raise to ₹1,649. When demand is this high customers don't compare prices — they just buy. You are leaving ₹150/unit on the table right now."},
    {"product":"Logo Crop Hoodie","your_price":999,"market_avg":849,"low":699,"high":1099,
     "suggested":849,"margin_pct":50,"opportunity":"Reduce Price ↓",
     "tip":"You are priced ₹150 above market average on a slow-moving item. Drop to ₹849 to move overstock faster. Bundle with cargo pants at ₹1,799 combo to protect margins."},
    {"product":"Straight Blazer","your_price":1499,"market_avg":1099,"low":799,"high":1399,
     "suggested":999,"margin_pct":12,"opportunity":"Clearance Sale 🔥",
     "tip":"CLEARANCE ONLY. Price at ₹999 (33% off). Your audience does not buy formal wear — this is a category mismatch. Move fast, recover capital, never restock."},
]

# ── Wholesalers ───────────────────────────────────────────────────────────────
WHOLESALERS = [
    {"id":1,"name":"Rajesh Textiles & Exports","city":"Surat","username":"seller1",
     "rating":4.8,"verified":True,"years":14,"speciality":"Bottoms & Denims",
     "tags":["BESTSELLER","FAST DISPATCH"],"min_order_value":15000,
     "about":"India's top cargo and linen wholesale supplier. 14 years in business. Ships pan-India in 7 days. Trusted by 500+ boutiques.",
     "products":[
         {"name":"Baggy Cargo Pants (Bulk)","moq":50,"price_per_unit":320,"fabric":"Cotton-Poly Blend","sizes":"S-XXL","colors":8,"lead_days":7,"category":"Bottoms","description":"Best-selling cargo pants in olive, beige, grey, black. 4-pocket utility design. Machine washable."},
         {"name":"Relaxed Linen Trousers","moq":30,"price_per_unit":280,"fabric":"Pure Linen","sizes":"S-XL","colors":5,"lead_days":10,"category":"Bottoms","description":"Premium pure linen in sand, white, olive, navy, black. Breathable and trending for summer workwear."},
     ]},
    {"id":2,"name":"Femina Fashion House","city":"Jaipur","username":"seller2",
     "rating":4.6,"verified":True,"years":9,"speciality":"Women's Fashion",
     "tags":["TOP RATED","WOMEN'S SPECIALIST"],"min_order_value":12000,
     "about":"Jaipur's leading women's fashion wholesaler. Specialises in trending dresses, skirts, and tops. Low MOQ friendly for small boutiques.",
     "products":[
         {"name":"Pastel Oversized Shirts (Bulk)","moq":60,"price_per_unit":210,"fabric":"Rayon Georgette","sizes":"S-XXL","colors":12,"lead_days":5,"category":"Tops","description":"12 pastel shades including lavender, mint, peach, sky blue. Lightweight Rayon Georgette. Instagram-ready finish."},
         {"name":"Printed Maxi Dresses","moq":40,"price_per_unit":380,"fabric":"Chiffon","sizes":"S-3XL","colors":10,"lead_days":8,"category":"Dresses","description":"Bold floral and abstract prints on chiffon. Available up to 3XL. Bestseller in boutiques across Hyderabad and Bangalore."},
         {"name":"Crochet Mini Skirts","moq":25,"price_per_unit":195,"fabric":"Crochet Cotton","sizes":"XS-L","colors":6,"lead_days":12,"category":"Bottoms","description":"Handcrafted crochet in white, beige, brown, rust, black, green. Boho-chic finish. Pairs with crop tops and oversized shirts."},
     ]},
]

# ── Fashion News ──────────────────────────────────────────────────────────────
FASHION_NEWS = [
    {"headline":"Cargo pants dominate Indian streets in 2025","source":"Vogue India","date":"Jun 2025","impact":"HIGH","summary":"Baggy cargo silhouettes are the #1 trend across Tier 1 and Tier 2 Indian cities. Boutiques in Hyderabad and Bangalore report selling out within days of restocking."},
    {"headline":"Festive season demand expected 34% higher than 2024","source":"Textile Today","date":"Jun 2025","impact":"HIGH","summary":"Industry analysts predict record festive buying this year. Ethnic fusion co-ords and printed dresses will lead the surge. Start stocking now — lead times are 8-14 days."},
    {"headline":"Crochet and handmade textures peak this summer","source":"Elle India","date":"Jun 2025","impact":"HIGH","summary":"Pinterest searches for crochet fashion are up 180% year-on-year. Small boutiques report selling out crochet skirts and tops within 48 hours of receiving stock."},
    {"headline":"Formal wear category shrinks 18% post-pandemic","source":"Business of Fashion","date":"May 2025","impact":"LOW","summary":"Office wear demand continues declining sharply. Experts advise small retailers to reduce or eliminate formal inventory and redirect capital to casual and festive categories."},
    {"headline":"Linen fabric prices drop 12% — great time to negotiate","source":"Fibre2Fashion","date":"Jun 2025","impact":"MEDIUM","summary":"Raw linen costs falling due to oversupply from Bangladesh exporters. This is an ideal window to negotiate better rates with linen wholesalers and lock in 3-month supply."},
    {"headline":"Gen-Z in Hyderabad driving streetwear demand surge","source":"Hyderabad Mirror","date":"Jun 2025","impact":"HIGH","summary":"The 18-25 age group in Hyderabad is spending 40% more on fashion compared to last year. Unisex streetwear, cargo pants, and oversized silhouettes are leading the charge."},
]

# ── Audience ──────────────────────────────────────────────────────────────────
AUDIENCE_DATA = {
    "age_groups":{"13-17":12,"18-24":38,"25-34":28,"35-44":14,"45+":8},
    "cities":{"Hyderabad":45,"Bangalore":22,"Mumbai":18,"Delhi":10,"Others":5},
    "gender":{"Women":68,"Men":24,"Non-binary":8},
    "top_categories":{"Bottoms":34,"Tops":28,"Dresses":20,"Sets":12,"Outerwear":6},
}

# ── Data functions ────────────────────────────────────────────────────────────
def get_revenue_data():
    return {
        "months":["Jan","Feb","Mar","Apr","May","Jun"],
        "revenue":[142000,168000,195000,221000,198000,245000],
        "target": [150000,170000,190000,210000,220000,240000],
        "units_sold":[112,138,162,185,160,198],
    }

def get_forecast_data():
    weeks = [f"W{i}" for i in range(1,13)]
    return {
        "weeks":weeks,
        "Baggy Cargo Pants":       [18,24,32,41,55,68,74,70,62,50,38,28],
        "Pastel Oversized Shirts": [22,28,35,44,52,61,65,60,52,42,30,22],
        "Crochet Mini Skirts":     [12,18,28,40,54,62,68,65,55,42,28,18],
        "Printed Maxi Dresses":    [30,38,48,58,65,70,68,60,48,35,24,18],
        "Formal Blazers":          [20,18,15,12,10, 8, 7, 6, 6, 5, 5, 4],
    }

def get_sales_history():
    dates = pd.date_range(end=datetime.today(), periods=30, freq='D')
    return pd.DataFrame({
        "date":dates,
        "revenue":np.random.randint(8000,28000,30),
        "units_sold":np.random.randint(15,65,30),
    })

CATEGORIES = ["All","Tops","Bottoms","Dresses","Sets","Outerwear"]

# ── AI responses ──────────────────────────────────────────────────────────────
def get_ai_response(question, role="buyer"):
    q = question.lower()
    if any(kw in q for kw in ILLEGAL_KEYWORDS):
        return "🚫 I cannot help with that request. It appears to involve illegal activity — including drugs, weapons, counterfeit goods, or financial crime. Trendora has a zero-tolerance policy. This conversation has been flagged."
    if "reorder" in q or "buy" in q or "purchase" in q or "order" in q:
        return "🔴 Top reorder priorities RIGHT NOW:\n\n1. Baggy Cargo Pants — only 4 days left. Order 90 units from Rajesh Textiles at ₹320/unit (₹28,800 total). Call today.\n2. Crochet Mini Skirts — 3 days left. Order 75 units from Femina at ₹195/unit (₹14,625). This peaks in 3 weeks.\n3. Printed Maxi Dresses — viral item, 4 days left. Order 120 units from Femina at ₹380/unit (₹45,600).\n\nTotal outlay needed: ₹89,025. Expected return at current sell prices: ₹1,82,700."
    if "trend" in q or "trending" in q or "popular" in q or "hot" in q:
        return "📈 Top 3 trends in Hyderabad RIGHT NOW:\n\n1. Baggy Cargo Pants — 94/100 heat score. +38% demand surge. Viral on Instagram and in colleges.\n2. Printed Maxi Dresses — 85/100. +29%. Going viral on Pinterest. Floral prints especially.\n3. Crochet Mini Skirts — 79/100. +21%. Boutique sellout item. Peaks in 3 weeks.\n\nYour niche is casual-to-festive women's fashion for Gen-Z and millennials in Hyderabad. These 3 trends match your audience perfectly."
    if "dead" in q or "clear" in q or "overstock" in q or "blazer" in q:
        return "📦 Dead stock action plan:\n\n78 Straight Blazers — ₹69,420 locked in capital at cost price.\n\nStep 1: Price at ₹999 (33% off from ₹1,499)\nStep 2: Post Instagram Story — '72-hour flash sale, limited stock'\nStep 3: At 10 units/week you clear in 8 weeks and recover ₹77,922\n\nNever restock blazers. Your audience is Gen-Z and millennial women — formal wear is a category mismatch for your niche."
    if "price" in q or "margin" in q or "profit" in q:
        return "💹 5 immediate pricing changes that add ₹18,000/month:\n\n1. Cargo Pants: ₹1,299 → ₹1,399 (+₹100/unit)\n2. Crochet Skirts: ₹799 → ₹899 (+₹100/unit)\n3. Maxi Dresses: ₹1,499 → ₹1,649 (+₹150/unit)\n4. Pastel Shirts: ₹899 → ₹949 (+₹50/unit)\n5. Co-ord Sets: ₹1,799 → ₹1,899 (+₹100/unit)\n\nAll still below market average. Your audience will not notice the increase — they buy based on trend, not price comparison."
    if "wholesaler" in q or "supplier" in q or "vendor" in q or "contact" in q:
        return "🏭 Best suppliers for your business:\n\n1. Rajesh Textiles, Surat — 4.8★, 14 years, MOQ 50 units at ₹320. Best for cargo pants and linen. Delivers in 7 days.\n\n2. Femina Fashion House, Jaipur — 4.6★, 9 years, MOQ as low as 25 units. Best for dresses, skirts, and pastel shirts. 5-12 day delivery.\n\nBoth are verified on Trendora. Message them directly from the Marketplace tab."
    if "audience" in q or "customer" in q or "who" in q or "target" in q or "niche" in q:
        return "👥 Your target audience profile:\n\nCore buyer: Women aged 18-34 (66% of your sales)\nLocation: Hyderabad (45%), Bangalore (22%)\nStyle niche: Casual-to-festive, boho, streetwear, Gen-Z fashion\nTop categories: Bottoms (34%), Tops (28%), Dresses (20%)\nPrice sweet spot: ₹799-1,799\nShopping triggers: Instagram trends, Pinterest, college fashion\n\nAlways stock items that are visual, trendy, and casual. Avoid formal and corporate wear — it does not match your audience."
    if "festive" in q or "season" in q or "diwali" in q or "upcoming" in q:
        return "🎉 Festive season strategy:\n\nDemand projected 34% higher than 2024.\n\nStock NOW (lead times are 8-14 days):\n1. Ethnic Co-ord Sets — 40 units minimum\n2. Printed Maxi Dresses — 120 units\n3. Pastel Oversized Shirts — 75 units\n\nLinen fabric prices are down 12% — negotiate bulk rates with Rajesh Textiles before prices recover. Target your 25-35 audience for festive — they spend more per order."
    if "revenue" in q or "sales" in q or "performance" in q or "money" in q:
        return "📊 Revenue snapshot:\n\nJune 2025: ₹2,45,000 — 24% above target ✅\nBest month ever. 198 units sold.\n\nTop performer: Printed Maxi Dresses at ₹1,499\nFastest growing: 18-24 age group in Hyderabad\n\nProjection: If you restock all 4 urgent items AND raise prices as suggested, July revenue forecast is ₹3,10,000-3,40,000 — a 27-39% increase."
    if "hello" in q or "hi" in q or "hey" in q or "help" in q:
        return "👋 Hello! I am Trendora AI, your fashion business advisor.\n\nI have full access to your inventory, trend data, pricing intelligence, supplier contacts, and revenue numbers. Ask me anything — I will give you sharp, specific advice based on YOUR business data.\n\nSome things I can help with:\n• What to reorder urgently\n• Which trends to stock\n• How to price for maximum profit\n• Which supplier to use\n• How to clear dead stock\n• Who your customers are"
    if "illegal" in q or "legal" in q or "rule" in q or "allowed" in q:
        return "⚖️ Trendora's safety rules:\n\n🚫 Strictly prohibited: counterfeit goods, drugs, weapons, child labour, smuggled items, tax fraud, trafficking, stolen goods\n\n✅ All sellers are verified before listing\n✅ All messages and listings are scanned automatically\n✅ Flagged accounts are suspended immediately\n✅ Serious violations are reported to authorities\n\nIf you see anything suspicious, use the Report button on any listing or message."
    return "🤖 Based on your current data:\n\n1. URGENT — Restock Cargo Pants, Maxi Dresses, and Crochet Skirts (all under 5 days of stock)\n2. PROFIT — Raise prices on 5 products to market average (adds ₹18K/month)\n3. CLEAR — Flash sale your 78 blazers to recover ₹78K in capital\n4. PREPARE — Start ordering festive stock NOW (Diwali demand up 34%)\n\nWhat would you like to go deeper on?"
