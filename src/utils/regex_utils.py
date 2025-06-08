import re

def extraer_referencia(self, b):
    """Extrae el número de referencia."""
    m = re.search(r"Referencia:\s+(\d+)", b)
    return m.group(1) if m else None


def extraer_via(self, b):
    """Extrae el tipo de vía entre 'Vía:' y 'Plazas:'."""
    m = re.search(r"Vía:\s*([^:]+):", b)
    return m.group(1).strip().split('\n')[0].strip() if m else None


def extraer_plazas(self, b):
    """Extrae las plazas convocadas y libres."""
    m = re.search(r"Convocadas:\s+(\d+),\s+Libre:\s+(\d+)", b)
    return (m.group(1), m.group(2)) if m else (None, None)


def extraer_fecha_apertura(self, b):
    """Extrae la fecha de apertura (formato largo)."""
    m = re.search(r"de\s+(\d{1,2}\s+de\s+\w+\s+de\s+\d{4})", b)
    return m.group(1) if m else None


def extraer_fecha_fin(self, b):
    """Extrae la fecha de fin de solicitudes (formato corto)."""
    m = re.search(r"Fin del plazo de presentación de solicitudes:\s+(\d{2}/\d{2}/\d{4})", b)
    return m.group(1) if m else None


def extraer_titulo(self, b):
    """Extrae el bloque en mayúsculas antes de 'Vía:'."""
    m = re.search(r"([A-ZÁÉÍÓÚÜÑ0-9\s/().,\-]+?)\s*Vía:", b, re.DOTALL)
    return m.group(1).strip().split('\n')[-1] if m else None