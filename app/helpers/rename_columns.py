import polars as pl

def rename_columns(df: pl.DataFrame) -> pl.DataFrame:
    column_mapping = {
        'name': 'name',
        'governmentId': 'government_id',
        'email': 'email',
        'debtAmount': 'debt_amount',
        'debtDueDate': 'debt_due_date',
        'debtId': 'id'
    }

    for old_name, new_name in column_mapping.items():
        if old_name in df.columns:
            df = df.rename({old_name: new_name})
    return df
