import pandas as pd


def simple_top_4star_users():
    # load data
    try:
        df = pd.read_csv('business_user_filtered_reviews.csv')
    except FileNotFoundError:
        # if filtered data doesn't exist, try to load all files
        file_paths = [
            'restaurant_5_star_review_file-2.csv',
            'restaurant_4_star_review_file.csv',
            'restaurant_2_star_review_file.csv', 
            'restaurant_1_star_review_file.csv'
        ]
        
        all_dfs = []
        for file_path in file_paths:
            try:
                all_dfs.append(pd.read_csv(file_path))
            except FileNotFoundError:
                continue
        
        if not all_dfs:
            print("No data files found!")
            return
        
        df = pd.concat(all_dfs, ignore_index=True)
    
    # filter for four-star reviews and count by user
    four_star_users = df[df['stars'] == 4.0]['user_id'].value_counts().head(5)
    
    print("TOP 5 USERS WITH MOST FOUR-STAR REVIEWS:")
    print("=" * 50)
    for i, (user_id, count) in enumerate(four_star_users.items(), 1):
        print(f"{i}. {user_id} - {count} four-star reviews")


simple_top_4star_users()