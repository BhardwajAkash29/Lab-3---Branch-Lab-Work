import pandas as pd
import numpy as np
import os
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_directories(*dirs: str) -> None:
    """Create directories if they don't exist."""
    for directory in dirs:
        Path(directory).mkdir(parents=True, exist_ok=True)
        logger.info(f"Directory ensured: {directory}")

def load_data(filepath: str, **kwargs) -> pd.DataFrame:
    """
    Load data from a CSV file with comprehensive error handling.
    
    Args:
        filepath: Path to the CSV file
        **kwargs: Additional arguments for pd.read_csv()
    
    Returns:
        pd.DataFrame: Loaded data
        
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file is empty or invalid
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    try:
        df = pd.read_csv(filepath, **kwargs)
        
        if df.empty:
            raise ValueError(f"File is empty: {filepath}")
            
        logger.info(f"Successfully loaded {len(df)} rows from {filepath}")
        logger.info(f"Columns: {list(df.columns)}")
        
        return df
        
    except pd.errors.EmptyDataError:
        raise ValueError(f"No data found in file: {filepath}")
    except pd.errors.ParserError as e:
        raise ValueError(f"Error parsing CSV file {filepath}: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error loading {filepath}: {str(e)}")

def validate_data(df: pd.DataFrame, required_columns: Optional[list] = None) -> pd.DataFrame:
    """
    Validate data structure and content.
    
    Args:
        df: DataFrame to validate
        required_columns: List of required column names
        
    Returns:
        pd.DataFrame: Validated data
        
    Raises:
        ValueError: If validation fails
    """
    if df.empty:
        raise ValueError("DataFrame is empty")
    
    if required_columns:
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
    
    logger.info(f"Data validation passed - Shape: {df.shape}")
    return df

def preprocess_data(df: pd.DataFrame, drop_na: bool = True, 
                   fill_na: bool = False, fill_method: str = 'mean') -> pd.DataFrame:
    """
    Preprocess the data with multiple cleaning options.
    
    Args:
        df: Input DataFrame
        drop_na: Whether to drop rows with NA values
        fill_na: Whether to fill NA values instead of dropping
        fill_method: Method for filling NA ('mean', 'median', 'mode', 'forward', 'backward')
        
    Returns:
        pd.DataFrame: Preprocessed data
    """
    original_shape = df.shape
    df_clean = df.copy()
    
    # Handle missing values
    if fill_na and not drop_na:
        numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
        
        if fill_method == 'mean':
            df_clean[numeric_cols] = df_clean[numeric_cols].fillna(df_clean[numeric_cols].mean())
        elif fill_method == 'median':
            df_clean[numeric_cols] = df_clean[numeric_cols].fillna(df_clean[numeric_cols].median())
        elif fill_method == 'forward':
            df_clean = df_clean.fillna(method='ffill')
        elif fill_method == 'backward':
            df_clean = df_clean.fillna(method='bfill')
        else:
            df_clean = df_clean.fillna(df_clean.mode().iloc[0])
            
        logger.info(f"Filled NA values using {fill_method} method")
        
    elif drop_na:
        df_clean = df_clean.dropna()
        logger.info(f"Dropped rows with NA values")
    
    # Remove duplicates
    initial_len = len(df_clean)
    df_clean = df_clean.drop_duplicates()
    duplicates_removed = initial_len - len(df_clean)
    
    if duplicates_removed > 0:
        logger.info(f"Removed {duplicates_removed} duplicate rows")
    
    # Clean text columns (strip whitespace, standardize case)
    text_cols = df_clean.select_dtypes(include=['object']).columns
    for col in text_cols:
        if df_clean[col].dtype == 'object':
            df_clean[col] = df_clean[col].astype(str).str.strip()
    
    final_shape = df_clean.shape
    logger.info(f"Preprocessing complete: {original_shape} → {final_shape}")
    
    return df_clean

def analyze_data(df: pd.DataFrame, include_correlations: bool = True, 
                custom_analysis: bool = True) -> Dict[str, Any]:
    """
    Perform comprehensive data analysis.
    
    Args:
        df: DataFrame to analyze
        include_correlations: Whether to include correlation analysis
        custom_analysis: Whether to include custom metrics
        
    Returns:
        Dict containing analysis results
    """
    analysis_results = {}
    
    # Basic statistics
    analysis_results['basic_stats'] = df.describe()
    analysis_results['shape'] = df.shape
    analysis_results['dtypes'] = df.dtypes.to_dict()
    analysis_results['null_counts'] = df.isnull().sum().to_dict()
    
    # Numeric columns analysis
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if numeric_cols:
        analysis_results['numeric_columns'] = numeric_cols
        analysis_results['numeric_summary'] = {
            'total_numeric_cols': len(numeric_cols),
            'mean_values': df[numeric_cols].mean().to_dict(),
            'std_values': df[numeric_cols].std().to_dict()
        }
        
        # Correlations
        if include_correlations and len(numeric_cols) > 1:
            analysis_results['correlations'] = df[numeric_cols].corr().to_dict()
    
    # Categorical columns analysis
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    if categorical_cols:
        analysis_results['categorical_columns'] = categorical_cols
        analysis_results['categorical_summary'] = {}
        
        for col in categorical_cols:
            analysis_results['categorical_summary'][col] = {
                'unique_count': df[col].nunique(),
                'most_frequent': df[col].mode().iloc[0] if not df[col].empty else None,
                'value_counts': df[col].value_counts().head().to_dict()
            }
    
    # Custom analysis
    if custom_analysis:
        analysis_results['custom_metrics'] = {
            'data_completeness': (1 - df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100,
            'duplicate_rate': (df.duplicated().sum() / len(df)) * 100,
            'analysis_timestamp': datetime.now().isoformat()
        }
    
    logger.info("Data analysis completed successfully")
    return analysis_results

def generate_report(analysis_results: Dict[str, Any]) -> str:
    """
    Generate a formatted text report from analysis results.
    
    Args:
        analysis_results: Dictionary containing analysis results
        
    Returns:
        str: Formatted report
    """
    report_lines = [
        "="*60,
        "DATA ANALYSIS REPORT",
        "="*60,
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        f"Dataset Shape: {analysis_results['shape'][0]} rows × {analysis_results['shape'][1]} columns",
        ""
    ]
    
    # Data completeness
    if 'custom_metrics' in analysis_results:
        completeness = analysis_results['custom_metrics']['data_completeness']
        duplicate_rate = analysis_results['custom_metrics']['duplicate_rate']
        report_lines.extend([
            f"Data Completeness: {completeness:.2f}%",
            f"Duplicate Rate: {duplicate_rate:.2f}%",
            ""
        ])
    
    # Numeric summary
    if 'numeric_summary' in analysis_results:
        report_lines.extend([
            "NUMERIC COLUMNS SUMMARY:",
            "-" * 30
        ])
        
        for col, mean_val in analysis_results['numeric_summary']['mean_values'].items():
            std_val = analysis_results['numeric_summary']['std_values'][col]
            report_lines.append(f"{col}: Mean={mean_val:.2f}, Std={std_val:.2f}")
        
        report_lines.append("")
    
    # Categorical summary
    if 'categorical_summary' in analysis_results:
        report_lines.extend([
            "CATEGORICAL COLUMNS SUMMARY:",
            "-" * 30
        ])
        
        for col, info in analysis_results['categorical_summary'].items():
            report_lines.append(f"{col}: {info['unique_count']} unique values")
        
        report_lines.append("")
    
    report_lines.append("="*60)
    
    return "\n".join(report_lines)

def save_results(results: Any, filepath: str, include_report: bool = True) -> Dict[str, str]:
    """
    Save analysis results to files with multiple formats.
    
    Args:
        results: Results to save (DataFrame or Dict)
        filepath: Base filepath for saving
        include_report: Whether to generate and save a text report
        
    Returns:
        Dict mapping file types to their paths
    """
    # Ensure output directory exists
    output_dir = os.path.dirname(filepath)
    if output_dir:
        setup_directories(output_dir)
    
    saved_files = {}
    base_name = os.path.splitext(filepath)[0]
    
    try:
        if isinstance(results, pd.DataFrame):
            # Save as CSV
            csv_path = f"{base_name}.csv"
            results.to_csv(csv_path, index=True)
            saved_files['csv'] = csv_path
            logger.info(f"Results saved to CSV: {csv_path}")
            
            # Save as Excel
            excel_path = f"{base_name}.xlsx"
            results.to_excel(excel_path, index=True)
            saved_files['excel'] = excel_path
            logger.info(f"Results saved to Excel: {excel_path}")
            
        elif isinstance(results, dict):
            # Save dictionary results
            import json
            
            # Handle basic stats DataFrame in the dictionary
            results_copy = results.copy()
            if 'basic_stats' in results_copy and isinstance(results_copy['basic_stats'], pd.DataFrame):
                csv_path = f"{base_name}.csv"
                results_copy['basic_stats'].to_csv(csv_path)
                saved_files['csv'] = csv_path
                logger.info(f"Basic stats saved to CSV: {csv_path}")
            
            # Save full results as JSON
            json_path = f"{base_name}.json"
            # Convert non-serializable objects
            serializable_results = {}
            for key, value in results_copy.items():
                if isinstance(value, pd.DataFrame):
                    serializable_results[key] = value.to_dict()
                elif isinstance(value, pd.Series):
                    serializable_results[key] = value.to_dict()
                else:
                    serializable_results[key] = value
            
            with open(json_path, 'w') as f:
                json.dump(serializable_results, f, indent=2, default=str)
            saved_files['json'] = json_path
            logger.info(f"Full results saved to JSON: {json_path}")
            
            # Generate and save report
            if include_report:
                report = generate_report(results)
                report_path = f"{base_name}_report.txt"
                with open(report_path, 'w') as f:
                    f.write(report)
                saved_files['report'] = report_path
                logger.info(f"Report saved: {report_path}")
        
        return saved_files
        
    except Exception as e:
        logger.error(f"Error saving results: {str(e)}")
        raise

def create_sample_data(filepath: str, num_rows: int = 100) -> pd.DataFrame:
    """
    Create sample data for testing purposes.
    
    Args:
        filepath: Path where to save the sample data
        num_rows: Number of rows to generate
        
    Returns:
        pd.DataFrame: Generated sample data
    """
    np.random.seed(42)  # For reproducible results
    
    sample_data = pd.DataFrame({
        'Name': [f'Person_{i}' for i in range(1, num_rows + 1)],
        'Age': np.random.randint(18, 80, num_rows),
        'Score': np.random.normal(85, 10, num_rows).round(1),
        'Category': np.random.choice(['A', 'B', 'C'], num_rows),
        'Date': pd.date_range('2023-01-01', periods=num_rows, freq='D')
    })
    
    # Add some missing values for testing
    sample_data.loc[np.random.choice(sample_data.index, 5), 'Score'] = np.nan
    sample_data.loc[np.random.choice(sample_data.index, 3), 'Age'] = np.nan
    
    # Ensure directory exists
    setup_directories(os.path.dirname(filepath))
    
    # Save sample data
    sample_data.to_csv(filepath, index=False)
    logger.info(f"Sample data created: {filepath} ({len(sample_data)} rows)")
    
    return sample_data

def print_summary(results: Dict[str, Any]) -> None:
    """Print a summary of analysis results to console."""
    print("\n" + "="*50)
    print("ANALYSIS SUMMARY")
    print("="*50)
    
    if 'shape' in results:
        print(f"Dataset: {results['shape'][0]} rows × {results['shape'][1]} columns")
    
    if 'custom_metrics' in results:
        print(f"Data Completeness: {results['custom_metrics']['data_completeness']:.2f}%")
        print(f"Duplicate Rate: {results['custom_metrics']['duplicate_rate']:.2f}%")
    
    if 'numeric_columns' in results:
        print(f"Numeric Columns: {len(results['numeric_columns'])}")
    
    if 'categorical_columns' in results:
        print(f"Categorical Columns: {len(results['categorical_columns'])}")
    
    print("="*50)
