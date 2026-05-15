from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.garden.mapview import MapView, MapMarker
import requests
from kivy.uix.image import Image
from kivy.garden.carousel import Carousel

API_URL = "http://10.0.2.2:8000"  # Android emulator localhost


class FindYourBranchApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.branches = []
        
    def build(self):
        self.title = "Find Your Branch"
        
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header = Label(text="Bank Branch & ATM Locator", size_hint_y=0.1, 
                      font_size='20sp', bold=True)
        main_layout.add_widget(header)
        
        # Search Box
        search_layout = BoxLayout(size_hint_y=0.1, spacing=5)
        self.search_input = TextInput(
            multiline=False,
            hint_text='Search branch name...',
            size_hint_x=0.8
        )
        search_btn = Button(text='Search', size_hint_x=0.2)
        search_btn.bind(on_press=self.search_branches)
        search_layout.add_widget(self.search_input)
        search_layout.add_widget(search_btn)
        main_layout.add_widget(search_layout)
        
        # Branches List
        scroll_view = ScrollView(size_hint=(1, 0.7))
        self.branches_grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.branches_grid.bind(minimum_height=self.branches_grid.setter('height'))
        scroll_view.add_widget(self.branches_grid)
        main_layout.add_widget(scroll_view)
        
        # Buttons
        button_layout = BoxLayout(size_hint_y=0.1, spacing=5)
        refresh_btn = Button(text='Refresh')
        refresh_btn.bind(on_press=self.load_branches)
        map_btn = Button(text='View Map')
        map_btn.bind(on_press=self.show_map)
        button_layout.add_widget(refresh_btn)
        button_layout.add_widget(map_btn)
        main_layout.add_widget(button_layout)
        
        self.load_branches(None)
        return main_layout
    
    def load_branches(self, instance):
        """Fetch branches from API"""
        try:
            response = requests.get(f"{API_URL}/branches", timeout=5)
            if response.status_code == 200:
                self.branches = response.json()
                self.display_branches(self.branches)
            else:
                self.show_error("Failed to load branches")
        except Exception as e:
            self.show_error(f"Connection error: {str(e)}")
    
    def search_branches(self, instance):
        """Search branches by name"""
        query = self.search_input.text.lower()
        filtered = [b for b in self.branches if query in str(b).lower()]
        self.display_branches(filtered if filtered else self.branches)
    
    def display_branches(self, branches):
        """Display branches in grid"""
        self.branches_grid.clear_widgets()
        
        if not branches:
            self.branches_grid.add_widget(
                Label(text='No branches found', size_hint_y=None, height=50)
            )
            return
        
        for branch in branches:
            branch_btn = Button(
                text=f"{branch.get('name', 'Branch')}\n{branch.get('location', 'Location')}",
                size_hint_y=None,
                height=60,
                background_color=(0.2, 0.6, 1, 1)
            )
            branch_btn.bind(on_press=lambda x, b=branch: self.show_branch_details(b))
            self.branches_grid.add_widget(branch_btn)
    
    def show_branch_details(self, branch):
        """Show branch details in popup"""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Branch info
        info_text = f"""
        Branch: {branch.get('name', 'N/A')}
        Location: {branch.get('location', 'N/A')}
        Address: {branch.get('address', 'N/A')}
        Phone: {branch.get('phone', 'N/A')}
        """
        
        info_label = Label(text=info_text, size_hint_y=0.8)
        content.add_widget(info_label)
        
        # Close button
        close_btn = Button(text='Close', size_hint_y=0.2)
        content.add_widget(close_btn)
        
        popup = Popup(title='Branch Details', content=content, size_hint=(0.9, 0.7))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def show_map(self, instance):
        """Show map view"""
        content = BoxLayout(orientation='vertical')
        
        # Map widget
        map_view = MapView(zoom=11, lat=-9.0320, lon=38.7469)  # Addis Ababa
        
        # Add markers for each branch
        for branch in self.branches[:10]:  # Limit to 10 markers
            try:
                lat = float(branch.get('latitude', -9.0320))
                lon = float(branch.get('longitude', 38.7469))
                marker = MapMarker(lat=lat, lon=lon)
                map_view.add_widget(marker)
            except:
                pass
        
        content.add_widget(map_view)
        
        close_btn = Button(text='Close', size_hint_y=0.1)
        content.add_widget(close_btn)
        
        popup = Popup(title='Branch Map', content=content, size_hint=(0.95, 0.95))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def show_error(self, message):
        """Show error message"""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=message))
        
        close_btn = Button(text='Close', size_hint_y=0.3)
        content.add_widget(close_btn)
        
        popup = Popup(title='Error', content=content, size_hint=(0.8, 0.4))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()


if __name__ == '__main__':
    FindYourBranchApp().run()
