from os import system, name
from getpass import getpass
from models.model_result import ResultModel
from enums.type_option import TypeOptionEnum
from enums.login_option import LoginOptionsEnum
from enums.account_option import AccountOptionsEnum
from enums.msg_colors import bcolors
from exceptions.bank_exc import SaldoInsuficienteError, OpcionInvalidaError, CuentaInvalidadError, InvalidoError
from auth import get_cuentas, verificar_password

cuentas = get_cuentas()

def depositar(cuenta_seleccionada):
    response = ResultModel()
    cantidad = float(input("ingrese la cantidad a depositar."))
    cuentas[cuenta_seleccionada]["saldo"] += cantidad
    clear()
    response.message = f"{bcolors.OKCYAN}Ha depositado {cantidad}. su saldo actual es {cuentas[cuenta_seleccionada]['saldo']}{bcolors.ENDC}"
    return response

def retirar(cuenta_seleccionada):
    response = ResultModel()
    cantidad = float(input("ingrese la cantidad a retirar."))
    cuenta = cuentas[cuenta_seleccionada]
    if cantidad > cuenta["saldo"]:
        raise SaldoInsuficienteError(cuenta["saldo"], cantidad)
    cuenta["saldo"] -= cantidad
    cuentas[cuenta_seleccionada]["saldo"] = cuenta["saldo"]
    clear()
    response.message = f"{bcolors.OKCYAN}Su saldo actual es {cuenta['saldo']}{bcolors.ENDC}"
    return response


def consultar(cuenta_seleccionada):
    response = ResultModel()
    clear()
    response.message = f"{bcolors.OKCYAN}su saldo actual es {cuentas[cuenta_seleccionada]['saldo']}{bcolors.ENDC}"
    return response

def transferir(cuenta_seleccionada):
    response = ResultModel()
    cuenta_destino = input("Ingrese la cuenta destino: ")
    if cuenta_destino not in cuentas:
        raise CuentaInvalidadError("Cuenta destino no es valida")
    
    cantidad = float(input("ingrese la cantidad a transferir."))
    if cantidad > cuentas[cuenta_seleccionada]["saldo"]:
        raise SaldoInsuficienteError(cuentas[cuenta_seleccionada]['saldo'], cantidad)
    
    cuentas[cuenta_seleccionada]["saldo"] -= cantidad
    cuentas[cuenta_destino]["saldo"] += cantidad
    clear()
    response.message = f"{bcolors.OKCYAN}Han sido tranferidos {cantidad} a {cuenta_destino}{bcolors.ENDC}"
    return response

def on_endSession():
    response = ResultModel()
    clear()
    response.message = f"{bcolors.WARNING}Sesión terminada. Hasta Pronto!{bcolors.ENDC}"
    return response
    
def salir():
    response = ResultModel()
    clear()
    response.message = f"{bcolors.OKCYAN}Gracias por usar nuestro banco. Hasta Pronto!{bcolors.ENDC}"
    return response

def mostrar_opciones(type: TypeOptionEnum):
    if type == TypeOptionEnum.Login:
        print(f"\n{LoginOptionsEnum.startSession.value}. Iniciar sesión")
        print(f"{LoginOptionsEnum.exit.value}. Salir")
        
        response = int(input(f"\n{bcolors.OKBLUE}Ingrese la opcion deseada:  {bcolors.ENDC}"))
        if response > len(LoginOptionsEnum):
            clear()
            raise OpcionInvalidaError()
        
    elif type == TypeOptionEnum.Account:                
        print(f"\n{AccountOptionsEnum.deposits.value}. Depositar dinero")
        print(f"{AccountOptionsEnum.withdrawals.value}. Retirar dinero")
        print(f"{AccountOptionsEnum.consult.value}. Consultar saldo")
        print(f"{AccountOptionsEnum.transfer.value}. Transferir dinero a otra cuenta")
        print(f"{AccountOptionsEnum.endSession.value}. Terminar sesión")
        print(f"{AccountOptionsEnum.exit.value}. Salir")
        
        response = int(input(f"\n{bcolors.OKBLUE}Ingrese la opcion deseada:  {bcolors.ENDC}"))
        if response > len(AccountOptionsEnum):
            clear()
            raise OpcionInvalidaError()
    else:
        clear()
        raise OpcionInvalidaError()
    return response

def logged(selected_account):
    while True:
        try:
            result = ResultModel()
            print(f"Cuenta: {selected_account}")
            print("\nSeleccione una opción: ")
            opcion = AccountOptionsEnum(mostrar_opciones(TypeOptionEnum.Account))
            
            if opcion == AccountOptionsEnum.deposits:
                result = depositar(selected_account)
            elif opcion == AccountOptionsEnum.withdrawals:
                result = retirar(selected_account)
            elif opcion == AccountOptionsEnum.consult:
                result = consultar(selected_account)
            elif opcion == AccountOptionsEnum.transfer:
                result = transferir(selected_account)
            elif opcion == AccountOptionsEnum.endSession:
                result = on_endSession()
                return result
            elif opcion == AccountOptionsEnum.exit:
                result = salir()
                result.success = False
                return result
            print(result.message)    
        except (CuentaInvalidadError, SaldoInsuficienteError, OpcionInvalidaError) as e:
            print(e.mensaje)
            
def clear(): 
    # for windows
    if name == 'nt':
        _ = system('cls') 
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

while True:
    try:
        result = ResultModel()
        selectedOption = LoginOptionsEnum(mostrar_opciones(TypeOptionEnum.Login))
        if selectedOption == LoginOptionsEnum.startSession:
            clear()
            print("Seleccione una cuenta: ")
            for cuenta in cuentas.keys():
                print(cuenta)
            cuenta_seleccionada = input()
            
            if cuenta_seleccionada not in cuentas:
                raise CuentaInvalidadError()
            
            print(f"{bcolors.WARNING}Por seguridad el password no se muestra al escribir\n{bcolors.ENDC}")
            password = getpass("\nIngrese su password: ")
            if not verificar_password(cuenta_seleccionada, password):
                raise CuentaInvalidadError(mensaje='Password incorrecto')
            
            result = logged(cuenta_seleccionada)  
            if not result.success:
                break
        elif selectedOption == LoginOptionsEnum.exit:
            result = salir()
            break
        print(result.message)
    except OpcionInvalidaError as ex:
        print(ex.mensaje)