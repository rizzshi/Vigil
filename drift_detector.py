"""
Algorzen Vigil - Drift Detector Module
Algorzen Research Division © 2025 — Author Rishi Singh

This module implements drift and anomaly detection algorithms for KPI time-series data.
Includes Z-score outlier detection, rolling-median deviation, and seasonal decomposition.
"""

import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.tsa.seasonal import seasonal_decompose
from typing import Dict, List, Tuple


class DriftDetector:
    """
    Detects anomalies and drift in time-series KPI data.
    
    Methods:
        - detect_zscore_outliers: Identifies values beyond 3 standard deviations
        - detect_rolling_deviation: Flags points with >25% deviation from rolling median
        - seasonal_analysis: Decomposes time-series into trend, seasonal, and residual components
        - generate_anomaly_summary: Aggregates all detected anomalies
    """
    
    def __init__(self, data: pd.DataFrame, date_column: str = 'date'):
        """
        Initialize the drift detector.
        
        Args:
            data: DataFrame containing time-series KPI data
            date_column: Name of the date/timestamp column
        """
        self.data = data.copy()
        self.date_column = date_column
        
        # Convert date column to datetime
        if date_column in self.data.columns:
            self.data[date_column] = pd.to_datetime(self.data[date_column])
            self.data = self.data.sort_values(date_column).reset_index(drop=True)
        
        self.numeric_columns = self.data.select_dtypes(include=[np.number]).columns.tolist()
        self.anomalies = {}
    
    def detect_zscore_outliers(self, threshold: float = 3.0) -> Dict[str, pd.DataFrame]:
        """
        Detect outliers using Z-score method (values beyond threshold standard deviations).
        
        Args:
            threshold: Number of standard deviations to consider as outlier (default: 3.0)
            
        Returns:
            Dictionary mapping column names to DataFrames of detected outliers
        """
        outliers = {}
        
        for col in self.numeric_columns:
            # Calculate Z-scores
            z_scores = np.abs(stats.zscore(self.data[col], nan_policy='omit'))
            
            # Identify outliers
            outlier_mask = z_scores > threshold
            outlier_data = self.data[outlier_mask].copy()
            
            if len(outlier_data) > 0:
                outlier_data['z_score'] = z_scores[outlier_mask]
                outlier_data['column'] = col
                outliers[col] = outlier_data
        
        self.anomalies['zscore'] = outliers
        return outliers
    
    def detect_rolling_deviation(self, window: int = 7, threshold: float = 0.25) -> Dict[str, pd.DataFrame]:
        """
        Detect anomalies using rolling median deviation method.
        Flags points where deviation from rolling median exceeds threshold percentage.
        
        Args:
            window: Rolling window size (default: 7 days)
            threshold: Deviation threshold as percentage (default: 0.25 = 25%)
            
        Returns:
            Dictionary mapping column names to DataFrames of detected anomalies
        """
        deviations = {}
        
        for col in self.numeric_columns:
            # Calculate rolling median
            rolling_median = self.data[col].rolling(window=window, center=True).median()
            
            # Calculate percentage deviation
            deviation = np.abs((self.data[col] - rolling_median) / rolling_median)
            
            # Identify anomalies
            anomaly_mask = deviation > threshold
            anomaly_data = self.data[anomaly_mask].copy()
            
            if len(anomaly_data) > 0:
                anomaly_data['deviation_pct'] = (deviation[anomaly_mask] * 100).round(2)
                anomaly_data['column'] = col
                anomaly_data['rolling_median'] = rolling_median[anomaly_mask]
                deviations[col] = anomaly_data
        
        self.anomalies['rolling_deviation'] = deviations
        return deviations
    
    def seasonal_analysis(self, column: str, period: int = 7) -> Dict:
        """
        Perform seasonal decomposition on a time-series column.
        
        Args:
            column: Name of the column to analyze
            period: Seasonal period (default: 7 for weekly patterns)
            
        Returns:
            Dictionary containing trend, seasonal, and residual components
        """
        if column not in self.numeric_columns:
            raise ValueError(f"Column '{column}' not found in numeric columns")
        
        # Ensure we have enough data points
        if len(self.data) < 2 * period:
            return {
                'trend': None,
                'seasonal': None,
                'residual': None,
                'message': f'Insufficient data for seasonal analysis (need at least {2 * period} points)'
            }
        
        try:
            # Perform seasonal decomposition
            decomposition = seasonal_decompose(
                self.data[column].dropna(),
                model='additive',
                period=period,
                extrapolate_trend='freq'
            )
            
            return {
                'trend': decomposition.trend,
                'seasonal': decomposition.seasonal,
                'residual': decomposition.resid,
                'original': self.data[column]
            }
        except Exception as e:
            return {
                'trend': None,
                'seasonal': None,
                'residual': None,
                'message': f'Seasonal analysis failed: {str(e)}'
            }
    
    def generate_anomaly_summary(self) -> Dict:
        """
        Generate a comprehensive summary of all detected anomalies.
        
        Returns:
            Dictionary containing anomaly counts, affected KPIs, and severity assessments
        """
        summary = {
            'total_anomalies': 0,
            'affected_kpis': set(),
            'by_method': {},
            'severity': 'Low',
            'details': []
        }
        
        # Process Z-score anomalies
        if 'zscore' in self.anomalies:
            zscore_count = sum(len(df) for df in self.anomalies['zscore'].values())
            summary['by_method']['zscore'] = zscore_count
            summary['total_anomalies'] += zscore_count
            summary['affected_kpis'].update(self.anomalies['zscore'].keys())
            
            for col, df in self.anomalies['zscore'].items():
                for _, row in df.iterrows():
                    summary['details'].append({
                        'date': row[self.date_column],
                        'kpi': col,
                        'method': 'Z-Score',
                        'value': row[col],
                        'z_score': row.get('z_score', 0)
                    })
        
        # Process rolling deviation anomalies
        if 'rolling_deviation' in self.anomalies:
            deviation_count = sum(len(df) for df in self.anomalies['rolling_deviation'].values())
            summary['by_method']['rolling_deviation'] = deviation_count
            summary['total_anomalies'] += deviation_count
            summary['affected_kpis'].update(self.anomalies['rolling_deviation'].keys())
            
            for col, df in self.anomalies['rolling_deviation'].items():
                for _, row in df.iterrows():
                    summary['details'].append({
                        'date': row[self.date_column],
                        'kpi': col,
                        'method': 'Rolling Deviation',
                        'value': row[col],
                        'deviation_pct': row.get('deviation_pct', 0)
                    })
        
        # Determine severity
        summary['affected_kpis'] = list(summary['affected_kpis'])
        if summary['total_anomalies'] == 0:
            summary['severity'] = 'None'
        elif summary['total_anomalies'] <= 5:
            summary['severity'] = 'Low'
        elif summary['total_anomalies'] <= 15:
            summary['severity'] = 'Medium'
        else:
            summary['severity'] = 'High'
        
        return summary
    
    def get_kpi_statistics(self) -> pd.DataFrame:
        """
        Calculate basic statistics for all numeric KPIs.
        
        Returns:
            DataFrame containing mean, std, min, max for each KPI
        """
        stats_data = []
        
        for col in self.numeric_columns:
            stats_data.append({
                'KPI': col,
                'Mean': self.data[col].mean(),
                'Std Dev': self.data[col].std(),
                'Min': self.data[col].min(),
                'Max': self.data[col].max(),
                'Count': self.data[col].count()
            })
        
        return pd.DataFrame(stats_data)


def load_kpi_data(file_path: str) -> pd.DataFrame:
    """
    Load KPI data from CSV file.
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        DataFrame containing the KPI data
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        raise Exception(f"Failed to load KPI data from {file_path}: {str(e)}")


if __name__ == "__main__":
    # Example usage
    print("Algorzen Vigil - Drift Detector Module")
    print("Algorzen Research Division © 2025 — Author Rishi Singh\n")
    
    # Load sample data
    data = load_kpi_data("data/sample_kpi_data.csv")
    
    # Initialize detector
    detector = DriftDetector(data, date_column='date')
    
    # Run detection methods
    print("Running Z-score outlier detection...")
    zscore_outliers = detector.detect_zscore_outliers(threshold=3.0)
    
    print("Running rolling deviation detection...")
    rolling_anomalies = detector.detect_rolling_deviation(window=7, threshold=0.25)
    
    # Generate summary
    summary = detector.generate_anomaly_summary()
    print(f"\nTotal anomalies detected: {summary['total_anomalies']}")
    print(f"Severity: {summary['severity']}")
    print(f"Affected KPIs: {', '.join(summary['affected_kpis'])}")
