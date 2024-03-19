drop database pharmacy;
create database pharmacy;

use pharmacy;
create table pharmacy.employee(
empId int auto_increment primary key,
empName varchar(50),
empContact varchar(50),
empAddress varchar(50),
loginPass varchar(50),
saleDone int default 0
);

insert into pharmacy.employee(empName,empContact,empAddress,loginPass)
values ("Ali","0333-1234567","123 Street Lahore","Ali"),("Ahmed","0300-67593548","456 Street Lahore","Ahmed");

create table pharmacy.supplier(
suppId int auto_increment primary key,
suppName varchar(50),
suppContact varchar(50),
suppAddress varchar(50)
);

insert into pharmacy.supplier(suppName,suppContact,suppAddress)
values ("Abbott Pharma","042-9991234","123 Harley Street Lahore"),("UniLever Pharma","042-1234342","456 Biden Street Lahore");

create table pharmacy.inventory(
itemId int auto_increment primary key,
suppId int,
foreign key (suppId) references pharmacy.supplier(suppId),
itemName varchar(50),
itemType varchar(50),
No_of_item_sold int default 0,
Quantity_avlb int default 0,
sellingPrice int,
PurchasedPrice int
);

insert into pharmacy.inventory(suppId,itemName,itemType,sellingPrice,PurchasedPrice,Quantity_avlb)
values (1,"Med1","Tablet",20,15,100),(2,"Med2","Syrup",70,50,5000);

create table pharmacy.Customer(
custId int auto_increment primary key,
custName varchar(50),
custContact varchar(50),
custType varchar(50)
);

insert into pharmacy.Customer(custName,custContact,custType)
values ("Imran","0332-8732756","Walk-in"),("Sajjad","0322-9876544","Walk-in");

create table pharmacy.receipt(
receiptId int auto_increment primary key,
empId int,
foreign key (empId) references pharmacy.employee(empId),
receiptDate date,
custId int,
foreign key (custId) references pharmacy.customer(custId),
totalBill int,
itemQuantity int
);

insert into pharmacy.receipt(empId, receiptDate, custId, totalBill, itemQuantity)
values (1, CURDATE(), 1,200, 5),(2, CURDATE(), 2, 70, 1);

update employee
set saleDone=200
where empId=1;
update employee
set saleDone=70
where empId=2;


create table pharmacy.itemDetail
(
  receiptId int,
  foreign key(receiptId) references pharmacy.receipt(receiptId),
  itemId int,
  foreign key(itemId) references pharmacy.inventory(itemId),
  purchased_Quantity int ,
  amount int
  
);

INSERT INTO pharmacy.itemDetail (receiptId, itemId,amount,purchased_Quantity)
VALUES (1, 1,60,3), (2, 2,70,1), (1, 2,140,2);

use pharmacy;
select * from inventory;
update pharmacy.inventory
set Quantity_avlb=100, No_of_item_sold=0
where itemId=1;

select * from employee;
select * from receipt;
select *from inventory;
select * from itemDetail;