import joblib
import pandas as pd

from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score

ROOT = Path(__file__).resolve().parents[1]

# =====================================
# Load Dataset
# =====================================

df = pd.read_csv(ROOT / "data" / "cleaned_data.csv")

print("Original Dataset Shape :", df.shape)

# =====================================
# Reduce Dataset Size (Optional)
# =====================================

if len(df) > 200000:
    df = df.sample(n=200000, random_state=42)

print("Training Dataset Shape :", df.shape)

# =====================================
# Date Features
# =====================================

df["Price Date"] = pd.to_datetime(df["Price Date"])

df["Day"] = df["Price Date"].dt.day
df["Month"] = df["Price Date"].dt.month
df["Year"] = df["Price Date"].dt.year

# =====================================
# Encode Categorical Columns
# =====================================

categorical_columns = [
    "STATE",
    "District Name",
    "Market Name",
    "Commodity",
    "Variety",
    "Grade",
]

encoders = {}

for col in categorical_columns:
    encoder = LabelEncoder()
    df[col] = encoder.fit_transform(df[col].astype(str))
    encoders[col] = encoder

# =====================================
# Features & Target
# =====================================

X = df[
    [
        "STATE",
        "District Name",
        "Market Name",
        "Commodity",
        "Variety",
        "Grade",
        "Day",
        "Month",
        "Year",
    ]
]

y = df["Modal_Price"]

# =====================================
# Train Test Split
# =====================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
)

# =====================================
# Optimized Random Forest
# =====================================

model = RandomForestRegressor(
    n_estimators=20,
    max_depth=15,
    min_samples_split=10,
    min_samples_leaf=5,
    max_features="sqrt",
    random_state=42,
    n_jobs=-1,
)

print("\nTraining Model...")

model.fit(X_train, y_train)

# =====================================
# Evaluation
# =====================================

pred = model.predict(X_test)

print("\n========== Model Performance ==========")
print("R2 Score :", round(r2_score(y_test, pred), 4))
print("MAE :", round(mean_absolute_error(y_test, pred), 2))

# =====================================
# Save Model
# =====================================

models_dir = ROOT / "models"
models_dir.mkdir(exist_ok=True)

joblib.dump(
    model,
    models_dir / "random_forest.pkl",
    compress=3,
)

joblib.dump(
    encoders,
    models_dir / "encoders.pkl",
)

print("\n✅ Model Saved Successfully!")
print("Location :", models_dir / "random_forest.pkl")