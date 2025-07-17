import requests
import pandas as pd
from sqlalchemy import create_engine

# Conexión a Supabase
conn_string = "postgresql://postgres:4224@db.qlrispqcjzartcbrykxj.supabase.co:5432/postgres"
engine = create_engine(conn_string)
TABLE_NAME = "cursos_api"

# API
API_URL = "https://bi-sanatorioallende.cluster-gyc.com/web/WSJSON/WS_coursesxuser.php"
API_KEY = "13fc60029b7d40f2c96ecf29207b87f9"

# Función para obtener datos de la API
def get_data_from_api():
    def get_page(page):
        payload = {
            "userid": "", "courseid": "", "category": "",
            "exclude_course_programs": 0, "days_activity": "TODOS",
            "blegajo": "", "soloaprobados": 0, "solofinalizados": 0,
            "exclude_tipo_programs": 0, "key": API_KEY, "page": page
        }
        r = requests.post(API_URL, json=payload)
        r.raise_for_status()
        json_data = r.json()
        return json_data.get("data", [])

    first_page = get_page(0)
    all_data = [item for sublist in first_page for item in sublist]
    total_pages = int(requests.post(API_URL, json=payload).json()["paging"]["totalpages"])

    for page in range(1, total_pages):
        page_data = get_page(page)
        flat = [item for sublist in page_data for item in sublist]
        all_data.extend(flat)

    return all_data

# Función para cargar a Supabase
def load_to_supabase(data):
    df = pd.DataFrame(data)
    df["inserted_at"] = pd.Timestamp.now()
    df.to_sql(TABLE_NAME, engine, if_exists="append", index=False)
    print(f"Cargadas {len(df)} filas en Supabase.")

# Ejecutar todo
if __name__ == "__main__":
    data = get_data_from_api()
    load_to_supabase(data)
