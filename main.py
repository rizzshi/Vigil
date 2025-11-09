#!/usr/bin/env python3
"""
Algorzen Vigil - Main Entry Point
Algorzen Research Division © 2025 — Author Rishi Singh

AI Drift Detection & Anomaly Monitoring Engine
Command-line interface for running complete analysis pipeline.
"""

import argparse
import sys
import os
from datetime import datetime
from drift_detector import DriftDetector, load_kpi_data
from anomaly_explainer import AnomalyExplainer
from report_generator import ReportGenerator


def main():
    """Main execution function."""
    
    # Display banner
    print("=" * 70)
    print("🧠 Algorzen Vigil - AI Drift Detection Engine")
    print("Algorzen Research Division © 2025 — Author Rishi Singh")
    print("Project Drop 002 — Anomaly Monitoring & Analytics")
    print("=" * 70)
    print()
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Algorzen Vigil: AI-powered drift detection and anomaly monitoring",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --input data/sample_kpi_data.csv
  %(prog)s --input data/sample_kpi_data.csv --use-openai
  %(prog)s --input mydata.csv --zscore-threshold 2.5 --output-dir custom_reports

For more information, visit: https://github.com/algorzen/vigil
        """
    )
    
    parser.add_argument(
        '--input', '-i',
        type=str,
        required=True,
        help='Path to input CSV file containing KPI time-series data'
    )
    
    parser.add_argument(
        '--output-dir', '-o',
        type=str,
        default='reports',
        help='Directory to save generated reports (default: reports)'
    )
    
    parser.add_argument(
        '--use-openai',
        action='store_true',
        help='Use OpenAI GPT-4 for AI-powered explanations (requires OPENAI_API_KEY)'
    )
    
    parser.add_argument(
        '--zscore-threshold',
        type=float,
        default=3.0,
        help='Z-score threshold for outlier detection (default: 3.0)'
    )
    
    parser.add_argument(
        '--rolling-window',
        type=int,
        default=7,
        help='Rolling window size for deviation detection (default: 7)'
    )
    
    parser.add_argument(
        '--deviation-threshold',
        type=float,
        default=0.25,
        help='Deviation threshold percentage (default: 0.25 = 25%%)'
    )
    
    parser.add_argument(
        '--date-column',
        type=str,
        default='date',
        help='Name of the date column in CSV (default: date)'
    )
    
    parser.add_argument(
        '--report-id',
        type=str,
        default=None,
        help='Custom report ID (auto-generated if not provided)'
    )
    
    args = parser.parse_args()
    
    # Validate input file
    if not os.path.exists(args.input):
        print(f"❌ Error: Input file not found: {args.input}")
        sys.exit(1)
    
    try:
        # Step 1: Load data
        print(f"📂 Loading KPI data from: {args.input}")
        data = load_kpi_data(args.input)
        print(f"✅ Loaded {len(data)} records with {len(data.columns)} columns")
        print()
        
        # Step 2: Initialize drift detector
        print("🔍 Initializing drift detection system...")
        detector = DriftDetector(data, date_column=args.date_column)
        print(f"✅ Monitoring {len(detector.numeric_columns)} KPIs: {', '.join(detector.numeric_columns)}")
        print()
        
        # Step 3: Run anomaly detection
        print(f"🎯 Running Z-score outlier detection (threshold: {args.zscore_threshold}σ)...")
        zscore_outliers = detector.detect_zscore_outliers(threshold=args.zscore_threshold)
        zscore_count = sum(len(df) for df in zscore_outliers.values())
        print(f"✅ Found {zscore_count} Z-score outliers")
        
        print(f"🎯 Running rolling deviation detection (window: {args.rolling_window}, threshold: {args.deviation_threshold*100}%)...")
        rolling_anomalies = detector.detect_rolling_deviation(
            window=args.rolling_window,
            threshold=args.deviation_threshold
        )
        rolling_count = sum(len(df) for df in rolling_anomalies.values())
        print(f"✅ Found {rolling_count} rolling deviation anomalies")
        print()
        
        # Step 4: Generate anomaly summary
        print("📊 Generating anomaly summary...")
        anomaly_summary = detector.generate_anomaly_summary()
        print(f"✅ Total anomalies: {anomaly_summary['total_anomalies']}")
        print(f"   Severity: {anomaly_summary['severity']}")
        print(f"   Affected KPIs: {', '.join(anomaly_summary['affected_kpis']) if anomaly_summary['affected_kpis'] else 'None'}")
        print()
        
        # Step 5: Get KPI statistics
        print("📈 Calculating KPI statistics...")
        kpi_stats = detector.get_kpi_statistics()
        print(f"✅ Generated statistics for {len(kpi_stats)} KPIs")
        print()
        
        # Step 6: Generate AI explanations
        print(f"🤖 Generating {'AI-powered (GPT-4)' if args.use_openai else 'heuristic-based'} explanations...")
        explainer = AnomalyExplainer(use_openai=args.use_openai)
        narrative = explainer.generate_full_report_narrative(
            anomaly_summary,
            kpi_stats.to_dict('records')
        )
        print("✅ Generated executive summary, key findings, and recommendations")
        print()
        
        # Step 7: Generate visualizations
        print("📊 Creating visualizations...")
        report_gen = ReportGenerator(output_dir=args.output_dir)
        charts = []
        
        # Create anomaly summary chart
        summary_chart_path = report_gen.create_anomaly_summary_chart(anomaly_summary)
        if os.path.exists(summary_chart_path):
            charts.append(summary_chart_path)
            print(f"✅ Created anomaly summary chart")
        
        # Create time-series charts for KPIs with anomalies
        for kpi in anomaly_summary['affected_kpis'][:3]:  # Limit to first 3 KPIs
            # Get anomaly indices for this KPI
            anomaly_indices = []
            for detail in anomaly_summary['details']:
                if detail['kpi'] == kpi:
                    # Find the index in the original data
                    idx = data[data[args.date_column] == detail['date']].index
                    if len(idx) > 0:
                        anomaly_indices.append(idx[0])
            
            if anomaly_indices:
                chart_path = report_gen.create_time_series_chart(
                    data, kpi, anomaly_indices, date_column=args.date_column
                )
                if os.path.exists(chart_path):
                    charts.append(chart_path)
                    print(f"✅ Created time-series chart for {kpi}")
        print()
        
        # Step 8: Generate PDF report
        print("📄 Generating PDF report...")
        report_path = report_gen.generate_pdf_report(
            data=data,
            anomaly_summary=anomaly_summary,
            narrative=narrative,
            kpi_stats=kpi_stats,
            charts=charts,
            report_id=args.report_id,
            use_openai=args.use_openai
        )
        print(f"✅ Report generated: {report_path}")
        print()
        
        # Display summary
        print("=" * 70)
        print("✨ Analysis Complete!")
        print("=" * 70)
        print(f"📊 Total Anomalies: {anomaly_summary['total_anomalies']}")
        print(f"⚠️  Severity Level: {anomaly_summary['severity']}")
        print(f"📈 KPIs Analyzed: {len(detector.numeric_columns)}")
        print(f"📄 Report Location: {report_path}")
        print(f"📋 Metadata: {os.path.join(args.output_dir, 'report_metadata.json')}")
        print()
        print("Executive Summary:")
        print("-" * 70)
        print(narrative['executive_summary'])
        print()
        print("=" * 70)
        print("🧠 Algorzen Research Division — Powering Data Intelligence")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error during execution: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
