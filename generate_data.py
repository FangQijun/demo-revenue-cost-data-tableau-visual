import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()

n_brands = 20
n_months = 15  # More months, for a visible trend
brand_types = ['Sports Club', 'Event Company']
revenue_streams = ['Ticket Sales', 'Sponsorship', 'Merchandise', 'Concessions']
cost_streams = ['Salaries', 'Venue Rent', 'Marketing', 'Logistics']

brands = [
    {
        'Brand Name': fake.company(),
        'Brand Type': np.random.choice(brand_types),
        'rev_trend': np.random.choice(['linear', 'exp', 'log', 'parabolic']),
        'cost_trend': np.random.choice(['linear', 'exp', 'log', 'parabolic']),
    }
    for _ in range(n_brands)
]

def brand_trend(trend, base, month, n_months):
    """Return a value for the given trend type and month index"""
    x = month + 1
    if trend == 'linear':
        return base + 0.08 * base * x
    elif trend == 'exp':
        return base * (1.04 ** x)
    elif trend == 'log':
        return base + 0.5 * base * np.log1p(x)
    elif trend == 'parabolic':
        return base + 0.02 * base * ((x - n_months // 2) ** 2)
    else:
        return base

rows = []

for brand in brands:
    # Assign a base value for realism
    revenue_base = np.random.randint(80000, 140000)
    cost_base = np.random.randint(40000, 100000)
    for m, month in enumerate(pd.date_range(start='2024-01-01', periods=n_months, freq='MS')):
        # Create clear pattern in total revenue/costs per month
        total_revenue = int(brand_trend(brand['rev_trend'], revenue_base, m, n_months))
        total_cost = int(brand_trend(brand['cost_trend'], cost_base, m, n_months))
        
        # Now subdivide into streams (weights are random for each brand/month)
        rev_weights = np.random.dirichlet(np.ones(len(revenue_streams)), 1)[0]
        cost_weights = np.random.dirichlet(np.ones(len(cost_streams)), 1)[0]
        
        rev_dict = {f"Revenue: {r}": int(total_revenue * w + np.random.normal(0, total_revenue*0.02)) for r, w in zip(revenue_streams, rev_weights)}
        cost_dict = {f"Cost: {c}": int(total_cost * w + np.random.normal(0, total_cost*0.02)) for c, w in zip(cost_streams, cost_weights)}
        
        net_margin = total_revenue - total_cost
        
        row = {
            "Brand Name": brand["Brand Name"],
            "Brand Type": brand["Brand Type"],
            "Month": month.strftime("%Y-%m"),
            **rev_dict,
            **cost_dict,
            "Total Revenue": total_revenue,
            "Total Cost": total_cost,
            "Net Margin": net_margin,
            "Revenue Trend": brand["rev_trend"].capitalize(),
            "Cost Trend": brand["cost_trend"].capitalize()
        }
        rows.append(row)

df = pd.DataFrame(rows)
df.to_excel("committed_cash_view_with_trends.xlsx", index=False)
print("Sample data ready: 'committed_cash_view_with_trends.xlsx'")