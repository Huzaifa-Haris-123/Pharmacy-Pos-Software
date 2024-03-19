from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector as sql
from datetime import date

conn=sql.connect(host="localhost",user="root",password="",database="pharmacy")
my_cursor=conn.cursor()    

conn.commit()
conn.close()


def bill_search():
    def searchBillBtn():
        
        search_value = int(id_entry.get().strip())
        bill_search_window.destroy()
        if not search_value:
            messagebox.showerror("Error", "Please enter an item name to search.")
            return

        conn = sql.connect(host="localhost", user="root", password="", database="pharmacy")
        my_cursor = conn.cursor()

        query="SELECT itemDetail.itemId,inventory.itemName,purchased_Quantity,amount FROM itemDetail inner join inventory on  itemDetail.itemId= inventory.itemId WHERE receiptId LIKE %s "
        search_value = f"%{search_value}%"
        my_cursor.execute(query, (search_value,))
        records = my_cursor.fetchall()
        
        
        conn.commit()
        conn.close()
        
        if not records:
            messagebox.showinfo("Search Result", "No matching item found.")
        else:
            search_result_console = Tk()
            search_result_console.state("zoomed")
            search_result_console.title("Search Result")
            search_result_console.config(bg="lightblue")
            
            result_tree = ttk.Treeview(search_result_console, columns=("Item ID", "Item Name","Quantity", "Price"))
            result_tree.heading('#0', text='', anchor=CENTER)
            result_tree.column('#0', anchor=CENTER, width=0)
            result_tree.heading("Item ID", text="Item ID",anchor=CENTER)
            result_tree.heading("Item Name", text="Item Name",anchor=CENTER)
            result_tree.heading("Quantity", text="Quantity",anchor=CENTER)
            result_tree.heading("Price", text="Price",anchor=CENTER)

            for record in records:
                result_tree.insert("", "end", values=record)
            
        conn = sql.connect(host="localhost", user="root", password="", database="pharmacy")
        my_cursor = conn.cursor()

        query="SELECT totalBill,itemQuantity,receiptDate,empId FROM receipt  WHERE receiptId LIKE %s "
        search_value = f"%{search_value}%"
        my_cursor.execute(query, (search_value,))
        records = my_cursor.fetchall()
        
        conn.commit()
        conn.close()
        Bill_purchased=records[0][0]
        itemQuantity_purchased=records[0][1]
        date_receipt=records[0][2]
        servedBy=records[0][3]
        Label(search_result_console,text=f"Net Total: {Bill_purchased}       Total Quantity: {itemQuantity_purchased}       Date of Purchase: {date_receipt}        Served By: {servedBy}",font=(12) ,bg="light blue").pack(side="top")
        result_tree.pack(expand=True, fill="both")
         
    
    bill_search_window=Tk()
    bill_search_window.geometry("400x150")
    bill_search_window.title("Remove Item")
    bill_search_window.config(bg="lightblue")

    Label( bill_search_window, text="Enter Bill ID:", font=(10)).place(relx=0.05, rely=0.2)
    id_entry = Entry( bill_search_window, font=(12))
    id_entry.place(relx=0.4, rely=0.2)
    
    bill_search_btn = Button( bill_search_window, text="Search Bill", command=searchBillBtn)
    bill_search_btn.place(relx=0.5, rely=0.6)

    bill_search_window.mainloop()
    

    


def change_cursor_enter(event):
    event.widget.config(cursor="hand2")  # Change cursor to a pointing hand when hovered

def change_cursor_leave(event):
    event.widget.config(cursor="")

def search():
    def search_item():
        search_value = search_entry.get().strip()
        if not search_value:
            messagebox.showerror("Error", "Please enter an item name to search.")
            return

        conn = sql.connect(host="localhost", user="root", password="", database="pharmacy")
        my_cursor = conn.cursor()

        query = "SELECT itemId, itemName, sellingPrice, Quantity_avlb FROM inventory WHERE itemName LIKE %s"
        search_value = f"%{search_value}%"
        my_cursor.execute(query, (search_value,))
        records = my_cursor.fetchall()

        conn.commit()
        conn.close()

        if not records:
            messagebox.showinfo("Search Result", "No matching item found.")
        else:
            search_result_console = Tk()
            search_result_console.state("zoomed")
            search_result_console.title("Search Result")
            search_result_console.config(bg="lightblue")

            result_tree = ttk.Treeview(search_result_console, columns=("Item ID", "Item Name", "Price","Quantity"))
            result_tree.heading('#0', text='', anchor=CENTER)
            result_tree.column('#0', anchor=CENTER, width=0)
            result_tree.heading("Item ID", text="Item ID",anchor=CENTER)
            result_tree.heading("Item Name", text="Item Name",anchor=CENTER)
            result_tree.heading("Price", text="Price",anchor=CENTER)
            result_tree.heading("Quantity", text="Quantity",anchor=CENTER)

            for record in records:
                result_tree.insert("", "end", values=record)

            result_tree.pack(expand=True, fill="both")

    search_console = Tk()
    search_console.geometry("600x200")
    search_console.title("Search Item")
    search_console.config(bg="lightblue")

    Label(search_console, text="Enter Item Name: ", font=(10)).place(relx=0.02, rely=0.2)
    search_entry = Entry(search_console, font=(10))
    search_entry.place(relx=0.4, rely=0.2)

    search_btn = Button(search_console, text="Search", command=search_item)
    search_btn.place(relx=0.5, rely=0.6)

    search_console.mainloop()

def showAll():
    conn = sql.connect(host="localhost", user="root", password="", database="pharmacy")
    my_cursor = conn.cursor()

    query = "SELECT itemId, itemName,Quantity_avlb, sellingPrice FROM inventory"
    my_cursor.execute(query)
    records = my_cursor.fetchall()

    conn.commit()
    conn.close()

    if not records:
        messagebox.showinfo("Inventory", "No items found in the inventory.")
        return

    show_all_console = Tk()
    show_all_console.state("zoomed")
    show_all_console.title("Inventory")
    show_all_console.config(bg="lightgreen")

    inventory_tree = ttk.Treeview(show_all_console, columns=("Item ID", "Item Name", "Quantity Available", "Selling Price"))
    inventory_tree.heading('#0', text='', anchor=CENTER)
    inventory_tree.column('#0', anchor=CENTER, width=0)
    inventory_tree.heading("Item ID", text="Item ID")
    inventory_tree.heading("Item Name", text="Item Name")
    inventory_tree.heading("Quantity Available", text="Quantity Available")
    inventory_tree.heading("Selling Price", text="Selling Price")

    for record in records:
        inventory_tree.insert("", "end", values=record)

    inventory_tree.pack(expand=True, fill="both")

    show_all_console.mainloop()


def main_biling_page(empId): # <= This empId will be tracking which employee is making the sale. And the amount of sale done by this particular employee
 
 def removeItem():
    def remove():
     item_id_to_remove = id_entry.get()
     if not item_id_to_remove.isdigit():
        messagebox.showerror("Error", "Please enter a valid numeric Item ID.")
        return

    # Iterate through items in the Treeview and remove the one with the specified Item ID
     for item in frame3Tree.get_children():
        values = frame3Tree.item(item, 'values')
        if values and str(values[0]) == item_id_to_remove:
            frame3Tree.delete(item)
            messagebox.showinfo("Success", f"Item with ID {item_id_to_remove} removed successfully.")
            remove_item_console.destroy()
            return

     messagebox.showerror("Error", f"Item with ID {item_id_to_remove} not found in the list.")


    remove_item_console = Tk()
    remove_item_console.geometry("400x150")
    remove_item_console.title("Remove Item")
    remove_item_console.config(bg="lightblue")

    Label(remove_item_console, text="Enter Item ID:", font=(10)).place(relx=0.05, rely=0.2)
    id_entry = Entry(remove_item_console, font=(12))
    id_entry.place(relx=0.4, rely=0.2)
    
    remove_btn = Button(remove_item_console, text="Remove", command=remove)
    remove_btn.place(relx=0.5, rely=0.6)

    remove_item_console.mainloop()




 def f1add_item_console1():
    def estimator():
        Name_item = Name_entry.get()
        id = Id_entry.get()
        if id == ""and Name_item=="" or quantity_entry.get()=="":
           messagebox.showerror("Error","Fill required fields!!!")
           return
        
        if id == ""and Name_item!="":
            conn = sql.connect(host="localhost", user="root", password="", database="pharmacy")
            my_cursor = conn.cursor()
            query = "SELECT inventory.sellingPrice FROM inventory WHERE inventory.itemName = %s"
            my_cursor.execute(query, (Name_item,))
            record = my_cursor.fetchone()
            if record is None:
             messagebox.showerror("Error", f"Item '{id}' not found!")
            else:
             messagebox.showinfo("Price estimator", f"Item with '{id}' will cost you ${record[0] * int(quantity_entry.get())}")

            conn.commit()
            conn.close() 
            return
        
        if id != ""and Name_item=="":
            conn = sql.connect(host="localhost", user="root", password="", database="pharmacy")
            my_cursor = conn.cursor()
            query = "SELECT inventory.sellingPrice FROM inventory WHERE inventory.itemId = %s"
            my_cursor.execute(query, (id,))
            record = my_cursor.fetchone()
            if(record==None):
                 messagebox.showerror("Error", f"Item '{Name_item}' not found!")
            else:
                messagebox.showinfo("Price estimator", f"Item '{Name_item}'  will cost you ${record[0]*int(quantity_entry.get())}")
            conn.commit()
            conn.close()    
            return
        
        if id != ""and Name_item!="":
            conn = sql.connect(host="localhost", user="root", password="", database="pharmacy")
            my_cursor = conn.cursor()
            query = "SELECT inventory.sellingPrice FROM inventory WHERE inventory.itemName = %s and inventory.itemId = %s"
            my_cursor.execute(query, (Name_item,id))
            record = my_cursor.fetchone()
            if record is None:
             messagebox.showerror("Error", f"Item '{id}' not found!")
            else:
             messagebox.showinfo("Price estimator", f"Item with '{id}' will cost you ${record[0] * int(quantity_entry.get())}")

            conn.commit()
            conn.close() 
            return
    def addCart():
        Name_item = Name_entry.get()
        id = Id_entry.get()
        if id == ""and Name_item=="" or quantity_entry.get()=="":
           messagebox.showerror("Error","Fill required fields!!!")
           return
        conn = sql.connect(host="localhost", user="root", password="", database="pharmacy")
        my_cursor = conn.cursor()
        query = "SELECT inventory.Quantity_avlb FROM inventory WHERE inventory.itemName = %s"
        my_cursor.execute(query, (Name_item,))
        record = my_cursor.fetchone()
        conn.commit()
        conn.close() 
        if int(record[0])<int(quantity_entry.get()):
            messagebox.showerror("Error", "Quantity Out of stock")
            add_item_console.destroy()
            return
        if id == ""and Name_item!="":
            conn = sql.connect(host="localhost", user="root", password="", database="pharmacy")
            my_cursor = conn.cursor()
            query = "SELECT inventory.itemId ,inventory.itemName,inventory.sellingPrice FROM inventory WHERE inventory.itemName = %s"
            my_cursor.execute(query, (Name_item,))
            record = my_cursor.fetchone()
            conn.commit()
            conn.close() 
            record2=(record[0],record[1],record[2],quantity_entry.get(),int(int(record[2]))*int(quantity_entry.get()))
            if record is None:
             messagebox.showerror("Error", f"Item '{id}' not found!")
            else:
            #  messagebox.showinfo("Price estimator", f"Item with '{id}' will cost you ${record[0] * int(quantity_entry.get())}")
        
             frame3Tree.insert("", "end", values=record2)

            add_item_console.destroy()
            return
        
        if id != ""and Name_item=="":
            conn = sql.connect(host="localhost", user="root", password="", database="pharmacy")
            my_cursor = conn.cursor()
            query = "SELECT inventory.sellingPrice FROM inventory WHERE inventory.itemId = %s"
            my_cursor.execute(query, (id,))
            record = my_cursor.fetchone()
            if(record==None):
                 messagebox.showerror("Error", f"Item '{Name_item}' not found!")
            else:
                messagebox.showinfo("Price estimator", f"Item '{Name_item}'  will cost you ${record[0]*int(quantity_entry.get())}")
            conn.commit()
            conn.close()    
            add_item_console.destroy()
            return
        
        if id != ""and Name_item!="":
            conn = sql.connect(host="localhost", user="root", password="", database="pharmacy")
            my_cursor = conn.cursor()
            query = "SELECT inventory.sellingPrice FROM inventory WHERE inventory.itemName = %s and inventory.itemId = %s"
            my_cursor.execute(query, (Name_item,id))
            record = my_cursor.fetchone()
            if record is None:
             messagebox.showerror("Error", f"Item '{id}' not found!")
            else:
             messagebox.showinfo("Price estimator", f"Item with '{id}' will cost you ${record[0] * int(quantity_entry.get())}")

            conn.commit()
            conn.close() 
            add_item_console.destroy()
            return
            

     
    add_item_console = Tk()
    add_item_console.geometry("600x600")
    add_item_console.title("Add Item")
    add_item_console.config(bg="lightblue")

    Label(add_item_console, text="Search on basis of:  ", font=(12)).place(relx=0.05, rely=0.05)
    Label(add_item_console, text="Item Id:  ", font=(12)).place(relx=0.05, rely=0.1)
    Id_entry = Entry(add_item_console, font=(12))
    Id_entry.place(relx=0.22, rely=0.1)
    Label(add_item_console, text="OR", font=(12)).place(relx=0.3, rely=0.15)
    Label(add_item_console, text="Item Name:  ", font=(12)).place(relx=0.05, rely=0.2)
    Name_entry = Entry(add_item_console, font=(12))
    Name_entry.place(relx=0.26, rely=0.2)
    Label(add_item_console, text="Quantity*:  ", font=(12)).place(relx=0.05, rely=0.3)
    quantity_entry=Entry(add_item_console, font=(12))
    quantity_entry.place(relx=0.26,rely=0.3)
    Button(add_item_console, text="Estimate Price", command=estimator).place(relx=0.7, rely=0.3)
    Button(add_item_console, text="Add to Cart", command=addCart).place(relx=0.7, rely=0.4)
    
    add_item_console.mainloop()

 bill=Tk()
#bill.geometry("1920x1080")
 bill.state("zoomed")
 bill.title("Billing")
 bill.configure(bg='light blue')
 conn = sql.connect(host="localhost", user="root", password="", database="pharmacy")
 my_cursor = conn.cursor()
 query = "SELECT employee.empName FROM employee WHERE employee.empId = %s"
 my_cursor.execute(query, (empId,))
 record = my_cursor.fetchone()
 conn.commit()
 conn.close()
 heading=Label(bill,text=f"Welcome {record[0]}",bg="white",font=("Comic Sans",20,"bold"))
 heading.place(relx=0.40,rely=0.01)
 heading2=Label(bill,text="Shandaar Pharmacy",bg="white",font=("Comic Sans",15))
 heading2.place(relx=0.01,rely=0.01)

 heading3=Label(bill,text="Employee Portal",bg="white",font=("Comic Sans",15))
 heading3.place(relx=0.89,rely=0.01)
    
 frame=Frame(bill,height=200,width=1000,bg="white")

 f1add_item_console=Button(frame,text="Add an Item ",
                   bg="#0198b3",
                   fg="White",
                   font=("Comic Sans",10,"bold"),
                   command=f1add_item_console1
                   )
 f1add_item_console.place(relx=0.02,rely=0.1)

 f1butt2=Button(frame,text="Search an Item ",
                   bg="#0198b3",
                   fg="White",
                   font=("Comic Sans",10,"bold"),
                   command=search)
 f1butt2.place(relx=0.02,rely=0.5)
 
 search_bill_btn=Button (frame,text="Search Bill",bg="#0198b3",
                   fg="White",
                   font=("Comic Sans",10,"bold"),
                   command=bill_search
                   )
 search_bill_btn.place(relx=0.6,rely=0.5)
 

 remove_btn=Button(frame,text="Remove an Item ",
                   bg="#0198b3",
                   fg="White",
                   font=("Comic Sans",10,"bold"),
                   command=removeItem)
 remove_btn.place(relx=0.3,rely=0.1)

 f1butt4=Button(frame,text="Show All ",
                   bg="#0198b3",
                   fg="White",
                   font=("Comic Sans",10,"bold"),
                   command=showAll)
 f1butt4.place(relx=0.3,rely=0.5)




 frame.place(relx=0.01,rely=0.07)
    

    
 frame2=Frame(bill,height=622,width=490,bg="white")
 frame2.place(relx=0.67,rely=0.07)
 
 frame3Tree = ttk.Treeview(bill,height=19)
 frame3Tree["columns"]=("Item Id","Item Name","Price","Quantity","Amount")
 for col in frame3Tree['columns']:
    frame3Tree.column(col, width=160, minwidth=32, anchor=CENTER)
    frame3Tree.heading(col, text=col)
    
 frame3Tree.place(relx=0.01,rely=0.35)

    
 frame4=Frame(bill,height=50,width=1510,bg="white")
 frame4.place(relx=0.01,rely=0.9)
 def generateBill():
    conn = sql.connect(host="localhost", user="root", password="", database="pharmacy")
    my_cursor = conn.cursor()
    # Assuming frame3Tree is a ttk.Treeview widget
    bill=int(0)
    quant=int(0)
    for item in frame3Tree.get_children():
        values = frame3Tree.item(item, 'values')
        bill=bill+int(values[4])
        quant=quant+int(values[3])
        
    query="insert into receipt(empId, receiptDate,totalBill, itemQuantity) values(%s,%s,%s,%s)"
    my_cursor.execute(query, (empId,date.today(),bill,quant,))
    query="select max(receipt.receiptId) from receipt"
    my_cursor.execute(query)
    receiptdId=my_cursor.fetchone()
    for item in frame3Tree.get_children():
        values = frame3Tree.item(item, 'values')
        
        query="select inventory.Quantity_avlb,inventory.No_of_item_sold from inventory where inventory.itemId= %s"
        my_cursor.execute(query, (values[0],))
        records = my_cursor.fetchone()
        quantity=int((records[0])-int(values[3]))
        no_of_sold=int((records[1])+int(values[3]))
        query="update inventory set inventory.Quantity_avlb= %s ,inventory.No_of_item_sold=%s where inventory.itemId= %s"
        my_cursor.execute(query, (quantity,no_of_sold,values[0],))
        query="select employee.saleDone from employee where employee.empId=%s"
        my_cursor.execute(query, (empId,))
        sale_emp=my_cursor.fetchone()
        sale=int(sale_emp[0]+int(values[4]))
        query="update employee set employee.saleDone= %s where employee.empId= %s"
        my_cursor.execute(query, (sale,empId,))
        query="insert into itemDetail(receiptId, itemId,amount,purchased_Quantity) values(%s,%s,%s,%s)"
        my_cursor.execute(query, ((receiptdId[0]),values[0],values[4],values[3],))
        
        
        print(records)
        print(f"Item ID: {values[0]}, Item Name: {values[1]}, Price: {values[2]}, Quantity: {values[3]}, Amount: {values[4]}")
    conn.commit()
    conn.close()    
    for item in frame3Tree.get_children():
        frame3Tree.delete(item)

    # Retrieve the details from the Treeview and print to console
    

    # You may want to perform additional actions related to generating a bill here
    # For example, you can calculate the total amount, save the bill to a database, etc.

    
 generateBilll=Button(frame4,text="Generate Bill",bg="black",fg="white",font=("Comic Sans",10),
                     command=generateBill)
 generateBilll.place(relx=0.9,rely=0.25)

 frame4.mainloop
 frame2.mainloop()
 frame.mainloop()
    
 bill.mainloop()



   
def employee_login_page():
  def reset_btn():
    emp_id.delete(0,'end')
    password.delete(0,'end')
     
  def login_btn():
    
    conn=sql.connect(host="localhost",user="root",password="",database="pharmacy")
    my_cursor=conn.cursor() 
    global empId
    empId=emp_id.get()
    if (empId==""  or password.get()==""):
        reset_btn()
        Label(frame, text="Fill all the required fields!!!", bg="white", fg="#f7f307", font=("Times new roman",13,"bold")).place(relx=0,rely=0.82) 
        return
    if empId.isdigit():
        empId = int(empId)
        login_data=(empId,password.get())
        print(login_data)
        reset_btn()
        flag=False
        my_cursor.execute("select employee.empId,employee.loginPass from employee")
        record=my_cursor.fetchall()
        for i in record:
            if(i==login_data):
                employee.destroy()
                main_biling_page(empId)
    
        conn.commit()
        conn.close()    
        if(flag==False):
         pass
        #Label(frame, text="Wrong User Name or Password Entered!!!", bg="white", fg="#fc0303",font=("Times new roman",13,"bold")).place(relx=0,rely=0.82) 
    else:
        Label(frame, text="Wrong User Name or Password Entered!!!", bg="white", fg="#fc0303", font=("Times new roman",13,"bold")).place(relx=0,rely=0.82)
    
   
    
  window.destroy()
  employee = Tk()
  employee.title("Employee Login Page")
  #employee.geometry("1920x1080")
  employee.state('zoomed')
  bg_image = PhotoImage(file="employee_background.png")
  bg_label = Label(employee, image=bg_image)
  bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    
  frame = Frame(employee, bg="white", bd=5)
  frame.place(relx=0.1, rely=0.25, width=350, height=350)
  Label(frame, text="Employee Login", bg="white", fg="black", font=("Bold", 25)).place(relx=0.15,rely=0.05)
  Label(frame, text="Employee ID:", bg="white", font=("Bold", 14)).place(rely=0.3, relx=0.0)
  emp_id = Entry(frame, font=("times new roman", 15, "bold"), bd=3)
  emp_id.place(rely=0.3, relx=0.35)
    
  Label(frame, text="Password:", bg="white", font=("Bold", 14)).place(rely=0.5, relx=0.0)
  password = Entry(frame, show="*", font=("times new roman", 15, "bold"), bd=3)
  password.place(rely=0.5, relx=0.35)
     
     #===== Buttons =======
  Login_button = Button(frame, text="Login", bg="#03c6fc", fg="white",font=("arial"),command=login_btn)
  Login_button.bind("<Enter>", change_cursor_enter)
  Login_button.bind("<Leave>", change_cursor_leave)
  Login_button.place(relx=0.8, rely=0.7)  
  Rest_button = Button(frame, text="Reset", bg="#03c6fc", fg="white",font=("arial"),command=reset_btn)
  Rest_button.bind("<Enter>", change_cursor_enter)
  Rest_button.bind("<Leave>", change_cursor_leave)
  Rest_button.place(relx=0.6, rely=0.7) 
    
  employee.mainloop()
    
    
def admin_login_page():
    def reset_btn():
     user_name.delete(0,'end')
     password.delete(0,'end')
     
    def login_btn():
        # reset_btn()
        if((user_name.get()=="admin" or user_name.get()=="Admin")and password.get()=="1"):
            print("Correct")
        else:
            Label(frame, text="Wrong User Name or Password Entered!!!", bg="white", fg="#fc0303", font=("Bold")).place(relx=0.1,rely=0.82) 
    window.destroy()
    admin = Tk()
    
    admin.title("Admin Login Page")
    admin.geometry("1920x1080")
    admin.state('zoomed')
    
    # Create and place the background image Label using place
    bg_image = PhotoImage(file="admin_background.png")
    bg_label = Label(admin, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    frame = Frame(admin, bg="white", bd=5)
    frame.place(relx=0.1, rely=0.25, width=350, height=350)
    
    Label(frame, text="Admin Login Page", bg="white", fg="black", font=("Bold", 30)).pack()
    Label(frame, text="User Name:", bg="white", font=("Bold", 14)).place(rely=0.3, relx=0.0)
    user_name = Entry(frame, font=("times new roman", 15, "bold"), bd=3)
    user_name.place(rely=0.3, relx=0.35)
    
    Label(frame, text="Password:", bg="white", font=("Bold", 14)).place(rely=0.5, relx=0.0)
    password = Entry(frame, show="*", font=("times new roman", 15, "bold"), bd=3)
    password.place(rely=0.5, relx=0.35)
     
     #===== Buttons =======
    Login_button = Button(frame, text="Login", bg="#03c6fc", fg="white",font=("arial"),command=login_btn)
    Login_button.bind("<Enter>", change_cursor_enter)
    Login_button.bind("<Leave>", change_cursor_leave)
    Login_button.place(relx=0.8, rely=0.7)  
    Rest_button = Button(frame, text="Reset", bg="#03c6fc", fg="white",font=("arial"),command=reset_btn)
    Rest_button.bind("<Enter>", change_cursor_enter)
    Rest_button.bind("<Leave>", change_cursor_leave)
    Rest_button.place(relx=0.6, rely=0.7) 
    
    admin.mainloop()


    # ======== Main login Section ========= 
window = Tk()
window.geometry("1920x1080")
window.state('zoomed')
window.title("Pharmacy Management System")
bg_image = PhotoImage(file="download.png")
bg_label = Label(window, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# ======== Admin Login Button ========= 
admin_icon=PhotoImage(file="admin_icon.png")
admin_button=Button(window,image=admin_icon,bd=0,command=admin_login_page)
admin_button.place(x=50,y=200)
admin_button.config(width=250)
admin_button.bind("<Enter>", change_cursor_enter)
admin_button.bind("<Leave>", change_cursor_leave)
Label(window,text="Admin Login",font=("open sans",25),fg="Purple").place(x=80,y=430)

# ======== Employee Login Button ========= 
employee_icon=PhotoImage(file="employee_icon.png")
employee_button=Button(window,image=employee_icon,bd=0,command=employee_login_page)
employee_button.place(x=400,y=200)
employee_button.config(width=250)
employee_button.bind("<Enter>", change_cursor_enter)
employee_button.bind("<Leave>", change_cursor_leave)
Label(window,text="Employee Login",font=("open sans",25),fg="Purple").place(x=400,y=430)


window.mainloop()