"""
Health Camp Data Generator
Generates realistic data for rural and urban health outreach camps.
"""
import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_health_camp_data(seed=42, num_camps=120):
    np.random.seed(seed)
    
    districts_info = [
        {"name": "Northern District", "lat": 18.5204, "lon": 73.8567, "base_pop": 45000},
        {"name": "Eastern Valley", "lat": 18.6298, "lon": 73.7997, "base_pop": 38000},
        {"name": "Southern Hills", "lat": 18.4485, "lon": 73.8587, "base_pop": 52000},
        {"name": "Western Coastal", "lat": 18.5089, "lon": 73.9260, "base_pop": 61000},
        {"name": "Central Metro", "lat": 18.5314, "lon": 73.8446, "base_pop": 75000},
        {"name": "Highland Tribal Zone", "lat": 18.7500, "lon": 73.6500, "base_pop": 29000}
    ]
    
    camp_types = ["General Screening", "Maternal & Child Health", "Eye & Dental Care", "Non-Communicable Diseases (NCD)", "Mobile Clinic Outreach", "Geriatric Special Care"]
    organizers = ["Ministry of Health", "Global Care Foundation", "Community Health Alliance", "Red Cross Services", "Apex Hospital Trust"]
    
    start_date = datetime.now() - timedelta(days=180)
    
    camps = []
    
    for i in range(1, num_camps + 1):
        dist = np.random.choice(districts_info)
        camp_type = np.random.choice(camp_types)
        organizer = np.random.choice(organizers)
        
        # Jitter coordinates slightly around district center
        lat = dist["lat"] + np.random.uniform(-0.08, 0.08)
        lon = dist["lon"] + np.random.uniform(-0.08, 0.08)
        
        camp_date = start_date + timedelta(days=int(np.random.uniform(0, 180)))
        
        # Target vs Actual Screened
        target_pop = int(np.random.normal(1500, 400))
        target_pop = max(400, target_pop)
        
        # Coverage efficiency factor
        efficiency = np.random.beta(a=6, b=2) if dist["name"] != "Highland Tribal Zone" else np.random.beta(a=3, b=3)
        screened_count = int(target_pop * efficiency)
        
        registered = int(screened_count * np.random.uniform(1.02, 1.15))
        
        # Demographics
        female_pct = np.random.uniform(0.48, 0.62)
        male_pct = 1.0 - female_pct
        female_count = int(screened_count * female_pct)
        male_count = screened_count - female_count
        
        under_18 = int(screened_count * np.random.uniform(0.15, 0.30))
        age_18_60 = int(screened_count * np.random.uniform(0.45, 0.60))
        above_60 = screened_count - under_18 - age_18_60
        
        # Clinical Screenings & Positives
        hypertension_cases = int(screened_count * np.random.uniform(0.12, 0.28))
        diabetes_cases = int(screened_count * np.random.uniform(0.08, 0.22))
        anemia_cases = int(screened_count * np.random.uniform(0.15, 0.35))
        vision_defect_cases = int(screened_count * np.random.uniform(0.10, 0.25))
        dental_issues = int(screened_count * np.random.uniform(0.12, 0.30))
        
        critical_referrals = int(screened_count * np.random.uniform(0.04, 0.11))
        
        # Staffing
        doctors = np.random.randint(2, 8)
        nurses = np.random.randint(4, 14)
        chws = np.random.randint(5, 20) # Community Health Workers
        
        # Budget & Cost
        budget_allocated = int(screened_count * np.random.uniform(18, 35) + np.random.uniform(2000, 5000))
        cost_per_patient = round(budget_allocated / max(1, screened_count), 2)
        
        # Coverage status determination
        coverage_pct = round((screened_count / target_pop) * 100, 1)
        if coverage_pct >= 90:
            status = "Target Exceeded"
        elif coverage_pct >= 75:
            status = "Optimal Coverage"
        elif coverage_pct >= 55:
            status = "Moderate Coverage"
        else:
            status = "Under-Served"
            
        camps.append({
            "camp_id": f"CMP-{1000 + i}",
            "camp_name": f"{dist['name']} {camp_type} #{i}",
            "district": dist["name"],
            "latitude": lat,
            "longitude": lon,
            "date": camp_date.strftime("%Y-%m-%d"),
            "camp_type": camp_type,
            "organizer": organizer,
            "target_population": target_pop,
            "registered_citizens": registered,
            "screened_patients": screened_count,
            "coverage_pct": coverage_pct,
            "coverage_status": status,
            "male_screened": male_count,
            "female_screened": female_count,
            "under_18": under_18,
            "age_18_60": age_18_60,
            "above_60": above_60,
            "hypertension_cases": hypertension_cases,
            "diabetes_cases": diabetes_cases,
            "anemia_cases": anemia_cases,
            "vision_defect_cases": vision_defect_cases,
            "dental_issues": dental_issues,
            "critical_referrals": critical_referrals,
            "doctors_deployed": doctors,
            "nurses_deployed": nurses,
            "chw_deployed": chws,
            "budget_usd": budget_allocated,
            "cost_per_patient": cost_per_patient
        })
        
    df = pd.DataFrame(camps)
    return df

if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(out_dir, exist_ok=True)
    df = generate_health_camp_data()
    out_path = os.path.join(out_dir, "health_camps.csv")
    df.to_csv(out_path, index=False)
    print(f"Generated {len(df)} health camp records at: {out_path}")
