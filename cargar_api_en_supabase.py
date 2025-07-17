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

    if 'totalpages' not in data:
        print("Error durante el proceso: 'totalpages'")
        print(data)
        exit(1)
    
    return int(data['totalpages'])

def get_data():
    total_pages = get_total_pages()
    all_data = []

    for page in range(total_pages):
        print(f"Descargando página {page + 1} de {total_pages}")
        url = f"https://bi-sanatorioallende.cluster-gyc.com/web/WSJSON/WS_coursesxuser.php?key=13fc60029b7d40f2c96ecf29207b87f9&DaysActivity=TODOS&page={page}&perpage=1000"
        response = requests.get(url)
        data = response.json()
        
        if 'data' in data:
            all_data.extend(data['data'])
        else:
            print(f"Advertencia: no se encontró 'data' en la página {page}")
    
    return all_data

def insert_data(data):
    for row in data:
        try:
            # Eliminar campos que no existen en tu tabla Supabase
            cleaned_row = {k: row[k] for k in [
                'courseid', 'userid', 'lastname', 'firstname', 'email', 'legajo', 'dni'
            ]}
            supabase.table("cursos_api").insert(cleaned_row).execute()
        except Exception as e:
            print(f"Error insertando fila: {e}")
            continue

if __name__ == "__main__":
    datos = get_data()
    insert_data(datos)
    print("Carga finalizada.")
