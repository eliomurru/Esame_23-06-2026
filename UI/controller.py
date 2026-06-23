from model.model import Model
from UI.view import View
import flet as ft

class Controller:
    def __init__(self, view : View, model : Model):
        self._view = view
        self._model = model

    def handler_crea_grafo(self, e):
        try:
            n_bus = int(self._view._txt_nBus.value)
        except ValueError:
            self._view.show_alert('Inserisci un valore numerico come numero di business')
            return
        if n_bus <= 0:
            self._view.show_alert('Inserisci un numero valido come numero di business')
            return
        self._model.build_graph(n_bus)
        self._view._lst_result.controls.clear()
        self._view._lst_result.controls.append(
            ft.Text(
                f"Grafo creato correttamente: Nodi : {self._model.num_nodi()}, Archi : {self._model.num_archi()}"
            )
        )
        utenti = self._model.get_nodi_grafo()
        if not utenti:
            self._view.show_alert('Nessun utente nel grafo')
            return
        self._view._ddUtente.options = [
            ft.dropdown.Option(text=u.name, key= str(u.user_id))
            for u in utenti
        ]
        self._view._ddUtente.disabled = False
        self._view._txtL.disabled = False
        self._view._btnUtentiConnessi.disabled = False
        self._view._btnSequenza.disabled = False

        self._view._ddUtente.update()
        self._view.update_page()

    def handler_utenti_connessi(self, e):
        lista_ordinata = self._model.classifica()
        self._view._lst_result.controls.clear()
        self._view._lst_result.controls.append(
            ft.Text(
                "Utenti ordinati in modo decrescente di strenght:\n"
            )
        )
        for u, strenght in lista_ordinata:
            self._view._lst_result.controls.append(
                ft.Text(
                    f"{u.name} ({u.user_id} - strenght: {strenght})"
                )
            )
        self._view.update_page()

    def handler_cerca_percorso(self):
        try:
            L = int(self._view._txtL.value)
        except ValueError:
            self._view.show_alert('Inserisci un valore valido per la lunghezza')
            return
        if L<2 or L>self._model.num_nodi():
            self._view.show_alert('L deve essere compreso tra 2 e il numero totale di nodi')
            return
        start_id = self._view._ddUtente.value
        if not start_id:
            self._view.show_alert('Seleziona un utente iniziale dalla lista')
            return
        path_ids, peso_totale = self._model.get_best_path(L,start_id)
        self._view._lst_result.controls.clear()
        if not path_ids:
            self._view.show_alert('Nessun percorso trovato')
            return
        self._view._lst_result.controls.append(
            ft.Text(
                f"Punteggio totale : {peso_totale}"
            )
        )
        self._view._lst_result.controls.append(
            ft.Text(
                "Sequenza trovata"
            )
        )
        for uid in path_ids:
            user = self._model.users_map[uid]
            self._view._lst_result.controls.append(
                ft.Text(
                    f"{user.name} ({user.user_id})"
                )
            )
        self._view.update_page()

