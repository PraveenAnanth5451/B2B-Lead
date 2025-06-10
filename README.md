# AI-Powered B2B Lead Enrichment & Scoring

A powerful web application that transforms raw lead data into actionable insights through intelligent enrichment and scoring. Built with Streamlit, this tool helps sales and marketing teams identify and prioritize high-quality leads.

## Features

- 📊 **Lead Enrichment**: Automatically enriches lead data with company information, job titles, and technology stack details
- 🎯 **AI Scoring**: Intelligent scoring system based on multiple criteria:
  - Job Title Relevance
  - Tech Stack Fit
  - Buying Intent
- 📈 **Analytics Dashboard**: Visual insights into lead quality and distribution
- ⚙️ **Customizable Scoring**: Adjust scoring weights to match your ideal customer profile
- 💾 **CSV Import/Export**: Easy data import and export functionality
- 📋 **Sample Data**: Includes sample CSV template for quick start


## Usage

1. Run the Streamlit application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the provided local URL (typically http://localhost:8501)

3. Upload your lead data in CSV format (use the sample CSV template for reference)

4. Configure scoring weights in the sidebar to match your requirements

5. Process your leads and explore the enriched data and analytics

## Data Format

The application expects a CSV file with the following columns:
- name
- email
- company_domain

## Scoring Methodology

The system evaluates leads based on three key criteria:

1. **Job Title Relevance**
   - Decision Makers (90-100)
   - Influencers (70-89)
   - Users (40-69)
   - Others (0-39)

2. **Tech Stack Fit**
   - Perfect Match (90-100)
   - Good Fit (70-89)
   - Potential Fit (40-69)
   - Poor Fit (0-39)

3. **Buying Intent**
   - High Intent (80-100)
   - Medium Intent (50-79)
   - Low Intent (20-49)
   - No Intent (0-19)
