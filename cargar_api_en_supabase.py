import requests
from supabase import create_client, Client
import os

# Leer claves desde variables de entorno
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_total_pages():
    url = "https://bi-sanatorioallende.cluster-gyc.com/web/WSJSON/WS_coursesxuser.php?key=13fc60029b7d40f2c96ecf29207b87f9&DaysActivity=TODOS&page=0&perpage=1000"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error en la respuesta de la API: {response.status_code}")
        print(response.text)
        exit(1)

    try:
        data = response.json()
    except Exception as e:
        print(f"Error al parsear JSON: {e}")
        print(response.text)
        exit(1)

    if "paging" not in data or "totalpages" not in data["paging"]:
        print("Error durante el proceso: 'paging.totalpages' no está presente")
        print(data)
        exit(1)

    return int(data["paging"]["totalpages"])

def get_data():
    total_pages = get_total_pages()
    all_data = []

    for page in range(total_pages):
        print(f"Descargando página {page + 1} de {total_pages}")
        url = f"https://bi-sanatorioallende.cluster-gyc.com/web/WSJSON/WS_coursesxuser.php?key=13fc60029b7d40f2c96ecf29207b87f9&DaysActivity=TODOS&page={page}&perpage=1000"
        response = requests.get(url)

        try:
            data = response.json()
        except Exception as e:
            print(f"Error al leer la página {page}: {e}")
            continue

        if 'data' in data:
            all_data.extend(data['data'])
        else:
            print(f"Advertencia: no se encontró 'data' en la página {page}")
    
    return all_data

def insert_data(data):
    insertados = 0
    for row in data:
        try:
            # Filtrar solo las columnas que existen en Supabase
            cleaned_row = {k: row[k] for k in [
                'courseid', 'userid', 'lastname', 'firstname', 'email',
                'legajo', 'dni', 'status', 'mandatory', 'score',
                'course_name', 'hidden', 'active', 'duracion',
                'category_name', 'category', 'start_date', 'end_date',
                'tipo', 'nota', 'tiempo', 'certificado'
            ] if k in row}

            supabase.table("cursos_api").insert(cleaned_row).execute()
            insertados += 1
        except Exception as e:
            print(f"Error insertando fila: {e}")
            continue
    print(f"✔️ Inserción finalizada: {insertados} registros insertados.")

if __name__ == "__main__":
    datos = get_data()
    insert_data(datos)


