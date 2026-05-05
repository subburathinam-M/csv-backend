from fastapi import FastAPI
from app.routers.csv_router import router as csv_router


app = FastAPI(
    title="CSV Processor API",
    description="""
    Upload a CSV file and get back a ZIP containing 3 Excel files:
    - **duplicates.xlsx**        → All duplicate rows (all occurrences)
    - **unique.xlsx**            → Unique rows (first occurrence of each)
    - **duplicate_grouped.xlsx** → All duplicate values in a single column
    """,
    version="1.0.0",
)

app.include_router(csv_router)


# @app.get("/")
# def root():
#     return {
#         "message": "CSV Processor API is running ✅",
#         "docs":    "Visit /docs to test the API"
#     }