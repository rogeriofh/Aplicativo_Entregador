from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
import sqlite3

class DeliveryApp(App):
    def build(self):
        self.title = 'Gerenciador de Entregas'
        self.sm = ScreenManager()

        # Tela para adicionar entrega
        add_screen = Screen(name='add')
        add_screen.add_widget(self.create_add_screen())
        self.sm.add_widget(add_screen)

        # Tela para visualizar entregas
        view_screen = Screen(name='view')
        view_screen.add_widget(self.create_view_screen())
        self.sm.add_widget(view_screen)

        return self.sm

    def create_add_screen(self):
        layout = BoxLayout(orientation='vertical')

        self.codigo_input = TextInput(hint_text="Código da Entrega")
        self.nome_cliente_input = TextInput(hint_text="Nome do Cliente")
        self.data_entrega_input = TextInput(hint_text="Data da Entrega")
        self.horario_input = TextInput(hint_text="Horário da Entrega")

        self.save_button = Button(text="Salvar Entrega")
        self.save_button.bind(on_press=self.save_delivery)

        self.view_button = Button(text="Minhas Entregas")
        self.view_button.bind(on_press=self.switch_to_view_screen)

        layout.add_widget(Label(text="Registre uma nova entrega:"))
        layout.add_widget(self.codigo_input)
        layout.add_widget(self.nome_cliente_input)
        layout.add_widget(self.data_entrega_input)
        layout.add_widget(self.horario_input)
        layout.add_widget(self.save_button)
        layout.add_widget(self.view_button)

        return layout

    def create_view_screen(self):
        layout = BoxLayout(orientation='vertical')

        self.view_label = Label(text="Minhas Entregas:")
        self.back_button = Button(text="Voltar", on_press=self.switch_to_add_screen)
        self.delete_button = Button(text="Excluir", on_press=self.delete_selected_delivery)  # Botão para excluir

        layout.add_widget(self.view_label)
        layout.add_widget(self.back_button)
        layout.add_widget(self.delete_button)  # Adiciona o botão de exclusão

        return layout

    def save_delivery(self, instance):
        codigo = self.codigo_input.text
        nome_cliente = self.nome_cliente_input.text
        data_entrega = self.data_entrega_input.text
        horario = self.horario_input.text

        # Conecta-se ao banco de dados SQLite (ou cria um se não existir)
        with sqlite3.connect('deliveries.db') as conn:
            cursor = conn.cursor()

            # Cria a tabela se não existir
            cursor.execute('''CREATE TABLE IF NOT EXISTS deliveries
                              (id INTEGER PRIMARY KEY AUTOINCREMENT,
                               codigo TEXT,
                               nome_cliente TEXT,
                               data_entrega TEXT,
                               horario TEXT)''')

            # Insere os dados da entrega no banco de dados
            cursor.execute("INSERT INTO deliveries (codigo, nome_cliente, data_entrega, horario) VALUES (?, ?, ?, ?)",
                           (codigo, nome_cliente, data_entrega, horario))

        # Limpa os campos de entrada após salvar
        self.codigo_input.text = ''
        self.nome_cliente_input.text = ''
        self.data_entrega_input.text = ''
        self.horario_input.text = ''

    def delete_selected_delivery(self, instance):
        selected_item = self.rv.data[self.rv.layout_manager.selected_nodes[0]]  # Obtém o item selecionado

        # Conecta-se ao banco de dados SQLite
        with sqlite3.connect('deliveries.db') as conn:
            cursor = conn.cursor()

            # Exclui o item do banco de dados
            cursor.execute("DELETE FROM deliveries WHERE codigo=?", (selected_item['text'].split(' ')[1],))

        # Atualiza a visualização após a exclusão
        self.update_view_label()

    def switch_to_view_screen(self, instance):
        self.update_view_label()
        self.sm.current = 'view'

    def update_view_label(self):
        # Conecta-se ao banco de dados e recupera os dados das entregas
        with sqlite3.connect('deliveries.db') as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM deliveries")
            deliveries = cursor.fetchall()

        # Atualiza o rótulo de visualização com os dados das entregas
        items_text = "\n".join([f"Código: {item[1]}, Nome: {item[2]}, Data: {item[3]}, Horário: {item[4]}" for item in deliveries])
        self.view_label.text = f"Itens Armazenados:\n{items_text}"

    def switch_to_add_screen(self, instance):
        self.sm.current = 'add'

if __name__ == '__main__':
    DeliveryApp().run()


