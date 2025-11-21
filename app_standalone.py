"""
============================================================================
MINDANAO EDUCATION DATA PORTAL - STANDALONE VERSION
============================================================================
Complete self-contained version with embedded data generation.
Deploy to Streamlit Cloud - No external files needed!

Data generates automatically on first visit.
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
# EMBEDDED DATA GENERATION
# ============================================================================

@st.cache_data
def generate_all_data():
    """Generate all education datasets - embedded in app"""
    
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
    
    YEARS = [2020, 2021, 2022, 2023, 2024]
    
    def add_noise(value, noise_level=0.05):
        noise = np.random.normal(0, noise_level * value)
        return max(0, value + noise)
    
    # ========== ENROLLMENT DATA ==========
    enrollment_data = []
    for city, config in CITIES.items():
        base = config['base_enrollment']
        for year in YEARS:
            factor = {2020: 0.92, 2021: 0.88, 2022: 0.95, 2023: 0.98, 2024: 1.02}[year]
            total = int(add_noise(base * factor, 0.03))
            
            enrollment_data.append({
                'City': city, 'Year': year, 'Total_Enrollment': total,
                'Elementary': int(total * 0.48), 'Junior_High': int(total * 0.32),
                'Senior_High': int(total * 0.20),
                'Male': int(total * np.random.uniform(0.48, 0.50)),
                'Female': total - int(total * np.random.uniform(0.48, 0.50)),
                'Public_Schools': int(total * (0.78 + config['poverty_rate'] * 0.3)),
                'Private_Schools': total - int(total * (0.78 + config['poverty_rate'] * 0.3)),
                'Enrollment_Rate': round(np.random.uniform(0.91, 0.97), 3)
            })
    
    # ========== GRADUATE DATA ==========
    graduates_data = []
    for city, config in CITIES.items():
        base_graduates = int(config['base_enrollment'] * 0.08)
        for year in YEARS:
            total = int(base_graduates * (0.7 if year < 2022 else 1.0))
            grad_rate = 0.95 - (config['poverty_rate'] * 0.15)
            actual = int(total * grad_rate)
            
            graduates_data.append({
                'City': city, 'Year': year, 'Total_Graduates': actual,
                'Graduation_Rate': round(grad_rate, 3),
                'To_College': int(actual * np.random.uniform(0.55, 0.68)),
                'To_Employment': int(actual * np.random.uniform(0.15, 0.25)),
                'NEET': int(actual * np.random.uniform(0.10, 0.20)),
                'STEM_Graduates': int(actual * 0.22), 'ABM_Graduates': int(actual * 0.18),
                'HUMSS_Graduates': int(actual * 0.25), 'TVL_Graduates': int(actual * 0.20),
                'GAS_Graduates': int(actual * 0.15)
            })
    
    # ========== OSY DATA ==========
    osy_data = []
    for city, config in CITIES.items():
        base_osy = int(config['population'] * 0.03 * (1 + config['poverty_rate']))
        for year in YEARS:
            factor = {2020: 1.15, 2021: 1.22, 2022: 1.14, 2023: 1.06, 2024: 1.0}[year]
            total_osy = int(add_noise(base_osy * factor, 0.06))
            
            osy_data.append({
                'City': city, 'Year': year, 'Total_OSY': total_osy,
                'Age_6_11': int(total_osy * 0.15), 'Age_12_15': int(total_osy * 0.28),
                'Age_16_18': int(total_osy * 0.35), 'Age_19_24': int(total_osy * 0.22),
                'ALS_Enrolled': int(total_osy * np.random.uniform(0.18, 0.28)),
                'Financial': int(total_osy * 0.42), 'Family_Obligations': int(total_osy * 0.23),
                'Distance_to_School': int(total_osy * 0.12), 'Lack_of_Interest': int(total_osy * 0.15),
                'Health_Issues': int(total_osy * 0.08)
            })
    
    # ========== POVERTY DATA ==========
    poverty_data = []
    for city, config in CITIES.items():
        total_students = config['base_enrollment']
        for year in YEARS:
            poverty_data.append({
                'City': city, 'Year': year, 'Total_Students': int(total_students),
                'FourPs_Beneficiaries': int(total_students * config['poverty_rate'] * 0.90),
                'Scholarship_Recipients': int(total_students * np.random.uniform(0.12, 0.18)),
                'Feeding_Program': int(total_students * np.random.uniform(0.25, 0.35)),
                'Financial_Assistance': int(total_students * np.random.uniform(0.15, 0.22)),
                'Poverty_Rate': round(config['poverty_rate'], 3)
            })
    
    # ========== INFRASTRUCTURE DATA ==========
    infrastructure_data = []
    for city, config in CITIES.items():
        total_schools = config['schools_public'] + config['schools_private']
        for year in YEARS:
            shortage_rate = max(0.05, 0.18 - (year - 2020) * 0.02)
            
            infrastructure_data.append({
                'City': city, 'Year': year, 'Total_Schools': total_schools,
                'Public_Schools': config['schools_public'], 'Private_Schools': config['schools_private'],
                'Classroom_Shortage': int(total_schools * shortage_rate * np.random.uniform(15, 25)),
                'Schools_With_Computers': int(total_schools * min(0.85, 0.45 + (year - 2020) * 0.08)),
                'Schools_With_Internet': int(total_schools * min(0.75, 0.35 + (year - 2020) * 0.08)),
                'Teacher_Student_Ratio': round(np.random.uniform(1/28, 1/35), 4),
                'Libraries': int(total_schools * np.random.uniform(0.65, 0.80)),
                'Science_Labs': int(total_schools * np.random.uniform(0.45, 0.60)),
                'Computer_Labs': int(total_schools * np.random.uniform(0.50, 0.70))
            })
    
    # ========== INCIDENTS DATA ==========
    incidents_data = []
    for city, config in CITIES.items():
        base_students = config['base_enrollment']
        for year in YEARS:
            factor = 0.6 if year in [2020, 2021] else 1.0
            
            incidents_data.append({
                'City': city, 'Year': year,
                'Bullying_Cases': int(base_students * np.random.uniform(0.008, 0.015) * factor),
                'Fighting_Incidents': int(base_students * np.random.uniform(0.004, 0.009) * factor),
                'Truancy_Cases': int(base_students * np.random.uniform(0.012, 0.025) * factor),
                'Substance_Related': int(base_students * np.random.uniform(0.002, 0.006) * factor),
                'Vandalism': int(base_students * np.random.uniform(0.003, 0.007) * factor),
                'Suspensions': int(base_students * np.random.uniform(0.005, 0.010) * factor),
                'Counseling_Referrals': int(base_students * np.random.uniform(0.015, 0.025) * factor),
                'Mental_Health_Referrals': int(base_students * np.random.uniform(0.015, 0.030)),
                'Absenteeism_Rate': round(np.random.uniform(0.08, 0.15), 3)
            })
    
    # ========== PERFORMANCE DATA ==========
    performance_data = []
    for city, config in CITIES.items():
        base_score = 75 - (config['poverty_rate'] * 30)
        for year in YEARS:
            improvement = (year - 2020) * 1.5
            nat_score = round(base_score + improvement + np.random.uniform(-3, 3), 2)
            
            performance_data.append({
                'City': city, 'Year': year, 'NAT_Average_Score': nat_score,
                'Math_Score': round(nat_score * np.random.uniform(0.92, 1.05), 2),
                'Science_Score': round(nat_score * np.random.uniform(0.95, 1.03), 2),
                'English_Score': round(nat_score * np.random.uniform(0.97, 1.04), 2),
                'Filipino_Score': round(nat_score * np.random.uniform(0.96, 1.02), 2),
                'Literacy_Rate': round(min(0.98, 0.88 + (year - 2020) * 0.02), 3),
                'Numeracy_Rate': round(min(0.95, 0.82 + (year - 2020) * 0.025), 3),
                'ICT_Basic': round(min(0.92, 0.55 + (year - 2020) * 0.08), 3),
                'ICT_Intermediate': round(min(0.65, 0.30 + (year - 2020) * 0.07), 3),
                'ICT_Advanced': round(min(0.35, 0.12 + (year - 2020) * 0.05), 3),
                'STEM_Competition_Participants': int(config['base_enrollment'] * 0.05),
                'STEM_Competition_Winners': int(config['base_enrollment'] * 0.05 * np.random.uniform(0.08, 0.15))
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
# STYLING & HELPER FUNCTIONS
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

def format_percentage(num):
    if pd.isna(num):
        return "N/A"
    return f"{num*100:.1f}%"

def display_data_table(df, table_id):
    html = f'<div id="{table_id}" class="data-table">\n'
    html += df.to_html(index=False, classes='dataframe', border=0)
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
    <p>Comprehensive education statistics for 5 major Mindanao cities covering 2020-2024.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="sub-header">📈 Regional Overview</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_enrollment = datasets['enrollment']['Total_Enrollment'].sum()
        st.metric("Total Students", format_number(total_enrollment))
    
    with col2:
        total_schools = datasets['infrastructure']['Total_Schools'].sum() // 5
        st.metric("Total Schools", format_number(total_schools))
    
    with col3:
        total_graduates = datasets['graduates']['Total_Graduates'].sum()
        st.metric("Total Graduates", format_number(total_graduates))
    
    with col4:
        avg_nat = datasets['performance']['NAT_Average_Score'].mean()
        st.metric("Avg NAT Score", f"{avg_nat:.1f}/100")
    
    st.markdown("---")
    
    st.markdown('<div class="sub-header">🏙️ Cities Covered</div>', unsafe_allow_html=True)
    
    cities = datasets['enrollment']['City'].unique()
    cols = st.columns(len(cities))
    for i, city in enumerate(cities):
        with cols[i]:
            city_data = datasets['enrollment'][datasets['enrollment']['City'] == city]
            latest = city_data[city_data['Year'] == city_data['Year'].max()]['Total_Enrollment'].values[0]
            st.metric(city, format_number(latest), "students")
    
    st.markdown("---")
    st.info(f"📅 Data Last Updated: {datetime.now().strftime('%B %d, %Y')} | 📊 Coverage: 2020-2024")

def page_city_dashboard(city, datasets):
    st.markdown(f'<div class="main-header">🏙️ {city} Education Dashboard</div>', unsafe_allow_html=True)
    
    year = st.selectbox("Select Year:", [2024, 2023, 2022, 2021, 2020], key=f"year_{city}")
    
    st.markdown("---")
    st.markdown('<div class="sub-header">📊 Key Metrics</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    enroll = datasets['enrollment'][(datasets['enrollment']['City'] == city) & (datasets['enrollment']['Year'] == year)]
    grads = datasets['graduates'][(datasets['graduates']['City'] == city) & (datasets['graduates']['Year'] == year)]
    perf = datasets['performance'][(datasets['performance']['City'] == city) & (datasets['performance']['Year'] == year)]
    infra = datasets['infrastructure'][(datasets['infrastructure']['City'] == city) & (datasets['infrastructure']['Year'] == year)]
    
    with col1:
        if not enroll.empty:
            st.metric("Total Enrollment", format_number(enroll['Total_Enrollment'].values[0]))
    with col2:
        if not grads.empty:
            st.metric("Graduation Rate", format_percentage(grads['Graduation_Rate'].values[0]))
    with col3:
        if not perf.empty:
            st.metric("NAT Average", f"{perf['NAT_Average_Score'].values[0]:.1f}/100")
    with col4:
        if not infra.empty:
            st.metric("Total Schools", format_number(infra['Total_Schools'].values[0]))
    
    st.markdown("---")
    st.markdown('<div class="sub-header">📊 Enrollment Statistics</div>', unsafe_allow_html=True)
    
    if not enroll.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            levels = ['Elementary', 'Junior_High', 'Senior_High']
            values = [enroll[level].values[0] for level in levels]
            fig = px.pie(values=values, names=['Elementary', 'Junior High', 'Senior High'],
                        title="Enrollment by Level", color_discrete_sequence=px.colors.sequential.Blues_r)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            gender_data = pd.DataFrame({
                'Gender': ['Male', 'Female'],
                'Count': [enroll['Male'].values[0], enroll['Female'].values[0]]
            })
            fig = px.bar(gender_data, x='Gender', y='Count', title="Enrollment by Gender",
                        color='Gender', color_discrete_map={'Male': '#3498db', 'Female': '#e74c3c'})
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown(f"**Enrollment Data Table (ID: enrollment_{city.replace(' ', '_')}_{year})**")
        display_data_table(enroll, f"enrollment_{city.replace(' ', '_')}_{year}")
    
    st.markdown("---")
    st.markdown('<div class="sub-header">📈 Student Performance</div>', unsafe_allow_html=True)
    
    if not perf.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            subjects = ['Math', 'Science', 'English', 'Filipino']
            scores = [perf[f'{subj}_Score'].values[0] for subj in subjects]
            fig = go.Figure()
            fig.add_trace(go.Bar(x=subjects, y=scores,
                                marker_color=['#3498db', '#2ecc71', '#e74c3c', '#f39c12'],
                                text=[f"{s:.1f}" for s in scores], textposition='auto'))
            fig.update_layout(title="Subject Scores", yaxis_title="Score", yaxis_range=[0, 100])
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            ict_levels = ['Basic', 'Intermediate', 'Advanced']
            ict_values = [perf['ICT_Basic'].values[0] * 100,
                         perf['ICT_Intermediate'].values[0] * 100,
                         perf['ICT_Advanced'].values[0] * 100]
            fig = px.bar(x=ict_levels, y=ict_values, title="ICT Proficiency Levels (%)",
                        labels={'x': 'Level', 'y': 'Percentage'}, color=ict_levels)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown(f"**Performance Data Table (ID: performance_{city.replace(' ', '_')}_{year})**")
        display_data_table(perf, f"performance_{city.replace(' ', '_')}_{year}")

def page_all_data(datasets):
    st.markdown('<div class="main-header">📊 Complete Data Tables</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background:#e3f2fd; padding:1rem; border-radius:8px;">
    <h3>🔍 Web Scraping Guide</h3>
    <p>All tables have unique IDs: <code>[category]_data_table</code></p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        selected_city = st.selectbox("Filter by City:", ['All Cities'] + list(datasets['enrollment']['City'].unique()))
    with col2:
        selected_year = st.selectbox("Filter by Year:", ['All Years'] + [2024, 2023, 2022, 2021, 2020])
    
    st.markdown("---")
    
    for category, df in datasets.items():
        st.markdown(f'<div class="sub-header">📊 {category.upper().replace("_", " ")} DATA</div>', unsafe_allow_html=True)
        
        df_filtered = df.copy()
        if selected_city != 'All Cities':
            df_filtered = df_filtered[df_filtered['City'] == selected_city]
        if selected_year != 'All Years':
            df_filtered = df_filtered[df_filtered['Year'] == selected_year]
        
        st.info(f"📋 Records: {len(df_filtered)} | 📊 Columns: {len(df_filtered.columns)} | 🔖 Table ID: `{category}_data_table`")
        display_data_table(df_filtered, f"{category}_data_table")
        
        csv = df_filtered.to_csv(index=False)
        st.download_button(f"💾 Download {category.upper()}", csv, f"{category}_data.csv", "text/csv", key=f"dl_{category}")
        st.markdown("---")

# ============================================================================
# MAIN APP
# ============================================================================

def main():
    local_css()
    
    # Generate all data (cached - only runs once)
    with st.spinner("🔄 Loading education data..."):
        datasets = generate_all_data()
    
    cities = list(datasets['enrollment']['City'].unique())
    
    with st.sidebar:
        st.markdown("### 🧭 Navigation")
        page = st.radio("Choose:", ["🏠 Home", "🏙️ City Dashboards", "📊 All Data Tables"], 
                       label_visibility="collapsed")
        
        st.markdown("---")
        
        selected_city = None
        if page == "🏙️ City Dashboards":
            st.markdown("### 🏙️ Select City")
            selected_city = st.selectbox("City:", cities, label_visibility="collapsed")
        
        st.markdown("---")
        st.info("""
        **Mindanao Education Portal**
        
        5 Cities | 7 Categories
        📅 Data: 2020-2024
        """)
    
    if page == "🏠 Home":
        page_home(datasets)
    elif page == "🏙️ City Dashboards":
        page_city_dashboard(selected_city, datasets)
    elif page == "📊 All Data Tables":
        page_all_data(datasets)

if __name__ == "__main__":
    main()
