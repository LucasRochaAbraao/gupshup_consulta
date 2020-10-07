
class Resposta:
    def __init__(self, saldo):
        self.saldo = saldo

        self.saldo_baixo = f"""\
                Foi detectado saldo baixo no Gupshup.
                Saldo atual: {self.saldo}."""
    
        self.saldo_baixo_html = f"""\
                <html>
                <body>
                    <p>Olá,<br>
                    Foi detectado <i>saldo baixo</i> no Gupshup.<br>
                    Saldo atual: <b><mark>{self.saldo}</mark></b>
                    </p>
                </body>
                </html>"""
    
        self.saldo_atual = f"""\
                Atualmente o saldo no gupshup é de {saldo} mensagens."""

        self.saldo_atual_html = f"""\
                <html>
                <body>
                    <p>Olá,<br>
                    Atualmente o saldo no gupshup é de <b><mark>{saldo}</mark></b> mensagens.
                    </p>
                </body>
                </html>"""


