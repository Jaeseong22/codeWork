import os
import librosa
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import classification_report

# 🔹 1. 데이터 폴더 경로 (자신의 경로로 수정)
DATA_DIR = "/Users/jaeseong/Desktop/Pyworkspace/data"

# 🔹 2. MFCC 특징 추출 함수 (평균값으로 축소)
def extract_mfcc_mean(file_path, n_mfcc=13):
    try:
        y, sr = librosa.load(file_path, sr=22050)
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
        return np.mean(mfcc, axis=1)
    except Exception as e:
        print(f"[오류] {file_path}: {e}")
        return None

# 🔹 3. 전체 데이터 로딩
X, y = [], []
SUPPORTED_EXTS = (".m4a", ".mp3", ".wav")

for label in os.listdir(DATA_DIR):
    class_dir = os.path.join(DATA_DIR, label)
    if not os.path.isdir(class_dir):
        continue
    for file_name in os.listdir(class_dir):
        if file_name.lower().endswith(SUPPORTED_EXTS):
            file_path = os.path.join(class_dir, file_name)
            features = extract_mfcc_mean(file_path)
            if features is not None:
                X.append(features)
                y.append(label)

X = np.array(X)
y = np.array(y)

# 🔹 4. 라벨 인코딩
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# 🔹 5. 교차검증 기반 SVM 모델 평가
model = SVC(kernel="linear", C=1)
cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)

print(f"🔍 클래스 목록: {le.classes_}")
print(f"🔍 총 샘플 수: {len(X)}")

# 전체 예측 결과 저장
y_pred_total = cross_val_predict(model, X, y_encoded, cv=cv)

# 🔹 6. classification_report 출력
print("\n📊 교차검증 결과:")
print(classification_report(y_encoded, y_pred_total, target_names=le.classes_))

# 🔹 7. 시각화
# 7-1. classification_report를 DataFrame으로 변환
report_dict = classification_report(y_encoded, y_pred_total, target_names=le.classes_, output_dict=True)
report_df = pd.DataFrame(report_dict).transpose()

# 7-2. 클래스별 precision, recall, f1-score만 추출
class_metrics = report_df.iloc[:len(le.classes_)][["precision", "recall", "f1-score"]]

# 7-3. 시각화
plt.figure(figsize=(10, 6))
class_metrics.plot(kind="bar", figsize=(10, 6), colormap="viridis")
plt.title("Classes Precision, Recall, F1-score")
plt.xlabel("Class")
plt.ylabel("Scores")
plt.ylim(0, 1.05)
plt.grid(axis='y')
plt.legend(loc="lower right")
plt.tight_layout()
plt.show()