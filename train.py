import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load data
df = pd.read_csv("/Users/ryanbakshi/Downloads/past_fight_data(csv).csv", index_col=0)

# Remove draws and convert stats to numeric
df = df[df['outcome'] != 'Draw'].copy()
stat_cols = ['F1_Str', 'F2_Str', 'F1_Td', 'F2_Td', 'F1_Kd', 'F2_Kd', 'F1_Sub', 'F2_Sub']
df[stat_cols] = df[stat_cols].apply(pd.to_numeric, errors='coerce')
df.dropna(inplace=True)

# Create difference features and target
df['diff_Str'] = df['F1_Str'] - df['F2_Str']
df['diff_Td'] = df['F1_Td'] - df['F2_Td']
df['diff_Kd'] = df['F1_Kd'] - df['F2_Kd']
df['diff_Sub'] = df['F1_Sub'] - df['F2_Sub']
df['target'] = (df['outcome'] == 'fighter1').astype(int)

# Swap fighters to reduce order bias
swapped = df.copy()
swapped[['fighter1', 'fighter2']] = df[['fighter2', 'fighter1']]
for stat in ['Str', 'Td', 'Kd', 'Sub']:
    swapped[f'F1_{stat}'], swapped[f'F2_{stat}'] = df[f'F2_{stat}'], df[f'F1_{stat}']
swapped['diff_Str'] = swapped['F1_Str'] - swapped['F2_Str']
swapped['diff_Td'] = swapped['F1_Td'] - swapped['F2_Td']
swapped['diff_Kd'] = swapped['F1_Kd'] - swapped['F2_Kd']
swapped['diff_Sub'] = swapped['F1_Sub'] - swapped['F2_Sub']
swapped['target'] = 1 - df['target']

# Combine and train model
final_df = pd.concat([df, swapped], ignore_index=True)
X = final_df[['diff_Str', 'diff_Td', 'diff_Kd', 'diff_Sub']]
y = final_df['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression()
model.fit(X_train, y_train)
print(f"Model accuracy: {accuracy_score(y_test, model.predict(X_test)):.2f}")

# Build average stats per fighter
fighter_stats = {}
fighters = pd.unique(final_df[['fighter1', 'fighter2']].values.ravel())
for fighter in fighters:
    rows1 = final_df[final_df['fighter1'] == fighter][['F1_Str', 'F1_Td', 'F1_Kd', 'F1_Sub']]
    rows2 = final_df[final_df['fighter2'] == fighter][['F2_Str', 'F2_Td', 'F2_Kd', 'F2_Sub']]
    avg = pd.concat([rows1.rename(columns=lambda x: x.replace('F1_', '').replace('F2_', '')) for rows1 in [rows1, rows2]]).mean()
    fighter_stats[fighter] = avg

# Predict outcome
f1 = input("Enter Fighter 1 name: ")
f2 = input("Enter Fighter 2 name: ")

if f1 not in fighter_stats or f2 not in fighter_stats:
    print("Fighter not found. Check spelling.")
else:
    diff = fighter_stats[f1] - fighter_stats[f2]
    input_df = pd.DataFrame([{
        'diff_Str': diff['Str'],
        'diff_Td': diff['Td'],
        'diff_Kd': diff['Kd'],
        'diff_Sub': diff['Sub']
    }])
    prob = model.predict_proba(input_df)[0][1]
    prob = np.clip(prob, 0.15, 0.85)
    print(f"Predicted winner: {f1 if prob > 0.5 else f2}")
    print(f"Probability {f1} wins: {prob:.2f}")
    print(f"Probability {f2} wins: {1 - prob:.2f}")
