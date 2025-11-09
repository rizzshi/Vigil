"""
Algorzen Vigil - Streamlit Web Application
Algorzen Research Division © 2025 — Author Rishi Singh

Interactive web interface for drift detection and anomaly analysis.
"""

import streamlit as st
import pandas as pd
import os
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
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
    /* Table styling */
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
        font-size: 0.9em;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
    }
    table thead tr {
        background-color: #2c3e50;
        color: #ffffff;
        text-align: left;
    }
    table th,
    table td {
        padding: 12px 15px;
    }
    table tbody tr {
        border-bottom: 1px solid #dddddd;
    }
    table tbody tr:nth-of-type(even) {
        background-color: #f3f3f3;
    }
    table tbody tr:last-of-type {
        border-bottom: 2px solid #2c3e50;
    }
    table tbody tr:hover {
        background-color: #e8f4f8;
        cursor: pointer;
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
    
    st.sidebar.markdown("---")
    
    # Advanced Analytics Options
    st.sidebar.subheader("🔬 Advanced Analytics")
    
    show_correlation = st.sidebar.checkbox(
        "KPI Correlation Analysis",
        value=True,
        help="Show correlation heatmap between KPIs"
    )
    
    show_distribution = st.sidebar.checkbox(
        "Distribution Analysis",
        value=True,
        help="Show KPI distribution plots"
    )
    
    show_trend = st.sidebar.checkbox(
        "Trend Analysis",
        value=True,
        help="Show trend decomposition and forecasting"
    )
    
    show_comparison = st.sidebar.checkbox(
        "Period Comparison",
        value=False,
        help="Compare different time periods"
    )
    
    st.sidebar.markdown("---")
    
    # Data Filtering Options
    st.sidebar.subheader("🔍 Data Filtering")
    
    enable_date_filter = st.sidebar.checkbox(
        "Filter by Date Range",
        value=False,
        help="Analyze specific date range only"
    )
    
    enable_kpi_filter = st.sidebar.checkbox(
        "Select Specific KPIs",
        value=False,
        help="Analyze only selected KPIs"
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
            
            # Apply date filter if enabled
            if enable_date_filter and date_column in data.columns:
                data[date_column] = pd.to_datetime(data[date_column])
                min_date = data[date_column].min().date()
                max_date = data[date_column].max().date()
                
                st.sidebar.markdown("#### Date Range")
                date_range = st.sidebar.date_input(
                    "Select date range",
                    value=(min_date, max_date),
                    min_value=min_date,
                    max_value=max_date
                )
                
                if len(date_range) == 2:
                    data = data[(data[date_column].dt.date >= date_range[0]) & 
                               (data[date_column].dt.date <= date_range[1])]
                    st.sidebar.success(f"Filtered to {len(data)} records")
            
            # Apply KPI filter if enabled
            if enable_kpi_filter:
                numeric_cols = data.select_dtypes(include=['number']).columns.tolist()
                if numeric_cols:
                    st.sidebar.markdown("#### Select KPIs")
                    selected_kpis = st.sidebar.multiselect(
                        "Choose KPIs to analyze",
                        numeric_cols,
                        default=numeric_cols
                    )
                    
                    if selected_kpis:
                        # Keep date column and selected KPIs
                        cols_to_keep = [date_column] + selected_kpis if date_column in data.columns else selected_kpis
                        data = data[cols_to_keep]
                        st.sidebar.success(f"Analyzing {len(selected_kpis)} KPIs")
                    else:
                        st.sidebar.warning("Please select at least one KPI")
                        return
            
            # Display data preview
            st.subheader("📊 Data Preview")
            st.markdown(data.head(10).to_html(), unsafe_allow_html=True)
            
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
                        
                        # Show first 10 rows by default
                        st.markdown(details_df.head(10).to_html(index=False), unsafe_allow_html=True)
                        
                        # Add expander for remaining rows if there are more than 10
                        if len(details_df) > 10:
                            with st.expander(f"📊 View All {len(details_df)} Anomalies (Click to expand)"):
                                st.markdown(details_df.to_html(index=False), unsafe_allow_html=True)
                    
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
                st.markdown(kpi_stats.to_html(index=False), unsafe_allow_html=True)
                
                # Advanced Analytics Sections
                st.markdown("---")
                st.header("🔬 Advanced Analytics")
                
                # Correlation Analysis
                if show_correlation:
                    st.subheader("📈 KPI Correlation Analysis")
                    
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        # Calculate correlation matrix
                        numeric_data = data[detector.numeric_columns]
                        correlation_matrix = numeric_data.corr()
                        
                        # Create heatmap
                        fig, ax = plt.subplots(figsize=(10, 8))
                        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', 
                                   center=0, square=True, linewidths=1, 
                                   cbar_kws={"shrink": 0.8}, fmt='.2f', ax=ax)
                        plt.title('KPI Correlation Heatmap', fontsize=14, fontweight='bold', pad=20)
                        plt.tight_layout()
                        st.pyplot(fig)
                        plt.close()
                    
                    with col2:
                        st.markdown("### 🔍 Insights")
                        
                        # Find strong correlations
                        strong_corr = []
                        for i in range(len(correlation_matrix.columns)):
                            for j in range(i+1, len(correlation_matrix.columns)):
                                corr_value = correlation_matrix.iloc[i, j]
                                if abs(corr_value) > 0.7:
                                    strong_corr.append({
                                        'KPI 1': correlation_matrix.columns[i],
                                        'KPI 2': correlation_matrix.columns[j],
                                        'Correlation': f"{corr_value:.2f}"
                                    })
                        
                        if strong_corr:
                            st.success(f"Found {len(strong_corr)} strong correlations (|r| > 0.7)")
                            for corr in strong_corr:
                                st.write(f"**{corr['KPI 1']}** ↔ **{corr['KPI 2']}**: {corr['Correlation']}")
                        else:
                            st.info("No strong correlations found (|r| > 0.7)")
                
                # Distribution Analysis
                if show_distribution:
                    st.subheader("📊 Distribution Analysis")
                    
                    selected_kpi = st.selectbox(
                        "Select KPI to analyze",
                        detector.numeric_columns,
                        key="dist_kpi"
                    )
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Histogram
                        fig, ax = plt.subplots(figsize=(8, 5))
                        ax.hist(data[selected_kpi].dropna(), bins=30, 
                               color='#3498db', edgecolor='black', alpha=0.7)
                        ax.set_xlabel(selected_kpi, fontweight='bold')
                        ax.set_ylabel('Frequency', fontweight='bold')
                        ax.set_title(f'{selected_kpi} - Distribution', fontweight='bold')
                        ax.grid(alpha=0.3)
                        plt.tight_layout()
                        st.pyplot(fig)
                        plt.close()
                    
                    with col2:
                        # Box plot
                        fig, ax = plt.subplots(figsize=(8, 5))
                        ax.boxplot(data[selected_kpi].dropna(), vert=True)
                        ax.set_ylabel(selected_kpi, fontweight='bold')
                        ax.set_title(f'{selected_kpi} - Box Plot', fontweight='bold')
                        ax.grid(alpha=0.3, axis='y')
                        plt.tight_layout()
                        st.pyplot(fig)
                        plt.close()
                    
                    # Statistical summary
                    st.markdown("### 📐 Statistical Summary")
                    stats_cols = st.columns(5)
                    
                    stats_data = data[selected_kpi].describe()
                    stats_cols[0].metric("Mean", f"{stats_data['mean']:.2f}")
                    stats_cols[1].metric("Median", f"{data[selected_kpi].median():.2f}")
                    stats_cols[2].metric("Std Dev", f"{stats_data['std']:.2f}")
                    stats_cols[3].metric("Skewness", f"{data[selected_kpi].skew():.2f}")
                    stats_cols[4].metric("Kurtosis", f"{data[selected_kpi].kurtosis():.2f}")
                
                # Trend Analysis
                if show_trend:
                    st.subheader("📈 Trend Analysis & Decomposition")
                    
                    selected_trend_kpi = st.selectbox(
                        "Select KPI for trend analysis",
                        detector.numeric_columns,
                        key="trend_kpi"
                    )
                    
                    # Seasonal decomposition
                    decomp = detector.seasonal_analysis(selected_trend_kpi, period=7)
                    
                    if decomp.get('trend') is not None:
                        fig, axes = plt.subplots(4, 1, figsize=(12, 10))
                        
                        # Original
                        axes[0].plot(data[date_column], data[selected_trend_kpi], color='#2c3e50', linewidth=2)
                        axes[0].set_title('Original Time Series', fontweight='bold')
                        axes[0].grid(alpha=0.3)
                        
                        # Trend
                        axes[1].plot(decomp['trend'], color='#e74c3c', linewidth=2)
                        axes[1].set_title('Trend Component', fontweight='bold')
                        axes[1].grid(alpha=0.3)
                        
                        # Seasonal
                        axes[2].plot(decomp['seasonal'], color='#3498db', linewidth=2)
                        axes[2].set_title('Seasonal Component', fontweight='bold')
                        axes[2].grid(alpha=0.3)
                        
                        # Residual
                        axes[3].plot(decomp['residual'], color='#2ecc71', linewidth=2)
                        axes[3].set_title('Residual Component', fontweight='bold')
                        axes[3].grid(alpha=0.3)
                        
                        plt.tight_layout()
                        st.pyplot(fig)
                        plt.close()
                    else:
                        st.warning(decomp.get('message', 'Could not perform seasonal decomposition'))
                
                # Period Comparison
                if show_comparison:
                    st.subheader("⚖️ Period Comparison")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        comparison_kpi = st.selectbox(
                            "Select KPI to compare",
                            detector.numeric_columns,
                            key="comp_kpi"
                        )
                    
                    with col2:
                        split_point = st.slider(
                            "Split point (%)",
                            min_value=20,
                            max_value=80,
                            value=50,
                            help="Percentage of data for first period"
                        )
                    
                    # Split data
                    split_idx = int(len(data) * split_point / 100)
                    period1 = data[comparison_kpi].iloc[:split_idx]
                    period2 = data[comparison_kpi].iloc[split_idx:]
                    
                    # Comparison metrics
                    comp_cols = st.columns(4)
                    
                    mean_change = ((period2.mean() - period1.mean()) / period1.mean()) * 100
                    std_change = ((period2.std() - period1.std()) / period1.std()) * 100
                    
                    comp_cols[0].metric("Period 1 Mean", f"{period1.mean():.2f}")
                    comp_cols[1].metric("Period 2 Mean", f"{period2.mean():.2f}", 
                                       delta=f"{mean_change:+.1f}%")
                    comp_cols[2].metric("Period 1 Std", f"{period1.std():.2f}")
                    comp_cols[3].metric("Period 2 Std", f"{period2.std():.2f}", 
                                       delta=f"{std_change:+.1f}%")
                    
                    # Comparison chart
                    fig, ax = plt.subplots(figsize=(12, 5))
                    ax.plot(data[date_column].iloc[:split_idx], period1, 
                           label='Period 1', color='#3498db', linewidth=2, alpha=0.7)
                    ax.plot(data[date_column].iloc[split_idx:], period2, 
                           label='Period 2', color='#e74c3c', linewidth=2, alpha=0.7)
                    ax.axvline(x=data[date_column].iloc[split_idx], 
                              color='gray', linestyle='--', linewidth=2, label='Split Point')
                    ax.set_xlabel('Date', fontweight='bold')
                    ax.set_ylabel(comparison_kpi, fontweight='bold')
                    ax.set_title(f'{comparison_kpi} - Period Comparison', fontweight='bold')
                    ax.legend()
                    ax.grid(alpha=0.3)
                    plt.xticks(rotation=45)
                    plt.tight_layout()
                    st.pyplot(fig)
                    plt.close()
                
                # Generate Report button
                st.subheader("📄 Generate PDF Report")
                
                # Export options
                export_cols = st.columns(3)
                
                with export_cols[0]:
                    if st.button("📥 Export Anomalies (CSV)", use_container_width=True):
                        if anomaly_summary['details']:
                            export_df = pd.DataFrame(anomaly_summary['details'])
                            csv = export_df.to_csv(index=False)
                            st.download_button(
                                label="Download CSV",
                                data=csv,
                                file_name=f"anomalies_{datetime.now().strftime('%Y%m%d')}.csv",
                                mime="text/csv",
                                use_container_width=True
                            )
                        else:
                            st.warning("No anomalies to export")
                
                with export_cols[1]:
                    if st.button("📊 Export KPI Stats (CSV)", use_container_width=True):
                        csv = kpi_stats.to_csv(index=False)
                        st.download_button(
                            label="Download CSV",
                            data=csv,
                            file_name=f"kpi_stats_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                
                with export_cols[2]:
                    if st.button("📋 Export Full Report (JSON)", use_container_width=True):
                        report_json = {
                            "generated_at": datetime.now().isoformat(),
                            "anomaly_summary": {
                                "total": anomaly_summary['total_anomalies'],
                                "severity": anomaly_summary['severity'],
                                "affected_kpis": anomaly_summary['affected_kpis']
                            },
                            "narrative": narrative,
                            "anomalies": anomaly_summary['details']
                        }
                        import json
                        json_str = json.dumps(report_json, indent=2, default=str)
                        st.download_button(
                            label="Download JSON",
                            data=json_str,
                            file_name=f"vigil_report_{datetime.now().strftime('%Y%m%d')}.json",
                            mime="application/json",
                            use_container_width=True
                        )
                
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
