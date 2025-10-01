import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Assuming filtered_df is the dataframe from part (d) of the previous question
# If not, let's recreate it or load it

def analyze_2017_reviews(filtered_df):
    # Convert date column to datetime format
    filtered_df['date_datetime'] = pd.to_datetime(filtered_df['date'])
    
    # Extract month and year
    filtered_df['month_number'] = filtered_df['date_datetime'].dt.month
    filtered_df['year_number'] = filtered_df['date_datetime'].dt.year
    
    # Filter for year 2017 only
    reviews_2017 = filtered_df[filtered_df['year_number'] == 2017].copy()
    
    # (a) Count reviews published monthly in 2017
    monthly_counts_2017 = reviews_2017['month_number'].value_counts().sort_index()
    
    # Create a complete series with all months (1-12) to ensure we have all months
    all_months = pd.Series(index=range(1, 13), dtype='float64')
    monthly_counts_complete = all_months.combine_first(monthly_counts_2017).fillna(0).astype(int)
    
    print("(a) Monthly Review Counts for 2017:")
    print("Month\tReview Count")
    print("-" * 20)
    for month, count in monthly_counts_complete.items():
        month_name = pd.to_datetime(f'2017-{month}-01').strftime('%B')
        print(f"{month_name}\t{count}")
    
    print(f"\nTotal reviews in 2017: {monthly_counts_complete.sum()}")
    
    # (b) Plot the graph
    plt.figure(figsize=(12, 6))
    
    # Create the plot
    bars = plt.bar(monthly_counts_complete.index, monthly_counts_complete.values, 
                   color='skyblue', edgecolor='navy', alpha=0.7)
    
    # Customize the plot
    plt.title('Monthly Review Counts in 2017', fontsize=16, fontweight='bold')
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Number of Reviews', fontsize=12)
    
    # Set x-axis labels as month names
    month_names = [pd.to_datetime(f'2017-{month}-01').strftime('%b') for month in monthly_counts_complete.index]
    plt.xticks(monthly_counts_complete.index, month_names)
    
    # Add value labels on top of bars
    for bar, count in zip(bars, monthly_counts_complete.values):
        if count > 0:  # Only add label if count is not zero
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    str(count), ha='center', va='bottom', fontweight='bold')
    
    # Add grid for better readability
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Adjust layout and display
    plt.tight_layout()
    plt.show()
    
    return monthly_counts_complete, reviews_2017

# Alternative approach with more detailed analysis
def detailed_2017_analysis(filtered_df):
    # Convert date and extract features
    filtered_df['date_datetime'] = pd.to_datetime(filtered_df['date'])
    filtered_df['month_number'] = filtered_df['date_datetime'].dt.month
    filtered_df['year_number'] = filtered_df['date_datetime'].dt.year
    filtered_df['month_name'] = filtered_df['date_datetime'].dt.strftime('%B')
    
    # Filter for 2017
    reviews_2017 = filtered_df[filtered_df['year_number'] == 2017]
    
    if reviews_2017.empty:
        print("No reviews found for 2017 in the filtered dataset.")
        return None, None
    
    # (a) Get monthly counts using groupby for more control
    monthly_stats = reviews_2017.groupby('month_number').agg({
        'review_id': 'count',
        'stars': 'mean',
        'business_id': 'nunique',
        'user_id': 'nunique'
    }).rename(columns={
        'review_id': 'review_count',
        'business_id': 'unique_businesses',
        'user_id': 'unique_users'
    })
    
    # Ensure we have all months (1-12)
    all_months_df = pd.DataFrame(index=range(1, 13))
    monthly_stats_complete = all_months_df.merge(monthly_stats, left_index=True, right_index=True, how='left')
    monthly_stats_complete = monthly_stats_complete.fillna(0)
    monthly_stats_complete['review_count'] = monthly_stats_complete['review_count'].astype(int)
    
    # Add month names
    monthly_stats_complete['month_name'] = [pd.to_datetime(f'2017-{month}-01').strftime('%B') 
                                          for month in monthly_stats_complete.index]
    
    print("(a) Detailed Monthly Statistics for 2017:")
    print("=" * 70)
    print(f"{'Month':<12} {'Reviews':<8} {'Avg Stars':<10} {'Businesses':<10} {'Users':<10}")
    print("-" * 70)
    
    for idx, row in monthly_stats_complete.iterrows():
        print(f"{row['month_name']:<12} {row['review_count']:<8} {row['stars']:<10.2f} "
              f"{row['unique_businesses']:<10} {row['unique_users']:<10}")
    
    print("-" * 70)
    print(f"{'TOTAL':<12} {monthly_stats_complete['review_count'].sum():<8} "
          f"{monthly_stats_complete['stars'].mean():<10.2f} "
          f"{monthly_stats_complete['unique_businesses'].sum():<10} "
          f"{monthly_stats_complete['unique_users'].sum():<10}")
    
    # (b) Create a more sophisticated plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # Plot 1: Bar chart for review counts
    bars = ax1.bar(monthly_stats_complete.index, monthly_stats_complete['review_count'],
                   color='lightcoral', edgecolor='darkred', alpha=0.7)
    
    ax1.set_title('Monthly Review Distribution in 2017', fontsize=16, fontweight='bold')
    ax1.set_ylabel('Number of Reviews', fontsize=12)
    ax1.set_xlabel('Month', fontsize=12)
    
    # Add value labels on bars
    for bar, count in zip(bars, monthly_stats_complete['review_count']):
        if count > 0:
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    str(count), ha='center', va='bottom', fontweight='bold')
    
    # Set x-axis labels
    ax1.set_xticks(monthly_stats_complete.index)
    ax1.set_xticklabels([pd.to_datetime(f'2017-{month}-01').strftime('%b') 
                        for month in monthly_stats_complete.index])
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Plot 2: Line chart for average stars
    ax2.plot(monthly_stats_complete.index, monthly_stats_complete['stars'], 
             marker='o', linewidth=2, markersize=8, color='green', label='Average Stars')
    ax2.set_title('Average Star Rating by Month (2017)', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Average Stars', fontsize=12)
    ax2.set_xlabel('Month', fontsize=12)
    ax2.set_xticks(monthly_stats_complete.index)
    ax2.set_xticklabels([pd.to_datetime(f'2017-{month}-01').strftime('%b') 
                        for month in monthly_stats_complete.index])
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    # Add star values as annotations
    for i, (month, stars) in enumerate(zip(monthly_stats_complete.index, monthly_stats_complete['stars'])):
        if stars > 0:  # Only annotate if there are reviews
            ax2.annotate(f'{stars:.2f}', (month, stars), 
                        textcoords="offset points", xytext=(0,10), ha='center', fontweight='bold')
    
    plt.tight_layout()
    plt.show()
    
    return monthly_stats_complete, reviews_2017

# Main execution
if __name__ == "__main__":
    # If you don't have filtered_df loaded, you can recreate it like this:
    # filtered_df = pd.read_csv('business_user_filtered_reviews.csv')
    
    # Assuming filtered_df is available from previous step
    try:
        # Simple analysis
        print("SIMPLE ANALYSIS:")
        print("=" * 50)
        monthly_counts, reviews_2017_simple = analyze_2017_reviews(filtered_df)
        
        print("\n" + "=" * 50)
        print("DETAILED ANALYSIS:")
        print("=" * 50)
        monthly_stats, reviews_2017_detailed = detailed_2017_analysis(filtered_df)
        
    except NameError:
        print("filtered_df not found. Please ensure you have the filtered dataframe from part (d).")
        print("You can load it using: filtered_df = pd.read_csv('business_user_filtered_reviews.csv')")