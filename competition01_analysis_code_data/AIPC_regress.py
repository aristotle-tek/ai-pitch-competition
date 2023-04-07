

#---------------
# Conclusions
#---------------

"""

- Q: Is the final score the product of the component dimensions? Yes, we can predict the final score quite well from the components (R^2=0.96).

- Q: Does it consider each dimension equally? Not quite, it places more emphasis on growth_potential, and less on leveraging_collaboration 
    - (technically can't just read this off the coef plot, but they have about the same mean, range so still holds)
    - For example, say A got 5/10 in growth_potential but 7/10 in collaboration, while B got 7/10 in growth but 5/10 in collaboration. B would come out 1.7 points ahead in the overall score, all else equal.

- Q: Does it matter who one gets compared to? Yes. Including the opponent score is statistically significant, though the effect is small. As expected the coefficient is negative, suggesting that when paired against a better competitor, the rating is lower.


- Q: Is there any value to your algorithm, beyond just 1-shot asking GPT? The results are definitely different, unfortunately there's no ground truth with this example, but I believe so. The correlation between my algorithm and a one-shot prompt is .4. While I standardized the scores, it's clear that the algorithm score is more evenly spread, in constrast to the 1-shot score which tends to bunch around the upper end of the scale (like humans, esp in the US?)



"""

import pandas as pd
import json
import random
import os
import pandas as pd


import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

import statsmodels.api as sm





df = pd.read_csv("all_round15.csv")

feature_columns = ['growth_potential', 'creativity', 'transformative_potential',
                   'leveraging_collaboration', 'risk_immunity', 'opponent_score']
target_column = 'overall_score'



X = df[feature_columns]
y = df[target_column]


model = LinearRegression()
model.fit(X, y)


y_pred = model.predict(X)



r2 = r2_score(y, y_pred)
mse = mean_squared_error(y, y_pred)
rmse = np.sqrt(mse)

print("R-squared:", r2)
print("Mean Squared Error:", mse)
print("Root Mean Squared Error:", rmse)

# R-squared: 0.9636968284000996
# Mean Squared Error: 1.5259961695561992
# Root Mean Squared Error: 1.235312174940488


plt.scatter(y, y_pred, alpha=0.5)
plt.xlabel("Overall Score")
plt.ylabel("Predicted Values")
plt.title("Overall Score vs Predicted from Components (incl Opponent Score)")

# Plot the diagonal line
diagonal_line = np.linspace(min(y.min(), y_pred.min()), max(y.max(), y_pred.max()), 100)
plt.plot(diagonal_line, diagonal_line, color='red', linestyle='--')

plt.show()





#------ with statsmodels

# Add constant
X = sm.add_constant(X)


model = sm.OLS(y, X).fit()



coef = model.params
std_err = model.bse
p_values = model.pvalues




# Plot coefs with se
fig, ax = plt.subplots()
coef.plot(kind='bar', yerr=std_err, ax=ax, color='blue', alpha=0.5)

ax.set_xticklabels(feature_columns + ['Intercept'], rotation=20, ha='right')

# Add horizontal lines for the p-value threshold (0.05)
ax.axhline(y=0, linestyle='--', color='black', linewidth=0.8)
ax.axhline(y=0.05, linestyle='--', color='red', linewidth=0.8)
ax.axhline(y=-0.05, linestyle='--', color='red', linewidth=0.8)

# Set the plot title and labels
ax.set_title('Coefficient plot with standard errors')
ax.set_xlabel('Predictor variables')
ax.set_ylabel('Coefficients')

plt.show()


#---------------
# pred without knowing opponent score



feature_columns = ['growth_potential', 'creativity', 'transformative_potential',
                   'leveraging_collaboration', 'risk_immunity']
target_column = 'overall_score'



X = df[feature_columns]
y = df[target_column]


model = LinearRegression()
model.fit(X, y)


y_pred = model.predict(X)



r2 = r2_score(y, y_pred)
mse = mean_squared_error(y, y_pred)
rmse = np.sqrt(mse)

print("R-squared:", r2)
print("Mean Squared Error:", mse)
print("Root Mean Squared Error:", rmse)

# R-squared: 0.9627251113093148
# Mean Squared Error: 1.5668420927381272
# Root Mean Squared Error: 1.2517356321276978


plt.scatter(y, y_pred, alpha=0.5)
plt.xlabel("Overall Score")
plt.ylabel("Predicted Values")
plt.title("Overall Score vs Predicted from Components")
diagonal_line = np.linspace(min(y.min(), y_pred.min()), max(y.max(), y_pred.max()), 100)
plt.plot(diagonal_line, diagonal_line, color='red', linestyle='--')

plt.show()



#------------
# coef plot
X = sm.add_constant(X)


model = sm.OLS(y, X).fit()



coef = model.params
std_err = model.bse
p_values = model.pvalues


fig, ax = plt.subplots()
coef[1:].plot(kind='bar', yerr=std_err[1:], ax=ax, color='blue', alpha=0.5)

ax.set_xticklabels(feature_columns, rotation=20, ha='right')
#ax.set_xticklabels(feature_columns + ['Intercept'], rotation=20, ha='right')

# Add horizontal lines for the p-value threshold (0.05)
ax.axhline(y=0, linestyle='--', color='black', linewidth=0.8)
ax.axhline(y=0.05, linestyle='--', color='red', linewidth=0.8)
ax.axhline(y=-0.05, linestyle='--', color='red', linewidth=0.8)

ax.set_title('Coefficient plot')
ax.set_xlabel('Predictor variables')
ax.set_ylabel('Coefficients')

plt.show()


#-------------------------
#  FINAL alg vs 1-shot
#-------------------------


dfo = pd.read_csv(data_dir + "final_ratings_norm_rnd15.csv")

df1 = pd.read_csv(data_dir + "all_1shot_apr1.csv")


from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()

dfo['score_alg'] = scaler.fit_transform(dfo[['final_rating']])


df1['score_1shot'] = scaler.fit_transform(df1[['result']])

df1 = df1.loc[:,['name', 'score_1shot']]
df1.columns = ['business', 'score_1shot']
mg = pd.merge(dfo, df1, on='business')


y = mg.score_1shot
y_pred = mg.score_alg
plt.scatter(mg.score_1shot, mg.score_alg, alpha=0.5)
plt.xlabel("1-Shot Score") # x is first.
plt.ylabel("Algorithm Score")
plt.title("1-Shot Score vs Algorithm Score")

diagonal_line = np.linspace(min(y.min(), y_pred.min()), max(y.max(), y_pred.max()), 100)
plt.plot(diagonal_line, diagonal_line, color='red', linestyle='--')

plt.show()



np.corrcoef(mg.score_1shot, mg.score_alg)

# correlation - .4







