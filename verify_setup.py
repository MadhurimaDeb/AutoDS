import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

print("Verifying core...")
try:
    from core.data_manager import DataManager
    print("✅ Core DataManager imported")
except ImportError as e:
    print(f"❌ Core DataManager failed: {e}")

print("\nVerifying Module Imports...")
modules = [
    "modules.ImportData.main",
    "modules.data_preparation.main",
    "modules.eda.main",
    "modules.feature_engineering.main",
    "modules.ml.main",
    "modules.evaluation.main"
]

for mod in modules:
    try:
        __import__(mod)
        print(f"✅ {mod} imported")
    except ImportError as e:
        print(f"❌ {mod} failed: {e}")
    except Exception as e:
        print(f"❌ {mod} failed with error: {e}")

print("\nVerifying Submodule Structure...")
sub_modules = [
    "modules.data_preparation.manual.main",
    "modules.data_preparation.auto.main",
    "modules.eda.manual.main",
    "modules.eda.auto.main",
    "modules.feature_engineering.manual.main",
    "modules.feature_engineering.auto.main",
    "modules.ml.manual.main",
    "modules.ml.auto.main",
    "modules.evaluation.manual.main",
    "modules.evaluation.auto.main"
]

for sub in sub_modules:
    try:
        __import__(sub)
        print(f"✅ {sub} imported")
    except ImportError as e:
        print(f"❌ {sub} failed: {e}")

print("\nVerification Complete.")
