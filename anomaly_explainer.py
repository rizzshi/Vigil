"""
Algorzen Vigil - Anomaly Explainer Module
Algorzen Research Division © 2025 — Author Rishi Singh

This module generates AI-powered explanations for detected anomalies using OpenAI GPT-4.
Includes fallback heuristic-based explanations when API access is unavailable.
"""

import os
from typing import Dict, List, Optional
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class AnomalyExplainer:
    """
    Generates executive-level explanations for detected anomalies.
    
    Uses GPT-4 for intelligent analysis with fallback to heuristic-based explanations.
    Produces three key sections: Executive Summary, Key Findings, and Recommendations.
    """
    
    def __init__(self, use_openai: bool = True):
        """
        Initialize the anomaly explainer.
        
        Args:
            use_openai: Whether to use OpenAI API (requires OPENAI_API_KEY environment variable)
        """
        self.use_openai = use_openai and OPENAI_AVAILABLE
        self.client = None
        
        if self.use_openai:
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key:
                try:
                    self.client = OpenAI(api_key=api_key)
                except Exception as e:
                    print(f"Warning: Failed to initialize OpenAI client: {e}")
                    self.use_openai = False
            else:
                print("Warning: OPENAI_API_KEY not found. Using fallback explanations.")
                self.use_openai = False
    
    def generate_executive_summary(self, anomaly_summary: Dict, kpi_stats: Dict) -> str:
        """
        Generate an executive summary of the analysis.
        
        Args:
            anomaly_summary: Summary of detected anomalies from DriftDetector
            kpi_stats: Statistical information about KPIs
            
        Returns:
            Executive summary text
        """
        if self.use_openai and self.client:
            return self._generate_gpt_executive_summary(anomaly_summary, kpi_stats)
        else:
            return self._generate_fallback_executive_summary(anomaly_summary, kpi_stats)
    
    def generate_key_findings(self, anomaly_summary: Dict) -> str:
        """
        Generate detailed key findings from anomaly data.
        
        Args:
            anomaly_summary: Summary of detected anomalies
            
        Returns:
            Key findings text
        """
        if self.use_openai and self.client:
            return self._generate_gpt_key_findings(anomaly_summary)
        else:
            return self._generate_fallback_key_findings(anomaly_summary)
    
    def generate_recommendations(self, anomaly_summary: Dict) -> str:
        """
        Generate actionable recommendations based on detected anomalies.
        
        Args:
            anomaly_summary: Summary of detected anomalies
            
        Returns:
            Recommendations text
        """
        if self.use_openai and self.client:
            return self._generate_gpt_recommendations(anomaly_summary)
        else:
            return self._generate_fallback_recommendations(anomaly_summary)
    
    def _generate_gpt_executive_summary(self, anomaly_summary: Dict, kpi_stats: Dict) -> str:
        """Generate executive summary using GPT-4."""
        try:
            prompt = f"""You are an executive business analyst at Algorzen Research Division.
            
Analyze the following KPI anomaly data and write a concise executive summary (3-4 sentences):

Total Anomalies Detected: {anomaly_summary['total_anomalies']}
Severity: {anomaly_summary['severity']}
Affected KPIs: {', '.join(anomaly_summary['affected_kpis'])}
Detection Methods: {', '.join(anomaly_summary['by_method'].keys())}

Write in a professional, executive tone. Focus on business impact and significance."""

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a senior business analyst writing executive reports."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"Warning: GPT-4 request failed: {e}. Using fallback.")
            return self._generate_fallback_executive_summary(anomaly_summary, kpi_stats)
    
    def _generate_gpt_key_findings(self, anomaly_summary: Dict) -> str:
        """Generate key findings using GPT-4."""
        try:
            # Prepare anomaly details for context
            details_summary = []
            for detail in anomaly_summary['details'][:10]:  # Limit to first 10 for token efficiency
                details_summary.append(
                    f"- {detail['date'].strftime('%Y-%m-%d')}: {detail['kpi']} "
                    f"({detail['method']}, value: {detail['value']})"
                )
            
            prompt = f"""You are an executive business analyst at Algorzen Research Division.

Based on the following anomaly detections, write 3-5 key findings in bullet points:

Total Anomalies: {anomaly_summary['total_anomalies']}
Severity: {anomaly_summary['severity']}

Sample Anomalies:
{chr(10).join(details_summary[:5])}

Write concise, actionable bullet points focused on business insights."""

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a senior business analyst writing executive reports."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"Warning: GPT-4 request failed: {e}. Using fallback.")
            return self._generate_fallback_key_findings(anomaly_summary)
    
    def _generate_gpt_recommendations(self, anomaly_summary: Dict) -> str:
        """Generate recommendations using GPT-4."""
        try:
            prompt = f"""You are an executive business analyst at Algorzen Research Division.

Based on the following anomaly analysis, provide 3-5 actionable recommendations:

Total Anomalies: {anomaly_summary['total_anomalies']}
Severity: {anomaly_summary['severity']}
Affected KPIs: {', '.join(anomaly_summary['affected_kpis'])}

Write clear, executive-level recommendations with business focus."""

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a senior business analyst writing executive reports."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"Warning: GPT-4 request failed: {e}. Using fallback.")
            return self._generate_fallback_recommendations(anomaly_summary)
    
    def _generate_fallback_executive_summary(self, anomaly_summary: Dict, kpi_stats: Dict) -> str:
        """Generate executive summary using heuristics."""
        severity = anomaly_summary['severity']
        total = anomaly_summary['total_anomalies']
        affected = len(anomaly_summary['affected_kpis'])
        
        if total == 0:
            return ("Our analysis of the KPI time-series data reveals stable performance across all "
                   "monitored metrics. No significant anomalies were detected during the review period, "
                   "indicating consistent operational health and predictable business patterns.")
        
        severity_desc = {
            'Low': 'minimal operational disruption',
            'Medium': 'moderate performance irregularities requiring attention',
            'High': 'critical deviations demanding immediate investigation'
        }
        
        return (f"Our algorithmic drift detection system has identified {total} anomalies across "
               f"{affected} key performance indicators, classified as {severity} severity. "
               f"The analysis reveals {severity_desc.get(severity, 'performance variations')} "
               f"in core business metrics. These findings warrant executive review to maintain "
               f"operational excellence and strategic alignment.")
    
    def _generate_fallback_key_findings(self, anomaly_summary: Dict) -> str:
        """Generate key findings using heuristics."""
        findings = []
        
        # Finding 1: Overall assessment
        total = anomaly_summary['total_anomalies']
        severity = anomaly_summary['severity']
        findings.append(
            f"• Detected {total} anomalies with {severity} severity classification, "
            f"indicating {'significant' if severity == 'High' else 'manageable'} deviations from expected patterns."
        )
        
        # Finding 2: Affected KPIs
        kpis = anomaly_summary['affected_kpis']
        if kpis:
            findings.append(
                f"• Primary impact observed in: {', '.join(kpis[:3])}{'...' if len(kpis) > 3 else ''}, "
                f"suggesting potential systemic issues."
            )
        
        # Finding 3: Detection methods
        methods = anomaly_summary['by_method']
        if 'zscore' in methods and methods['zscore'] > 0:
            findings.append(
                f"• Z-score analysis identified {methods['zscore']} extreme outliers "
                f"exceeding 3 standard deviations from the mean."
            )
        
        if 'rolling_deviation' in methods and methods['rolling_deviation'] > 0:
            findings.append(
                f"• Rolling deviation analysis flagged {methods['rolling_deviation']} instances "
                f"of >25% deviation from recent trends."
            )
        
        # Finding 4: Temporal patterns (if available)
        if anomaly_summary['details']:
            dates = [d['date'] for d in anomaly_summary['details']]
            if dates:
                findings.append(
                    f"• Anomalies span from {min(dates).strftime('%Y-%m-%d')} to "
                    f"{max(dates).strftime('%Y-%m-%d')}, requiring temporal correlation analysis."
                )
        
        return '\n'.join(findings)
    
    def _generate_fallback_recommendations(self, anomaly_summary: Dict) -> str:
        """Generate recommendations using heuristics."""
        recommendations = []
        
        severity = anomaly_summary['severity']
        total = anomaly_summary['total_anomalies']
        
        if severity == 'High' or total > 15:
            recommendations.append(
                "• Immediate Investigation: Convene cross-functional team to assess root causes "
                "of critical anomalies and implement corrective measures within 48 hours."
            )
            recommendations.append(
                "• Enhanced Monitoring: Deploy real-time alerting systems for affected KPIs "
                "to prevent recurrence and enable proactive intervention."
            )
        elif severity == 'Medium' or total > 5:
            recommendations.append(
                "• Scheduled Review: Conduct weekly analysis of flagged KPIs to identify "
                "emerging patterns and potential systemic issues."
            )
        
        recommendations.append(
            "• Data Validation: Verify data collection processes and instrumentation accuracy "
            "for affected metrics to rule out measurement errors."
        )
        
        recommendations.append(
            "• Trend Analysis: Establish baseline performance thresholds and implement "
            "automated drift detection to maintain operational visibility."
        )
        
        if anomaly_summary['affected_kpis']:
            recommendations.append(
                f"• Stakeholder Communication: Brief department heads responsible for "
                f"{', '.join(anomaly_summary['affected_kpis'][:2])} on findings and remediation plans."
            )
        
        return '\n'.join(recommendations)
    
    def generate_full_report_narrative(self, anomaly_summary: Dict, kpi_stats: Dict) -> Dict[str, str]:
        """
        Generate complete narrative for the report including all sections.
        
        Args:
            anomaly_summary: Summary of detected anomalies
            kpi_stats: Statistical information about KPIs
            
        Returns:
            Dictionary with executive_summary, key_findings, and recommendations
        """
        return {
            'executive_summary': self.generate_executive_summary(anomaly_summary, kpi_stats),
            'key_findings': self.generate_key_findings(anomaly_summary),
            'recommendations': self.generate_recommendations(anomaly_summary)
        }


if __name__ == "__main__":
    print("Algorzen Vigil - Anomaly Explainer Module")
    print("Algorzen Research Division © 2025 — Author Rishi Singh\n")
    
    # Example usage
    sample_summary = {
        'total_anomalies': 8,
        'severity': 'Medium',
        'affected_kpis': ['revenue', 'churn_rate', 'server_uptime'],
        'by_method': {'zscore': 3, 'rolling_deviation': 5},
        'details': [
            {'date': datetime(2024, 2, 10), 'kpi': 'revenue', 'method': 'Z-Score', 'value': 95000}
        ]
    }
    
    explainer = AnomalyExplainer(use_openai=False)
    narrative = explainer.generate_full_report_narrative(sample_summary, {})
    
    print("Executive Summary:")
    print(narrative['executive_summary'])
    print("\nKey Findings:")
    print(narrative['key_findings'])
    print("\nRecommendations:")
    print(narrative['recommendations'])
