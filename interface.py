import wx
import subprocess


class DoacaoSangue(wx.Frame):
    def __init__(self, parent, title):
        super(DoacaoSangue, self).__init__(parent, title=title, size=(700, 500))
        self.InitUI()

    def InitUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Título
        title = wx.StaticText(panel, label="sistema especialista de doação de sangue")
        font = title.GetFont()
        font.PointSize += 4
        font = font.Bold()
        title.SetFont(font)
        vbox.Add(title, flag=wx.ALIGN_CENTER | wx.TOP, border=10)

        # Área de consulta
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)

        self.query_label = wx.StaticText(panel, label="Consulta:")
        hbox1.Add(self.query_label, flag=wx.RIGHT, border=8)

        self.query_input = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
        hbox1.Add(self.query_input, proportion=1)

        self.run_btn = wx.Button(panel, label="Executar")
        self.run_btn.Bind(wx.EVT_BUTTON, self.OnRun)
        hbox1.Add(self.run_btn, flag=wx.LEFT, border=8)

        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # Área de resultados
        self.result_label = wx.StaticText(panel, label="Resultados:")
        vbox.Add(self.result_label, flag=wx.LEFT | wx.TOP, border=10)

        self.result_output = wx.TextCtrl(
            panel, style=wx.TE_MULTILINE | wx.TE_READONLY, size=(-1, 300)
        )
        vbox.Add(self.result_output, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)

        panel.SetSizer(vbox)

    def OnRun(self, event):
        # consulta do usuario
        query = self.query_input.GetValue()

        if not query:
            self.result_output.SetValue("insira consulta")
            return

        # consulta no prolog
        result = self.RunPrologQuery(query)
        self.result_output.SetValue(result)

    def RunPrologQuery(self, query):
        try:
            # executa SWI-Prolog
            process = subprocess.Popen(
                ["swipl", "-s", "base_conhecimento.pl", "-g", query, "-t", "halt."],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            stdout, stderr = process.communicate()

            # retorna resultado ou erro
            if stdout:
                return stdout.strip()
            if stderr:
                return f"Erro: {stderr.strip()}"
        except FileNotFoundError:
            return "swi-prolog nao encontrado"

        return "consulta sem resultados"


if __name__ == "__main__":
    app = wx.App()
    frame = DoacaoSangue(None, title="doacao de sangue")
    frame.Show()
    app.MainLoop()


