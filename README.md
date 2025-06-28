# Refactoring Project

This project demonstrates professional code refactoring principles with a comprehensive data analysis pipeline. All processing logic has been extracted into reusable functions within the `utils.py` module, following best practices for maintainable and testable code.

## 🚀 Features

### Core Functionality
- **Modular Design**: All processing logic separated into focused, reusable functions
- **Comprehensive Error Handling**: Robust error management with informative messages
- **Type Hints**: Full type annotations for better code documentation and IDE support
- **Logging**: Detailed logging for debugging and monitoring
- **Flexible Data Processing**: Multiple options for handling missing data and preprocessing

### Advanced Capabilities
- **Multiple Output Formats**: CSV, Excel, JSON, and formatted text reports
- **Statistical Analysis**: Descriptive statistics, correlations, and custom metrics
- **Data Validation**: Automatic data quality checks and validation
- **Command Line Interface**: Flexible CLI with multiple configuration options
- **Sample Data Generation**: Built-in sample data creation for testing

## 📁 Project Structure

```
refactoring-project/
├── main.py              # Main execution script (only function calls)
├── utils.py             # All reusable utility functions
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── data/               # Input data directory
│   └── example.csv     # Sample input file
└── output/             # Output directory (auto-created)
    ├── results.csv     # Statistical results
    ├── results.xlsx    # Excel format results
    ├── results.json    # Complete analysis in JSON
    └── results_report.txt  # Human-readable report
```

## ⚡ Quick Start

### Basic Usage
```bash
# Install dependencies
pip install -r requirements.txt

# Run basic analysis
python main.py

# Create sample data and run analysis
python main.py --create-sample
```

### Advanced Usage
```bash
# Custom input/output paths
python main.py --input data/my_data.csv --output results/analysis

# Fill missing values instead of dropping
python main.py --fill-na --fill-method median

# Specify required columns
python main.py --required-columns Name Age Score

# Skip correlation analysis for faster processing
python main.py --no-correlations
```

## 🛠️ Available Functions

### Data Loading & Validation
- `load_data()` - Load CSV with comprehensive error handling
- `validate_data()` - Ensure data meets requirements
- `setup_directories()` - Create necessary directories

### Data Processing
- `preprocess_data()` - Clean and standardize data
  - Handle missing values (drop or fill)
  - Remove duplicates
  - Clean text columns
  - Multiple fill methods: mean, median, mode, forward, backward

### Analysis & Reporting
- `analyze_data()` - Comprehensive statistical analysis
  - Descriptive statistics
  - Correlation analysis
  - Categorical data summary
  - Custom metrics (completeness, duplicates)
- `generate_report()` - Create formatted text reports
- `print_summary()` - Console summary output

### Output & Utilities
- `save_results()` - Multi-format output (CSV, Excel, JSON, text)
- `create_sample_data()` - Generate test datasets

## 📊 Output Examples

### CSV Output (results.csv)
```csv
,Age,Score
count,50.0,47.0
mean,48.2,85.1
std,17.8,9.2
min,18.0,65.5
max,79.0,98.7
```

### Text Report (results_report.txt)
```
============================================================
DATA ANALYSIS REPORT
============================================================
Generated: 2024-01-15 14:30:22

Dataset Shape: 50 rows × 5 columns
Data Completeness: 94.00%
Duplicate Rate: 0.00%

NUMERIC COLUMNS SUMMARY:
------------------------------
Age: Mean=48.20, Std=17.84
Score: Mean=85.13, Std=9.22
============================================================
```

## 🎯 Refactoring Principles Applied

### 1. **Single Responsibility**
Each function has one clear, focused purpose:
- Data loading ≠ Data cleaning ≠ Analysis ≠ Output

### 2. **Function Extraction**
- **Before**: 50+ lines of inline processing
- **After**: 15+ focused, reusable functions

### 3. **Error Handling**
- Comprehensive try-catch blocks
- Informative error messages
- Graceful failure handling

### 4. **Type Safety**
- Full type annotations
- Runtime type checking
- Better IDE support

### 5. **Configuration**
- Command-line arguments
- Flexible parameters
- Environment-aware settings

## 🧪 Testing Your Refactored Code

```bash
# Test with sample data
python main.py --create-sample --input data/test.csv

# Test error handling
python main.py --input nonexistent.csv

# Test data validation
python main.py --required-columns Name Age Email

# Test different preprocessing options
python main.py --fill-na --fill-method median
```

## 🔧 Development Workflow

### For New Features
1. Add function to `utils.py`
2. Add corresponding call to `main.py`
3. Update type hints and docstrings
4. Test with various data scenarios

### For Bug Fixes
1. Identify the specific function with the issue
2. Fix in isolation within `utils.py`
3. Test the specific function
4. Verify end-to-end pipeline still works

## 📈 Benefits of This Refactoring

| Aspect | Before | After |
|--------|--------|-------|
| **Reusability** | Monolithic script | Modular functions |
| **Testability** | Hard to test parts | Each function testable |
| **Maintainability** | Changes affect everything | Isolated changes |
| **Readability** | 100+ line main function | Clean function calls |
| **Error Handling** | Basic try-catch | Comprehensive error management |
| **Documentation** | Minimal comments | Full docstrings + type hints |

## 🚦 Error Handling Examples

The refactored code handles various error scenarios gracefully:

```bash
# File not found
❌ File Error: File not found: data/missing.csv
💡 Tip: Use --create-sample to generate test data

# Invalid data structure
❌ Data Error: Missing required columns: ['Email']

# Unexpected errors
❌ Unexpected Error: Permission denied: /protected/output/
```

## 🎉 Success Indicators

When refactoring is complete, you should see:
- ✅ Main function contains only function calls
- ✅ Each function has a single, clear purpose
- ✅ Comprehensive error handling throughout
- ✅ Type hints on all function parameters
- ✅ Detailed logging and user feedback
- ✅ Multiple output formats available
- ✅ Flexible configuration options

## 📚 Next Steps

After implementing this refactoring:
1. **Add Unit Tests**: Create tests for each function in `utils.py`
2. **Add More Analysis**: Extend `analyze_data()` with domain-specific metrics
3. **Create Documentation**: Generate API docs from docstrings
4. **Performance Optimization**: Profile and optimize slow functions
5. **Configuration Files**: Add YAML/JSON config file support

---

This refactored codebase demonstrates professional software development practices and serves as a template for clean, maintainable data processing pipelines.
