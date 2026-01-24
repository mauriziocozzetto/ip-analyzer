from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import ipaddress

app = FastAPI()


@app.get("/api/{ip}/{cidr}")
def calculate_network(ip: str, cidr: int):
    try:
        # Ricostruiamo la stringa dell'interfaccia
        interface_str = f"{ip}/{cidr}"
        interfaccia = ipaddress.IPv4Interface(interface_str)
        rete = interfaccia.network

        return {
            "success": True,
            "result": {
                "Indirizzo di rete": str(rete.network_address),
                "Indirizzo di broadcast": str(rete.broadcast_address),
                "Maschera di sottorete": str(rete.netmask),
                "CIDR": f"/{rete.prefixlen}",
                "Primo indirizzo utile": str(rete.network_address + 1) if rete.num_addresses > 2 else "N/A",
                "Ultimo indirizzo utile": str(rete.broadcast_address - 1) if rete.num_addresses > 2 else "N/A",
                "Host utilizzabili": rete.num_addresses - 2 if rete.num_addresses > 2 else 0
            }
        }
    except (ipaddress.AddressValueError, ipaddress.NetmaskValueError) as e:
        return {"success": False, "error": f"Dati non validi: {e}"}
    except Exception as e:
        return {"success": False, "error": f"Errore imprevisto: {str(e)}"}


@app.get("/api/calculate")
def calculate_network_query(ip: str, cidr: int):
    return calculate_network(ip, cidr)


@app.get("/")
def read_index():
    return FileResponse('static/index.html')


app.mount("/static", StaticFiles(directory="static"), name="static")

# if __name__ == "__main__":
#    import uvicorn
#    uvicorn.run(app, host="127.0.0.1", port=8000)
