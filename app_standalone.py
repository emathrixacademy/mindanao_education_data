"""
============================================================================
MINDANAO EDUCATION DATA PORTAL - WEB SCRAPING VERSION
============================================================================
Version for teaching web scraping:
- NO download buttons
- NO pagination
- ALL data displayed in full tables
- Perfect for rvest scraping in R
============================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Mindanao Education Data Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# EMBEDDED DATA GENERATION (1000+ ROWS PER CATEGORY)
# ============================================================================

@st.cache_data
def generate_all_data():
    """Generate all education datasets - 1000+ rows per category"""
    
    np.random.seed(42)
    
    # City configurations
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
    
    YEARS = list(range(2015, 2025))  # 10 years: 2015-2024
    MONTHS = list(range(1, 13))  # 12 months
    QUARTERS = ['Q1', 'Q2', 'Q3', 'Q4']
    SCHOOL_TYPES = ['Public', 'Private']
    GRADE_LEVELS = ['Grade 1', 'Grade 2', 'Grade 3', 'Grade 4', 'Grade 5', 'Grade 6',
                    'Grade 7', 'Grade 8', 'Grade 9', 'Grade 10',
                    'Grade 11', 'Grade 12']
    
    def add_noise(value, noise_level=0.05):
        noise = np.random.normal(0, noise_level * value)
        return max(0, value + noise)
    
    # ========== ENROLLMENT DATA (600+ rows) ==========
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
                    'City': city,
                    'Year': year,
                    'Month': month,
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
    
    # ========== GRADUATE DATA (1000+ rows) ==========
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
                        'City': city,
                        'Year': year,
                        'Track': track,
                        'School_Type': school_type,
                        'Total_Graduates': actual,
                        'Graduation_Rate': round(grad_rate + np.random.uniform(-0.05, 0.05), 3),
                        'To_College': int(actual * np.random.uniform(0.55, 0.68)),
                        'To_Employment': int(actual * np.random.uniform(0.15, 0.25)),
                        'To_Vocational': int(actual * np.random.uniform(0.05, 0.12)),
                        'NEET': int(actual * np.random.uniform(0.08, 0.15)),
                        'Average_Grade': round(np.random.uniform(82, 94), 2)
                    })
    
    # ========== OSY DATA (1400+ rows) ==========
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
                        'City': city,
                        'Year': year,
                        'Age_Group': age_group,
                        'Reason': reason,
                        'Total_OSY': total_osy,
                        'ALS_Enrolled': int(total_osy * np.random.uniform(0.15, 0.30)),
                        'Returned_to_School': int(total_osy * np.random.uniform(0.05, 0.12)),
                        'Gender_Male': int(total_osy * np.random.uniform(0.45, 0.55)),
                        'Gender_Female': total_osy - int(total_osy * np.random.uniform(0.45, 0.55))
                    })
    
    # ========== POVERTY DATA (1150+ rows) ==========
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
                    'City': city,
                    'Year': year,
                    'Barangay': f'Barangay {barangay_num}',
                    'Total_Students': barangay_students,
                    'FourPs_Beneficiaries': int(barangay_students * local_poverty_rate * 0.85),
                    'Scholarship_Recipients': int(barangay_students * np.random.uniform(0.10, 0.20)),
                    'Feeding_Program': int(barangay_students * np.random.uniform(0.20, 0.40)),
                    'Financial_Assistance': int(barangay_students * np.random.uniform(0.12, 0.25)),
                    'Poverty_Rate': round(local_poverty_rate, 3)
                })
    
    # ========== INFRASTRUCTURE DATA (1590+ rows) ==========
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
                    'City': city,
                    'Year': year,
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
    
    # ========== INCIDENTS DATA (4800+ rows) ==========
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
                        'City': city,
                        'Year': year,
                        'Month': month,
                        'Incident_Type': incident_type,
                        'Incident_Count': count,
                        'Resolved': int(count * np.random.uniform(0.70, 0.95)),
                        'Pending': int(count * np.random.uniform(0.05, 0.20)),
                        'Escalated': int(count * np.random.uniform(0, 0.10)),
                        'Student_Suspended': int(count * np.random.uniform(0.10, 0.30)),
                        'Parent_Conference': int(count * np.random.uniform(0.50, 0.80)),
                        'Counseling_Provided': int(count * np.random.uniform(0.40, 0.70))
                    })
    
    # ========== PERFORMANCE DATA (4320+ rows) ==========
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
                        'City': city,
                        'Year': year,
                        'Grade_Level': grade,
                        'Subject': subject,
                        'Average_Score': score,
                        'Passing_Rate': round(min(0.98, max(0.60, (score - 30) / 70)), 3),
                        'High_Performers': int(200 * ((score - 60) / 40)),
                        'Low_Performers': int(200 * ((85 - score) / 40)),
                        'Class_Size_Avg': int(np.random.uniform(35, 50)),
                        'Teacher_Quality_Rating': round(np.random.uniform(3.5, 5.0), 2)
                    })
    
    # Convert to DataFrames
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
# STYLING
# ============================================================================

def local_css():
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
        border-bottom: 3px solid #1f77b4;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.8rem;
        font-weight: 600;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-left: 5px solid #3498db;
        padding-left: 15px;
    }
    .data-table {
        border: 2px solid #e0e0e0;
        border-radius: 8px;
        overflow: hidden;
        max-height: 600px;
        overflow-y: auto;
    }
    table {
        width: 100%;
        border-collapse: collapse;
    }
    table th {
        background-color: #1f77b4;
        color: white;
        padding: 12px;
        text-align: left;
        font-weight: 600;
        position: sticky;
        top: 0;
        z-index: 10;
    }
    table td {
        padding: 10px;
        border-bottom: 1px solid #ddd;
    }
    table tr:hover {
        background-color: #f5f5f5;
    }
    </style>
    """, unsafe_allow_html=True)

def format_number(num):
    if pd.isna(num):
        return "N/A"
    return f"{int(num):,}"

def display_data_table(df, table_id):
    """Display COMPLETE dataframe as scrollable HTML table - NO PAGINATION"""
    html = f'<div id="{table_id}" class="data-table">\n'
    html += df.to_html(index=False, classes='dataframe', border=0, escape=False)
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

# ============================================================================
# PAGES
# ============================================================================

def page_home(datasets):
    st.markdown('<div class="main-header">🎓 Mindanao Education Data Portal</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background:#e3f2fd; padding:1rem; border-radius:8px; border-left:4px solid #2196f3; margin:1rem 0;">
    <h3>📊 Welcome to the Mindanao Education Data Portal</h3>
    <p>Comprehensive education statistics for 5 major Mindanao cities covering 2015-2024.</p>
    <p><strong>🎓 For Web Scraping Practice:</strong> All data tables display complete datasets for scraping with R or Python!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="sub-header">📈 Regional Overview</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_records = sum(len(df) for df in datasets.values())
        st.metric("Total Records", format_number(total_records))
    
    with col2:
        st.metric("Categories", "7")
    
    with col3:
        st.metric("Cities", "5")
    
    with col4:
        st.metric("Years", "2015-2024")
    
    st.markdown("---")
    
    st.markdown('<div class="sub-header">📊 Dataset Sizes</div>', unsafe_allow_html=True)
    
    dataset_info = []
    for name, df in datasets.items():
        dataset_info.append({
            'Category': name.upper(),
            'Total Records': len(df),
            'Columns': len(df.columns),
            'Scrapable': '✅ Yes'
        })
    
    info_df = pd.DataFrame(dataset_info)
    st.dataframe(info_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.success("🎯 All data is displayed in full on the 'Data Tables' page for web scraping practice!")

def page_all_data(datasets):
    st.markdown('<div class="main-header">📊 Complete Data Tables</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background:#fff3cd; padding:1rem; border-radius:8px; border-left:4px solid #ff9800; margin:1rem 0;">
    <h3>🎓 Web Scraping Instructions</h3>
    <p><strong>All tables display COMPLETE datasets</strong> - perfect for web scraping practice!</p>
    <p>Each table has a unique ID: <code>[category]_data_table</code></p>
    <p><strong>Example:</strong> Use <code>enrollment_data_table</code> to scrape enrollment data with R (rvest) or Python (BeautifulSoup)</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    for category, df in datasets.items():
        st.markdown(f'<div class="sub-header">📊 {category.upper().replace("_", " ")} DATA</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info(f"📋 **Total Records:** {len(df):,}")
        with col2:
            st.info(f"📊 **Columns:** {len(df.columns)}")
        with col3:
            st.info(f"🔖 **Table ID:** `{category}_data_table`")
        
        # Display COMPLETE table (scrollable)
        st.markdown(f"**Displaying ALL {len(df):,} rows** (scroll to view)")
        display_data_table(df, f"{category}_data_table")
        
        st.markdown("---")

# ============================================================================
# MAIN APP
# ============================================================================

def main():
    local_css()
    
    with st.spinner("🔄 Loading education data..."):
        datasets = generate_all_data()
    
    with st.sidebar:
        st.markdown("### 🧭 Navigation")
        page = st.radio("Choose:", ["🏠 Home", "📊 Data Tables"], 
                       label_visibility="collapsed")
        
        st.markdown("---")
        
        total_records = sum(len(df) for df in datasets.values())
        st.success(f"**{format_number(total_records)}** records ready")
        
        st.info("""
        **Web Scraping Portal**
        
        🏙️ 5 Cities  
        📊 7 Categories  
        📅 2015-2024  
        🎓 Full data display
        """)
        
        st.markdown("---")
        st.markdown("### 🎯 For Students")
        st.markdown("""
        All data tables show **complete datasets** for web scraping practice!
        
        Use R (rvest) or Python (BeautifulSoup) to extract data.
        """)
    
    if page == "🏠 Home":
        page_home(datasets)
    else:
        page_all_data(datasets)

if __name__ == "__main__":
    main()
