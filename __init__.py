"""
Algorzen Vigil - AI Drift Detection & Anomaly Monitoring Engine
Algorzen Research Division © 2025 — Author Rishi Singh

A complete Python system for detecting data drift, outliers, and anomalies
in time-series KPI data, with AI-powered explanations and professional reporting.
"""

__version__ = "1.0.0"
__author__ = "Rishi Singh"
__organization__ = "Algorzen Research Division"
__project__ = "Vigil - Drop 002"

from drift_detector import DriftDetector, load_kpi_data
from anomaly_explainer import AnomalyExplainer
from report_generator import ReportGenerator

__all__ = [
    'DriftDetector',
    'AnomalyExplainer',
    'ReportGenerator',
    'load_kpi_data',
]
