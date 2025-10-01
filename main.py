import pandas as pd
import os

def comprehensive_analysis():
    # (a) load all files
    file_paths = [
        'restaurant_5_star_review_file-2.csv',
        'restaurant_4_star_review_file-2.csv',
        'restaurant_2_star_review_file-2.csv', 
        'restaurant_1_star_review_file-2.csv'
    ]
    
    all_dfs = []
    for file_path in file_paths:
        try:
            df = pd.read_csv(file_path)
            all_dfs.append(df)
            print(f"Loaded {file_path}: {len(df)} reviews")
        except FileNotFoundError:
            print(f"Could not find {file_path}")
            continue
    
    if not all_dfs:
        return None
    
    combined_df = pd.concat(all_dfs, ignore_index=True)
    
    # (b) businesses with 5+ reviews
    business_stats = combined_df['business_id'].value_counts().reset_index()
    business_stats.columns = ['business_id', 'review_count']
    businesses_5_plus = business_stats[business_stats['review_count'] >= 5]['business_id'].tolist()
    
    # (c) users with 3+ reviews  
    user_stats = combined_df['user_id'].value_counts().reset_index()
    user_stats.columns = ['user_id', 'review_count']
    users_3_plus = user_stats[user_stats['review_count'] >= 3]['user_id'].tolist()
    
    # (d) create filtered dataframe
    filtered_df = combined_df[
        combined_df['business_id'].isin(businesses_5_plus) & 
        combined_df['user_id'].isin(users_3_plus)
    ].copy()
    
    # add summary columns
    filtered_df['business_review_count'] = filtered_df['business_id'].map(
        combined_df['business_id'].value_counts()
    )
    filtered_df['user_review_count'] = filtered_df['user_id'].map(
        combined_df['user_id'].value_counts()
    )
    
    return combined_df, filtered_df, businesses_5_plus, users_3_plus

# run the analysis
result = comprehensive_analysis()

if result:
    combined_df, filtered_df, businesses_5_plus, users_3_plus = result
    
    print("\n" + "="*50)
    print("ANALYSIS RESULTS")
    print("="*50)
    
    print(f"(a) Total reviews across all files: {len(combined_df)}")
    print(f"(b) Businesses with 5+ reviews: {len(businesses_5_plus)}")
    print(f"(c) Users with 3+ reviews: {len(users_3_plus)}")
    print(f"(d) Filtered dataframe size: {filtered_df.shape}")
    
    print("\nFiltered DataFrame Sample:")
    print(filtered_df[['business_id', 'user_id', 'stars', 'business_review_count', 'user_review_count']].head(10))
    
    # save results
    filtered_df.to_csv('business_user_filtered_reviews.csv', index=False)
    
    # save business and user lists
    pd.DataFrame({'business_id': businesses_5_plus}).to_csv('businesses_5_plus_reviews.csv', index=False)
    pd.DataFrame({'user_id': users_3_plus}).to_csv('users_3_plus_reviews.csv', index=False)
    
    print("\nFiles saved:")
    print("- business_user_filtered_reviews.csv")
    print("- businesses_5_plus_reviews.csv") 
    print("- users_3_plus_reviews.csv")