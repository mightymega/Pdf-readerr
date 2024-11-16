from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
import fitz  # PyMuPDF


class PDFReaderApp(App):
    def build(self):
        self.title = "PDF Reader"
        self.current_page = 0
        self.doc = None

        self.layout = BoxLayout(orientation='vertical', spacing=10)
        self.pdf_image = Image(size_hint_y=None, height=500)

        # File Chooser
        self.file_chooser = FileChooserListView(on_selection=self.load_pdf)
        self.layout.add_widget(self.file_chooser)

        # Navigation buttons
        nav_layout = BoxLayout(size_hint_y=None, height=50)
        self.prev_btn = Button(text="Previous", on_press=self.previous_page, disabled=True)
        self.next_btn = Button(text="Next", on_press=self.next_page, disabled=True)
        nav_layout.add_widget(self.prev_btn)
        nav_layout.add_widget(self.next_btn)

        self.layout.add_widget(nav_layout)

        # Display Label
        self.page_label = Label(size_hint_y=None, height=30, text="No PDF Loaded")
        self.layout.add_widget(self.page_label)

        return self.layout

    def load_pdf(self, filechooser, selection):
        if selection:
            file_path = selection[0]
            try:
                self.doc = fitz.open(file_path)
                self.current_page = 0
                self.display_page(self.current_page)
                self.prev_btn.disabled = False
                self.next_btn.disabled = False
                self.page_label.text = f"Loaded: {file_path} (Page 1 of {self.doc.page_count})"
            except Exception as e:
                self.show_popup("Error", f"Failed to load PDF: {e}")

    def display_page(self, page_num):
        if self.doc:
            page = self.doc.load_page(page_num)
            pix = page.get_pixmap()
            img_data = pix.tobytes("png")

            # Save to a temporary file for Kivy Image
            with open("temp_page.png", "wb") as f:
                f.write(img_data)

            self.pdf_image.source = "temp_page.png"
            self.layout.add_widget(self.pdf_image)
            self.page_label.text = f"Page {page_num + 1} of {self.doc.page_count}"

    def previous_page(self, instance):
        if self.current_page > 0:
            self.current_page -= 1
            self.display_page(self.current_page)

    def next_page(self, instance):
        if self.current_page < self.doc.page_count - 1:
            self.current_page += 1
            self.display_page(self.current_page)

    def show_popup(self, title, message):
        popup_layout = BoxLayout(orientation="vertical", spacing=10)
        popup_layout.add_widget(Label(text=message))
        close_btn = Button(text="Close", size_hint_y=None, height=50)
        popup = Popup(title=title, content=popup_layout, size_hint=(0.8, 0.5))
        close_btn.bind(on_press=popup.dismiss)
        popup_layout.add_widget(close_btn)
        popup.open()


if __name__ == "__main__":
    PDFReaderApp().run()
