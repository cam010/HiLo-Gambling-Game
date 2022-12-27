
import controller
import customtkinter

from tkinter import messagebox
customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("theme.json")


class Main:
    def __init__(self) -> None:
        self.window = customtkinter.CTk()
        self.window.title("HiLo Betting")
        self.window.geometry("300x300")
        self.window.resizable(False, False)

        ROW_AMOUNT = 3
        for i in range(ROW_AMOUNT):
            self.window.grid_rowconfigure(i, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        self.title_label = customtkinter.CTkLabel(self.window, text="HiLo Gambling Game", fg_color="transparent")
        self.title_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")
        self.title_label.cget("font").configure(size=20)

        self.starting_money_entry = customtkinter.CTkEntry(
            self.window, placeholder_text="Enter Starting Money")
        self.starting_money_entry.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.start_button = customtkinter.CTkButton(
            self.window, text="Start", command=lambda: self.start())
        self.start_button.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="nsew")

        self.window.mainloop()
    
    def start(self):
        starting_money = self.starting_money_entry.get()

        try:
            starting_money = int(starting_money)
        except:
            pass

        if type(starting_money) != int or starting_money > 999_999 or starting_money < 10:
            messagebox.showerror("Input Error", "Please enter a whole number between 10 and 999,999")
            return
        
        self.window.destroy()

        MainApp(starting_money)


class MainApp:
    def __init__(self, starting_money) -> None:
        # Prequisites
        self.bet_amount = 10
        self.bank = controller.Bank(starting_money)
        self.set_new_num()
        self.bets_placed = 0

        # Setup Win
        self.setup_window()

        # Apply first set of numbers
        self.update_widgets()

        # Loop
        self.window.mainloop()

    def setup_window(self):
        self.window = customtkinter.CTk()
        self.window.title("HiLo Betting")
        self.window.geometry("800x700")
        # self.window['bg'] = "#d30000"

        COLUMN_AMOUNT, ROW_AMOUNT = 3, 4
        for i in range(COLUMN_AMOUNT):
            self.window.grid_columnconfigure(i, weight=1)
        for i in range(ROW_AMOUNT):
            self.window.grid_rowconfigure(i, weight=1)

        self.setup_widgets()

    def setup_widgets(self):
        # Number Label
        self.number_label = customtkinter.CTkLabel(
            self.window, text=" ", corner_radius=8)
        self.number_label.grid(row=0, column=0, columnspan=4,
                               sticky="nsew", pady=5, padx=5)

        # 'High' Side
        self.high_label = customtkinter.CTkLabel(
            self.window, text="High")
        self.high_label.grid(row=1, column=0, sticky="nsew", pady=5, padx=5)

        self.high_odds = customtkinter.CTkLabel(
            self.window, text=" ")
        self.high_odds.grid(row=2, column=0, sticky="nsew", pady=5, padx=5)

        self.bet_high_btn = customtkinter.CTkButton(
            self.window, text="Bet!", command=lambda: self.bet(controller.HIGH))
        self.bet_high_btn.grid(row=3, column=0, sticky="nsew", pady=5, padx=5)

        # 'Same' Side
        self.same_label = customtkinter.CTkLabel(
            self.window, text="Same")
        self.same_label.grid(row=1, column=1, sticky="nsew", pady=5, padx=5)

        self.same_odds = customtkinter.CTkLabel(
            self.window, text=" ")
        self.same_odds.grid(row=2, column=1, sticky="nsew", pady=5, padx=5)

        self.bet_same_btn = customtkinter.CTkButton(
            self.window, text="Bet!", command=lambda: self.bet(controller.SAME), corner_radius=8)
        self.bet_same_btn.grid(row=3, column=1, sticky="nsew", pady=5, padx=5)

        # 'Low' Side
        self.low_label = customtkinter.CTkLabel(
            self.window, text="Low")
        self.low_label.grid(row=1, column=2, sticky="nsew", pady=5, padx=5)

        self.low_odds = customtkinter.CTkLabel(
            self.window, text=" ")
        self.low_odds.grid(row=2, column=2, sticky="nsew", pady=5, padx=5)

        self.bet_low_btn = customtkinter.CTkButton(
            self.window, text="Bet!", command=lambda: self.bet(controller.LOW))
        self.bet_low_btn.grid(row=3, column=2, sticky="nsew", pady=5, padx=5)

        # 'Bet Amount' Label
        self.bet_amount_label = customtkinter.CTkLabel(
            self.window, text=f"Bet Amount:\n£{self.bet_amount}")
        self.bet_amount_label.grid(
            row=1, column=3, sticky="nsew", pady=5, padx=5)

        # 'Increase Bet' Button
        self.increase_bet_btn = customtkinter.CTkButton(
            self.window, text="Increase Bet", command=lambda: self.change_bet_amount("+", 10))
        self.increase_bet_btn.grid(
            row=2, column=3, sticky="nsew", pady=5, padx=5)

        # 'Decrease Bet' Button
        self.decrease_bet_btn = customtkinter.CTkButton(
            self.window, text="Decrease Bet", command=lambda: self.change_bet_amount("-", 10))
        self.decrease_bet_btn.grid(
            row=3, column=3, sticky="nsew", pady=5, padx=5)

        # 'Money' Label
        self.money_label = customtkinter.CTkLabel(
            self.window, text=f"Money: £{self.bank.money}")
        self.money_label.grid(row=4, column=0, sticky="nsew", pady=5, padx=5)

        # 'Win/Lose amount' Label
        self.win_loose_label = customtkinter.CTkLabel(self.window, text="")
        self.win_loose_label.grid(
            row=4, column=3, sticky='nsew', pady=5, padx=5)

        # 'Bets Placed' Label
        self.bets_placed_label = customtkinter.CTkLabel(
            self.window, text=f"Bets Placed: {self.bets_placed}")
        self.bets_placed_label.grid(
            row=4, column=1, sticky='nsew', pady=5, padx=5)

        # 'Total Winnings' Label
        self.total_money_label = customtkinter.CTkLabel(
            self.window, text=f"All Time Earnings: £{self.bank.all_time_earnings}")
        self.total_money_label.grid(
            row=4, column=2, sticky='nsew', pady=5, padx=5)

    def set_new_num(self):
        self.num = controller.generate_number()

    def update_widgets(self):
        # Number Label
        self.number_label.configure(text=self.num)

        # Chances / Odds
        self.chances = controller.generate_chances(self.num)
        self.odds = controller.generate_odds(self.chances)
        self.high_odds.configure(
            text=f"Chance:\n{self.chances[0]}/12\nOdds:\n{self.odds[0][0]}")
        self.low_odds.configure(
            text=f"Chance:\n{self.chances[1]}/12\nOdds:\n{self.odds[1][0]}")
        self.same_odds.configure(
            text=f"Chance:\n{self.chances[2]}/12\nOdds:\n{self.odds[2][0]}")

        # Money Label
        self.money_label.configure(text=f"Money: £{self.bank.money}")

        # Bets Placed Label
        self.bets_placed_label.configure(
            text=f"Bets Placed: {self.bets_placed}")

        # Total Money Label
        self.total_money_label.configure(
            text=f"All Time Earnings: £{self.bank.all_time_earnings}")

    def bet(self, choice):
        if self.bank.money < self.bet_amount:
            return

        self.bank.bet(self.bet_amount)
        self.bank.money = round(self.bank.money, 2)

        self.bets_placed += 1

        num = self.num
        self.set_new_num()

        win = controller.evaluate_win(
            num, self.num, choice)
        if win:
            odds = [self.odds[0][1], self.odds[1][1], self.odds[2][1]]
            self.win_amount = controller.generate_win_amount(
                odds, self.bet_amount, choice)
            self.win_amount = round(self.win_amount, 2)
            self.bank.win(self.win_amount)
            self.bank.all_time_earnings += self.win_amount - self.bet_amount
            self.win_loose_label.configure(
                text=f"WON: £{self.win_amount - self.bet_amount}")
        else:
            self.win_loose_label.configure(text="Lost!")

        print(self.bank.money)
        self.update_widgets()

        if self.bank.money < 10:
            messagebox.showinfo(
                "Oh No!", "Looks like your money ran out... better luck next time")
            self.window.destroy()
            Main()

    def change_bet_amount(self, operator: str, amount: int):
        if operator == '+':
            if self.bet_amount < 100 and self.bet_amount != self.bank.money:
                self.bet_amount += amount
        elif operator == '-':
            if self.bet_amount > 10:
                self.bet_amount -= amount
        self.bet_amount_label.configure(
            text=f"Bet Amount:\n£{self.bet_amount}")


if __name__ == "__main__":
    Main()
