import pandas as pd


def read_csv(file_path):

    try:
        df = pd.read_csv(file_path)

        return {
            "success": True,
            "columns": list(df.columns),
            "rows": len(df),
            "data": df.to_dict(orient="records"),
        }

    except Exception as e:

        return {"success": False, "error": str(e)}
