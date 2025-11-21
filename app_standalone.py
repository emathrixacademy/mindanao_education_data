"""
============================================================================
MINDANAO EDUCATION DATA PORTAL - WEB SCRAPING VERSION
============================================================================
All data tables load immediately on home page for easy scraping
============================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(
    page_title="Mindanao Education Data Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# DATA GENERATION (same as before)
# ============================================================================

@st.cache_data
def generate_all_data():
    """Generate all education datasets - 1000+ rows per category"""
    
    np.random.seed(42)
    
    CITIES = {
        'General Santos': {'population': 697315, 'schools_public': 245, 'schools_private': 89, 
                          'base_enrollment': 185000, 'poverty_rate': 0.24},
        'Tacurong': {'population': 109319, 'schools_public': 78, 'schools_private': 23, 
                    'base_enrollment': 28000, 'poverty_rate': 0.31},
        'Isulan': {'population': 97490, 'schools_public': 65, 'schools_private': 18, 
                  'base_enrollment': 24000, 'poverty_rate': 0.29},
        'Koronadal': {'population': 184573, 'schools_public': 142, 'schools_private': 54, 
                     'base_enrollment': 48000, 'poverty_rate': 0.26},
        'Kidapawan': {'population': 160791, 'schools_public': 128, 'schools_private': 41, 
                     'base_enrollment': 42000, 'poverty_rate': 0.28}
    }
    
    YEARS = list(range(2015, 2025))
    MONTHS = list(range(1, 13))
    QUARTERS = ['Q1', 'Q2', 'Q3', 'Q4']
    SCHOOL_TYPES = ['Public', 'Private']
    GRADE_LEVELS = ['Grade 1', 'Grade 2', 'Grade 3', 'Grade 4', 'Grade 5', 'Grade 6',
                    'Grade 7', 'Grade 8', 'Grade 9', 'Grade 10', 'Grade 11', 'Grade 12']
    
    def add_noise(value, noise_level=0.05):
        noise = np.random.normal(0, noise_level * value)
        return max(0, value + noise)
    
    # ENROLLMENT DATA
    enrollment_data = []
    for city, config in CITIES.items():
        base = config['base_enrollment']
        for year in YEARS:
            if year < 2020:
                factor = 1.0
            elif year == 2020:
                factor = 0.92
            elif year == 2021:
                factor = 0.88
            elif year == 2022:
                factor = 0.95
            elif year == 2023:
                factor = 0.98
            else:
                factor = 1.02
            
            for month in MONTHS:
                month_factor = 1.1 if month in [6, 7, 8] else 1.0 if month in [9, 10, 11, 12, 1] else 0.95
                total = int(add_noise(base * factor * month_factor, 0.03))
                
                enrollment_data.append({
                    'City': city, 'Year': year, 'Month': month,
                    'Quarter': QUARTERS[(month-1)//3],
                    'Total_Enrollment': total,
                    'Elementary': int(total * 0.48),
                    'Junior_High': int(total * 0.32),
                    'Senior_High': int(total * 0.20),
                    'Male': int(total * np.random.uniform(0.48, 0.50)),
                    'Female': total - int(total * np.random.uniform(0.48, 0.50)),
                    'Public_Schools': int(total * (0.78 + config['poverty_rate'] * 0.3)),
                    'Private_Schools': total - int(total * (0.78 + config['poverty_rate'] * 0.3)),
                    'Enrollment_Rate': round(np.random.uniform(0.89, 0.97), 3)
                })
    
    # GRADUATE DATA
    graduates_data = []
    for city, config in CITIES.items():
        base_graduates = int(config['base_enrollment'] * 0.08)
        for year in YEARS:
            total = int(base_graduates * (0.7 if year < 2018 else 1.0))
            grad_rate = 0.95 - (config['poverty_rate'] * 0.15)
            
            tracks = ['STEM', 'ABM', 'HUMSS', 'TVL', 'GAS']
            track_dist = {'STEM': 0.22, 'ABM': 0.18, 'HUMSS': 0.25, 'TVL': 0.20, 'GAS': 0.15}
            
            for track in tracks:
                for school_type in SCHOOL_TYPES:
                    type_factor = 0.30 if school_type == 'Private' else 0.70
                    actual = int(total * track_dist[track] * type_factor * grad_rate)
                    
                    graduates_data.append({
                        'City': city, 'Year': year, 'Track': track,
                        'School_Type': school_type,
                        'Total_Graduates': actual,
                        'Graduation_Rate': round(grad_rate + np.random.uniform(-0.05, 0.05), 3),
                        'To_College': int(actual * np.random.uniform(0.55, 0.68)),
                        'To_Employment': int(actual * np.random.uniform(0.15, 0.25)),
                        'To_Vocational': int(actual * np.random.uniform(0.05, 0.12)),
                        'NEET': int(actual * np.random.uniform(0.08, 0.15)),
                        'Average_Grade': round(np.random.uniform(82, 94), 2)
                    })
    
    # OSY DATA
    osy_data = []
    for city, config in CITIES.items():
        base_osy = int(config['population'] * 0.03 * (1 + config['poverty_rate']))
        for year in YEARS:
            if year < 2020:
                factor = 1.0
            elif year == 2020:
                factor = 1.15
            elif year == 2021:
                factor = 1.22
            elif year == 2022:
                factor = 1.14
            elif year == 2023:
                factor = 1.06
            else:
                factor = 1.0
            
            age_groups = ['6-11', '12-15', '16-18', '19-24']
            age_dist = {'6-11': 0.15, '12-15': 0.28, '16-18': 0.35, '19-24': 0.22}
            reasons = ['Financial', 'Family_Obligations', 'Distance', 'Lack_Interest', 'Health', 'Marriage', 'Work']
            reason_dist = {'Financial': 0.35, 'Family_Obligations': 0.20, 'Distance': 0.12, 
                          'Lack_Interest': 0.15, 'Health': 0.08, 'Marriage': 0.05, 'Work': 0.05}
            
            for age_group in age_groups:
                for reason in reasons:
                    total_osy = int(add_noise(base_osy * factor * age_dist[age_group] * reason_dist[reason], 0.08))
                    
                    osy_data.append({
                        'City': city, 'Year': year,
                        'Age_Group': age_group, 'Reason': reason,
                        'Total_OSY': total_osy,
                        'ALS_Enrolled': int(total_osy * np.random.uniform(0.15, 0.30)),
                        'Returned_to_School': int(total_osy * np.random.uniform(0.05, 0.12)),
                        'Gender_Male': int(total_osy * np.random.uniform(0.45, 0.55)),
                        'Gender_Female': total_osy - int(total_osy * np.random.uniform(0.45, 0.55))
                    })
    
    # POVERTY DATA
    poverty_data = []
    for city, config in CITIES.items():
        total_students = config['base_enrollment']
        for year in YEARS:
            num_barangays = {'General Santos': 26, 'Tacurong': 20, 'Isulan': 21, 
                            'Koronadal': 27, 'Kidapawan': 40}
            
            for barangay_num in range(1, num_barangays.get(city, 20) + 1):
                barangay_students = int(total_students / num_barangays.get(city, 20))
                poverty_variance = np.random.uniform(-0.15, 0.15)
                local_poverty_rate = max(0.05, min(0.60, config['poverty_rate'] + poverty_variance))
                
                poverty_data.append({
                    'City': city, 'Year': year,
                    'Barangay': f'Barangay {barangay_num}',
                    'Total_Students': barangay_students,
                    'FourPs_Beneficiaries': int(barangay_students * local_poverty_rate * 0.85),
                    'Scholarship_Recipients': int(barangay_students * np.random.uniform(0.10, 0.20)),
                    'Feeding_Program': int(barangay_students * np.random.uniform(0.20, 0.40)),
                    'Financial_Assistance': int(barangay_students * np.random.uniform(0.12, 0.25)),
                    'Poverty_Rate': round(local_poverty_rate, 3)
                })
    
    # INFRASTRUCTURE DATA
    infrastructure_data = []
    for city, config in CITIES.items():
        total_schools = config['schools_public'] + config['schools_private']
        
        for year in YEARS:
            for school_num in range(1, total_schools + 1):
                school_type = 'Public' if school_num <= config['schools_public'] else 'Private'
                shortage_rate = max(0.02, 0.20 - (year - 2015) * 0.015)
                
                if school_type == 'Public':
                    school_size = np.random.choice(['Small', 'Medium', 'Large'], p=[0.3, 0.5, 0.2])
                    base_students = {'Small': 200, 'Medium': 500, 'Large': 1000}[school_size]
                else:
                    school_size = np.random.choice(['Small', 'Medium', 'Large'], p=[0.5, 0.4, 0.1])
                    base_students = {'Small': 150, 'Medium': 300, 'Large': 600}[school_size]
                
                infrastructure_data.append({
                    'City': city, 'Year': year,
                    'School_ID': f'{city[:3].upper()}-{school_num:03d}',
                    'School_Type': school_type,
                    'School_Size': school_size,
                    'Student_Population': int(base_students * np.random.uniform(0.9, 1.1)),
                    'Classrooms': int(base_students / 40),
                    'Classroom_Shortage': int((base_students / 40) * shortage_rate),
                    'Has_Computer_Lab': np.random.choice([1, 0], p=[min(0.90, 0.40 + (year-2015)*0.05), 
                                                                     max(0.10, 0.60 - (year-2015)*0.05)]),
                    'Has_Internet': np.random.choice([1, 0], p=[min(0.85, 0.30 + (year-2015)*0.055), 
                                                                 max(0.15, 0.70 - (year-2015)*0.055)]),
                    'Has_Library': np.random.choice([1, 0], p=[0.75, 0.25]),
                    'Has_Science_Lab': np.random.choice([1, 0], p=[0.55, 0.45]),
                    'Teacher_Count': int(base_students / 30),
                    'Teacher_Student_Ratio': round(1 / np.random.uniform(25, 38), 4)
                })
    
    # INCIDENTS DATA
    incidents_data = []
    for city, config in CITIES.items():
        base_students = config['base_enrollment']
        
        for year in YEARS:
            factor = 0.5 if year in [2020, 2021] else 1.0
            
            incident_types = ['Bullying', 'Fighting', 'Truancy', 'Substance', 'Vandalism', 
                             'Theft', 'Cyberbullying', 'Others']
            
            for month in MONTHS:
                month_factor = 1.2 if month in [9, 10, 11, 1, 2, 3] else 0.3
                
                for incident_type in incident_types:
                    type_rates = {
                        'Bullying': 0.012, 'Fighting': 0.008, 'Truancy': 0.020,
                        'Substance': 0.004, 'Vandalism': 0.006, 'Theft': 0.005,
                        'Cyberbullying': 0.007, 'Others': 0.003
                    }
                    
                    count = int(base_students * type_rates[incident_type] * factor * month_factor / 12)
                    
                    incidents_data.append({
                        'City': city, 'Year': year, 'Month': month,
                        'Incident_Type': incident_type,
                        'Incident_Count': count,
                        'Resolved': int(count * np.random.uniform(0.70, 0.95)),
                        'Pending': int(count * np.random.uniform(0.05, 0.20)),
                        'Escalated': int(count * np.random.uniform(0, 0.10)),
                        'Student_Suspended': int(count * np.random.uniform(0.10, 0.30)),
                        'Parent_Conference': int(count * np.random.uniform(0.50, 0.80)),
                        'Counseling_Provided': int(count * np.random.uniform(0.40, 0.70))
                    })
    
    # PERFORMANCE DATA
    performance_data = []
    for city, config in CITIES.items():
        base_score = 75 - (config['poverty_rate'] * 30)
        
        for year in YEARS:
            improvement = (year - 2015) * 1.2
            
            subjects = ['Math', 'Science', 'English', 'Filipino', 'History', 'Arts']
            
            for grade in GRADE_LEVELS:
                grade_num = int(grade.split()[1])
                grade_factor = 1.0 - (grade_num / 100)
                
                for subject in subjects:
                    subject_difficulty = {
                        'Math': 0.90, 'Science': 0.93, 'English': 0.96,
                        'Filipino': 0.97, 'History': 0.98, 'Arts': 1.02
                    }
                    
                    score = round((base_score + improvement) * grade_factor * 
                                 subject_difficulty[subject] + np.random.uniform(-4, 4), 2)
                    score = max(40, min(100, score))
                    
                    performance_data.append({
                        'City': city, 'Year': year,
                        'Grade_Level': grade, 'Subject': subject,
                        'Average_Score': score,
                        'Passing_Rate': round(min(0.98, max(0.60, (score - 30) / 70)), 3),
                        'High_Performers': int(200 * ((score - 60) / 40)),
                        'Low_Performers': int(200 * ((85 - score) / 40)),
                        'Class_Size_Avg': int(np.random.uniform(35, 50)),
                        'Teacher_Quality_Rating': round(np.random.uniform(3.5, 5.0), 2)
                    })
    
    datasets = {
        'enrollment': pd.DataFrame(enrollment_data),
        'graduates': pd.DataFrame(graduates_data),
        'osy': pd.DataFrame(osy_data),
        'poverty': pd.DataFrame(poverty_data),
        'infrastructure': pd.DataFrame(infrastructure_data),
        'incidents': pd.DataFrame(incidents_data),
        'performance': pd.DataFrame(performance_data)
    }
    
    return datasets

# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def display_table_for_scraping(df, table_id, category_name):
    """Display table with proper HTML structure for scraping"""
    
    st.markdown(f"### 📊 {category_name.upper()} DATA")
    st.info(f"**Table ID:** `{table_id}` | **Records:** {len(df):,} | **Columns:** {len(df.columns)}")
    
    # Create HTML table with ID
    html = f'<div id="{table_id}">\n'
    html += '<table border="1" class="dataframe">\n<thead>\n<tr style="text-align: left;">\n'
    
    # Headers
    for col in df.columns:
        html += f'<th>{col}</th>\n'
    html += '</tr>\n</thead>\n<tbody>\n'
    
    # Rows
    for idx, row in df.iterrows():
        html += '<tr>\n'
        for val in row:
            html += f'<td>{val}</td>\n'
        html += '</tr>\n'
    
    html += '</tbody>\n</table>\n</div>'
    
    # Display in scrollable container
    st.markdown(f'<div style="max-height: 400px; overflow-y: auto;">{html}</div>', unsafe_allow_html=True)
    st.markdown("---")

# ============================================================================
# MAIN APP
# ============================================================================

def main():
    st.title("🎓 Mindanao Education Data Portal")
    st.markdown("### Web Scraping Practice Portal")
    
    st.info("""
    **🎯 For Web Scraping Workshop**
    
    All data tables are displayed below with unique IDs for scraping practice.
    
    **Table IDs:**
    - `enrollment_data_table`
    - `graduates_data_table`
    - `osy_data_table`
    - `poverty_data_table`
    - `infrastructure_data_table`
    - `incidents_data_table`
    - `performance_data_table`
    """)
    
    with st.spinner("🔄 Loading data..."):
        datasets = generate_all_data()
    
    st.success(f"✅ Loaded {sum(len(df) for df in datasets.values()):,} total records across 7 categories")
    
    st.markdown("---")
    
    # Display all tables
    for category, df in datasets.items():
        table_id = f"{category}_data_table"
        display_table_for_scraping(df, table_id, category)

if __name__ == "__main__":
    main()
