#!/usr/bin/env python3
"""
Enhanced Main Script - Refactored Data Analysis Pipeline
========================================================

This script demonstrates a clean, modular approach to data processing
with comprehensive error handling and flexible configuration.
"""

import sys
import argparse
from pathlib import Path
from utils import (
    setup_directories,
    load_data,
    validate_data,
    preprocess_data,
    analyze_data,
    save_results,
    create_sample_data,
    print_summary
)

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Enhanced Data Analysis Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--input', '-i',
        default="data/example.csv",
        help="Input CSV file path (default: data/example.csv)"
    )
    
    parser.add_argument(
        '--output', '-o',
        default="output/results",
        help="Output file base path (default: output/results)"
    )
    
    parser.add_argument(
        '--create-sample',
        action='store_true',
        help="Create sample data if input file doesn't exist"
    )
    
    parser.add_argument(
        '--fill-na',
        action='store_true',
        help="Fill missing values instead of dropping them"
    )
    
    parser.add_argument(
        '--fill-method',
        choices=['mean', 'median', 'mode', 'forward', 'backward'],
        default='mean',
        help="Method for filling missing values (default: mean)"
    )
    
    parser.add_argument(
        '--no-correlations',
        action='store_true',
        help="Skip correlation analysis"
    )
    
    parser.add_argument(
        '--required-columns',
        nargs='+',
        help="List of required column names"
    )
    
    return parser.parse_args()

def main():
    """
    Main execution function with comprehensive pipeline.
    Enhanced with error handling, logging, and flexible options.
    """
    # Parse command line arguments
    args = parse_arguments()
    
    try:
        # Setup directories
        setup_directories("data", "output")
        
        # Handle sample data creation
        if args.create_sample and not Path(args.input).exists():
            print(f"Creating sample data at {args.input}...")
            create_sample_data(args.input, num_rows=50)
        
        # Data loading and validation
        print("Loading and validating data...")
        data = load_data(args.input)
        validated_data = validate_data(data, args.required_columns)
        
        # Data preprocessing
        print("Preprocessing data...")
        clean_data = preprocess_data(
            validated_data, 
            drop_na=not args.fill_na,
            fill_na=args.fill_na,
            fill_method=args.fill_method
        )
        
        # Data analysis
        print("Analyzing data...")
        results = analyze_data(
            clean_data,
            include_correlations=not args.no_correlations,
            custom_analysis=True
        )
        
        # Save results
        print("Saving results...")
        saved_files = save_results(results, f"{args.output}.csv", include_report=True)
        
        # Print summary
        print_summary(results)
        
        # Show saved files
        print("\nFiles saved:")
        for file_type, filepath in saved_files.items():
            print(f"  {file_type.upper()}: {filepath}")
        
        print("\n✓ Analysis pipeline completed successfully!")
        return True
        
    except FileNotFoundError as e:
        print(f"❌ File Error: {e}")
        if not args.create_sample:
            print("💡 Tip: Use --create-sample to generate test data")
        return False
        
    except ValueError as e:
        print(f"❌ Data Error: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False

def run_basic_analysis():
    """Simple function for basic analysis without arguments."""
    try:
        # Basic pipeline execution
        data = load_data("data/example.csv")
        clean_data = preprocess_data(data)
        results = analyze_data(clean_data)
        saved_files = save_results(results, "output/results.csv")
        print_summary(results)
        
        print("Basic analysis completed!")
        return results
        
    except Exception as e:
        print(f"Error in basic analysis: {e}")
        return None

if __name__ == "__main__":
    # Run with command line arguments
    success = main()
    sys.exit(0 if success else 1)
