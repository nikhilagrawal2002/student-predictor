from sklearn.linear_model import LinearRegression
import numpy as np

def predict_grade(assessments):
    if len(assessments) < 2:
        return assessments[-1] if assessments else 0
    X = np.array([[i] for i in range(len(assessments))])
    y = np.array(assessments)
    model = LinearRegression()
    model.fit(X, y)
    return round(model.predict([[len(assessments)]])[0], 2)
