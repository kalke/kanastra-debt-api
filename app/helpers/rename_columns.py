def rename_columns(df):
    column_mapping = {
        'governmentId': 'government_id',
        'email': 'email',
        'debtAmount': 'debt_amount',
        'debtDueDate': 'debt_due_date',
        'debtId': 'id'
    }
    for old_name, new_name in column_mapping.items():
        df = df.rename({old_name: new_name})
    return df