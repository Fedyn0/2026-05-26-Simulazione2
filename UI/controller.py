import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDsRating(self):
        ratings = self._model.getAllRatings()

        for rating in ratings:
            self._view._ddrating1.options.append(
                ft.dropdown.Option(rating)
            )
            self._view._ddrating2.options.append(
                ft.dropdown.Option(rating)
            )

        self._view.update_page()

    def handleCreaGrafo(self, e):

        self._view.txt_result.controls.clear()

        if self._view._ddrating1.value is None or self._view._ddrating2.value is None:
            self._view.create_alert("Selezionare rank dai campi voto")
            self._view.update_page()
            return

        self._model.creaGrafo(self._view._ddrating1.value, self._view._ddrating2.value)

        self._view.txt_result.controls.append(
            ft.Text(f"Grafo correttamente creato")
        )

        nNodi, nArchi = self._model.getDettagliGrafo()

        self._view.txt_result.controls.append(
            ft.Text(f"Numero di nodi: {nNodi}")
        )

        self._view.txt_result.controls.append(
            ft.Text(f"Numero di archi: {nArchi}")
        )

        self._view.txt_result.controls.append(
            ft.Text(f"Top 5 archi:")
        )

        archi = self._model.getArchiPesoMaggiore()
        for a in archi:
            self._view.txt_result.controls.append(
                ft.Text(f"{a[0].name} <-> {a[1].name}: {a[2]}")
            )

        lun, largest = self._model.getCompConn()
        self._view.txt_result.controls.append(
            ft.Text(f"Il grafo ha {lun} componenti connesse")
        )

        self._view.txt_result.controls.append(
            ft.Text(f"La più grande componente connessa è lunga {len(largest)}")
        )

        for i in largest:
            self._view.txt_result.controls.append(
                ft.Text(f"{i.name}")
            )

        self._view.update_page()

    def handleCammino(self, e):
        pass