from fastapi import FastAPI
import ipaddress
from fastapi.responses import FileResponse

app = FastAPI()


@app.get("/")
def read_index():
    return FileResponse("index.html")


def get_network_details(ip: str, prefix: int):
    if not (2 <= prefix <= 30):
        return {"stato": "insuccesso", "messaggio": "Il prefisso deve essere compreso tra 2 e 30."}

    try:
        rete = ipaddress.ip_network(f"{ip}/{prefix}", strict=False)

        return {
            "stato": "successo",
            "dati": {
                "indirizzo_rete": str(rete.network_address),
                "subnet_mask": str(rete.netmask),
                "primo_ip_utile": str(rete[1]),
                "ultimo_ip_utile": str(rete[-2]),
                "indirizzo_broadcast": str(rete.broadcast_address),
                "num_host": rete.num_addresses - 2  # <--- Calcolo host utili
            }
        }
    except Exception as e:
        return {"stato": "insuccesso", "messaggio": f"Dati non validi: {str(e)}"}

# Unificato: Gestisce sia /networks/1.1.1.1/24 che /networks?ip=1.1.1.1&prefix=24


@app.get("/networks/{ip}/{prefix}")
@app.get("/networks")
def read_network(ip: str = None, prefix: int = None):
    if ip is None or prefix is None:
        return {"stato": "insuccesso", "messaggio": "IP e prefisso sono obbligatori."}
    return get_network_details(ip, prefix)
