import pandas as pd
import re
from io import StringIO

def validate_csv_format(df: pd.DataFrame) -> bool:
    """Validate that CSV has required columns"""
    # Normalize column names to lowercase for flexible matching
    df_columns_lower = [col.lower().strip() for col in df.columns]
    
    # Required columns with flexible naming
    required_mappings = {
        'name': ['name', 'full_name', 'contact_name', 'lead_name'],
        'email': ['email', 'email_address', 'contact_email'],
        'company_domain': ['company_domain', 'domain', 'website', 'company_website', 'company']
    }
    
    # Check if we can find matches for all required fields
    found_columns = {}
    for required_field, possible_names in required_mappings.items():
        found = False
        for possible_name in possible_names:
            if possible_name in df_columns_lower:
                # Map to the actual column name in the dataframe
                actual_col_index = df_columns_lower.index(possible_name)
                found_columns[required_field] = df.columns[actual_col_index]
                found = True
                break
        
        if not found:
            return False
    
    # Store the column mapping for later use
    df._column_mapping = found_columns
    
    # Check if dataframe is not empty
    if df.empty:
        return False
    
    # Validate email format using the mapped email column
    email_col = found_columns['email']
    email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    invalid_emails = df[~df[email_col].astype(str).str.match(email_pattern, na=False)]
    
    # Allow some invalid emails but warn if too many
    invalid_ratio = len(invalid_emails) / len(df)
    if invalid_ratio > 0.5:  # More than 50% invalid emails
        return False
    
    return True

def validate_email(email: str) -> bool:
    """Validate individual email format"""
    pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    return bool(pattern.match(email))

def extract_domain(email: str) -> str:
    """Extract domain from email address"""
    try:
        return email.split('@')[1].lower()
    except (IndexError, AttributeError):
        return ""

def create_sample_csv() -> str:
    """Create sample CSV data for demonstration"""
    sample_data = [
        ["John Smith", "john.smith@techcorp.com", "techcorp.com"],
        ["Sarah Johnson", "sarah.j@innovatesoft.io", "innovatesoft.io"],
        ["Michael Chen", "m.chen@dataworks.net", "dataworks.net"],
        ["Emily Rodriguez", "emily@startupco.com", "startupco.com"],
        ["David Wilson", "dwilson@enterprise-solutions.com", "enterprise-solutions.com"],
        ["Lisa Anderson", "l.anderson@cloudtech.org", "cloudtech.org"],
        ["Robert Taylor", "rtaylor@devops-pro.com", "devops-pro.com"],
        ["Jennifer Lee", "jennifer.lee@aicompany.io", "aicompany.io"],
        ["Mark Thompson", "mark@scalable-systems.net", "scalable-systems.net"],
        ["Amanda Davis", "a.davis@fintech-innovate.com", "fintech-innovate.com"]
    ]
    
    # Create DataFrame
    df = pd.DataFrame(sample_data)
    df.columns = ['name', 'email', 'company_domain']
    
    # Convert to CSV string
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    return csv_buffer.getvalue()

def format_score_color(score: float) -> str:
    """Return color code based on score value"""
    if score >= 80:
        return "#28a745"  # Green
    elif score >= 60:
        return "#ffc107"  # Yellow
    else:
        return "#dc3545"  # Red

def calculate_quality_metrics(df: pd.DataFrame) -> dict:
    """Calculate lead quality metrics"""
    if df.empty:
        return {
            'total_leads': 0,
            'high_quality': 0,
            'medium_quality': 0,
            'low_quality': 0,
            'average_score': 0,
            'quality_rate': 0
        }
    
    total_leads = len(df)
    high_quality = len(df[df['lead_score'] >= 80])
    medium_quality = len(df[(df['lead_score'] >= 60) & (df['lead_score'] < 80)])
    low_quality = len(df[df['lead_score'] < 60])
    average_score = df['lead_score'].mean()
    quality_rate = (high_quality / total_leads * 100) if total_leads > 0 else 0
    
    return {
        'total_leads': total_leads,
        'high_quality': high_quality,
        'medium_quality': medium_quality,
        'low_quality': low_quality,
        'average_score': round(average_score, 1),
        'quality_rate': round(quality_rate, 1)
    }

def normalize_dataframe_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize dataframe columns to standard format"""
    if not hasattr(df, '_column_mapping'):
        return df
    
    # Create a copy and rename columns
    normalized_df = df.copy()
    for standard_name, actual_column in df._column_mapping.items():
        if actual_column in normalized_df.columns:
            normalized_df.rename(columns={actual_column: standard_name}, inplace=True)
    
    # Clean company domain column if it contains websites
    if 'company_domain' in normalized_df.columns:
        normalized_df['company_domain'] = normalized_df['company_domain'].apply(clean_company_domain)
    
    return normalized_df

def clean_company_domain(domain: str) -> str:
    """Clean and normalize company domain"""
    if not domain:
        return ""
    
    # Remove common prefixes
    domain = domain.lower().strip()
    prefixes = ['http://', 'https://', 'www.']
    for prefix in prefixes:
        if domain.startswith(prefix):
            domain = domain[len(prefix):]
    
    # Remove trailing slashes and paths
    domain = domain.split('/')[0]
    
    return domain
