import pandas as pd
from datetime import datetime

def assign_codes(collaborators_df, codes_df):
    available = codes_df[codes_df["estado"] == "disponible"]

    if len(available) < len(collaborators_df):
        raise Exception("No hay suficientes códigos disponibles")

    assignments = []

    for i, row in collaborators_df.iterrows():
        code = available.iloc[i]["codigo"]
        assignments.append({
            "correo": row["correo"],
            "codigo": code,
            "fecha": datetime.now()
        })
        codes_df.loc[codes_df["codigo"] == code, "estado"] = "usado"

    return pd.DataFrame(assignments), codes_df
