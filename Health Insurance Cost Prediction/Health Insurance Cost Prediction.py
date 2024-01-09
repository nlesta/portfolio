import pandas as pd
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error

# Declare CSV file path
csv_file_path = 'C:\\Users\\nicho\\OneDrive\\Documents\\Projects\\portfolio\\Health Insurance Cost Prediction\\insurance.csv'

# Read the CSV file into a pandas DataFrame
charges_df = pd.read_csv(csv_file_path)

# Handling Missing Values
print(charges_df.isnull().sum())
# This shows we have no missing values and can proceed

# Get data types of all columns
column_types = charges_df.dtypes
# Print or display the result
print(column_types)
# While this data appears to be formatted properly, we often run into issues with singular values or desire different formats. Let's ensure our columns are the appropriate data types
# Data Type Conversion
charges_df['age'] = charges_df['age'].astype(int)
charges_df['sex'] = charges_df['sex'].astype(object)
charges_df['bmi'] = charges_df['bmi'].astype(float)
charges_df['children'] = charges_df['children'].astype(int)
charges_df['smoker'] = charges_df['smoker'].astype(object)
charges_df['region'] = charges_df['region'].astype(object)
charges_df['charges'] = charges_df['charges'].astype(float)

# Removing Duplicates
print(len(charges_df))
charges_df.drop_duplicates(inplace=True)
print(len(charges_df))
# It appears we did have one duplicate value! This value has been dropped so as to not alter our data exploration

# I also want to remove some outliers so there is a more representative mean. This code removes any outliers that are more than 4 standard deviations from the mean for the numerical values in the dataset.
from scipy.stats import zscore
print(len(charges_df))
z_scores = zscore(charges_df[['age', 'bmi', 'children', 'charges']])
charges_df = charges_df[(z_scores < 4).all(axis=1)]
print(len(charges_df))
# As we can see, we removed 2 values that were classified as outliers. Let's find out what rows have been deleted so far.
orig_charges_df = pd.read_csv(csv_file_path)
merged_df = orig_charges_df.merge(charges_df, how='outer', indicator=True).loc[lambda x: x['_merge'] == 'left_only']
print(merged_df)
# This table demonstrates the outliers being those with very high medical charges (no age/bmi outliers)

# The last modification I want to make to the data is to add some categorical variables to better group the observations, as well as add an age group column
charges_df = pd.get_dummies(charges_df, columns=['sex', 'smoker', 'region'], drop_first=False)
charges_df['age_group'] = pd.cut(charges_df['age'], bins=[0, 26, 42, 58, 100], labels=['Generation Z', 'Millenial', 'Generation X', 'Baby Boomer'])
print(charges_df.columns)

# I'm now going to drop a few redundant columns, such as sex_male considering we have sex_female and it is binary
charges_df = charges_df.drop(columns=['sex_male', 'smoker_no'])

# Now I will run some basic SQL queries just to get a sense of the data
# Create an SQLite in-memory database (you can also use a file-based database)
conn = sqlite3.connect(':memory:')

# Write the DataFrame to an SQLite table
charges_df.to_sql('charges_table', conn, index=False, if_exists='replace')

# Top 5 highest charges:
query = '''
        SELECT * 
        FROM charges_table 
        ORDER BY charges DESC 
        LIMIT 5'''
result_df = pd.read_sql_query(query, conn)
print(result_df)

# Average charges by age group:
query = '''
        SELECT age_group, AVG(charges) AS avg_charges
        FROM charges_table 
        GROUP BY age_group 
        ORDER BY avg_charges DESC'''
result_df = pd.read_sql_query(query, conn)
print(result_df)

# Average charges for smokers and non-smokers:
query = '''
        SELECT smoker_yes AS smoker, AVG(charges) AS avg_charges 
        FROM charges_table 
        GROUP BY smoker'''
result_df = pd.read_sql_query(query, conn)
print(result_df)

# Number of individuals in each region for this dataset:
query = '''
        SELECT
        SUM(CASE WHEN region_southwest = 1 THEN 1 ELSE 0 END) AS count_southwest,
        SUM(CASE WHEN region_northwest = 1 THEN 1 ELSE 0 END) AS count_northwest,
        SUM(CASE WHEN region_southeast = 1 THEN 1 ELSE 0 END) AS count_southeast,
        SUM(CASE WHEN region_northeast = 1 THEN 1 ELSE 0 END) AS count_northeast
        FROM charges_table'''
result_df = pd.read_sql_query(query, conn)
print(result_df)
# Some takeaways from our queries - our highest charges are in the 50-60k range, and all observations have above average BMIs. Charges go up significantly with both age group and smoker status. The final query is more of a data quality check, it appears we have roughly the same number of observations from every region, and each region is represented enough to draw conclusions from

# Let's now take a look at correlations to confirm our suspicions about age, BMI, and smoker status impacting charges
print(charges_df.corr()['charges'].sort_values())
# As we can see, age, BMI, and smoker status all have positive correlations with our charges variables, albeit to varying magnitudes.

# As a final check before we begin to build any models, let's make sure we have enough observations for these binary variables ie. smoker_yes and sex_female
count_smokers = charges_df['smoker_yes'].sum()
count_non_smokers = len(charges_df) - count_smokers
print('Number of smokers: ' + str(count_smokers) + ', Number of non-smokers: ' + str(count_non_smokers))
count_females = charges_df['sex_female'].sum()
count_males = len(charges_df) - count_females
print('Number of females: ' + str(count_females) + ', Number of males: ' + str(count_males))
# Our male to female ratio is exceptional, however I do think we have an underrepresentation of smokers (20% of the data). Let's address this problem before building out our model, so as to not introduce any bias

# First, let's split our data into training and testing data for our regression model. We can address the bias later. We need to drop age_group now, as it isn't numerical and therefore cannot be run in a regression. If we wanted to, we could repeat the process for regions using bins, however this is a bit redundant with our age variable
X = charges_df.drop(['age_group', 'charges'], axis=1)
y = charges_df['charges']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=6)
train_charges_df = pd.concat([X_train, y_train], axis=1)
count_smokers = train_charges_df['smoker_yes'].sum()
count_non_smokers = len(train_charges_df) - count_smokers
print('Number of smokers: ' + str(count_smokers) + ', Number of non-smokers: ' + str(count_non_smokers))

# I have decided to perform undersampling here, as bringing the number of non-smokers to 216 keeps us well above our 30 observations per feature restriction. We have 9 features so we need at a minimum 270 observations, and we would have 432
nonsmokers_train_df = train_charges_df[train_charges_df['smoker_yes'] == 0]
random_sample = nonsmokers_train_df.sample(n=216, random_state=6)
unbiased_train_charges_df = pd.concat([train_charges_df[train_charges_df['smoker_yes'] == 1], random_sample], axis=0)
new_X_train = unbiased_train_charges_df.drop('charges', axis=1)
new_y_train = unbiased_train_charges_df['charges']

# Finally, let's run our model and determine how our features interact with charges
model = LinearRegression()
model.fit(new_X_train, new_y_train)
y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
n = X_test.shape[0]
p = X_test.shape[1]
adj_r2 = 1 - ((1 - r2) * (n - 1)) / (n - p - 1)
rmse = mean_squared_error(y_test, y_pred, squared=False)
coefficients = model.coef_
intercept = model.intercept_
print(r2)
print(adj_r2)
print(rmse)
print(X_train.columns)
print(coefficients)
print(intercept)
