import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

random.seed(42)
np.random.seed(42)

ILLEGAL_KEYWORDS = [
    "counterfeit", "fake brand", "replica", "duplicate", "pirated",
    "child labour", "smuggled", "black market", "money laundering",
    "tax evasion", "underage", "exploit", "stolen", "forged",
    "prohibited", "banned fabric", "illegal dye", "fraud"
]

def check_illegal_content(text):
    text_lower = text.lower()
    return [kw for kw in ILLEGAL_KEYWORDS if kw in text_lower]

MESSAGES = [
    {"id": 1, "from": "buyer1", "to": "seller1", "text": "Hi! I am interested in 100 units of Baggy Cargo Pants. What is your best price?", "time": "10:32 AM", "date": "Today"},
    {"id": 2, "from": "seller1", "to": "buyer1", "text": "Hello Priya! For 100 units we can offer ₹295/unit. Delivery in 7 days.", "time": "10:45 AM", "date": "Today"},
    {"id": 3, "from": "buyer1", "to": "seller1", "text": "Can you do ₹280 if I order 150 units?", "time": "11:02 AM", "date": "Today"},
    {"id": 4, "from": "buyer2", "to": "seller2", "text": "Do you have Printed Maxi Dresses in plus sizes?", "time": "9:15 AM", "date": "Today"},
    {"id": 5, "from": "seller2", "to": "buyer2", "text": "Yes! We have S to 3XL. MOQ is 40 units. Shall I send samples?", "time": "9:30 AM", "date": "Today"},
]

TRENDS = [
    {"id": 1, "name": "Baggy Cargo Pants", "category": "Bottoms", "heat": 94,
     "direction": "🔥 Viral", "city": "Hyderabad", "change": "+38%",
     "tags": ["streetwear", "Gen-Z", "unisex"], "urgency": "HIGH",
     "description": "Cargo silhouettes dominating local markets. Demand spike driven by college campuses.",
     "peak_weeks": 6, "image": ""},
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

PRICING = [
    {"product": "Baggy Cargo Pants", "your_price": 1299, "market_avg": 1350, "low": 999, "high": 1799, "suggested": 1399, "margin_pct": 63, "opportunity": "Price UP ↑"},
    {"product": "Pastel Oversized Shirt", "your_price": 899, "market_avg": 849, "low": 699, "high": 1199, "suggested": 949, "margin_pct": 64, "opportunity": "Price UP ↑"},
    {"product": "Ethnic Co-ord Set", "your_price": 1799, "market_avg": 1899, "low": 1499, "high": 2499, "suggested": 1899, "margin_pct": 64, "opportunity": "Price UP ↑"},
    {"product": "Crochet Mini Skirt", "your_price": 799, "market_avg": 899, "low": 599, "high": 1299, "suggested": 899, "margin_pct": 71, "opportunity": "Price UP ↑"},
    {"product": "Printed Maxi Dress", "your_price": 1499, "market_avg": 1599, "low": 1199, "high": 2199, "suggested": 1649, "margin_pct": 66, "opportunity": "Price UP ↑"},
    {"product": "Logo Crop Hoodie", "your_price": 999, "market_avg": 849, "low": 699, "high": 1099, "suggested": 849, "margin_pct": 50, "opportunity": "Reduce Price ↓"},
    {"product": "Straight Blazer", "your_price": 1499, "market_avg": 1099, "low": 799, "high": 1399, "suggested": 999, "margin_pct": 12, "opportunity": "Clearance Sale 🔥"},
]

WHOLESALERS = [
    {"id": 1, "name": "Rajesh Textiles & Exports", "city": "Surat", "username": "seller1",
     "rating": 4.8, "verified": True, "years": 14, "speciality": "Bottoms & Denims",
     "tags": ["BESTSELLER", "FAST DISPATCH"], "min_order_value": 15000,
     "products": [
         {"name": "Baggy Cargo Pants (Bulk)", "moq": 50, "price_per_unit": 320, "fabric": "Cotton-Poly Blend", "sizes": "S-XXL", "colors": 8, "lead_days": 7, "category": "Bottoms"},
         {"name": "Relaxed Linen Trousers", "moq": 30, "price_per_unit": 280, "fabric": "Pure Linen", "sizes": "S-XL", "colors": 5, "lead_days": 10, "category": "Bottoms"},
     ]},
    {"id": 2, "name": "Femina Fashion House", "city": "Jaipur", "username": "seller2",
     "rating": 4.6, "verified": True, "years": 9, "speciality": "Women's Fashion",
     "tags": ["TOP RATED", "WOMEN'S SPECIALIST"], "min_order_value": 12000,
     "products": [
         {"name": "Pastel Oversized Shirts (Bulk)", "moq": 60, "price_per_unit": 210, "fabric": "Rayon Georgette", "sizes": "S-XXL", "colors": 12, "lead_days": 5, "category": "Tops"},
         {"name": "Printed Maxi Dresses", "moq": 40, "price_per_unit": 380, "fabric": "Chiffon", "sizes": "S-3XL", "colors": 10, "lead_days": 8, "category": "Dresses"},
         {"name": "Crochet Mini Skirts", "moq": 25, "price_per_unit": 195, "fabric": "Crochet Cotton", "sizes": "XS-L", "colors": 6, "lead_days": 12, "category": "Bottoms"},
     ]},
]

FASHION_NEWS = [
    {"headline": "Cargo pants dominate Indian streets in 2025", "source": "Vogue India", "date": "Jun 2025", "impact": "HIGH", "summary": "Baggy cargo silhouettes are the #1 trend in Tier 1 and Tier 2 Indian cities. Stock up immediately."},
    {"headline": "Festive season demand expected 34% higher than 2024", "source": "Textile Today", "date": "Jun 2025", "impact": "HIGH", "summary": "Analysts predict record festive buying. Ethnic fusion and co-ord sets will lead the surge."},
    {"headline": "Crochet and handmade textures peak this summer", "source": "Elle India", "date": "Jun 2025", "impact": "HIGH", "summary": "Pinterest searches for crochet fashion up 180% YoY. Boutiques report selling out within days."},
    {"headline": "Formal wear category shrinks 18% post-pandemic", "source": "Business of Fashion", "date": "May 2025", "impact": "LOW", "summary": "Office wear demand continues declining. Experts advise reducing formal inventory significantly."},
    {"headline": "Linen fabric prices drop 12% — great time to stock", "source": "Fibre2Fashion", "date": "Jun 2025", "impact": "MEDIUM", "summary": "Raw linen costs falling due to oversupply from Bangladesh. Good window to negotiate wholesale prices."},
    {"headline": "Gen-Z in Hyderabad driving streetwear demand", "source": "Hyderabad Mirror", "date": "Jun 2025", "impact": "HIGH", "summary": "18-25 age group in Hyderabad spending 40% more on fashion vs last year. Unisex streetwear leading."},
]

AUDIENCE_DATA = {
    "age_groups": {"13-17": 12, "18-24": 38, "25-34": 28, "35-44": 14, "45+": 8},
    "cities": {"Hyderabad": 45, "Bangalore": 22, "Mumbai": 18, "Delhi": 10, "Others": 5},
    "gender": {"Women": 68, "Men": 24, "Non-binary": 8},
    "top_categories": {"Bottoms": 34, "Tops": 28, "Dresses": 20, "Sets": 12, "Outerwear": 6},
}

def get_revenue_data():
    return {
        "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "revenue": [142000, 168000, 195000, 221000, 198000, 245000],
        "target":  [150000, 170000, 190000, 210000, 220000, 240000],
        "units_sold": [112, 138, 162, 185, 160, 198],
    }

def get_forecast_data():
    weeks = [f"W{i}" for i in range(1, 13)]
    return {
        "weeks": weeks,
        "Baggy Cargo Pants":        [18,24,32,41,55,68,74,70,62,50,38,28],
        "Pastel Oversized Shirts":  [22,28,35,44,52,61,65,60,52,42,30,22],
        "Crochet Mini Skirts":      [12,18,28,40,54,62,68,65,55,42,28,18],
        "Printed Maxi Dresses":     [30,38,48,58,65,70,68,60,48,35,24,18],
        "Formal Blazers":           [20,18,15,12,10, 8, 7, 6, 6, 5, 5, 4],
    }

def get_sales_history():
    dates = pd.date_range(end=datetime.today(), periods=30, freq='D')
    return pd.DataFrame({
        "date": dates,
        "revenue": np.random.randint(8000, 28000, 30),
        "units_sold": np.random.randint(15, 65, 30),
    })

CATEGORIES = ["All", "Tops", "Bottoms", "Dresses", "Sets", "Outerwear"]

def get_ai_response(question, role="buyer"):
    q = question.lower()
    if any(kw in q for kw in ILLEGAL_KEYWORDS):
        return "🚫 I cannot help with that. This may violate legal or ethical standards."
    if "reorder" in q or "buy" in q or "purchase" in q:
        return "🔴 Top reorder priorities: Baggy Cargo Pants (4 days left — order 90 units from Rajesh Textiles at ₹320/unit), Crochet Mini Skirts (3 days left — 75 units from Femina), Printed Maxi Dresses (viral — order 120 units immediately). Peak demand in 5–7 weeks."
    if "trend" in q or "trending" in q or "popular" in q:
        return "📈 Top trends in Hyderabad right now: Baggy Cargo Pants (94/100 heat, +38%), Printed Maxi Dresses (85/100, viral on Instagram and Pinterest), Crochet Mini Skirts (79/100, peaking in 3 weeks). Gen-Z aged 18-24 are driving most demand."
    if "dead" in q or "clear" in q or "overstock" in q or "blazer" in q:
        return "📦 Dead stock plan: 78 Straight Blazers are blocking ₹69,420 in capital. Run a 30% flash sale this week (₹1,049 from ₹1,499). Use Instagram Stories with a 72-hour countdown. At 10 units/week you recover ₹81,822 in 8 weeks."
    if "price" in q or "margin" in q or "profit" in q:
        return "💹 Pricing opportunities: Raise Baggy Cargo Pants to ₹1,399, Crochet Skirts to ₹899, Maxi Dresses to ₹1,649 — all below market average. Adds approximately ₹18,000/month in margin at zero extra cost."
    if "wholesaler" in q or "supplier" in q or "vendor" in q:
        return "🏭 Best suppliers: Rajesh Textiles in Surat (4.8★, 14 years, MOQ 50 at ₹320) for cargo and linen. Femina Fashion House in Jaipur (4.6★, MOQ 40) for dresses and skirts. Both verified on Trendora."
    if "audience" in q or "customer" in q:
        return "👥 Your audience: 68% women, primary age 18-24 (38% of buyers), Hyderabad-based. They shop Bottoms (34%) and Tops (28%). Active on Instagram and Pinterest. Focus on Gen-Z streetwear and ethnic fusion."
    if "festive" in q or "season" in q or "diwali" in q:
        return "🎉 Festive demand projected 34% higher than 2024. Stock Ethnic Co-ord Sets and Printed Maxi Dresses NOW — lead times are 8-14 days. Linen fabric prices also down 12% — good time to negotiate bulk rates."
    if "revenue" in q or "sales" in q or "performance" in q:
        return "📊 June 2025 revenue: ₹2,45,000 — up 24% vs target. Best SKU: Printed Maxi Dresses. Units sold: 198. Fastest growth from 18-24 age group in Hyderabad. Double your Maxi Dress and Cargo Pants inventory before July."
    if "hello" in q or "hi" in q or "hey" in q:
        return "👋 Hello! I'm Trendora AI, your fashion business advisor. I can help with trends, stock, pricing, suppliers, audience analysis, and revenue forecasting. What would you like to know?"
    return "🤖 Based on current data: your top priority is restocking fast-moving items (Cargo Pants, Maxi Dresses, Crochet Skirts), raising prices on 5 products to market average (adds ₹18K/month), and clearing your Blazer dead stock with a flash sale. Want me to go deeper on any area?"
