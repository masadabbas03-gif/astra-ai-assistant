import customtkinter as ctk


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class AstraUI(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title("Astra")

        self.geometry("500x700")

        self.resizable(False, False)

        self.status = ctk.CTkLabel(

            self,

            text="🟢 Online",

            font=("Arial", 18)

        )

        self.status.pack(

            pady=20

        )

        self.title_label = ctk.CTkLabel(

            self,

            text="ASTRA",

            font=("Arial", 34, "bold")

        )

        self.title_label.pack(

            pady=10

        )

        self.chat_box = ctk.CTkTextbox(

            self,

            width=430,

            height=450

        )

        self.chat_box.pack(

            pady=20
        )

        self.chat_box.insert(

            "end",

            "Astra is ready, Boss.\n\n"

        )

        self.input_box = ctk.CTkEntry(

            self,

            width=350,

            placeholder_text="Talk to Astra..."
        )

        self.input_box.pack(

            side="left",

            padx=20,

            pady=20
        )

        self.send_button = ctk.CTkButton(

            self,

            text="Send"

        )

        self.send_button.pack(

            side="right",

            padx=20,

            pady=20
        )


app = AstraUI()

app.mainloop()