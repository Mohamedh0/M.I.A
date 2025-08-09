# **Reporting**

## **1. Data Preprocessing**

1. **Missing Values**  
   - Checked for null values — no missing data found.

2. **Duplicate Records**  
   - Found duplicate rows and removed them from the dataset.

3. **Outlier Treatment**  
   - Detected outliers using the Interquartile Range (IQR) method.  
   - Applied capping to handle extreme values.

4. **Skewness Handling**  
   - Identified high skewness in the `Body temp` feature (`-1.0223`).  
   - Applied **reflection** followed by **log transformation** to reduce skewness.

5. **Multicollinearity Check**  
   - Calculated Variance Inflation Factor (VIF) — found that most features had high VIF values.

6. **Categorical Encoding**  
   - Applied **One-Hot Encoding** for categorical features.  
   - Dropped the first column to avoid dummy variable trap.

7. **Feature Engineering**  
   - Derived additional features based on domain knowledge.

8. **Rechecking Multicollinearity & Correlation**  
   - Conducted a second VIF check after feature engineering.  
   - Plotted a correlation heatmap to analyze relationships between features.

9. **Feature Selection**  
   - Used **XGBoost** with **SHAP explainer** to assess feature importance.  
   - Selected the top 5 most impactful features.

10. **Train-Test Preparation**  
    - Selected final features for modeling.  
    - Split dataset into training and validation sets.  
    - Removed ID columns from the test set and saved them separately.

11. **Scaling**  
    - Applied **RobustScaler** to handle outliers while scaling.

---

## **2. Modeling**

1. **Hyperparameter Tuning**  
   - Used **Optuna** for tuning parameters of:
     - XGBoost  
     - LightGBM  
     - RandomForest  

2. **Model Evaluation**  
   - Compared models using **Root Mean Square Error (RMSE)**.  
   - Evaluated single models vs. ensemble approaches.

3. **First Notebook — Voting Ensemble**  
   - Combined **XGBoost** and **LightGBM** using a **Voting Regressor**.

4. **Second Notebook — Stacking Ensemble**  
   - Stacked **XGBoost**, **LightGBM**, **RandomForest**, and **Ridge Regression**.
