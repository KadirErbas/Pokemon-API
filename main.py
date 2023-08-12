import tkinter as tk
import tkinter.messagebox
from urllib.request import urlopen
import requests
from PIL import Image, ImageTk
import io


url = "https://pokeapi.co/api/v2/pokemon?offset=0&limit=1010"
pokemon_name = ""
pokemon_types = []
pokemon_abilities = []
pokemon_png_url = ""


def get_pokemon():
    pokemon_types.clear()
    pokemon_abilities.clear()
    global pokemon_name
    global pokemon_png_url
    pokemon_name = ""
    pokemon_png_url = ""

    enter_name = enter_name_entry.get()
    if enter_name == "":
        tkinter.messagebox.showinfo(title="Error!", message="Please, enter pokemon name!")
        result_label.config(text="Please, enter pokemon name!")
    else:
        pokemons_data = requests.get(url).json()
        for pokemon_data in pokemons_data["results"]:
            if pokemon_data["name"] == enter_name:
                result_label.config(text="Found!", font=('Arial', 12, 'normal'))
                pokemon_name = enter_name
                pokemon_url = pokemon_data["url"]
                pokemon_response = requests.get(pokemon_url).json()
                pokemon_form_response = requests.get(pokemon_response["forms"][0]["url"]).json()
                pokemon_png_url = pokemon_form_response['sprites']["front_default"]

                for i in pokemon_response["abilities"]:
                    pokemon_abilities.append(i["ability"]["name"])
                for i in pokemon_response["types"]:
                    pokemon_types.append(i['type']["name"])

                show_info(pokemon_name, pokemon_types, pokemon_abilities, pokemon_png_url)
                break
            if pokemon_name == "":
                result_label.config(text=f"There is no pokemon named {enter_name}!", font=('Arial', 12, 'normal'))
                clear_info()


def show_info(name, types, abilities, image_url):

    pokemon_name_label.config(text=f"Pokemon Name: {name}", font=('Arial', 12, 'normal'))
    pokemon_types_label.config(text=f"Pokemon Types: {types}", font=('Arial', 12, 'normal'))
    pokemon_abilities_label.config(text=f"Pokemon Abilities: {abilities}", font=('Arial', 12, 'normal'))

    def show_image():
        u = urlopen(image_url)
        raw_data = u.read()
        u.close()

        im = Image.open(io.BytesIO(raw_data))
        im = im.resize((250, 250))
        photo = ImageTk.PhotoImage(im)

        pokemon_image_label.config(image=photo)
        pokemon_image_label.image = photo

    show_image()


def clear_info():
    pokemon_name_label.config(text="")
    pokemon_types_label.config(text="")
    pokemon_abilities_label.config(text="")
    pokemon_image_label.config(image="")


# ui
window = tk.Tk()
window.title("Pokemon")
window.geometry("450x550")

# URL entry label and entry box
tk.Label().pack(pady=8)
enter_name_label = tk.Label(text="Enter Pokemon Name", font=('Arial', 14, 'bold'))
enter_name_label.pack()
enter_name_entry = tk.Entry(width=30, font=('Arial', 12, 'normal'))
enter_name_entry.focus()
enter_name_entry.pack(pady=10)

# button
get_pokemon_button = tk.Button(
    text="Get Pokemon", font=('Arial', 12, 'bold'), command=get_pokemon, bg="black", fg="white"
)

get_pokemon_button.update()
get_pokemon_button.pack(pady=20)
result_label = tk.Label()
result_label.pack(pady=10)

# info
pokemon_name_label = tk.Label()
pokemon_name_label.pack(pady=10)
pokemon_types_label = tk.Label()
pokemon_types_label.pack(pady=10)
pokemon_abilities_label = tk.Label()
pokemon_abilities_label.pack(pady=10)
pokemon_image_label = tk.Label()
pokemon_image_label.pack()

window.mainloop()
