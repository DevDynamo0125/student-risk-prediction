import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns


# 1. Load dataset
data = pd.read_csv("student-data.csv")

# 2. Input features (X) and output label (y)
X = data[
    ["attendance", "study_hours", "previous_marks", "assignment_completion"]
]
y = data["risk"]

# 3. Split data into training and testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

# 4. Train the AI model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# 5. Test model
predictions = model.predict(X_test)

# 6. Accuracy
accuracy = accuracy_score(y_test, predictions)
print("Model accuracy:", accuracy)

# 7. Predict risk for a new student
new_student = [[70, 4, 60, 65]]
result = model.predict(new_student)

print("New student at risk?", "YES" if result[0] == 1 else "NO")

plt.figure(figsize=(8, 5))
sns.scatterplot(
    data=data,
    x="attendance",
    y="previous_marks",
    hue="risk",
    palette={0: "green", 1: "red"}
)

plt.title("Attendance vs Previous Marks")
plt.xlabel("Attendance (%)")
plt.ylabel("Previous Marks (%)")


plt.figure(figsize=(8, 5))
sns.scatterplot(
    data=data,
    x="study_hours",
    y="assignment_completion",
    hue="risk",
    palette={0: "green", 1: "red"}
)

plt.title("Study Hours vs Assignment Completion")
plt.xlabel("Study Hours")
plt.ylabel("Assignment Completion (%)")


features = [
    "attendance",
    "study_hours",
    "previous_marks",
    "assignment_completion"
]

data[features].hist(bins=10, figsize=(10, 6))
plt.suptitle("Feature Distributions")
plt.show()

