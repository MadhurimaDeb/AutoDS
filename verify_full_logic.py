import sys
import os

sys.path.append(os.getcwd())

print("🔍 Verifying Full Logic Dependencies...")

try:
    import plotly
    print("✅ Plotly installed")
except ImportError:
    print("❌ Plotly MISSING")

try:
    import sklearn
    print("✅ scikit-learn installed")
except ImportError:
    print("❌ scikit-learn MISSING")

try:
    import google.generativeai
    print("✅ google-generativeai installed")
except ImportError:
    print("❌ google-generativeai MISSING")

print("\n🔍 Verifying New Modules...")
modules = [
    "modules.chat",
    "modules.data_preparation.manual.main",
    "modules.data_preparation.auto.main",
    "modules.eda.manual.main",
    "modules.eda.auto.main",
    "modules.feature_engineering.manual.main",
    "modules.feature_engineering.auto.main",
    "modules.ml.manual.main",
    "modules.ml.auto.main",
    "modules.evaluation.manual.main",
    "modules.evaluation.auto.main",
    "modules.export.main"
]

print("\n🔍 Checking Neural Networks support...")
try:
    from sklearn.neural_network import MLPClassifier, MLPRegressor
    print("✅ MLP classes available")
except ImportError:
    print("❌ MLP not found (sklearn issue?)")

for mod in modules:
    try:
        __import__(mod)
        print(f"✅ {mod} imported successfully")
    except ImportError as e:
        print(f"❌ {mod} FAILED: {e}")
    except Exception as e:
        print(f"❌ {mod} FAILED (Runtime Error): {e}")

print("\nVerification Finished.")
