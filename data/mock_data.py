import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

random.seed(42)
np.random.seed(42)

# ── Users ─────────────────────────────────────────────────────────────────────
USERS = {
    "buyer1": {"password": "buy123", "role": "buyer", "name": "Priya Sharma", "city": "Hyderabad", "business": "Priya Boutique"},
    "buyer2": {"password": "buy456", "role": "buyer", "name": "Ananya Reddy", "city": "Bangalore", "business": "Ananya Fashion House"},
    "seller1": {"password": "sell123", "role": "seller", "name": "Rajesh Gupta", "city": "Surat", "business": "Rajesh Textiles & Exports"},
    "seller2": {"password": "sell456", "role": "seller", "name": "Meena Patel", "city": "Jaipur", "business": "Femina Fashion House"},
    "admin": {"password": "admin123", "role": "admin", "name": "Admin", "city": "Mumbai", "business": "Trendora HQ"},
}

# ── Illegal keywords detector ─────────────────────────────────────────────────
ILLEGAL_KEYWORDS = [
    "counterfeit", "fake brand", "replica", "duplicate", "pirated",
    "child labour", "smuggled", "black market", "money laundering",
    "tax evasion", "underage", "exploit", "stolen", "forged",
    "prohibited", "banned fabric", "illegal dye", "fraud"
]

def check_illegal_content(text):
    text_lower = text.lower()
    flagged = [kw for kw in ILLEGAL_KEYWORDS if kw in text_lower]
    return flagged

# ── Messages ──────────────────────────────────────────────────────────────────
MESSAGES = [
    {"id": 1, "from": "buyer1", "to": "seller1", "text": "Hi! I am interested in 100 units of Baggy Cargo Pants. What is your best price?", "time": "10:32 AM", "date": "Today"},
    {"id": 2, "from": "seller1", "to": "buyer1", "text": "Hello Priya! For 100 units we can offer ₹295/unit. Delivery in 7 days.", "time": "10:45 AM", "date": "Today"},
    {"id": 3, "from": "buyer1", "to": "seller1", "text": "Can you do ₹280 if I order 150 units?", "time": "11:02 AM", "date": "Today"},
    {"id": 4, "from": "buyer2", "to": "seller2", "text": "Do you have Printed Maxi Dresses in plus sizes?", "time": "9:15 AM", "date": "Today"},
    {"id": 5, "from": "seller2", "to": "buyer2", "text": "Yes! We have S to 3XL. MOQ is 40 units. Shall I send samples?", "time": "9:30 AM", "date": "Today"},
]

# ── Trends ────────────────────────────────────────────────────────────────────
TRENDS = [
    {"id": 1, "name": "Baggy Cargo Pants", "category": "Bottoms", "heat": 94,
     "direction": "🔥 Viral", "city": "Hyderabad", "change": "+38%",
     "tags": ["streetwear", "Gen-Z", "unisex"], "urgency": "HIGH",
     "description": "Cargo silhouettes dominating local markets. Demand spike driven by college campuses.",
     "peak_weeks": 6, "image": "https://i.pinimg.com/736x/8e/2b/4e/8e2b4e1234567890abcdef.jpg"},

    {"id": 2, "name": "Pastel Oversized Shirts", "category": "Tops", "heat": 87,
     "direction": "📈 Rising", "city": "Hyderabad", "change": "+24%",
     "tags": ["summer", "unisex", "casual"], "urgency": "HIGH",
     "description": "Pastel colour-blocked shirts trending across Instagram reels and Pinterest boards.",
     "peak_weeks": 8, "image": ""},

    {"id": 3, "name": "Co-ord Sets (Ethnic Fusion)", "category": "Sets", "heat": 82,
     "direction": "📈 Rising", "city": "Hyderabad", "change": "+19%",
     "tags": ["fusion", "women", "festive"], "urgency": "MEDIUM",
     "description": "Ethnic-modern fusion co-ords gaining traction pre-festive season.",
     "peak_weeks": 10, "image": ""},

    {"id": 4, "name": "Relaxed Linen Trousers", "category": "Bottoms", "heat": 71,
     "direction": "📈 Rising", "city": "Hyderabad", "change": "+15%",
     "tags": ["summer", "workwear", "sustainable"], "urgency": "MEDIUM",
     "description": "Comfort-work hybrid trend. Linen in muted earth tones performing well.",
     "peak_weeks": 12, "image": ""},

    {"id": 5, "name": "Logo Crop Hoodies", "category": "Tops", "heat": 65,
     "direction": "→ Stable", "city": "Hyderabad", "change": "+4%",
     "tags": ["streetwear", "women", "casual"], "urgency": "LOW",
     "description": "Holding steady. Good consistent seller but no surge expected.",
     "peak_weeks": 16, "image": ""},

    {"id": 6, "name": "Formal Straight-Cut Blazers", "category": "Outerwear", "heat": 38,
     "direction": "📉 Declining", "city": "Hyderabad", "change": "-12%",
     "tags": ["formal", "office", "classic"], "urgency": "DEAD_STOCK",
     "description": "Post-pandemic formal wear slowing down. Reduce inventory now.",
     "peak_weeks": 0, "image": ""},

    {"id": 7, "name": "Crochet Mini Skirts", "category": "Bottoms", "heat": 79,
     "direction": "📈 Rising", "city": "Hyderabad", "change": "+21%",
     "tags": ["boho", "summer", "women"], "urgency": "HIGH",
     "description": "Crochet textures exploding on social. Boutique favourite this season.",
     "peak_weeks": 7, "image": ""},

    {"id": 8, "name": "Printed Maxi Dresses", "category": "Dresses", "heat": 85,
     "direction": "🔥 Viral", "city": "Hyderabad", "change": "+29%",
     "tags": ["summer", "women", "festive"], "urgency": "HIGH",
     "description": "Bold prints in floral and abstract trending hard this season.",
     "peak_weeks": 5, "image": ""},
]

# ── Inventory ─────────────────────────────────────────────────────────────────
INVENTORY = [
    {"sku": "BGC-001", "name": "Baggy Cargo Pants - Olive", "qty": 12, "reorder_point": 30,
     "cost": 480, "selling_price": 1299, "days_of_stock": 4, "velocity": "Fast",
     "status": "REORDER NOW", "category": "Bottoms", "trend_alignment": 94},
    {"sku": "PST-002", "name": "Pastel Oversized Shirt - Blue", "qty": 8, "reorder_point": 25,
     "cost": 320, "selling_price": 899, "days_of_stock": 5, "velocity": "Fast",
     "status": "REORDER NOW", "category": "Tops", "trend_alignment": 87},
    {"sku": "CRD-003", "name": "Ethnic Co-ord Set - Beige", "qty": 34, "reorder_point": 20,
     "cost": 650, "selling_price": 1799, "days_of_stock": 18, "velocity": "Medium",
     "status": "HEALTHY", "category": "Sets", "trend_alignment": 82},
    {"sku": "LIN-004", "name": "Linen Trouser - Sand", "qty": 45, "reorder_point": 15,
     "cost": 390, "selling_price": 999, "days_of_stock": 28, "velocity": "Medium",
     "status": "HEALTHY", "category": "Bottoms", "trend_alignment": 71},
    {"sku": "BLZ-005", "name": "Straight Blazer - Black", "qty": 78, "reorder_point": 10,
     "cost": 890, "selling_price": 1499, "days_of_stock": 90, "velocity": "Slow",
     "status": "DEAD STOCK", "category": "Outerwear", "trend_alignment": 38},
    {"sku": "CRC-006", "name": "Crochet Mini Skirt - White", "qty": 6, "reorder_point": 20,
     "cost": 280, "selling_price": 799, "days_of_stock": 3, "velocity": "Fast",
     "status": "REORDER NOW", "category": "Bottoms", "trend_alignment": 79},
    {"sku": "MAX-007", "name": "Printed Maxi Dress - Floral", "qty": 9, "reorder_point": 25,
     "cost": 540, "selling_price": 1499, "days_of_stock": 4, "velocity": "Fast",
     "status": "REORDER NOW", "category": "Dresses", "trend_alignment": 85},
    {"sku": "HDD-008", "name": "Logo Crop Hoodie - Pink", "qty": 52, "reorder_point": 15,
     "cost": 420, "selling_price": 999, "days_of_stock": 35, "velocity": "Slow",
     "status": "OVERSTOCK", "category": "Tops", "trend_alignment": 65},
]

# ── Pricing ───────────────────────────────────────────────────────────────────
PRICING = [
    {"product": "Baggy Cargo Pants", "your_price": 1299, "market_avg": 1350,
     "low": 999, "high": 1799, "suggested": 1399, "margin_pct": 63, "opportunity": "Price UP ↑"},
    {"product": "Pastel Oversized Shirt", "your_price": 899, "market_avg": 849,
     "low": 699, "high": 1199, "suggested": 949, "margin_pct": 64, "opportunity": "Price UP ↑"},
    {"product": "Ethnic Co-ord Set", "your_price": 1799, "market_avg": 1899,
     "low": 1499, "high": 2499, "suggested": 1899, "margin_pct": 64, "opportunity": "Price UP ↑"},
    {"product": "Crochet Mini Skirt", "your_price": 799, "market_avg": 899,
     "low": 599, "high": 1299, "suggested": 899, "margin_pct": 71, "opportunity": "Price UP ↑"},
    {"product": "Printed Maxi Dress", "your_price": 1499, "market_avg": 1599,
     "low": 1199, "high": 2199, "suggested": 1649, "margin_pct": 66, "opportunity": "Price UP ↑"},
    {"product": "Logo Crop Hoodie", "your_price": 999, "market_avg": 849,
     "low": 699, "high": 1099, "suggested": 849, "margin_pct": 50, "opportunity": "Reduce Price ↓"},
    {"product": "Straight Blazer", "your_price": 1499, "market_avg": 1099,
     "low": 799, "high": 1399, "suggested": 999, "margin_pct": 12, "opportunity": "Clearance Sale 🔥"},
]

# ── Wholesalers ───────────────────────────────────────────────────────────────
WHOLESALERS = [
    {"id": 1, "name": "Rajesh Textiles & Exports", "city": "Surat", "username": "seller1",
     "rating": 4.8, "verified": True, "years": 14, "speciality": "Bottoms & Denims",
     "tags": ["BESTSELLER", "FAST DISPATCH"], "min_order_value": 15000,
     "products": [
         {"name": "Baggy Cargo Pants (Bulk)", "moq": 50, "price_per_unit": 320,
          "fabric": "Cotton-Poly Blend", "sizes": "S-XXL", "colors": 8, "lead_days": 7, "category": "Bottoms"},
         {"name": "Relaxed Linen Trousers", "moq": 30, "price_per_unit": 280,
          "fabric": "Pure Linen", "sizes": "S-XL", "colors": 5, "lead_days": 10, "category": "Bottoms"},
     ]},
    {"id": 2, "name": "Femina Fashion House", "city": "Jaipur", "username": "seller2",
     "rating": 4.6, "verified": True, "years": 9, "speciality": "Women's Fashion",
     "tags": ["TOP RATED", "WOMEN'S SPECIALIST"], "min_order_value": 12000,
     "products": [
         {"name": "Pastel Oversized Shirts (Bulk)", "moq": 60, "price_per_unit": 210,
          "fabric": "Rayon Georgette", "sizes": "S-XXL", "colors": 12, "lead_days": 5, "category": "Tops"},
         {"name": "Printed Maxi Dresses", "moq": 40, "price_per_unit": 380,
          "fabric": "Chiffon", "sizes": "S-3XL", "colors": 10, "lead_days": 8, "category": "Dresses"},
         {"name": "Crochet Mini Skirts", "moq": 25, "price_per_unit": 195,
          "fabric": "Crochet Cotton", "sizes": "XS-L", "colors": 6, "lead_days": 12, "category": "Bottoms"},
     ]},
]

# ── Current Fashion News ──────────────────────────────────────────────────────
FASHION_NEWS = [
    {"headline": "Cargo pants dominate Indian streets in 2025", "source": "Vogue India", "date": "Jun 2025",
     "impact": "HIGH", "summary": "Baggy cargo silhouettes are the #1 trend in Tier 1 and Tier 2 Indian cities. Stock up immediately."},
    {"headline": "Festive season demand expected 34% higher than 2024", "source": "Textile Today", "date": "Jun 2025",
     "impact": "HIGH", "summary": "Analysts predict record festive buying. Ethnic fusion and co-ord sets will lead the surge."},
    {"headline": "Crochet and handmade textures peak this summer", "source": "Elle India", "date": "Jun 2025",
     "impact": "HIGH", "summary": "Pinterest searches for crochet fashion up 180% YoY. Boutiques report selling out within days."},
    {"headline": "Formal wear category shrinks 18% post-pandemic", "source": "Business of Fashion", "date": "May 2025",
     "impact": "LOW", "summary": "Office wear demand continues declining. Experts advise reducing formal inventory significantly."},
    {"headline": "Linen fabric prices drop 12% — great time to stock", "source": "Fibre2Fashion", "date": "Jun 2025",
     "impact": "MEDIUM", "summary": "Raw linen costs falling due to oversupply from Bangladesh. Good window to negotiate wholesale prices."},
    {"headline": "Gen-Z in Hyderabad driving streetwear demand", "source": "Hyderabad Mirror", "date": "Jun 2025",
     "impact": "HIGH", "summary": "18-25 age group in Hyderabad spending 40% more on fashion vs last year. Unisex streetwear leading."},
]

# ── Audience Data ─────────────────────────────────────────────────────────────
AUDIENCE_DATA = {
    "age_groups": {"13-17": 12, "18-24": 38, "25-34": 28, "35-44": 14, "45+": 8},
    "cities": {"Hyderabad": 45, "Bangalore": 22, "Mumbai": 18, "Delhi": 10, "Others": 5},
    "gender": {"Women": 68, "Men": 24, "Non-binary": 8},
    "top_categories": {"Bottoms": 34, "Tops": 28, "Dresses": 20, "Sets": 12, "Outerwear": 6},
}

# ── Revenue Data ──────────────────────────────────────────────────────────────
def get_revenue_data():
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    return {
        "months": months,
        "revenue": [142000, 168000, 195000, 221000, 198000, 245000],
        "target": [150000, 170000, 190000, 210000, 220000, 240000],
        "units_sold": [112, 138, 162, 185, 160, 198],
    }

def get_forecast_data():
    weeks = [f"W{i}" for i in range(1, 13)]
    return {
        "weeks": weeks,
        "Baggy Cargo Pants": [18, 24, 32, 41, 55, 68, 74, 70, 62, 50, 38, 28],
        "Pastel Oversized Shirts": [22, 28, 35, 44, 52, 61, 65, 60, 52, 42, 30, 22],
        "Crochet Mini Skirts": [12, 18, 28, 40, 54, 62, 68, 65, 55, 42, 28, 18],
        "Printed Maxi Dresses": [30, 38, 48, 58, 65, 70, 68, 60, 48, 35, 24, 18],
        "Formal Blazers": [20, 18, 15, 12, 10, 8, 7, 6, 6, 5, 5, 4],
    }

def get_sales_history():
    dates = pd.date_range(end=datetime.today(), periods=30, freq='D')
    return pd.DataFrame({
        "date": dates,
        "revenue": np.random.randint(8000, 28000, 30),
        "units_sold": np.random.randint(15, 65, 30),
    })

CATEGORIES = ["All", "Tops", "Bottoms", "Dresses", "Sets", "Outerwear"]

# ── AI Chatbot Responses ──────────────────────────────────────────────────────
def get_ai_response(question, role="buyer"):
    q = question.lower()

    if any(kw in q for kw in ILLEGAL_KEYWORDS):
        return "🚫 I cannot help with that. This activity may violate legal or ethical standards. Trendora has a strict policy against counterfeit, illegal, or unethical trade."

    if "reorder" in q or "buy" in q or "purchase" in q:
        return "🔴 Top reorder priorities right now: Baggy Cargo Pants (4 days of stock left — order 90 units from Rajesh Textiles at ₹320/unit), Crochet Mini Skirts (3 days left — order 75 units from Femina Fashion House), and Printed Maxi Dresses (viral right now — order 120 units immediately). These three items have peak demand in the next 5-7 weeks."

    if "trend" in q or "trending" in q or "popular" in q:
        return "📈 Current top trends in Hyderabad: Baggy Cargo Pants (94/100 heat score, +38% demand), Printed Maxi Dresses (85/100, viral on Instagram and Pinterest), and Crochet Mini Skirts (79/100, peaking in 3 weeks). Gen-Z shoppers aged 18-24 are driving most of this demand. Stock these immediately."

    if "dead" in q or "clear" in q or "overstock" in q or "blazer" in q:
        return "📦 Dead stock action plan: Your 78 Straight Blazers are blocking ₹69,420 in capital. Run a 30% flash sale this week (₹1,049 from ₹1,499). Use Instagram Stories with a 72-hour countdown. At 10 units per week you will recover ₹81,822 in 8 weeks. Never reorder this SKU."

    if "price" in q or "margin" in q or "profit" in q:
        return "💹 Pricing opportunities: Raise Baggy Cargo Pants to ₹1,399 (market supports it), Crochet Skirts to ₹899, Maxi Dresses to ₹1,649. All are currently priced below market average. This adds approximately ₹18,000 per month in margin with zero extra cost. Your current average gross margin is 64% on trending items — protect it."

    if "wholesaler" in q or "supplier" in q or "vendor" in q:
        return "🏭 Best suppliers right now: Rajesh Textiles in Surat (4.8 stars, 14 years, MOQ 50 units at ₹320) for cargo pants and linen. Femina Fashion House in Jaipur (4.6 stars, MOQ 40 units) for dresses and skirts. Both are verified on Trendora. Message them directly from the Marketplace page."

    if "audience" in q or "customer" in q or "who" in q:
        return "👥 Your target audience in Hyderabad: 68% women, primary age group 18-24 (38% of buyers). They shop mostly for Bottoms (34%) and Tops (28%). They are active on Instagram and Pinterest. Price sensitivity is medium — they will pay premium for trending items but expect value. Focus on Gen-Z streetwear and women's ethnic fusion."

    if "festive" in q or "season" in q or "diwali" in q or "upcoming" in q:
        return "🎉 Upcoming season alert: Festive demand is projected 34% higher than 2024. Start stocking Ethnic Co-ord Sets and Printed Maxi Dresses NOW — lead times are 8-14 days so you need to order by next week to be ready. Linen fabric prices are also down 12% right now — good time to negotiate bulk rates."

    if "revenue" in q or "sales" in q or "performance" in q:
        return "📊 Your revenue this month (June 2025) is ₹2,45,000 — up 24% vs target of ₹2,40,000. Best performing SKU is Printed Maxi Dresses at ₹1,499. Units sold this month: 198. Your fastest growth is coming from the 18-24 age group in Hyderabad. Recommendation: double your Maxi Dress and Cargo Pants inventory before July."

    if "hello" in q or "hi" in q or "hey" in q:
        return "👋 Hello! I am Trendora AI, your fashion business advisor. I can help you with trends, stock management, pricing strategy, supplier recommendations, audience analysis, and revenue forecasting. What would you like to know today?"

    if "illegal" in q or "legal" in q or "allowed" in q:
        return "⚖️ Trendora strictly prohibits counterfeit goods, child labour, smuggled fabrics, and tax fraud. All sellers are verified. Any listing flagged for illegal activity is removed immediately and reported. If you suspect a violation, use the Report button on any product or message."

    return "🤖 Great question! Based on current Hyderabad market data: your top priority should be restocking fast-moving items (Cargo Pants, Maxi Dresses, Crochet Skirts) before they stock out, raising prices on 5 products to market average (adds ₹18K/month margin), and clearing your Blazer dead stock with a flash sale. Want me to go deeper on any of these areas?"
