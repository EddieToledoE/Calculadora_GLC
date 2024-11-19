import tkinter as tk
from tkinter import messagebox
from logica import CalculadoraLogica


class CalculadoraApp:
    def __init__(self, root):
        self.logica = CalculadoraLogica()
        self.root = root
        self.root.title("Calculadora con Gramática")
        self.root.geometry("900x600")
        self.root.configure(bg="#1E1E2F")

        # Marco principal
        marco_principal = tk.Frame(self.root, bg="#1E1E2F")
        marco_principal.pack(fill="both", expand=True, padx=10, pady=10)

        # Marco izquierdo (Calculadora)
        marco_calculadora = tk.Frame(marco_principal, bg="#2E2E3E")
        marco_calculadora.pack(side="left", fill="y", padx=10, pady=10)

        # Encabezado
        etiqueta_encabezado = tk.Label(
            marco_calculadora,
            text="Calculadora con Gramática",
            font=("Verdana", 20, "bold"),
            bg="#2E2E3E",
            fg="#E94560",
        )
        etiqueta_encabezado.pack(pady=10)

        # Entrada de texto
        self.entrada_var = tk.StringVar()
        self.entrada_texto = tk.Entry(
            marco_calculadora,
            textvariable=self.entrada_var,
            font=("Courier", 18),
            width=25,
            bg="#1E1E2F",
            fg="#E94560",
            bd=2,
            relief="flat",
            justify="center",
        )
        self.entrada_texto.pack(pady=10)

        # Resultado
        etiqueta_resultado_titulo = tk.Label(
            marco_calculadora,
            text="Resultado:",
            font=("Verdana", 16, "bold"),
            bg="#2E2E3E",
            fg="#FFFFFF",
        )
        etiqueta_resultado_titulo.pack(pady=5)

        self.resultado_var = tk.StringVar()
        etiqueta_resultado = tk.Label(
            marco_calculadora,
            textvariable=self.resultado_var,
            font=("Courier", 22, "bold"),
            bg="#1E1E2F",
            fg="#32E0C4",
            relief="sunken",
            width=20,
            height=2,
        )
        etiqueta_resultado.pack(pady=10)

        # Botones
        marco_botones = tk.Frame(marco_calculadora, bg="#2E2E3E")
        marco_botones.pack(pady=10)

        botones = [
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
            ("0", 4, 0), (".", 4, 1), ("+", 4, 2), ("=", 4, 3),
        ]

        for (texto, fila, columna) in botones:
            boton = tk.Button(
                marco_botones,
                text=texto,
                font=("Verdana", 14, "bold"),
                width=4,
                height=2,
                bg="#1E1E2F" if texto not in "=C" else "#E94560",
                fg="#FFFFFF",
                relief="raised",
                borderwidth=2,
                activebackground="#32E0C4",
                command=lambda t=texto: self.clic_boton(t),
            )
            boton.grid(row=fila, column=columna, padx=5, pady=5)

        # Botón de limpiar
        boton_limpiar = tk.Button(
            marco_botones,
            text="C",
            font=("Verdana", 14, "bold"),
            width=4,
            height=2,
            bg="#E94560",
            fg="#FFFFFF",
            relief="raised",
            borderwidth=2,
            activebackground="#32E0C4",
            command=self.limpiar,
        )
        boton_limpiar.grid(row=5, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)

        # Marco derecho (Árbol de derivación)
        marco_arbol = tk.Frame(marco_principal, bg="#1E1E2F")
        marco_arbol.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        etiqueta_arbol = tk.Label(
            marco_arbol,
            text="Árbol de Derivación",
            font=("Verdana", 16, "bold"),
            bg="#1E1E2F",
            fg="#32E0C4",
        )
        etiqueta_arbol.pack(pady=10)

        self.lienzo_arbol = tk.Canvas(marco_arbol, width=600, height=400, bg="#2E2E3E", bd=2, relief="flat")
        self.lienzo_arbol.pack(side="left", fill="both", expand=True)

    def clic_boton(self, caracter):
        if caracter == "=":
            try:
                expresion = self.entrada_var.get()
                resultado = self.logica.calcular_resultado(expresion)
                self.resultado_var.set(resultado)
                arbol = self.logica.generar_arbol(expresion)
                self.dibujar_arbol(arbol)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            self.entrada_var.set(self.entrada_var.get() + caracter)

    def dibujar_arbol(self, arbol, x=300, y=20, coords_padre=None):
        """Dibuja el árbol de derivación en el lienzo."""
        self.lienzo_arbol.delete("all")  # Limpia el Canvas
        radio_nodo = 20

        def dibujar_nodo(x, y, texto, coords_padre=None):
            self.lienzo_arbol.create_oval(
                x - radio_nodo,
                y - radio_nodo,
                x + radio_nodo,
                y + radio_nodo,
                fill="#32E0C4",
                outline="#1E1E2F",
            )
            self.lienzo_arbol.create_text(x, y, text=texto, font=("Verdana", 10), fill="#1E1E2F")
            if coords_padre:
                self.lienzo_arbol.create_line(
                    coords_padre[0], coords_padre[1] + radio_nodo, x, y - radio_nodo, width=2, fill="#32E0C4"
                )

        def recorrer_arbol(nodo, x, y, coords_padre=None):
            if isinstance(nodo, tuple):
                texto, izq, der = nodo
                dibujar_nodo(x, y, texto, coords_padre)
                recorrer_arbol(izq, x - 100, y + 80, (x, y))
                recorrer_arbol(der, x + 100, y + 80, (x, y))
            else:
                dibujar_nodo(x, y, nodo, coords_padre)

        recorrer_arbol(arbol, x, y)

    def limpiar(self):
        """Limpia la entrada y el resultado."""
        self.entrada_var.set("")
        self.resultado_var.set("")
        self.lienzo_arbol.delete("all")


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraApp(root)
    root.mainloop()
