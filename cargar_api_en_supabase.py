import requests
from supabase import create_client, Client
import os

# Configuración Supabase
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# Parámetros base de la API
API_URL = "https://bi-sanatorioallende.cluster-gyc.com//web/WSJSON/WS_coursesxuser.php"
API_KEY = "13fc60029b7d40f2c96ecf29207b87f9"

def get_total_pages():
    """Obtiene la cantidad total de páginas desde la API"""
    params = {
        "key": API_KEY,
        "DaysActivity": "TODOS",
        "page": 0,
        "perpage": 1000
    }
    response = requests.get(API_URL, params=params)
    response.raise_for_status()
    data = response.json()
    return int(data["totalpages"])

def get_all_data():
    """Itera por todas las páginas y acumula los datos"""
    total_pages = get_total_pages()
    all_items = []

    for page in range(total_pages):
        print(f"Descargando página {page + 1} de {total_pages}")
        params = {
            "key": API_KEY,
            "DaysActivity": "TODOS",
            "page": page,
            "perpage": 1000
        }
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        if "data" in data:
            all_items.extend(data["data"])  # o el campo correcto si no se llama "data"
        else:
            print(f"Advertencia: No se encontró campo 'data' en la página {page}")
    
    return all_items

def cargar_en_supabase(data):
    """Carga los datos en una tabla de Supabase"""
    if not data:
        print("No hay datos para insertar.")
        return
    
    # Dividir en lotes de 500 si es necesario
    for i in range(0, len(data), 500):
        lote = data[i:i + 500]
        res = supabase.table("cursos_api").insert(lote).execute()
        print(f"Lote {i // 500 + 1}: {res.status_code}")

if __name__ == "__main__":
    try:
        datos = get_all_data()
        cargar_en_supabase(datos)
        print("Carga finalizada correctamente.")
    except Exception as e:
        print("Error durante el proceso:", e)
        
response = requests.get(url)
print(response.text)  # <-- AÑADÍ ESTO TEMPORALMENTE
data = response.json()


