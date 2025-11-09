"""
Algorzen Vigil - Report Generator Module
Algorzen Research Division © 2025 — Author Rishi Singh

This module generates professional PDF reports with Algorzen branding.
Includes charts, tables, narrative text, and metadata export.
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, 
    Spacer, PageBreak, Image, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

# Set matplotlib style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)


class ReportGenerator:
    """
    Generates branded PDF reports for anomaly detection results.
    
    Features:
        - Algorzen Research Division branding
        - Time-series visualizations with anomaly highlights
        - Executive narrative sections
        - KPI statistics tables
        - Metadata JSON export
    """
    
    def __init__(self, output_dir: str = "reports"):
        """
        Initialize the report generator.
        
        Args:
            output_dir: Directory to save generated reports
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Initialize styles
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
    
    def _create_custom_styles(self):
        """Create custom paragraph styles for the report."""
        # Title style
        self.styles.add(ParagraphStyle(
            name='AlgorzenTitle',
            parent=self.styles['Title'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='AlgorzenSubtitle',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#666666'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica'
        ))
        
        # Section heading style
        self.styles.add(ParagraphStyle(
            name='AlgorzenHeading',
            parent=self.styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=20,
            fontName='Helvetica-Bold'
        ))
        
        # Body text style
        self.styles.add(ParagraphStyle(
            name='AlgorzenBody',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#333333'),
            alignment=TA_JUSTIFY,
            spaceAfter=12,
            leading=16,
            fontName='Helvetica'
        ))
        
        # Footer style
        self.styles.add(ParagraphStyle(
            name='AlgorzenFooter',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#888888'),
            alignment=TA_CENTER,
            fontName='Helvetica'
        ))
    
    def _add_header_footer(self, canvas, doc):
        """Add header and footer to each page."""
        canvas.saveState()
        
        # Header
        canvas.setFont('Helvetica-Bold', 10)
        canvas.drawString(inch, letter[1] - 0.5 * inch, "Algorzen Research Division")
        
        # Footer
        canvas.setFont('Helvetica', 8)
        footer_text = "Algorzen Research Division © 2025 — Author Rishi Singh"
        canvas.drawCentredString(letter[0] / 2, 0.5 * inch, footer_text)
        canvas.drawCentredString(letter[0] / 2, 0.35 * inch, f"Page {doc.page}")
        
        canvas.restoreState()
    
    def create_time_series_chart(
        self, 
        data: pd.DataFrame, 
        column: str,
        anomaly_indices: List[int] = None,
        date_column: str = 'date',
        output_path: str = None
    ) -> str:
        """
        Create a time-series chart with anomaly highlights.
        
        Args:
            data: DataFrame containing the time-series data
            column: Name of the column to plot
            anomaly_indices: Indices of anomaly points to highlight
            date_column: Name of the date column
            output_path: Path to save the chart (auto-generated if None)
            
        Returns:
            Path to the saved chart image
        """
        fig, ax = plt.subplots(figsize=(10, 5))
        
        # Plot main time series
        ax.plot(data[date_column], data[column], 
               linewidth=2, label=column, color='#2c3e50', alpha=0.8)
        
        # Highlight anomalies
        if anomaly_indices and len(anomaly_indices) > 0:
            anomaly_data = data.iloc[anomaly_indices]
            ax.scatter(anomaly_data[date_column], anomaly_data[column],
                      color='red', s=100, zorder=5, label='Anomalies', alpha=0.7)
        
        # Styling
        ax.set_xlabel('Date', fontsize=11, fontweight='bold')
        ax.set_ylabel(column.replace('_', ' ').title(), fontsize=11, fontweight='bold')
        ax.set_title(f'{column.replace("_", " ").title()} - Time Series Analysis', 
                    fontsize=13, fontweight='bold', pad=15)
        ax.legend(loc='best', frameon=True, shadow=True)
        ax.grid(True, alpha=0.3)
        
        # Rotate x-axis labels
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        # Save chart
        if output_path is None:
            output_path = os.path.join(self.output_dir, f'chart_{column}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
        
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return output_path
    
    def create_anomaly_summary_chart(
        self,
        anomaly_summary: Dict,
        output_path: str = None
    ) -> str:
        """
        Create a summary chart showing anomaly distribution.
        
        Args:
            anomaly_summary: Summary dictionary from DriftDetector
            output_path: Path to save the chart
            
        Returns:
            Path to the saved chart image
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Chart 1: Anomalies by KPI
        if anomaly_summary['affected_kpis']:
            kpis = anomaly_summary['affected_kpis']
            counts = []
            
            for kpi in kpis:
                count = sum(1 for d in anomaly_summary['details'] if d['kpi'] == kpi)
                counts.append(count)
            
            ax1.barh(kpis, counts, color='#e74c3c', alpha=0.7)
            ax1.set_xlabel('Number of Anomalies', fontweight='bold')
            ax1.set_ylabel('KPI', fontweight='bold')
            ax1.set_title('Anomalies by KPI', fontweight='bold', pad=15)
            ax1.grid(axis='x', alpha=0.3)
        
        # Chart 2: Anomalies by Detection Method
        if anomaly_summary['by_method']:
            methods = list(anomaly_summary['by_method'].keys())
            method_counts = list(anomaly_summary['by_method'].values())
            
            colors_map = ['#3498db', '#2ecc71']
            ax2.pie(method_counts, labels=[m.replace('_', ' ').title() for m in methods],
                   autopct='%1.1f%%', startangle=90, colors=colors_map)
            ax2.set_title('Anomalies by Detection Method', fontweight='bold', pad=15)
        
        plt.tight_layout()
        
        # Save chart
        if output_path is None:
            output_path = os.path.join(self.output_dir, f'anomaly_summary_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
        
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return output_path
    
    def create_correlation_heatmap(self, data: pd.DataFrame, numeric_columns: List[str], output_path: str = None) -> str:
        """Create correlation heatmap for KPIs."""
        numeric_data = data[numeric_columns]
        correlation_matrix = numeric_data.corr()
        
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', 
                   center=0, square=True, linewidths=1, 
                   cbar_kws={"shrink": 0.8}, fmt='.2f', ax=ax)
        plt.title('KPI Correlation Heatmap', fontsize=14, fontweight='bold', pad=20)
        plt.tight_layout()
        
        if output_path is None:
            output_path = os.path.join(self.output_dir, f'correlation_heatmap_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
        
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return output_path
    
    def create_distribution_analysis(self, data: pd.DataFrame, kpi: str, output_path: str = None) -> str:
        """Create distribution analysis charts (histogram and box plot)."""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
        
        # Histogram
        ax1.hist(data[kpi].dropna(), bins=30, color='#3498db', edgecolor='black', alpha=0.7)
        ax1.set_xlabel(kpi, fontweight='bold')
        ax1.set_ylabel('Frequency', fontweight='bold')
        ax1.set_title(f'{kpi} - Distribution', fontweight='bold')
        ax1.grid(alpha=0.3)
        
        # Box plot
        ax2.boxplot(data[kpi].dropna(), vert=True)
        ax2.set_ylabel(kpi, fontweight='bold')
        ax2.set_title(f'{kpi} - Box Plot', fontweight='bold')
        ax2.grid(alpha=0.3, axis='y')
        
        plt.tight_layout()
        
        if output_path is None:
            output_path = os.path.join(self.output_dir, f'distribution_{kpi}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
        
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return output_path
    
    def create_trend_decomposition(self, data: pd.DataFrame, date_column: str, kpi: str, 
                                   decomp: Dict, output_path: str = None) -> str:
        """Create seasonal decomposition chart."""
        fig, axes = plt.subplots(4, 1, figsize=(12, 10))
        
        # Original
        axes[0].plot(data[date_column], data[kpi], color='#2c3e50', linewidth=2)
        axes[0].set_title('Original Time Series', fontweight='bold')
        axes[0].grid(alpha=0.3)
        axes[0].set_ylabel(kpi)
        
        # Trend
        axes[1].plot(decomp['trend'], color='#e74c3c', linewidth=2)
        axes[1].set_title('Trend Component', fontweight='bold')
        axes[1].grid(alpha=0.3)
        axes[1].set_ylabel('Trend')
        
        # Seasonal
        axes[2].plot(decomp['seasonal'], color='#3498db', linewidth=2)
        axes[2].set_title('Seasonal Component', fontweight='bold')
        axes[2].grid(alpha=0.3)
        axes[2].set_ylabel('Seasonal')
        
        # Residual
        axes[3].plot(decomp['residual'], color='#2ecc71', linewidth=2)
        axes[3].set_title('Residual Component', fontweight='bold')
        axes[3].grid(alpha=0.3)
        axes[3].set_ylabel('Residual')
        axes[3].set_xlabel('Time')
        
        plt.tight_layout()
        
        if output_path is None:
            output_path = os.path.join(self.output_dir, f'trend_decomp_{kpi}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
        
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return output_path
    
    def generate_pdf_report(
        self,
        data: pd.DataFrame,
        anomaly_summary: Dict,
        narrative: Dict[str, str],
        kpi_stats: pd.DataFrame,
        charts: List[str] = None,
        report_id: str = None,
        use_openai: bool = False,
        detector = None,
        date_column: str = 'date'
    ) -> str:
        """
        Generate the complete PDF report.
        
        Args:
            data: Original KPI data
            anomaly_summary: Summary of detected anomalies
            narrative: Dictionary with executive_summary, key_findings, recommendations
            kpi_stats: DataFrame with KPI statistics
            charts: List of chart image paths to include
            report_id: Custom report ID (auto-generated if None)
            use_openai: Whether OpenAI was used for analysis
            detector: DriftDetector instance for advanced analytics
            date_column: Name of the date column
            
        Returns:
            Path to the generated PDF report
        """
        # Generate report filename with timestamp to avoid overwriting
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"Vigil_Report_{timestamp}.pdf"
        report_path = os.path.join(self.output_dir, report_filename)
        
        # Generate report ID
        if report_id is None:
            quarter = (datetime.now().month - 1) // 3 + 1
            report_id = f"VIGIL-{datetime.now().year}-Q{quarter}-{datetime.now().strftime('%m%d')}"
        
        # Create PDF document
        doc = SimpleDocTemplate(
            report_path,
            pagesize=letter,
            rightMargin=inch,
            leftMargin=inch,
            topMargin=inch,
            bottomMargin=inch
        )
        
        # Build story (content)
        story = []
        
        # Title Page
        story.append(Spacer(1, 1.5 * inch))
        story.append(Paragraph("Algorzen Vigil", self.styles['AlgorzenTitle']))
        story.append(Paragraph("AI Drift Detection & Anomaly Monitoring Report", self.styles['AlgorzenSubtitle']))
        story.append(Spacer(1, 0.5 * inch))
        
        # Report metadata
        meta_data = [
            ['Report ID:', report_id],
            ['Generated:', datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            ['Analysis Period:', f"{data['date'].min()} to {data['date'].max()}"],
            ['Total KPIs Monitored:', str(len(kpi_stats))],
            ['AI-Powered Analysis:', 'Yes (GPT-4)' if use_openai else 'No (Heuristic)']
        ]
        
        meta_table = Table(meta_data, colWidths=[2*inch, 3.5*inch])
        meta_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 10),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#2c3e50')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.HexColor('#dddddd')),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(meta_table)
        story.append(PageBreak())
        
        # Executive Summary
        story.append(Paragraph("Executive Summary", self.styles['AlgorzenHeading']))
        story.append(Paragraph(narrative.get('executive_summary', 'No summary available.'), 
                             self.styles['AlgorzenBody']))
        story.append(Spacer(1, 0.3 * inch))
        
        # Anomaly Overview
        story.append(Paragraph("Anomaly Overview", self.styles['AlgorzenHeading']))
        overview_data = [
            ['Metric', 'Value'],
            ['Total Anomalies Detected', str(anomaly_summary['total_anomalies'])],
            ['Severity Level', anomaly_summary['severity']],
            ['Affected KPIs', ', '.join(anomaly_summary['affected_kpis'][:3]) + 
             ('...' if len(anomaly_summary['affected_kpis']) > 3 else '')],
            ['Detection Methods Used', ', '.join(k.replace('_', ' ').title() for k in anomaly_summary['by_method'].keys())]
        ]
        
        overview_table = Table(overview_data, colWidths=[2.5*inch, 3*inch])
        overview_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 11),
            ('FONT', (0, 1), (-1, -1), 'Helvetica', 10),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dddddd')),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(overview_table)
        story.append(Spacer(1, 0.3 * inch))
        
        # Key Findings
        story.append(Paragraph("Key Findings", self.styles['AlgorzenHeading']))
        findings_text = narrative.get('key_findings', 'No findings available.')
        for line in findings_text.split('\n'):
            if line.strip():
                story.append(Paragraph(line, self.styles['AlgorzenBody']))
        story.append(Spacer(1, 0.3 * inch))
        
        # Recommendations
        story.append(Paragraph("Recommendations", self.styles['AlgorzenHeading']))
        recommendations_text = narrative.get('recommendations', 'No recommendations available.')
        for line in recommendations_text.split('\n'):
            if line.strip():
                story.append(Paragraph(line, self.styles['AlgorzenBody']))
        
        story.append(PageBreak())
        
        # KPI Statistics
        story.append(Paragraph("KPI Statistics Summary", self.styles['AlgorzenHeading']))
        
        # Convert DataFrame to table data
        stats_data = [kpi_stats.columns.tolist()] + kpi_stats.round(2).values.tolist()
        stats_table = Table(stats_data, colWidths=[1.5*inch, 1*inch, 1*inch, 1*inch, 1*inch, 0.8*inch])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 9),
            ('FONT', (0, 1), (-1, -1), 'Helvetica', 8),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dddddd')),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        story.append(stats_table)
        story.append(Spacer(1, 0.3 * inch))
        
        # Advanced Analytics Section
        if detector is not None:
            story.append(PageBreak())
            story.append(Paragraph("Advanced Analytics", self.styles['AlgorzenHeading']))
            story.append(Spacer(1, 0.2 * inch))
            
            # Correlation Analysis
            story.append(Paragraph("Correlation Analysis", self.styles['AlgorzenSubheading']))
            try:
                corr_chart = self.create_correlation_heatmap(data, detector.numeric_columns)
                if os.path.exists(corr_chart):
                    img = Image(corr_chart, width=6*inch, height=4.5*inch)
                    story.append(img)
                    story.append(Spacer(1, 0.2 * inch))
                    
                    # Find strong correlations
                    numeric_data = data[detector.numeric_columns]
                    correlation_matrix = numeric_data.corr()
                    strong_corr = []
                    for i in range(len(correlation_matrix.columns)):
                        for j in range(i+1, len(correlation_matrix.columns)):
                            corr_value = correlation_matrix.iloc[i, j]
                            if abs(corr_value) > 0.7:
                                strong_corr.append(f"• {correlation_matrix.columns[i]} ↔ {correlation_matrix.columns[j]}: {corr_value:.2f}")
                    
                    if strong_corr:
                        story.append(Paragraph(f"<b>Strong Correlations Found (|r| > 0.7):</b>", self.styles['AlgorzenBody']))
                        for corr_text in strong_corr[:5]:  # Limit to top 5
                            story.append(Paragraph(corr_text, self.styles['AlgorzenBody']))
                    else:
                        story.append(Paragraph("No strong correlations found (|r| > 0.7)", self.styles['AlgorzenBody']))
                    
                    story.append(Spacer(1, 0.3 * inch))
            except Exception as e:
                story.append(Paragraph(f"Could not generate correlation analysis: {str(e)}", self.styles['AlgorzenBody']))
                story.append(Spacer(1, 0.2 * inch))
            
            # Distribution Analysis for top KPI
            if len(detector.numeric_columns) > 0:
                story.append(Paragraph("Distribution Analysis", self.styles['AlgorzenSubheading']))
                top_kpi = detector.numeric_columns[0]  # Analyze first KPI
                try:
                    dist_chart = self.create_distribution_analysis(data, top_kpi)
                    if os.path.exists(dist_chart):
                        img = Image(dist_chart, width=6*inch, height=2*inch)
                        story.append(img)
                        story.append(Spacer(1, 0.2 * inch))
                        
                        # Statistical summary
                        stats_data = data[top_kpi].describe()
                        summary_text = f"<b>{top_kpi} Statistics:</b> Mean={stats_data['mean']:.2f}, Median={data[top_kpi].median():.2f}, Std={stats_data['std']:.2f}, Skewness={data[top_kpi].skew():.2f}"
                        story.append(Paragraph(summary_text, self.styles['AlgorzenBody']))
                        story.append(Spacer(1, 0.3 * inch))
                except Exception as e:
                    story.append(Paragraph(f"Could not generate distribution analysis: {str(e)}", self.styles['AlgorzenBody']))
                    story.append(Spacer(1, 0.2 * inch))
            
            # Trend Decomposition for top KPI
            if len(detector.numeric_columns) > 0 and date_column in data.columns:
                story.append(Paragraph("Trend Decomposition", self.styles['AlgorzenSubheading']))
                top_kpi = detector.numeric_columns[0]
                try:
                    decomp = detector.seasonal_analysis(top_kpi, period=7)
                    if decomp.get('trend') is not None:
                        trend_chart = self.create_trend_decomposition(data, date_column, top_kpi, decomp)
                        if os.path.exists(trend_chart):
                            img = Image(trend_chart, width=6*inch, height=5*inch)
                            story.append(img)
                            story.append(Spacer(1, 0.2 * inch))
                            story.append(Paragraph(f"Seasonal decomposition analysis for {top_kpi} showing trend, seasonal patterns, and residual components.", self.styles['AlgorzenBody']))
                    else:
                        story.append(Paragraph(decomp.get('message', 'Could not perform seasonal decomposition'), self.styles['AlgorzenBody']))
                    story.append(Spacer(1, 0.3 * inch))
                except Exception as e:
                    story.append(Paragraph(f"Could not generate trend decomposition: {str(e)}", self.styles['AlgorzenBody']))
                    story.append(Spacer(1, 0.2 * inch))
        
        # Add charts
        if charts:
            story.append(PageBreak())
            story.append(Paragraph("Visual Analysis", self.styles['AlgorzenHeading']))
            
            for chart_path in charts:
                if os.path.exists(chart_path):
                    img = Image(chart_path, width=6*inch, height=3*inch)
                    story.append(img)
                    story.append(Spacer(1, 0.2 * inch))
        
        # Build PDF
        doc.build(story, onFirstPage=self._add_header_footer, onLaterPages=self._add_header_footer)
        
        # Generate metadata JSON
        self._save_metadata(report_path, report_id, anomaly_summary, use_openai)
        
        return report_path
    
    def _save_metadata(self, report_path: str, report_id: str, anomaly_summary: Dict, use_openai: bool):
        """Save report metadata as JSON."""
        metadata = {
            "project": "Algorzen Vigil",
            "report_id": report_id,
            "generated_by": "Rishi Singh",
            "created_at": datetime.now().isoformat(),
            "tone": "Executive Business",
            "openai_used": use_openai,
            "report_file": os.path.basename(report_path),
            "anomaly_summary": {
                "total_anomalies": anomaly_summary['total_anomalies'],
                "severity": anomaly_summary['severity'],
                "affected_kpis": anomaly_summary['affected_kpis']
            }
        }
        
        metadata_path = os.path.join(self.output_dir, "report_metadata.json")
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"Metadata saved to: {metadata_path}")


if __name__ == "__main__":
    print("Algorzen Vigil - Report Generator Module")
    print("Algorzen Research Division © 2025 — Author Rishi Singh\n")
    print("This module generates branded PDF reports with visualizations.")
