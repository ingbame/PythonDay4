from enums.msg_colors import bcolors

class SaldoInsuficienteError(Exception):
    def __init__(self, saldo_actual, cantidad_retirada):
        super().__init__(f"{bcolors.FAIL}Saldo insuficente: intentaste retirar {cantidad_retirada} pero solo tienes {saldo_actual}{bcolors.ENDC}")
        self.saldo_actual = saldo_actual
        self.cantidad_retirada = cantidad_retirada

class InvalidoError(Exception):
    def __init__(self, mensaje):
        self.mensaje = mensaje
    
class CuentaInvalidadError(InvalidoError):
    def __init__(self, mensaje=f'{bcolors.FAIL}Cuenta no valida{bcolors.ENDC}'):
        super().__init__(mensaje)

class OpcionInvalidaError(InvalidoError):
    def __init__(self):
        super().__init__(mensaje=f'{bcolors.FAIL}Opcion no valida{bcolors.ENDC}')