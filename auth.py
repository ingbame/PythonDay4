def get_cuentas():
    return {
        "daniel": {"saldo": 0, "password": "123456789"},
        "Eder": {"saldo": 0, "password": "abcdfg"}
    }

def verificar_password(cuenta, password):
    cuentas = get_cuentas()
    if cuenta in cuentas and cuentas[cuenta]["password"] == password:
        return True
    return False