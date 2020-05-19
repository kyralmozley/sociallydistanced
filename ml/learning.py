import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import pickle

col_names = [
    'placeID', 'name', 'time', 'types', 'googleForecast', 'feelslike', 'temp', 'cloudcoverage','forecastCode', 'chanceRain', 'weekTrend', 'dayTrend',
    'tweets', 'label'
]
# import dataset
df = pd.read_csv('data.csv', names=col_names)

# remove null values, or any where the label is -1
df = df[~(df.label==-1)]
df.dropna()

y = df['label']
xs = df.drop(['placeID', 'name', 'label'], axis=1)

# hot enocde type of place data
google_types = []
for i in range(len(xs)):
    types = xs.iloc[i]['types'].strip('[]').replace("'",'').split(", ")
    for t in types:
        if t not in google_types:
            google_types.append(t)

for i in range(len(google_types)):
    xs[google_types[i]] = 0

for i in xs.index:
    types = xs.loc[i]['types'].strip('[]').replace("'",'').split(", ")
    for t in types:
        xs.at[i,t] = 1


xs = xs.drop(['types'], axis=1)
rf = RandomForestRegressor(random_state=0)
rf.fit(xs, y)
filename = "final_model.sav"
pickle.dump(rf, open(filename, 'wb'))
