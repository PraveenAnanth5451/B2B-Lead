import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import time

from lead_enricher import LeadEnricher
from scoring_engine import ScoringEngine
from utils import validate_csv_format, create_sample_csv, normalize_dataframe_columns

# Page configuration
st.set_page_config(
    page_title="AI Lead Enrichment & Scoring",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'processed_leads' not in st.session_state:
    st.session_state.processed_leads = None
if 'enricher' not in st.session_state:
    st.session_state.enricher = LeadEnricher()
if 'scorer' not in st.session_state:
    st.session_state.scorer = ScoringEngine()

def main():
    st.title("🎯 AI-Powered B2B Lead Enrichment & Scoring")
    st.markdown("Transform raw lead data into actionable insights with intelligent enrichment and scoring")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Scoring weights configuration
        st.subheader("Scoring Weights")
        job_title_weight = st.slider("Job Title Relevance", 0.0, 1.0, 0.4, 0.1)
        tech_stack_weight = st.slider("Tech Stack Fit", 0.0, 1.0, 0.3, 0.1)
        buying_intent_weight = st.slider("Buying Intent", 0.0, 1.0, 0.3, 0.1)
        
        # Update scoring weights
        st.session_state.scorer.update_weights({
            'job_title': job_title_weight,
            'tech_stack': tech_stack_weight,
            'buying_intent': buying_intent_weight
        })
        
        # Minimum score filter
        min_score = st.slider("Minimum Score Filter", 0, 100, 0, 5)
        
        # Download sample CSV
        st.subheader("📥 Sample Data")
        if st.button("Download Sample CSV"):
            sample_csv = create_sample_csv()
            st.download_button(
                label="💾 Download Sample",
                data=sample_csv,
                file_name="sample_leads.csv",
                mime="text/csv"
            )
    
    # Main content area
    tab1, tab2, tab3 = st.tabs(["📊 Data Processing", "📈 Analytics", "ℹ️ Methodology"])
    
    with tab1:
        # File upload section
        st.header("📤 Upload Lead Data")
        uploaded_file = st.file_uploader(
            "Choose a CSV file with lead data",
            type="csv",
            help="CSV should contain columns: name, email, company_domain"
        )
        
        if uploaded_file is not None:
            try:
                # Read and validate CSV
                df = pd.read_csv(uploaded_file)
                
                if validate_csv_format(df):
                    st.success(f"✅ Valid CSV uploaded with {len(df)} leads")
                    
                    # Normalize the dataframe columns
                    normalized_df = normalize_dataframe_columns(df)
                    
                    # Show preview
                    st.subheader("📋 Data Preview")
                    st.dataframe(normalized_df.head(), use_container_width=True)
                    
                    # Process leads button
                    if st.button("🚀 Enrich & Score Leads", type="primary"):
                        process_leads(normalized_df)
                    
                else:
                    st.error("❌ Invalid CSV format. Please ensure your CSV has columns like: Name/Email/Company or Website")
                    
            except Exception as e:
                st.error(f"❌ Error reading CSV file: {str(e)}")
        
        # Display processed leads
        if st.session_state.processed_leads is not None:
            display_processed_leads(min_score)
    
    with tab2:
        if st.session_state.processed_leads is not None:
            display_analytics()
        else:
            st.info("📊 Upload and process leads to view analytics")
    
    with tab3:
        display_methodology()

def process_leads(df):
    """Process leads with enrichment and scoring"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Step 1: Enrich leads
        status_text.text("🔄 Enriching lead data...")
        progress_bar.progress(25)
        enriched_df = st.session_state.enricher.enrich_leads(df)
        time.sleep(0.5)  # Simulate processing time
        
        # Step 2: Score leads
        status_text.text("🧠 Scoring leads with AI...")
        progress_bar.progress(75)
        scored_df = st.session_state.scorer.score_leads(enriched_df)
        time.sleep(0.5)
        
        # Step 3: Complete
        status_text.text("✅ Processing complete!")
        progress_bar.progress(100)
        
        st.session_state.processed_leads = scored_df
        time.sleep(0.5)
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
        
        st.success(f"🎉 Successfully processed {len(scored_df)} leads!")
        
    except Exception as e:
        st.error(f"❌ Error processing leads: {str(e)}")

def display_processed_leads(min_score):
    """Display processed leads with filtering"""
    df = st.session_state.processed_leads
    
    # Apply score filter
    filtered_df = df[df['lead_score'] >= min_score]
    
    st.header("📊 Enriched & Scored Leads")
    st.markdown(f"Showing {len(filtered_df)} of {len(df)} leads (score >= {min_score})")
    
    # Color coding for scores
    def color_score(val):
        if val >= 80:
            return 'background-color: #d4edda'  # Light green
        elif val >= 60:
            return 'background-color: #fff3cd'  # Light yellow
        else:
            return 'background-color: #f8d7da'  # Light red
    
    # Display dataframe with styling
    styled_df = filtered_df.style.applymap(color_score, subset=['lead_score'])
    st.dataframe(styled_df, use_container_width=True)
    
    # Download processed data
    csv_buffer = BytesIO()
    filtered_df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    
    col1, col2 = st.columns([1, 4])
    with col1:
        st.download_button(
            label="💾 Download CSV",
            data=csv_buffer.getvalue(),
            file_name="enriched_leads.csv",
            mime="text/csv"
        )

def display_analytics():
    """Display analytics dashboard"""
    df = st.session_state.processed_leads
    
    st.header("📈 Lead Analytics Dashboard")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_score = df['lead_score'].mean()
        st.metric("Average Score", f"{avg_score:.1f}")
    
    with col2:
        high_quality = len(df[df['lead_score'] >= 80])
        st.metric("High Quality Leads", high_quality)
    
    with col3:
        total_leads = len(df)
        st.metric("Total Leads", total_leads)
    
    with col4:
        conversion_rate = (high_quality / total_leads * 100) if total_leads > 0 else 0
        st.metric("Quality Rate", f"{conversion_rate:.1f}%")
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        # Score distribution
        fig_hist = px.histogram(
            df, 
            x='lead_score', 
            nbins=20,
            title="Lead Score Distribution",
            labels={'lead_score': 'Lead Score', 'count': 'Number of Leads'}
        )
        fig_hist.update_layout(showlegend=False)
        st.plotly_chart(fig_hist, use_container_width=True)
    
    with col2:
        # Job title distribution
        job_title_counts = df['job_title'].value_counts().head(10)
        fig_bar = px.bar(
            x=job_title_counts.values,
            y=job_title_counts.index,
            orientation='h',
            title="Top Job Titles",
            labels={'x': 'Count', 'y': 'Job Title'}
        )
        fig_bar.update_layout(showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Score breakdown by criteria
    st.subheader("Score Breakdown Analysis")
    
    criteria_cols = ['job_title_score', 'tech_stack_score', 'buying_intent_score']
    avg_scores = df[criteria_cols].mean()
    
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=avg_scores.values,
        theta=['Job Title Relevance', 'Tech Stack Fit', 'Buying Intent'],
        fill='toself',
        name='Average Scores'
    ))
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=False,
        title="Average Scores by Criteria"
    )
    st.plotly_chart(fig_radar, use_container_width=True)

def display_methodology():
    """Display scoring methodology and explanations"""
    st.header("ℹ️ Scoring Methodology")
    
    st.markdown("""
    ### Lead Enrichment Process
    
    Our AI-powered system enriches your raw lead data through the following steps:
    
    1. **Data Validation**: Ensures email format and domain validity
    2. **Company Analysis**: Extracts insights from company domain
    3. **Profile Enrichment**: Adds job titles, seniority levels, and LinkedIn profiles
    4. **Technology Stack Detection**: Identifies relevant technologies used by the company
    5. **Buying Intent Analysis**: Evaluates signals indicating purchase readiness
    
    ### Scoring Algorithm
    
    Each lead receives a composite score (0-100) based on three key criteria:
    
    #### 🎯 Job Title Relevance (Configurable Weight)
    - **Decision Makers** (90-100): CEO, CTO, VP Engineering, Head of IT
    - **Influencers** (70-89): Engineering Manager, Technical Lead, Senior Developer
    - **Users** (40-69): Developer, Software Engineer, IT Specialist
    - **Others** (0-39): Non-technical roles
    
    #### 🛠️ Tech Stack Fit (Configurable Weight)
    - **Perfect Match** (90-100): Uses target technologies directly
    - **Good Fit** (70-89): Uses complementary or similar technologies
    - **Potential Fit** (40-69): Uses related but different technologies
    - **Poor Fit** (0-39): No relevant technology alignment
    
    #### 📊 Buying Intent (Configurable Weight)
    - **High Intent** (80-100): Recent hiring, funding, technology adoption signals
    - **Medium Intent** (50-79): Some growth indicators or technology interest
    - **Low Intent** (20-49): Stable company with minimal change signals
    - **No Intent** (0-19): No detectable buying signals
    
    ### Quality Thresholds
    
    - **High Quality** (80-100): Prime prospects for immediate outreach
    - **Medium Quality** (60-79): Good prospects for nurturing campaigns
    - **Low Quality** (0-59): Requires further qualification or different approach
    
    ### Customization
    
    Use the sidebar controls to adjust scoring weights based on your specific ICP criteria and sales strategy.
    """)

if __name__ == "__main__":
    main()
