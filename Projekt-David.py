import tkinter as tk  # tkinter för att skapa fönster
from PIL import Image, ImageTk  # Pillow för att hantera bilder
import requests  # Requests för att göra HTTP förfrågningar
import os  # Os för fil och mapp-hantering
from tkinter import simpledialog, messagebox  # tkinter för dialog och text-ruta


class DogImageApp:  # Definiera en klass för hund appen 
    def __init__(self, root):
        self.root = root  # Huvudfönstret
        self.root.title("Hund appen")  # fönstre titel
        self.root.geometry("550x500")  # fönstre storlek
        

        os.makedirs("hund_map", exist_ok=True)  # Skapar en mapp om den inte finns, lagra hund-bilder i 

        self.dog_image_url = ""  # Variabel för att lagra URL till aktuell hundbild
        self.temp_file = "dog_picture.jpg"  # Filnamn för temporär hundbild
        self.saved_image_urls = []  # Lista för att lagra sparade hundbilders URL
        
        self.label = tk.Label(root)  # Skapar en label för att visa hundbilden 
        self.label.pack()  # Lägger till labeln i fönstret

        self.mini_frame = tk.Frame(root)  # Skapar en ram för knappar
        self.mini_frame.pack(pady=10)  # Lägger till ramen i fönstret

        self.create_buttons()  # Anropar metod för att skapa knappar
    
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)  # Hantera stängning av fönstret

        self.show_random_dog_image()  # Hämtar och visar en slumpmässig hundbild
    
    def get_full_path(self, filename):  # Funktion för att få fullständig sökväg till en bild
        return os.path.join("hund_map", filename) # Full_path

    def create_buttons(self):  # Metod för att skapa knappar 
        self.button = tk.Button(self.root, text="Visa hund", command=self.show_random_dog_image)  # Knapp för att visa hundbild
        self.button.pack(pady=2)  # Lägger till knappen i fönstret

        self.save_button = tk.Button(self.root, text="Spara hundbild", command=self.save_image)  # Knapp för att spara hundbild
        self.save_button.pack(pady=2)  

        self.show_button = tk.Button(self.root, text="Visa sparade hundar", command=self.show_saved_images)  # Knapp för att visa sparade bilder
        self.show_button.pack(pady=2)  

        self.back_button = tk.Button(self.root, text="Tillbaka till hundar", command=self.go_back_to_start)  # Knapp för att återgå till start
        self.back_button.pack_forget()  # Döljer tillbaka-knappen

    def fetch_and_save_image(self, url, path):  # Metod för att hämta och spara en bild från en URL
        try:
            img_data = requests.get(url).content  # Gör en HTTP-förfrågan för att hämta bildinnehållet
            with open(path, "wb") as f:  # Öppna filen i binärt läge för skrivning
                f.write(img_data)  # Skriv bilden till fil
        except Exception as e:
            print(f"Fel vid hämtning av bild: {e}")  # Skriv ut felmeddelande om något går fel

    def show_random_dog_image(self):  # Metod för att visa en slumpmässig hundbild
        url = "https://dog.ceo/api/breeds/image/random"  # API-url för att hämta en slumpmässig hundbild
        response = requests.get(url)  # Gör en GET-förfrågan till AP
        data = response.json()  # Konvertera svaret till JSON
        self.dog_image_url = data['message']  # Hämta URL till hundbilden

        self.fetch_and_save_image(self.dog_image_url, self.temp_file)  # Hämta hundbild och spara i den temprär filen 
        self.display_image(self.temp_file, (490, 350))  # Visa den hämtade bilden

    def display_image(self, path, size):  # Metod för att visa en bild i tkinter fönstret
        image = Image.open(path).resize(size)  # Öppna och ändra storlek på bilden
        tk_image = ImageTk.PhotoImage(image)  # Konvertera bilden till ett format som tkinter kan hantera
        
        self.label.config(image=tk_image)  # Uppdatera labeln med den nya bilden
        self.label.image = tk_image  # Hålla en referens till bilden

    def save_image(self):  # Metod för att spara den aktuella hundbilden
        if not self.dog_image_url:  # Kontrollera om det finns en hundbild att spara
            messagebox.showwarning("Ingen bild", "Ingen hundbild att spara.")  # Visa varning om ingen bild
            return
        if self.dog_image_url in self.saved_image_urls: # Kontrollera om den aktuella hundbildens URL redan finns(sparad)
            messagebox.showwarning("Dubblett", "Denna hunden är radan i katalogen") # Visa varning om bilden redan finns
            return
        filename = simpledialog.askstring("Spara bild", "Ange ett namn till hunden:") # dialogruta som ber användaren att ange ett namn till hunden 
        if filename:  # Kontrollera om användaren har angett ett namn
            full_path = self.get_full_path(f"{filename}.jpg") # # Hämtar fullständig sökväg för att spara bilden
            self.fetch_and_save_image(self.dog_image_url, full_path)  # Spara bilden i mappen
            self.saved_image_urls.append(self.dog_image_url)  # Spara URL i listan
            messagebox.showinfo("Sparad", f"Bilden har sparats som '{filename}.jpg' i 'hund_map'.")  # Bekräfta sparandet
        elif filename == "":  # Om inget namn har angetts
            messagebox.showwarning("Fel", "Filnamnet får inte vara tomt!")  # Visa ett varningsmeddelande

    def show_large_image(self, filename):  # Metod för att visa en större version av en sparad bild
        self.display_image(self.get_full_path(filename), (490, 350))  # Visa den valda bilden
        self.back_button.pack(pady=10)  



    def show_saved_images(self):  # Metod för att visa sparade hundbilder
        self.button.pack_forget()  # Dölja huvudknappar
        self.save_button.pack_forget()  # Dölja spara-knappen
        self.show_button.pack_forget()  # Dölja visa sparade-knappen
        self.back_button.pack(pady=10)  # Visa tillbaka-knappen

        for widget in self.mini_frame.winfo_children():  # Ta bort tidigare bilder från ramen
            widget.destroy()
        

        images = os.listdir("hund_map")  # Lista över alla bilder i hund_map
        
        if images:  # Om det finns bilder
            self.update_frame_height(len(images))  # Justera fönstret höjd baserat på antal bilder

        for i in range(0, len(images), 5):  # Loopar igenom bilderna i grupper om 5
            row_frame = tk.Frame(self.mini_frame)  # Skapa en ny ram för varje rad med bilder
            row_frame.pack(side="top", pady=0)  # Lägg till raden i mini-ramen

            for filename in images[i:i + 5]:  # Loopar igenom filnamnen i den aktuella gruppen
                self.create_image_container(row_frame, filename)  # Skapa en bildcontainer för varje bild

        if not images:  # Om det inte finns några sparade bilder
            messagebox.showinfo("Inga bilder", "Det finns inga sparade hundbilder i 'hund_map'.")  # Informera användaren

    def create_image_container(self, parent, filename):  # Metod för att skapa en container för en bild
        full_path = self.get_full_path(filename)  # Hämtar den fullständiga sökvägen för den angivna bilden
        tk_image = ImageTk.PhotoImage(Image.open(full_path).resize((60, 50)))  # Öppna och ändra storlek på bilden

        container = tk.Frame(parent, width=100, height=80)  # Skapa en ram för bilden
        container.pack_propagate(False)  # Ställ in på att inte ändra storlek baserat på innehållet
        container.pack(side="left", padx=5)  # Lägg till ramen i parent

        label = tk.Label(container, image=tk_image)  # Skapa en label för att visa bilden
        label.image = tk_image  # Hålla en referens till bilden
        label.pack()  # Lägg till labeln i containern

        name_label = tk.Label(container, text=filename.split('.')[0])  # Skapa en label för bildens namn
        name_label.pack()  # Lägg till namnet i containern

        label.bind("<Button-1>", lambda e: self.show_large_image(filename))  # Bind musvänsterklick till att visa en större version av bilden
        label.bind("<Button-3>", lambda e: self.show_context_menu(e, filename))  # Bind mushögerklick till att visa en kontextmeny

    def show_context_menu(self, event, filename):  # Metod för att visa en kontextmeny vid högerklick
        menu = tk.Menu(self.root, tearoff=0)  # Skapa en meny 
        menu.add_command(label="Radera", command=lambda: self.delete_image(filename))  # Lägger till alternativ för att radera bilden
        menu.add_command(label="Ändra namn", command=lambda: self.rename_image(filename))  # Lägger till alternativ för att ändra bildens namn
        menu.tk_popup(event.x_root, event.y_root)  # Visa menyn vid musens position

    def delete_image(self, filename):  # Metod för att ta bort en sparad bild
        full_path = self.get_full_path(filename)  # Hämtar den fullständiga sökvägen för den angivna bilden

        if os.path.exists(full_path):  # Kontrollera om bilden finns
            os.remove(full_path)  # Ta bort bilden
            if self.dog_image_url in self.saved_image_urls:  # Kontrollerar om den aktuella hundbildens URL finns i listan 
                self.saved_image_urls.remove(self.dog_image_url) # Tar bort URL-en från listan

            messagebox.showinfo("Raderad", f"Bilden '{filename}' har raderats.")  # Visa meddelande om att bilden har raderats
            self.show_saved_images()  # Uppdatera visningen av sparade bilder
        else:
            messagebox.showerror("Fel", f"Bilden '{filename}' hittades inte.")  # Visa felmeddelande om bilden inte finns

    def rename_image(self, filename):  # Metod för att ändra namnet på en sparad bild
        new_name = simpledialog.askstring("Ändra namn", "Ange ett nytt namn till hunden :")  # Fråga användaren om det nya namnet
        if new_name:  # Kontrollera att användaren angav ett namn
            full_path = self.get_full_path(filename)  # Hämta den fullständiga sökvägen till den gamla bilden
            new_full_path = self.get_full_path(f"{new_name}.jpg")  # Hämtar den fullständiga sökvägen för den nya bildnamnet
            os.rename(full_path, new_full_path)  # Byt namn på bilden
            messagebox.showinfo("Ändrad", f"Bilden har döpts om till '{new_name}.jpg'.")  # Bekräfta namnändringen
            self.show_saved_images()  # Uppdatera visningen av sparade bilder
        else:
            messagebox.showwarning("Fel", "Filnamnet får inte vara tomt!") # Visa varning om namnet är tomt
 

    def go_back_to_start(self):  # Metod för att återgå till startvyn
        self.mini_frame.destroy()  # Ta bort mini-ramen för sparade bilder
        self.mini_frame = tk.Frame(self.root)  # Skapa en ny mini-ram
        self.mini_frame.pack(pady=20)  # Lägg till den nya ramen i fönstret

        self.root.geometry("550x500")  # Återställ fönstrets storlek
        self.show_buttons()  # Visa huvudknapparna igen

    def show_buttons(self):  # Metod för att visa huvudknapparna
        self.button.pack(pady=2)  # Visa knappen för att hämta en hundbild
        self.save_button.pack(pady=2)  # Visa knappen för att spara hundbild
        self.show_button.pack(pady=2)  # Visa knappen för att visa sparade bilder
        self.back_button.pack_forget()  # Dölja tillbaka-knappen

    def update_frame_height(self, num_images):  # Metod för att uppdatera höjden på fönstret baserat på antalet sparade bilder
        rows = (num_images + 4) // 5  # Beräkna antalet rader som behövs (5 bilder per rad)
        new_height = 500 + (rows * 60)  # Justera höjden på fönstret
        self.root.geometry(f"600x{new_height}")  # Sätt fönstrets nya storlek

    def on_closing(self):  # Metod som körs när fönstret stängs
        if messagebox.askokcancel("Avsluta", "Vill du verkligen stänga programmet?"):  # Meddelan om användare vill verkligen stänga fönstert 
            self.remove_temp_image()  # Ta bort temporär bild
            self.root.destroy()  # Stäng fönstret

    def remove_temp_image(self):  # Metod för att ta bort temporär bild
        if os.path.exists(self.temp_file):  # Kontrollera om den temporära bilden finns
            os.remove(self.temp_file)  # Ta bort den temporära bilden


if __name__ == "__main__":  # Kontrollera om skriptet körs direkt
    root = tk.Tk()  # Skapa huvudfönstret
    app = DogImageApp(root)  # Skapa en instans av DogImageApp
    root.mainloop()  # Starta händelseloopen