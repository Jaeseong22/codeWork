# 전체 데이터셋: 10130건, 학습데이터셋:8104, 테스트데이터셋:2026 
# 전체 데이터셋과 테스트 데이터셋에 대한 혼동행렬 출력
# 성능이 우수한 SVM_linear, SVM_RBF, RF만 혼동행렬 출력 

# 분류 실험 (논문 Table II 참고) 
# All 데이터셋 Occupancy_Estimation.csv 사용
# scaler = StandardScaler() 사용
# 불균형 클래스 이므로 StratifiedKFold 사용: skf = StratifiedKFold(n_splits=10, shuffle=False)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis as QDA
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, classification_report
from sklearn.pipeline import Pipeline

# Load the dataset
file_path = 'Occupancy_Estimation.csv'
df = pd.read_csv(file_path)

# 특성과 타겟 분리
X = df.drop(['Date', 'Time', 'Room_Occupancy_Count'], axis=1)
y = df['Room_Occupancy_Count']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the data
scaler = StandardScaler()

# Initialize models
models = {
    "SVM_linear": SVC(kernel='linear', random_state=42),
    "SVM_RBF": SVC(kernel='rbf', random_state=42),
    "RF": RandomForestClassifier(n_estimators=30, random_state=42)
}

# Define StratifiedKFold
skf = StratifiedKFold(n_splits=10, shuffle=False)

# Perform experiments
results = {}
conf_matrices = {}
for name, model in models.items():
    # Create a pipeline with scaling only
    pipeline = Pipeline([
        ('scaler', scaler),
        ('classifier', model)
    ])
    
    # Perform cross-validation
    scores = cross_val_score(pipeline, X_train, y_train, cv=skf, scoring='accuracy')
    f1_scores = cross_val_score(pipeline, X_train, y_train, cv=skf, scoring='f1_macro')
    
    # Train the model on the full training data and evaluate on test data
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    
    test_accuracy = accuracy_score(y_test, y_pred)
    test_f1 = f1_score(y_test, y_pred, average='macro')
    
    # Store results
    results[name] = {
        "Cross-validated Accuracy": scores.mean(),
        "Cross-validated F1 Score": f1_scores.mean(),
        "Test Accuracy": test_accuracy,
        "Test F1 Score": test_f1
    }
    
    # Confusion matrix for test data
    conf_matrices[name] = confusion_matrix(y_test, y_pred)

# Confusion matrix for full dataset using the trained models
full_data_conf_matrices = {}
for name, model in models.items():
    pipeline = Pipeline([
        ('scaler', scaler),
        ('classifier', model)
    ])
    pipeline.fit(X, y)
    y_pred_full = pipeline.predict(X)
    full_data_conf_matrices[name] = confusion_matrix(y, y_pred_full)

# Plotting results
labels = list(results.keys())
cross_val_acc = [results[name]['Cross-validated Accuracy'] for name in labels]
cross_val_f1 = [results[name]['Cross-validated F1 Score'] for name in labels]
test_acc = [results[name]['Test Accuracy'] for name in labels]
test_f1 = [results[name]['Test F1 Score'] for name in labels]

x = range(len(labels))

fig, ax = plt.subplots(1, 2, figsize=(14, 6))

# Accuracy plot
ax[0].bar(x, cross_val_acc, width=0.4, label='Cross-validated Accuracy', align='center')
ax[0].bar([i + 0.4 for i in x], test_acc, width=0.4, label='Test Accuracy', align='center')
ax[0].set_xticks([i + 0.2 for i in x])
ax[0].set_xticklabels(labels)
ax[0].set_title('Accuracy Comparison')
ax[0].legend()

# Adding data labels
for i in x:
    ax[0].text(i, cross_val_acc[i] + 0.01, f"{cross_val_acc[i]:.4f}", ha='center')
    ax[0].text(i + 0.4, test_acc[i] + 0.01, f"{test_acc[i]:.4f}", ha='center')

# F1 Score plot
ax[1].bar(x, cross_val_f1, width=0.4, label='Cross-validated F1 Score', align='center')
ax[1].bar([i + 0.4 for i in x], test_f1, width=0.4, label='Test F1 Score', align='center')
ax[1].set_xticks([i + 0.2 for i in x])
ax[1].set_xticklabels(labels)
ax[1].set_title('F1 Score Comparison')
ax[1].legend()

# Adding data labels
for i in x:
    ax[1].text(i, cross_val_f1[i] + 0.01, f"{cross_val_f1[i]:.4f}", ha='center')
    ax[1].text(i + 0.4, test_f1[i] + 0.01, f"{test_f1[i]:.4f}", ha='center')

plt.tight_layout()
plt.show()

# Plot confusion matrices for test data
fig, axs = plt.subplots(1, 3, figsize=(18, 5))
for i, name in enumerate(labels):
    sns.heatmap(conf_matrices[name], annot=True, fmt='d', cmap='Blues', ax=axs[i])
    axs[i].set_title(f'{name} - Test Data Confusion Matrix')
    axs[i].set_xlabel('Predicted')
    axs[i].set_ylabel('Actual')

plt.tight_layout()
plt.show()

# Plot confusion matrices for full dataset
fig, axs = plt.subplots(1, 3, figsize=(18, 5))
for i, name in enumerate(labels):
    sns.heatmap(full_data_conf_matrices[name], annot=True, fmt='d', cmap='Greens', ax=axs[i])
    axs[i].set_title(f'{name} - Full Data Confusion Matrix')
    axs[i].set_xlabel('Predicted')
    axs[i].set_ylabel('Actual')

plt.tight_layout()
plt.show()
