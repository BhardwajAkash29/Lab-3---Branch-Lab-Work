from utils import load_data, preprocess_data, analyze_data, save_results

def main():
    data = load_data("data/example.csv")
    clean_data = preprocess_data(data)
    results = analyze_data(clean_data)
    save_results(results, "output/result.csv")

if __name__ == "__main__":
    main()
