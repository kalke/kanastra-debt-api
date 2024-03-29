from datetime import date

import polars as pl

from app.helpers.rename_columns import rename_columns

def test_rename_columns():
    mock_data = {
        'governmentId': ['123456789', '987654321'],
        'email': ['email1@example.com', 'email2@example.com'],
        'debtAmount': [1000.50, 2000.75],
        'debtDueDate': [date(2023, 1, 1), date(2023, 12, 31)],
        'debtId': ['debt1', 'debt2']
    }   

    df = pl.DataFrame(mock_data)

    renamed_df = rename_columns(df)

    assert "government_id" in renamed_df.columns
    assert "email" in renamed_df.columns
    assert "debt_amount" in renamed_df.columns
    assert "debt_due_date" in renamed_df.columns
    assert "id" in renamed_df.columns
    
