"""
Algorzen Vigil - Streamlit Web Application
Algorzen Research Division © 2025 — Author Rishi Singh

Interactive web interface for drift detection and anomaly analysis.
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime
from drift_detector import DriftDetector
from anomaly_explainer import AnomalyExplainer
from report_generator import ReportGenerator


# Page configuration
st.set_page_config(
    page_title="Algorzen Vigil - AI Drift Detection",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #7f8c8d;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        border-left: 4px solid #3498db;
    }
    .footer {
        text-align: center;
        color: #888888;
        font-size: 0.9rem;
        margin-top: 3rem;
        padding: 1rem;
        border-top: 1px solid #ddd;
    }
    </style>
""", unsafe_allow_html=True)


def display_header():
    """Display application header."""
    st.markdown('<div class="main-header">🧠 Algorzen Vigil</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">AI Drift Detection & Anomaly Monitoring Engine<br>Algorzen Research Division © 2025 — Author Rishi Singh</div>', unsafe_allow_html=True)


def display_footer():
    """Display application footer."""
    st.markdown('<div class="footer">Algorzen Research Division © 2025 — Author Rishi Singh<br>Project Drop 002 — AI Drift Detection Engine</div>', unsafe_allow_html=True)


def main():
    """Main Streamlit application."""
    
    display_header()
    
    # Sidebar configuration
    st.sidebar.title("⚙️ Configuration")
    
    # File upload
    uploaded_file = st.sidebar.file_uploader(
        "Upload KPI Data (CSV)",
        type=['csv'],
        help="Upload a CSV file containing time-series KPI data with a date column"
    )
    
    # Detection parameters
    st.sidebar.subheader("Detection Parameters")
    
    zscore_threshold = st.sidebar.slider(
        "Z-Score Threshold",
        min_value=1.0,
        max_value=5.0,
        value=3.0,
        step=0.1,
        help="Number of standard deviations for outlier detection"
    )
    
    rolling_window = st.sidebar.slider(
        "Rolling Window (days)",
        min_value=3,
        max_value=30,
        value=7,
        step=1,
        help="Window size for rolling deviation calculation"
    )
    
    deviation_threshold = st.sidebar.slider(
        "Deviation Threshold (%)",
        min_value=10,
        max_value=50,
        value=25,
        step=5,
        help="Percentage deviation threshold"
    ) / 100.0
    
    date_column = st.sidebar.text_input(
        "Date Column Name",
        value="date",
        help="Name of the date/timestamp column in your CSV"
    )
    
    use_openai = st.sidebar.checkbox(
        "Use OpenAI GPT-4",
        value=False,
        help="Enable AI-powered explanations (requires OPENAI_API_KEY)"
    )
    
    # Main content area
    if uploaded_file is None:
        # Welcome screen
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.info("👈 Upload a CSV file to begin analysis")
            
            st.subheader("Features")
            st.markdown("""
            - **🎯 Multi-Method Detection**: Z-score and rolling deviation analysis
            - **📊 Interactive Visualizations**: Time-series charts with anomaly highlights
            - **🤖 AI-Powered Insights**: GPT-4 driven executive summaries
            - **📄 Professional Reports**: Branded PDF reports with metadata
            - **📈 KPI Statistics**: Comprehensive statistical analysis
            """)
            
            st.subheader("Quick Start")
            st.markdown("""
            1. Upload your CSV file (must contain a date column)
            2. Configure detection parameters in the sidebar
            3. Click **Analyze Data** to run the detection engine
            4. Review findings and generate PDF report
            """)
            
            st.subheader("Sample Data Format")
            st.code("""
date,revenue,customer_acquisition,churn_rate
2024-01-01,125000,450,2.1
2024-01-02,128000,465,2.0
2024-01-03,130000,472,1.9
            """, language="csv")
    
    else:
        # Data uploaded - show analysis interface
        try:
            # Load data
            data = pd.read_csv(uploaded_file)
            
            # Display data preview
            st.subheader("📊 Data Preview")
            st.write(data.head(10))
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Records", len(data))
            with col2:
                st.metric("Columns", len(data.columns))
            with col3:
                numeric_cols = data.select_dtypes(include=['number']).columns
                st.metric("Numeric KPIs", len(numeric_cols))
            
            # Analyze button
            if st.button("🎯 Analyze Data", type="primary", use_container_width=True):
                
                with st.spinner("Running drift detection analysis..."):
                    
                    # Initialize detector
                    detector = DriftDetector(data, date_column=date_column)
                    
                    # Run detection
                    progress_bar = st.progress(0)
                    st.text("Running Z-score detection...")
                    
                    zscore_outliers = detector.detect_zscore_outliers(threshold=zscore_threshold)
                    progress_bar.progress(33)
                    
                    st.text("Running rolling deviation detection...")
                    rolling_anomalies = detector.detect_rolling_deviation(
                        window=rolling_window,
                        threshold=deviation_threshold
                    )
                    progress_bar.progress(66)
                    
                    st.text("Generating summary...")
                    anomaly_summary = detector.generate_anomaly_summary()
                    kpi_stats = detector.get_kpi_statistics()
                    progress_bar.progress(100)
                    
                    st.success("✅ Analysis complete!")
                
                # Display results
                st.subheader("🎯 Analysis Results")
                
                # Metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        "Total Anomalies",
                        anomaly_summary['total_anomalies'],
                        delta=None
                    )
                
                with col2:
                    severity_color = {
                        'None': '🟢',
                        'Low': '🟡',
                        'Medium': '🟠',
                        'High': '🔴'
                    }
                    st.metric(
                        "Severity",
                        f"{severity_color.get(anomaly_summary['severity'], '⚪')} {anomaly_summary['severity']}",
                        delta=None
                    )
                
                with col3:
                    st.metric(
                        "Affected KPIs",
                        len(anomaly_summary['affected_kpis']),
                        delta=None
                    )
                
                with col4:
                    st.metric(
                        "Detection Methods",
                        len(anomaly_summary['by_method']),
                        delta=None
                    )
                
                # Anomaly details
                if anomaly_summary['total_anomalies'] > 0:
                    st.subheader("📋 Anomaly Details")
                    
                    # Create DataFrame from details
                    details_df = pd.DataFrame(anomaly_summary['details'])
                    if not details_df.empty:
                        # Format the dataframe
                        details_df['date'] = pd.to_datetime(details_df['date']).dt.strftime('%Y-%m-%d')
                        st.write(details_df)
                    
                    # Visualizations
                    st.subheader("📈 Visualizations")
                    
                    report_gen = ReportGenerator(output_dir="reports")
                    
                    # Summary chart
                    summary_chart_path = report_gen.create_anomaly_summary_chart(anomaly_summary)
                    if os.path.exists(summary_chart_path):
                        st.image(summary_chart_path, use_column_width=True)
                    
                    # Time-series charts
                    for kpi in anomaly_summary['affected_kpis'][:3]:
                        st.subheader(f"Time Series: {kpi}")
                        
                        # Get anomaly indices
                        anomaly_indices = []
                        for detail in anomaly_summary['details']:
                            if detail['kpi'] == kpi:
                                idx = data[data[date_column] == detail['date']].index
                                if len(idx) > 0:
                                    anomaly_indices.append(idx[0])
                        
                        if anomaly_indices:
                            chart_path = report_gen.create_time_series_chart(
                                data, kpi, anomaly_indices, date_column=date_column
                            )
                            if os.path.exists(chart_path):
                                st.image(chart_path, use_column_width=True)
                
                # AI Explanations
                st.subheader("🤖 AI Analysis")
                
                with st.spinner("Generating AI explanations..."):
                    explainer = AnomalyExplainer(use_openai=use_openai)
                    narrative = explainer.generate_full_report_narrative(
                        anomaly_summary,
                        kpi_stats.to_dict('records')
                    )
                
                # Display narrative sections
                st.markdown("### Executive Summary")
                st.info(narrative['executive_summary'])
                
                st.markdown("### Key Findings")
                st.write(narrative['key_findings'])
                
                st.markdown("### Recommendations")
                st.write(narrative['recommendations'])
                
                # KPI Statistics
                st.subheader("📊 KPI Statistics")
                st.dataframe(kpi_stats, use_container_width=True)
                
                # Generate Report button
                st.subheader("📄 Generate PDF Report")
                
                if st.button("Generate PDF Report", type="primary", use_container_width=True):
                    
                    with st.spinner("Generating PDF report..."):
                        # Create charts
                        charts = []
                        
                        summary_chart = report_gen.create_anomaly_summary_chart(anomaly_summary)
                        if os.path.exists(summary_chart):
                            charts.append(summary_chart)
                        
                        for kpi in anomaly_summary['affected_kpis'][:3]:
                            anomaly_indices = []
                            for detail in anomaly_summary['details']:
                                if detail['kpi'] == kpi:
                                    idx = data[data[date_column] == detail['date']].index
                                    if len(idx) > 0:
                                        anomaly_indices.append(idx[0])
                            
                            if anomaly_indices:
                                chart_path = report_gen.create_time_series_chart(
                                    data, kpi, anomaly_indices, date_column=date_column
                                )
                                if os.path.exists(chart_path):
                                    charts.append(chart_path)
                        
                        # Generate PDF
                        report_path = report_gen.generate_pdf_report(
                            data=data,
                            anomaly_summary=anomaly_summary,
                            narrative=narrative,
                            kpi_stats=kpi_stats,
                            charts=charts,
                            use_openai=use_openai
                        )
                    
                    st.success(f"✅ Report generated: {report_path}")
                    
                    # Download button
                    if os.path.exists(report_path):
                        with open(report_path, 'rb') as f:
                            st.download_button(
                                label="📥 Download PDF Report",
                                data=f,
                                file_name=os.path.basename(report_path),
                                mime="application/pdf",
                                use_container_width=True
                            )
        
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
            st.exception(e)
    
    # Footer
    display_footer()


if __name__ == "__main__":
    main()
