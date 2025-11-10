import flet as ft

class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    # -------------------- INIT DD --------------------
    def fillDDYear(self):
        years = self._model.getYears()
        self._view._ddAnno.options.clear()
        for y in years:
            self._view._ddAnno.options.append(ft.dropdown.Option(str(y)))
        self._view.update_page()

    def fillDDCountry(self):
        # Se il Model espone getCountries(), usala.
        # In alternativa esponi DAO.getAllCountries() e chiamala da qui.
        countries = getattr(self._model, "getCountries", lambda: [])()
        self._view._ddCountry.options.clear()
        for c in countries:
            self._view._ddCountry.options.append(ft.dropdown.Option(c))
        self._view.update_page()

    # -------------------- CREA GRAFO --------------------
    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()

        country = self._view._ddCountry.value
        year = self._view._ddAnno.value
        if not country or not year:
            self._view.txt_result.controls.append(ft.Text("Seleziona Country e Year."))
            self._view.update_page()
            return

        try:
            n_nodes, n_edges = self._model.buildGraph(country, int(year))
            self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato:"))
            self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {n_nodes}"))
            self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {n_edges}"))
        except Exception as ex:
            self._view.txt_result.controls.append(ft.Text(f"Errore buildGraph: {ex}"))

        self._view.update_page()

    # -------------------- VOLUMI (Punto 1) --------------------
    def handleVolumi(self, e):
        self._view.txt_result.controls.clear()
        try:
            rows = self._model.getRetailersVolume()
            if not rows:
                self._view.txt_result.controls.append(ft.Text("Nessun dato di volume."))
            else:
                self._view.txt_result.controls.append(ft.Text("Volumi retailer (decrescente):"))
                for r, vol in rows:
                    self._view.txt_result.controls.append(
                        ft.Text(f"{r.retailer_name} ({r.country})  ->  volume={vol}")
                    )
        except Exception as ex:
            self._view.txt_result.controls.append(ft.Text(f"Errore calcolo volumi: {ex}"))

        self._view.update_page()

    # -------------------- PUNTO 2: ciclo chiuso di esatti N archi --------------------
    def handleCerca(self, e):
        # N preso dal TextField come nel tuo esempio (_txtIntK -> qui _txtIntN)
        n_str = self._view._txtIntN.value
        self._view.txt_result.controls.clear()

        if not n_str or not n_str.isdigit():
            self._view.txt_result.controls.append(ft.Text("Inserisci N intero (>=3)."))
            self._view.update_page()
            return

        N = int(n_str)
        if N < 3:
            self._view.txt_result.controls.append(ft.Text("N deve essere almeno 3."))
            self._view.update_page()
            return

        try:
            path, total = self._model.getCamminoOttimo(N)
            if not path:
                self._view.txt_result.controls.append(ft.Text(f"Nessun ciclo di lunghezza esatta {N}."))
            else:
                self._view.txt_result.controls.append(ft.Text(f"Somma totale pesi: {total}"))
                self._view.txt_result.controls.append(ft.Text("Percorso:"))
                for i in range(len(path) - 1):
                    a, b = path[i], path[i + 1]
                    w = self._model._graph[a][b]["weight"]
                    self._view.txt_result.controls.append(
                        ft.Text(f"{a.retailer_name} —> {b.retailer_name} : {w}")
                    )
        except Exception as ex:
            self._view.txt_result.controls.append(ft.Text(f"Errore ricerca percorso: {ex}"))

        self._view.update_page()
