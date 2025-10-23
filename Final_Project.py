import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

time_choices = [
    "09:00", "09:30", "10:05", "10:30",
    "11:00", "11:30", "12:00", "12:30",
    "13:00", "13:30", "14:00", "14:30",
    "15:00", "15:30", "16:00", "16:30"
]


class Procedure:
    def __init__(self, procedure_name, price, duration):
        self.procedure_name = procedure_name
        self.price = price
        self.duration = duration


class ProcedureInfo(Procedure):
    procedures = {
        "manicure": {"price": 15, "duration": 20},
        "manicure + full coverage": {"price": 25, "duration": 80},
        "nail removing": {"price": 5, "duration": 15},
        "nail removing + manicure + full coverage": {"price": 45, "duration": 115}
    }

    client_visits = {}
    total_earned_money = 0
    total_duration = 0
    num_of_procedures = 0

    def __init__(self, client_name, name_of_procedure):
        self.client_name = client_name
        self.is_regular_client = False
        self._name_of_procedure = name_of_procedure
        self.notes = ""
        price = self.procedures[name_of_procedure]["price"]
        duration = self.procedures[name_of_procedure]["duration"]
        super().__init__(name_of_procedure, price, duration)
        self.add_clients()
        self.count_discount()
        self.update_total_earned_money()
        self.update_total_duration()

    def __str__(self):
        if self.is_regular_client:
            regular_client_str = "Yes"
        else:
            regular_client_str = "No"
        return (f"\nClient name: {self.client_name} ; "
                f"\nDuration of the procedure: {self.duration} minutes ;"
                f"\nEarned money: ${self.price:.2f};"
                f"\nRegular client: {regular_client_str} ;"
                f"\nNotes: {self.notes};")

    @property
    def name_of_procedure(self):
        return self._name_of_procedure

    @name_of_procedure.setter
    def name_of_procedure(self, name_of_procedure):
        self._name_of_procedure = name_of_procedure
        print(f"The name of the procedure has been set to: {name_of_procedure}")

    def add_clients(self):
        if self.client_name in ProcedureInfo.client_visits:
            ProcedureInfo.client_visits[self.client_name] += 1
        else:
            ProcedureInfo.client_visits[self.client_name] = 1

    def count_discount(self):
        if ProcedureInfo.client_visits.get(self.client_name, 0) > 2:
            self.price *= 0.85
            self.is_regular_client = True
            print(f"{self.client_name} is now a regular client and gets a 15% discount.")

    @staticmethod
    def count_visits():
        return len(ProcedureInfo.client_visits)

    def update_total_earned_money(self):
        ProcedureInfo.total_earned_money += self.price

    @staticmethod
    def get_total_earned_money():
        return ProcedureInfo.total_earned_money

    def update_total_duration(self):
        ProcedureInfo.total_duration += self.duration
        ProcedureInfo.num_of_procedures += 1

    @staticmethod
    def get_total_duration():
        return ProcedureInfo.total_duration

    @staticmethod
    def get_average_duration():
        if ProcedureInfo.num_of_procedures == 0:
            return 0
        return ProcedureInfo.total_duration / ProcedureInfo.num_of_procedures

    def add_notes(self, notes):
        self.notes = notes


class NailMasterNotebook:
    def __init__(self, root):
        self.main_window = root
        self.main_window.title("------Notebook for the nail master------")

        self.title_label = ttk.Label(root, text="You can put here information about your clients.")
        self.title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        # client name
        self.name_label = ttk.Label(root, text="Client name:", width=20)
        self.name_label.grid(row=1, column=0, padx=10, pady=5)
        self.name_entry = ttk.Entry(root, width=33)
        self.name_entry.grid(row=1, column=1, padx=10, pady=5)

        # date
        self.date_label = ttk.Label(root, text="Date:", width=20)
        self.date_label.grid(row=2, column=0, padx=10, pady=5)
        self.date_picker = DateEntry(root, width=30, background='lightpink', foreground='white', borderwidth=1)
        self.date_picker.grid(row=2, column=1, padx=10, pady=5)

        # procedures
        self.procedure_label = ttk.Label(root, text="Procedure:", width=20)
        self.procedure_label.grid(row=3, column=0, padx=10, pady=5)
        self.procedure_choice = tk.StringVar(root)
        self.procedure_choice.set("Select one procedure:")
        self.procedure_list = ttk.Combobox(root, textvariable=self.procedure_choice, state='readonly', width=30)
        self.procedure_list['values'] = list(ProcedureInfo.procedures.keys())
        self.procedure_list.grid(row=3, column=1, padx=10, pady=5)

        # time choice
        self.time_label = ttk.Label(root, text="Time Slot:", width=20)
        self.time_label.grid(row=4, column=0, padx=10, pady=5)
        self.time_choice = tk.StringVar(root)  # root - is a link between var and tkinter frame
        self.time_choice.set("Select a time slot:")
        self.time_list = ttk.Combobox(root, textvariable=self.time_choice, state='readonly', width=30)
        self.time_list['values'] = time_choices
        self.time_list.grid(row=4, column=1, padx=10, pady=5)

        # notes
        self.notes_label = ttk.Label(root, text="Notes:", width=20)
        self.notes_label.grid(row=5, column=0, padx=10, pady=5)
        self.notes_entry = tk.Entry(root, width=33)
        self.notes_entry.grid(row=5, column=1, padx=10, pady=5)

        # button submit
        self.submit_button = ttk.Button(root, text="Submit", command=self.show_info, width=35)
        self.submit_button.grid(row=6, column=0, columnspan=2, padx=10, pady=5)


        # button client summary
        self.summary_button = ttk.Button(root, text="Show summary of clients", command=self.show_total_number_of_visits, width=35)
        self.summary_button.grid(row=7, column=0, columnspan=2, padx=10, pady=5)

        # button total time
        self.time_button = ttk.Button(root, text="Show total time spent", command=self.show_total_time, width=35)
        self.time_button.grid(row=8, column=0, columnspan=2, padx=10, pady=5)

        # button average duration
        self.average_time_button = ttk.Button(root, text="Show average duration", command=self.show_average_duration, width=35)
        self.average_time_button.grid(row=9, column=0, columnspan=2, padx=10, pady=5)

        # button total earned money
        self.total_salary_button = ttk.Button(root, text="Show all earned money", command=self.show_total_earned_money, width=35)
        self.total_salary_button.grid(row=10, column=0, columnspan=2, padx=10, pady=5)

    def show_info(self):
        client_name = self.name_entry.get()
        select_procedure = self.procedure_choice.get()
        select_time = self.time_choice.get()
        notes = self.notes_entry.get()

        if not client_name or select_procedure == "Select one procedure:" or select_time == "Select a time slot:":
            messagebox.showerror("Input Error", "Please enter all required fields.")
            return

        try:
            procedure_info = ProcedureInfo(client_name, select_procedure)
            procedure_info.add_notes(notes)
            messagebox.showinfo("Client Information", str(procedure_info))
        except ValueError as e:
            messagebox.showerror("Invalid Date", str(e))

    def show_total_number_of_visits(self):
        client_summary = ProcedureInfo.count_visits()
        messagebox.showinfo("Summary of clients", f"Total number of clients: {client_summary} ")

    def show_total_time(self):
        total_time = ProcedureInfo.get_total_duration()
        messagebox.showinfo("Total duration", f"Total time spent on procedures: {total_time} minutes")

    def show_average_duration(self):
        average_time = ProcedureInfo.get_average_duration()
        messagebox.showinfo("Average duration", f"Average duration from all procedures: {average_time} minutes")

    def show_total_earned_money(self):
        total_money = ProcedureInfo.get_total_earned_money()
        messagebox.showinfo("Total salary", f"Total amount of earned money: {total_money} $")


main_window = tk.Tk()
main_window.configure(bg="#ADD8E6")
main_window.resizable(False, True)
app = NailMasterNotebook(main_window)
main_window.mainloop()
