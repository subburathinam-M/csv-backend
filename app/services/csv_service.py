import pandas as pd
import zipfile
from io import BytesIO


def process_csv(file_bytes: bytes):
    """
    Process CSV and return zip with 3 excel files:
    1. duplicates.xlsx      - all duplicate rows (all occurrences)
    2. unique.xlsx          - unique rows (first occurrence of each)
    3. duplicate_grouped.xlsx - duplicate rows values in single column
    """
    # ── Read CSV ───────────────────────────────────────
    df = pd.read_csv(BytesIO(file_bytes))

    # ── 1. All duplicate rows (all occurrences) ─────────
    duplicate_mask = df.duplicated(keep=False)
    df_duplicates = df[duplicate_mask].reset_index(drop=True)

    # ── 2. Unique rows only ─────────────────────────────
    df_unique = df.drop_duplicates(keep='first').reset_index(drop=True)

    # ── 3. Duplicate rows → single column (comma-separated) ─
    if not df_duplicates.empty:
        # Get unique duplicate values only (drop duplicate duplicates)
        df_grouped = df_duplicates.drop_duplicates().copy()
        df_grouped["combined"] = df_grouped.astype(str).agg(",".join, axis=1)
        df_single_col = df_grouped[["combined"]]
    else:
        # Empty DataFrame with header
        df_single_col = pd.DataFrame(columns=["combined"])

    # ── Write ZIP ───────────────────────────────────────
    zip_buffer = BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for filename, dataframe in [
            ("duplicates.xlsx", df_duplicates),
            ("unique.xlsx", df_unique),
            ("duplicate_grouped.xlsx", df_single_col),
        ]:
            excel_buf = BytesIO()
            dataframe.to_excel(excel_buf, index=False)
            excel_buf.seek(0)
            zf.writestr(filename, excel_buf.read())

    zip_buffer.seek(0)

    stats = {
        "total_rows": len(df),
        "duplicate_rows": len(df_duplicates),
        "unique_rows": len(df_unique),
    }

    print("\n" + "="*30)
    print("CSV PROCESS STATS:")
    print(stats)
    print("="*30 + "\n")
    # ----------------------------------

    return zip_buffer, stats