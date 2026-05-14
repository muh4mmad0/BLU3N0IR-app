import customtkinter as ctk
from tkinter import messagebox
import mysql.connector

# ================= DATABASE CONNECTION =================

con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Nithish@1234",
    database="nithish_railway",
    auth_plugin="mysql_native_password"
)

cur = con.cursor()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ================= CREATE TABLE =================

cur.execute("""
CREATE TABLE IF NOT EXISTS tickets (
    ticket_id INT PRIMARY KEY,
    passenger VARCHAR(100),
    train_no VARCHAR(20),
    from_station VARCHAR(100),
    to_station VARCHAR(100),
    travel_date DATE,
    seat_class VARCHAR(20)
)
""")

con.commit()

# ================= FUNCTIONS =================

def add_ticket():
    try:
        values = (
            int(entry_id.get()),
            entry_passenger.get(),
            entry_train.get(),
            entry_from.get(),
            entry_to.get(),
            entry_date.get(),
            entry_class.get()
        )

        cur.execute(
            "INSERT INTO tickets VALUES (%s,%s,%s,%s,%s,%s,%s)",
            values
        )

        con.commit()

        messagebox.showinfo(
            "Success",
            "Ticket Booked Successfully!"
        )

        clear_fields()

    except Exception as e:
        messagebox.showerror("Error", str(e))


def view_tickets():

    cur.execute("SELECT * FROM tickets")
    rows = cur.fetchall()

    output.delete("1.0", "end")

    for r in rows:
        output.insert(
            "end",
            f"ID:{r[0]}  Passenger:{r[1]}  Train:{r[2]}  "
            f"From:{r[3]}  To:{r[4]}  Date:{r[5]}  Class:{r[6]}\n"
        )

        output.insert("end", "-" * 80 + "\n\n")


def search_ticket():

    try:
        tid = int(entry_id.get())

        cur.execute(
            "SELECT * FROM tickets WHERE ticket_id=%s",
            (tid,)
        )

        r = cur.fetchone()

        output.delete("1.0", "end")

        if r:
            output.insert(
                "end",
                f"Ticket ID  : {r[0]}\n"
                f"Passenger  : {r[1]}\n"
                f"Train No   : {r[2]}\n"
                f"From       : {r[3]}\n"
                f"To         : {r[4]}\n"
                f"Travel Date: {r[5]}\n"
                f"Seat Class : {r[6]}\n"
            )

        else:
            output.insert("end", "Ticket Not Found")

    except Exception as e:
        messagebox.showerror("Error", str(e))


def update_ticket():

    try:
        values = (
            entry_passenger.get(),
            entry_train.get(),
            entry_from.get(),
            entry_to.get(),
            entry_date.get(),
            entry_class.get(),
            int(entry_id.get())
        )

        cur.execute("""
        UPDATE tickets
        SET passenger=%s,
            train_no=%s,
            from_station=%s,
            to_station=%s,
            travel_date=%s,
            seat_class=%s
        WHERE ticket_id=%s
        """, values)

        con.commit()

        messagebox.showinfo(
            "Success",
            "Ticket Updated Successfully!"
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))


def cancel_ticket():

    try:
        tid = int(entry_id.get())

        cur.execute(
            "DELETE FROM tickets WHERE ticket_id=%s",
            (tid,)
        )

        con.commit()

        messagebox.showinfo(
            "Success",
            "Ticket Cancelled Successfully!"
        )

        clear_fields()

    except Exception as e:
        messagebox.showerror("Error", str(e))


def clear_fields():

    for e in [
        entry_id,
        entry_passenger,
        entry_train,
        entry_from,
        entry_to,
        entry_date,
        entry_class
    ]:
        e.delete(0, "end")


# ================= UI LAYOUT =================

app = ctk.CTk()
app.geometry("1000x620")
app.title("Railway Dashboard")

# ================= SIDEBAR =================

sidebar = ctk.CTkFrame(
    app,
    width=220,
    corner_radius=0,
    fg_color="#0F172A"
)

sidebar.pack(side="left", fill="y")

ctk.CTkLabel(
    sidebar,
    text=" Railway App",
    font=("Segoe UI", 20, "bold"),
    text_color="#00F5D4"
).pack(pady=30)


def side_btn(text, cmd, color):

    return ctk.CTkButton(
        sidebar,
        text=text,
        command=cmd,
        fg_color=color,
        hover_color="#1f2937",
        corner_radius=10
    )


side_btn(
    " Add Ticket",
    add_ticket,
    "#7C3AED"
).pack(pady=10, padx=20)

side_btn(
    " View Tickets",
    view_tickets,
    "#06B6D4"
).pack(pady=10, padx=20)

side_btn(
    " Search",
    search_ticket,
    "#22C55E"
).pack(pady=10, padx=20)

side_btn(
    " Update",
    update_ticket,
    "#F59E0B"
).pack(pady=10, padx=20)

side_btn(
    " Cancel Ticket",
    cancel_ticket,
    "#EF4444"
).pack(pady=10, padx=20)

side_btn(
    " Clear",
    clear_fields,
    "#64748B"
).pack(pady=10, padx=20)

# ================= MAIN AREA =================

main = ctk.CTkFrame(
    app,
    fg_color="#020617"
)

main.pack(fill="both", expand=True)

ctk.CTkLabel(
    main,
    text="RAILWAY TICKET RESERVATION SYSTEM",
    font=("Segoe UI", 34, "bold"),
    text_color="#E2E8F0"
).pack(pady=20)

# ================= FORM CARD =================

card = ctk.CTkFrame(
    main,
    corner_radius=20,
    fg_color="#0F172A"
)

card.pack(pady=10, padx=40, fill="x")


def create_entry(label):

    frame = ctk.CTkFrame(
        card,
        fg_color="#0F172A"
    )

    frame.pack(
        pady=6,
        fill="x",
        padx=20
    )

    ctk.CTkLabel(
        frame,
        text=label,
        text_color="#94A3B8",
        width=160,
        anchor="w"
    ).pack(side="left")

    entry = ctk.CTkEntry(
        frame,
        width=250,
        fg_color="#1E293B",
        text_color="white",
        corner_radius=8,
        border_color="#7C3AED"
    )

    entry.pack(side="right")

    return entry


entry_id = create_entry("Ticket ID")
entry_passenger = create_entry("Passenger Name")
entry_train = create_entry("Train No")
entry_from = create_entry("From Station")
entry_to = create_entry("To Station")
entry_date = create_entry("Travel Date (YYYY-MM-DD)")
entry_class = create_entry("Seat Class")

# ================= BUTTONS ROW =================

btn_frame = ctk.CTkFrame(
    main,
    fg_color="#020617"
)

btn_frame.pack(pady=12)

ctk.CTkButton(
    btn_frame,
    text="Add",
    command=add_ticket,
    fg_color="#7C3AED"
).grid(row=0, column=0, padx=10)

ctk.CTkButton(
    btn_frame,
    text="Search",
    command=search_ticket,
    fg_color="#22C55E"
).grid(row=0, column=1, padx=10)

ctk.CTkButton(
    btn_frame,
    text="Update",
    command=update_ticket,
    fg_color="#F59E0B"
).grid(row=0, column=2, padx=10)

ctk.CTkButton(
    btn_frame,
    text="Cancel",
    command=cancel_ticket,
    fg_color="#EF4444"
).grid(row=0, column=3, padx=10)

ctk.CTkButton(
    btn_frame,
    text="View",
    command=view_tickets,
    fg_color="#06B6D4"
).grid(row=0, column=4, padx=10)

# ================= OUTPUT BOX =================

output = ctk.CTkTextbox(
    main,
    height=160,
    fg_color="#0F172A",
    text_color="#E2E8F0",
    corner_radius=15,
    border_color="#334155",
    font=("Segoe UI", 14)
)

output.pack(
    padx=40,
    pady=10,
    fill="both",
    expand=True
)

# ================= RUN APP =================

app.mainloop()