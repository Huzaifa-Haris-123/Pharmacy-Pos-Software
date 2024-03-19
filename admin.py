from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector as sql
from datetime import date



conn=sql.connect(host="localhost",user="root",password="",database="pharmacy")
my_cursor=conn.cursor()    

conn.commit()
conn.close()

def showAll():
    conn = sql.connect(host="localhost", user="root", password="", database="pharmacy")
    my_cursor = conn.cursor()

    query = "SELECT itemId, itemName,Quantity_avlb, sellingPrice,PurchasedPrice FROM inventory"
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

    inventory_tree = ttk.Treeview(show_all_console, columns=("Item ID", "Item Name", "Quantity Available", "Selling Price","Purchased Price"))
    inventory_tree.heading('#0', text='', anchor=CENTER)
    inventory_tree.column('#0', anchor=CENTER, width=0)
    inventory_tree.heading("Item ID", text="Item ID")
    inventory_tree.heading("Item Name", text="Item Name")
    inventory_tree.heading("Quantity Available", text="Quantity Available")
    inventory_tree.heading("Selling Price", text="Selling Price")
    inventory_tree.heading("Purchased Price", text="Purchased Price")

    for record in records:
        inventory_tree.insert("", "end", values=record)

    inventory_tree.pack(expand=True, fill="both")

    show_all_console.mainloop()

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
def search():
    def search_item():
        search_value = search_entry.get().strip()
        if not search_value:
            messagebox.showerror("Error", "Please enter an item name to search.")
            return

        conn = sql.connect(host="localhost", user="root", password="", database="pharmacy")
        my_cursor = conn.cursor()

        query = "SELECT itemId, itemName, sellingPrice, Quantity_avlb,PurchasedPrice FROM inventory WHERE itemName LIKE %s"
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

            result_tree = ttk.Treeview(search_result_console, columns=("Item ID", "Item Name", "Price","Quantity","Purchased Price"))
            result_tree.heading('#0', text='', anchor=CENTER)
            result_tree.column('#0', anchor=CENTER, width=0)
            result_tree.heading("Item ID", text="Item ID",anchor=CENTER)
            result_tree.heading("Item Name", text="Item Name",anchor=CENTER)
            result_tree.heading("Price", text="Price",anchor=CENTER)
            result_tree.heading("Quantity", text="Quantity",anchor=CENTER)
            result_tree.heading("Purchased Price", text="Purchased Price",anchor=CENTER)

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


def search_employee():
    def search_emp():
        search_value = search_entry.get().strip()
        search_console.destroy()
        if not search_value:
            messagebox.showerror("Error", "Please enter an item name to search.")
            return

        conn = sql.connect(host="localhost", user="root", password="", database="pharmacy")
        my_cursor = conn.cursor()

        query = "SELECT empId, empName, empContact, empAddress,saleDone,loginPass FROM employee WHERE empId LIKE %s"
        search_value = f"%{search_value}%"
        my_cursor.execute(query, (search_value,))
        records = my_cursor.fetchall()

        conn.commit()
        conn.close()

        if not records:
            messagebox.showerror("Search Result", "No matching Employee found.")
        else:
            search_result_console = Tk()
            search_result_console.state("zoomed")
            search_result_console.title("Search Result")
            search_result_console.config(bg="lightblue")

            result_tree = ttk.Treeview(search_result_console, columns=("Employee ID", "Employee Name", "Contact","Address", "Sale Done", "Login Password"))
            result_tree.heading('#0', text='', anchor=CENTER)
            result_tree.column('#0', anchor=CENTER, width=0)
            result_tree.heading("Employee ID", text="Employee ID",anchor=CENTER)
            result_tree.heading("Employee Name", text="Employee Name",anchor=CENTER)
            result_tree.heading("Contact", text="Contact",anchor=CENTER)
            result_tree.heading("Address", text="Address",anchor=CENTER)
            result_tree.heading("Sale Done", text="Sale Done",anchor=CENTER)
            result_tree.heading("Login Password", text="Login Password",anchor=CENTER)

            for record in records:
                result_tree.insert("", "end", values=record)

            result_tree.pack(expand=True, fill="both")

    search_console = Tk()
    search_console.geometry("600x200")
    search_console.title("Search Item")
    search_console.config(bg="lightblue")

    Label(search_console, text="Enter Employee ID: ", font=(10)).place(relx=0.02, rely=0.2)
    search_entry = Entry(search_console, font=(10))
    search_entry.place(relx=0.4, rely=0.2)

    search_btn = Button(search_console, text="Search", command=search_emp)
    search_btn.place(relx=0.5, rely=0.6)

    search_console.mainloop()

def search_supplier():
    def search_supp():
        search_value = search_entry.get().strip()
        search_console.destroy()
        if not search_value:
            messagebox.showerror("Error", "Please enter an Supplier Id to search.")
            return

        conn = sql.connect(host="localhost", user="root", password="", database="pharmacy")
        my_cursor = conn.cursor()

        query = "SELECT suppId, suppName, suppContact, suppAddress FROM supplier WHERE suppId LIKE %s"
        search_value = f"%{search_value}%"
        my_cursor.execute(query, (search_value,))
        records = my_cursor.fetchall()

        conn.commit()
        conn.close()

        if not records:
            messagebox.showerror("Search Result", "No matching Employee found.")
        else:
            search_result_console = Tk()
            search_result_console.state("zoomed")
            search_result_console.title("Search Result")
            search_result_console.config(bg="lightblue")

            result_tree = ttk.Treeview(search_result_console, columns=("Supplier ID", "Supplier Name", "Contact","Address"))
            result_tree.heading('#0', text='', anchor=CENTER)
            result_tree.column('#0', anchor=CENTER, width=0)
            result_tree.heading("Supplier ID", text="Supplier ID",anchor=CENTER)
            result_tree.heading("Supplier Name", text="Supplier Name",anchor=CENTER)
            result_tree.heading("Contact", text="Contact",anchor=CENTER)
            result_tree.heading("Address", text="Address",anchor=CENTER)
           
            for record in records:
                result_tree.insert("", "end", values=record)

            result_tree.pack(expand=True, fill="both")

    search_console = Tk()
    search_console.geometry("600x200")
    search_console.title("Search Item")
    search_console.config(bg="lightblue")

    Label(search_console, text="Enter Supplier ID: ", font=(10)).place(relx=0.02, rely=0.2)
    search_entry = Entry(search_console, font=(10))
    search_entry.place(relx=0.4, rely=0.2)

    search_btn = Button(search_console, text="Search", command=search_supp)
    search_btn.place(relx=0.5, rely=0.6)

    search_console.mainloop()



def add_item():
    def reset_btn():
        itemName.delete(0,'end')
        supplierId.delete(0,'end')
        ItemType.delete(0,'end')
        QuantityPurchased.delete(0,'end')
        SellPrice.delete(0,'end')
        PurchasedPrice.delete(0,'end')
        
    def add_to_inventory():
        Name_item=itemName.get()
        Id_supplier=supplierId.get()
        Type_item=ItemType.get()
        purchased_quant=QuantityPurchased.get()
        Price_sell=SellPrice.get()
        price_pur=PurchasedPrice.get()
        if(Name_item=="" or Id_supplier=="" or Type_item=="" or Price_sell=="" or price_pur==""):
             messagebox.showerror("Error", "Please enter all required fields!!!.")
             return
        Price_sell=int(Price_sell)
        price_pur=int(price_pur)  
        if(Price_sell < price_pur):
            messagebox.showerror("Error", "Purchased Price must be less than selling price!!!.")
            return
        else:
            Id_supplier=int(Id_supplier)
            if(purchased_quant==""):
                purchased_quant=0
            purchased_quant=int(purchased_quant)
        conn=sql.connect(host="localhost",user="root",password="",database="pharmacy")
        my_cursor=conn.cursor()
        query="select * from supplier where suppId= %s"
        my_cursor.execute(query, (Id_supplier,))
        record=my_cursor.fetchall()
        if(record=="[]"):
            messagebox.showerror("Error", "Invalid Supplier Id Entered!!.")
            return      
                              
        conn=sql.connect(host="localhost",user="root",password="",database="pharmacy")
        my_cursor=conn.cursor()
        query="insert into pharmacy.inventory(suppId,itemName,itemType,sellingPrice,PurchasedPrice,Quantity_avlb) values(%s,%s,%s,%s,%s,%s)"
        my_cursor.execute(query, (Id_supplier,Name_item,Type_item,Price_sell,price_pur,purchased_quant,))
        conn.commit()
        conn.close()
        add_item_console.destroy()
        query="select max(itemId) from inventory"
        my_cursor.execute(query,)
        record=my_cursor.fetchone()
        messagebox.showinfo(f"Item Added", "Item Added successfully with Item Id= {record[0]}.")
        
    add_item_console=Tk()
    add_item_console.geometry("450x600")
    add_item_console.config(bg="light blue")
    Label(add_item_console,text="Add Item",font=(12),bg="light blue").pack(side="top")
    
    Label(add_item_console,text="Item Name: ",bg="light blue",font=(10)).place(relx=0.05,rely=0.1)
    itemName=Entry(add_item_console,font=(10))
    itemName.place(relx=0.40,rely=0.1)
    
    Label(add_item_console,text="Supplier Id: ",bg="light blue",font=(10)).place(relx=0.05,rely=0.2)
    supplierId=Entry(add_item_console,font=(10))
    supplierId.place(relx=0.40,rely=0.2)
    
    Label(add_item_console,text="Item Type: ",bg="light blue",font=(10)).place(relx=0.05,rely=0.3)
    ItemType=Entry(add_item_console,font=(10))
    ItemType.place(relx=0.40,rely=0.3)
    
    Label(add_item_console,text="Quantity : ",bg="light blue",font=(10)).place(relx=0.05,rely=0.4)
    QuantityPurchased=Entry(add_item_console,font=(10))
    QuantityPurchased.place(relx=0.40,rely=0.4)
    
    Label(add_item_console,text="Selling Price: ",bg="light blue",font=(10)).place(relx=0.05,rely=0.5)
    SellPrice=Entry(add_item_console,font=(10))
    SellPrice.place(relx=0.40,rely=0.5)
    
    Label(add_item_console,text="Purchased Price: ",bg="light blue",font=(10)).place(relx=0.05,rely=0.6)
    PurchasedPrice=Entry(add_item_console,font=(10))
    PurchasedPrice.place(relx=0.40,rely=0.6)
    
    Button(add_item_console,text="Submit",command=add_to_inventory).place(relx=0.5,rely=0.7)
    Button(add_item_console,text="Reset",command=reset_btn).place(relx=0.5,rely=0.75)
    
    add_item_console.mainloop()
    


















admin_window=Tk()
admin_window.state("zoomed")
admin_window.geometry("1920x1080")
admin_window.config(bg="light blue")
admin_window.title("Admin Page")

frame1=Frame(admin_window,bg="white",height=700,width=450)
frame1.place(relx=0.01,rely=0.07)
Label(frame1,text="Admin Control Panel",bg="white",font=20).place(relx=0.28,rely=0.05)

Button(frame1,text="Update Item").place(relx=0.28,rely=0.1)
Button(frame1,text="Add Item",command=add_item).place(relx=0.545,rely=0.1)

Button(frame1,text="Search Item",command=search).place(relx=0.28,rely=0.20)
Button(frame1,text="Show All Items",command=showAll).place(relx=0.545,rely=0.20)

Button(frame1,text="Search Bill",command=bill_search).place(relx=0.28,rely=0.30)
Button(frame1,text="Search Employee",command=search_employee).place(relx=0.545,rely=0.30)

Button(frame1,text="Add Employee").place(relx=0.28,rely=0.40)
Button(frame1,text="Remove Employee").place(relx=0.545,rely=0.40)

Button(frame1,text="Add Supplier").place(relx=0.28,rely=0.50)
Button(frame1,text="Search Supplier",command=search_supplier).place(relx=0.545,rely=0.50)

Button(frame1,text="Update Employee Info").place(relx=0.35,rely=0.60)

admin_window.mainloop()
