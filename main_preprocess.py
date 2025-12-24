from modules.db_manager import create_table, insert_dataframe
from modules.preprocess_utils import process_excel
from pathlib import Path

EXCEL_PATH = Path("testset.xlsx")

def main():
    if not EXCEL_PATH.exists():
        print("❌ Excel file not found.")
        return

    print(f"📂 Processing file: {EXCEL_PATH.name}")
    df = process_excel(EXCEL_PATH)
    create_table()
    insert_dataframe(df, if_exists="replace")
    print(f"✅ {len(df)} rows inserted into weather.db")

if __name__ == "__main__":
    main()





