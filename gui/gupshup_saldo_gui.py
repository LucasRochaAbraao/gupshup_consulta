import eel
import gupshup_api_saldo

eel.init('web')

@eel.expose
def consultar_saldo():
    return gupshup_api_saldo.consultar_saldo()

eel.start('main.html', size=(500, 350))
