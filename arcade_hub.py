import tkinter as tk
from tkinter import ttk, messagebox
import importlib
import sys
from pathlib import Path

class ArcadeHub:
    def __init__(self, root):
        self.root = root
        self.root.title("Arcade Hub")
        self.root.geometry("800x600")
        
        # Configure style
        style = ttk.Style()
        style.configure("Game.TButton", padding=20, font=('Helvetica', 16))
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="40")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="Welcome to Arcade Hub!",
            font=('Helvetica', 36, 'bold')
        )
        title_label.pack(pady=40)
        
        # Game buttons container
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.BOTH, expand=True)
        
        # Game buttons
        self.games = {
            "Fruit Catcher": "fruitcatcher",
            "Pong": "pong",
            "Worm and Grapes": "snakegame"
        }
        
        for game_name, module_name in self.games.items():
            btn = ttk.Button(
                button_frame,
                text=game_name,
                style="Game.TButton",
                command=lambda m=module_name, n=game_name: self.launch_game(m, n)
            )
            btn.pack(pady=20, fill=tk.X, padx=100)
        
        # Quit button
        quit_btn = ttk.Button(
            main_frame,
            text="Quit",
            style="Game.TButton",
            command=root.quit
        )
        quit_btn.pack(pady=40)
    
    def launch_game(self, module_name, game_name):
        try:
            # Add the current directory to Python path
            current_dir = str(Path(__file__).parent)
            if current_dir not in sys.path:
                sys.path.append(current_dir)
            
            # Import the game module
            game_module = importlib.import_module(module_name)
            
            # Close the hub window temporarily
            self.root.withdraw()
            
            # Launch based on game type
            if game_name == "Fruit Catcher":
                game = game_module.Game()
                game.run()
            elif hasattr(game_module, 'main'):
                game_module.main()
            elif hasattr(game_module, 'run_game'):
                game_module.run_game()
            elif hasattr(game_module, 'start_game'):
                game_module.start_game()
            elif hasattr(game_module, 'run'):
                game_module.run()
            else:
                raise AttributeError("Could not find a main game function")
            
            # Show the hub window again when the game closes
            self.root.deiconify()
            
        except Exception as e:
            tk.messagebox.showerror(
                "Error",
                f"Failed to launch {module_name}: {str(e)}"
            )
            self.root.deiconify()  # Make sure hub reappears even if there's an error

def main():
    root = tk.Tk()
    app = ArcadeHub(root)
    root.mainloop()

if __name__ == "__main__":
    main()