import pandas as pd
import os
from django.apps import apps
from django.conf import settings
from datetime import datetime

def make_timezone_naive(df):
    for col in df.select_dtypes(include=['datetimetz']).columns:
        df[col] = df[col].dt.tz_localize(None)
    return df

def export_selected_models_to_excel(model_list, file_path=None):
    """
    Export only specified models to Excel.
    
    Args:
        model_list (list): List of model classes (not strings).
        file_path (str): Optional full path to the output file.
        
    Returns:
        str: Path to the generated Excel file.
    """
    if file_path is None:
        file_name = f"partial_db_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        file_path = os.path.join(settings.BASE_DIR, file_name)

    writer = pd.ExcelWriter(file_path, engine='openpyxl')

    for model in model_list:
        model_name = model._meta.label.replace('.', '_')  # e.g., app_model
        try:
            queryset = model.objects.all().values()
            if queryset.exists():
                df = pd.DataFrame.from_records(queryset)
                df = make_timezone_naive(df)
                df.to_excel(writer, sheet_name=model_name[:31], index=False)
            else:
                pd.DataFrame().to_excel(writer, sheet_name=model_name[:31])
        except Exception as e:
            print(f"Error exporting {model_name}: {e}")
            continue

    writer.close()
    print(f"Selected models export completed: {file_path}")
    return file_path
