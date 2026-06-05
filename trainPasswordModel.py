import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pickle


# Load the data from dataset file 
df = pd.read_csv('password_data.csv')

# separate features and labels 
x = df.drop(['password', 'label'], axis=1) # Features (10 numbers)
y = df['label'] # labels (0,1, or 2)



# This will print all of the features declared in the dataset file
print("Features the model will learn from: ")
x_columns = x.columns.tolist()
print(x_columns)

# Split data: 80% for training, 20% for testing
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)


print(f"Training data: {len(x_train)} passwords")
print(f"Training data: {len(x_test)} passwords")

# normalize geatures (make them on same scale)
scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

# create and train the model 
# Random forest = ensemble of decision trees
model = RandomForestClassifier(n_estimators=100, random_state=42)

print('Training the model...')
model.fit(x_train, y_train)
print('Training complete!!')

print("\nClasses learned:")
print(model.classes_)

# test the model 
accuracy = model.score(x_test, y_test)
print(f"Model acuraccy: {accuracy * 100:.2f}%")

print('\nMost Important Features:')

for feature, importance in sorted(
    zip(x_columns, model.feature_importances_),
    key=lambda x: x[1],
    reverse=True
):
    if importance > 0.05:
        print(f" {feature}: {importance:.3f}")
        

#save the model for later use
with open ('password_model.pkl', 'wb') as f:
    pickle.dump((model, scaler), f)

print("Model saved")
