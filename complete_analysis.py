import pandas as pd
import matplotlib.pyplot as plt
import os

def create_filtered_dataframe():
    """
    Step 1: Combine all CSV files and create the filtered dataframe from parts (a)-(d)
    """
    print("Step 1: Creating filtered dataframe from all review files...")
    
    # List of file paths - adjust these to match your actual file names
    file_paths = [
        'restaurant_5_star_review_file-2.csv',
        'restaurant_4_star_review_file.csv',
        'restaurant_2_star_review_file.csv', 
        'restaurant_1_star_review_file.csv'
    ]
    
    # Check which files exist
    existing_files = []
    for file_path in file_paths:
        if os.path.exists(file_path):
            existing_files.append(file_path)
            print(f"Found: {file_path}")
        else:
            print(f"Warning: {file_path} not found")
    
    if not existing_files:
        print("No CSV files found! Please check your file paths.")
        return None
    
    # Load and combine all files
    all_dfs = []
    for file_path in existing_files:
        df = pd.read_csv(file_path)
        all_dfs.append(df)
        print(f"Loaded {file_path}: {len(df)} reviews")
    
    # Combine all dataframes
    combined_df = pd.concat(all_dfs, ignore_index=True)
    print(f"Combined all files: {len(combined_df)} total reviews")
    
    # (b) Identify businesses with 5 or more reviews
    business_review_counts = combined_df['business_id'].value_counts()
    businesses_5_plus_reviews = business_review_counts[business_review_counts >= 5].index.tolist()
    print(f"Found {len(businesses_5_plus_reviews)} businesses with 5+ reviews")
    
    # (c) Identify users with 3 or more reviews
    user_review_counts = combined_df['user_id'].value_counts()
    users_3_plus_reviews = user_review_counts[user_review_counts >= 3].index.tolist()
    print(f"Found {len(users_3_plus_reviews)} users with 3+ reviews")
    
    # (d) Create filtered dataframe
    filtered_df = combined_df[
        (combined_df['business_id'].isin(businesses_5_plus_reviews)) & 
        (combined_df['user_id'].isin(users_3_plus_reviews))
    ].copy()
    
    print(f"Created filtered dataframe: {len(filtered_df)} reviews")
    print(f"Filtered data represents {len(filtered_df)/len(combined_df)*100:.1f}% of original data")
    
    # Save the filtered dataframe for future use
    filtered_df.to_csv('business_user_filtered_reviews.csv', index=False)
    print("Saved filtered data to 'business_user_filtered_reviews.csv'")
    
    return filtered_df

def analyze_2017_reviews(filtered_df):
    """
    Step 2: Analyze 2017 monthly reviews and create visualization
    """
    print("\nStep 2: Analyzing 2017 monthly reviews...")
    
    # Convert date column to datetime format
    filtered_df['date_datetime'] = pd.to_datetime(filtered_df['date'])
    
    # Extract month and year
    filtered_df['month_number'] = filtered_df['date_datetime'].dt.month
    filtered_df['year_number'] = filtered_df['date_datetime'].dt.year
    
    # Filter for year 2017 only
    reviews_2017 = filtered_df[filtered_df['year_number'] == 2017].copy()
    
    if reviews_2017.empty:
        print("No reviews found for 2017 in the filtered dataset.")
        return
    
    print(f"Found {len(reviews_2017)} reviews from 2017")
    
    # (a) Count reviews published monthly in 2017
    monthly_counts_2017 = reviews_2017['month_number'].value_counts().sort_index()
    
    # Create a complete series with all months (1-12) to ensure we have all months
    all_months = pd.Series(index=range(1, 13), dtype='float64')
    monthly_counts_complete = all_months.combine_first(monthly_counts_2017).fillna(0).astype(int)
    
    print("\n(a) Monthly Review Counts for 2017:")
    print("=" * 30)
    print(f"{'Month':<12} {'Reviews':<8} {'Percentage':<10}")
    print("-" * 30)
    
    total_2017 = monthly_counts_complete.sum()
    for month in range(1, 13):
        month_name = pd.to_datetime(f'2017-{month}-01').strftime('%B')
        count = monthly_counts_complete[month]
        percentage = (count / total_2017 * 100) if total_2017 > 0 else 0
        print(f"{month_name:<12} {count:<8} {percentage:>6.1f}%")
    
    print("-" * 30)
    print(f"{'TOTAL':<12} {total_2017:<8} {100:>6.1f}%")
    
    # (b) Plot the graph
    plt.figure(figsize=(12, 6))
    
    # Create the plot with different colors for each bar
    colors = plt.cm.viridis(range(12))
    bars = plt.bar(monthly_counts_complete.index, monthly_counts_complete.values, 
                   color=colors, edgecolor='black', alpha=0.7)
    
    # Customize the plot
    plt.title('Monthly Review Counts in 2017\n(Businesses with 5+ reviews & Users with 3+ reviews)', 
              fontsize=14, fontweight='bold')
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Number of Reviews', fontsize=12)
    
    # Set x-axis labels as month names
    month_names = [pd.to_datetime(f'2017-{month}-01').strftime('%b') for month in monthly_counts_complete.index]
    plt.xticks(monthly_counts_complete.index, month_names)
    
    # Add value labels on top of bars
    for bar, count in zip(bars, monthly_counts_complete.values):
        if count > 0:  # Only add label if count is not zero
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    str(count), ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # Add grid for better readability
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add some statistics to the plot
    max_month = monthly_counts_complete.idxmax()
    max_month_name = pd.to_datetime(f'2017-{max_month}-01').strftime('%B')
    plt.figtext(0.02, 0.02, f"Peak month: {max_month_name} ({monthly_counts_complete[max_month]} reviews)", 
                fontsize=10, style='italic')
    
    # Adjust layout and display
    plt.tight_layout()
    plt.savefig('2017_monthly_reviews.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"\nGraph saved as '2017_monthly_reviews.png'")
    
    return monthly_counts_complete

def main():
    """
    Main function to run the complete analysis
    """
    print("YELP REVIEWS ANALYSIS")
    print("=" * 50)
    
    # Check if filtered data already exists
    if os.path.exists('business_user_filtered_reviews.csv'):
        print("Found existing filtered data file. Loading...")
        filtered_df = pd.read_csv('business_user_filtered_reviews.csv')
        print(f"Loaded {len(filtered_df)} reviews from existing file")
    else:
        # Create filtered data from scratch
        filtered_df = create_filtered_dataframe()
        if filtered_df is None:
            return
    
    # Analyze 2017 data
    monthly_counts = analyze_2017_reviews(filtered_df)
    
    print("\n" + "=" * 50)
    print("ANALYSIS COMPLETE!")
    print("=" * 50)

# Run the main function
if __name__ == "__main__":
    main()