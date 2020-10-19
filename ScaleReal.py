import  sqlite3
conn  =  sqlite3.connect ( 'MyCart.db' )
cursor  =  conn.cursor ()

cursor.execute("CREATE TABLE IF NOT EXISTS Category( ID int NOT NULL ,name char(10) NOT NULL, PRIMARY KEY (ID));")
cursor.execute("CREATE TABLE IF NOT EXISTS Product( ProductId int NOT NULL, ProductName char(30) NOT NULL, Price int NOT NULL,CategoryId int NOT NULL, ProductDetails char(100),PRIMARY KEY (ProductId),FOREIGN KEY (CategoryId) REFERENCES Catrgory(ID));")
cursor.execute("CREATE TABLE IF NOT EXISTS Customer( CustomerId int NOT NULL, CustomerName char(30) NOT NULL,PRIMARY KEY (CustomerId));")
cursor.execute("CREATE TABLE IF NOT EXISTS MyCart( CartId INTEGER PRIMARY KEY AUTOINCREMENT, CustomerId int ,ProductId int ,FOREIGN KEY (CustomerId) REFERENCES Customer(CustomerId), FOREIGN KEY (ProductId) REFERENCES Product(ProductId));")


bill = {}
MyCart = {}

def getIdentity(Identity):

	if Identity == 1:
		print('Welcome Admin')
	elif Identity == 2:
		print('Welcome User')
	else : print('Unkown request, please provide correct credentials')

def lastNote(Identity):

	if Identity == 1:
		print('Data updated successfully')
	elif Identity == 2:
		print('Thank you for shopping')
	conn.close()
	print('DB connection close')


def PrintProductList(records):
	if records:
		print('(Id  ProductName CategoryId)')
		for i in records:
			print(i[0],i[1],i[2])
		print('************')
	else: print('No records')

def PrintCategoryList(records):
	if records:
		print('(Id  Name)')
		for i in records:
			print(i[0],i[1])
		print('************')
	else: print('No records')


def ShowCategory():
	try:
		cursor.execute("""SELECT * from Category;""")
		records = cursor.fetchall()
		if len(records) == 0:
			print('No records found, please add records')
		else :
			print('Available categories are :')
			PrintCategoryList(records)
	except Exception as e:
		print(e)

def AddCategory():
	try:
		ShowCategory()
		print('Input new category id and name')
		Id = input('Id:')
		name = input('Name:')
		cursor.execute("""INSERT INTO Category(ID, name) VALUES (?,?);""", (Id,name))
		conn.commit ()
		print ('Category added successfully.')
		ShowCategory()
	except Exception as e:
		print(e)
	


def ShowProduct():

	try:
		cursor.execute("""SELECT * from Product;""")
		records = cursor.fetchall()
		if len(records) == 0:
			print('No records found, please add records')
			print('To add new products to category, refer below list')
		else :
			print('Products list is :')
			PrintProductList(records)
	except Exception as e:
		print(e)


def AddProduct():
	try:
		ShowProduct()
		print('Available Categories are:')
		cursor.execute("""SELECT * from Category;""")
		records = cursor.fetchall()
		PrintCategoryList(records)
		print('\n Input new product')
		ProductId = input('ProductId :')
		Name = input('Name:')
		Price = input('Price:')
		CategoryId = input('CategoryId:')
		Details = input('Details :')
		cursor.execute("""INSERT INTO Product(ProductId,ProductName,Price,CategoryId,ProductDetails) VALUES (?,?,?,?,?);""",(ProductId,Name,Price,CategoryId,Details))
		conn.commit()
		print ('Product added successfully.')
	except Exception as e:
		print(e)


def ViewUserDetails():
	cursor.execute("""SELECT Customer.CustomerId, Customer.CustomerName, MyCart.ProductId  FROM Customer
					INNER JOIN Mycart ON MyCart.CustomerId = Customer.CustomerId;""")
	b = cursor.fetchall()
	print('CustomerId  CustomerName  ProductId')
	for i in b:
		print(i)

def ViewBills(id):
	productsIncart =[]
	finalPrice = 0
	Discount = 0
	getitems = showCart(id)
	if len(getitems) != 0:
		for i in getitems:
			productsIncart.append(i[2])
	for i in productsIncart:
		cursor.execute("""SELECT Price FROM Product WHERE ProductId =? ;""",(i,))
		price = cursor.fetchall()
		finalPrice += price[0][0]
		if finalPrice > 10000:
			finalPrice -= 500
			Discount = 500
	bill.update({'UserId' : id, 'ProductCount' : len(productsIncart) ,'TotalPrice' : finalPrice, 'Discount' : Discount,'FinalPrice' : finalPrice+Discount })
	print(bill)
	return bill

def showCart(getUserId):
	cursor.execute("""SELECT * FROM MyCart WHERE CustomerId =? ;""",(getUserId,))
	print('CartId   CustomerId    ProductId')
	getallitems = cursor.fetchall()
	for i in getallitems:
		print(i)
	return getallitems

def AddProductToCart():
	try:
		key = 1
		ShowProduct()
		print('Please select item to be added')
		addItem = input('Add Itme :')
		cursor.execute("""SELECT ProductName FROM Product WHERE ProductId=?;""",(addItem,))
		getProductName = cursor.fetchone()
		getUserId = input('Enter your User Id :')
		cursor.execute("""INSERT INTO  MyCart(CustomerId ,ProductId) VALUES(?,?);""",(getUserId, addItem))
		conn.commit()
		print('Item added successfully')
		showCart(getUserId)
	except Exception as e:
		print(e)
	

def DeleteProductFromCart(CustomerId):

	try:
		list = showCart(CustomerId)
		if len(list) == 0:
			print('No items in cart to delete')
		
		else:
			print('Select cart id to be deleted')
			ItemSelected = input('Item :')
			cursor.execute("""DELETE FROM MyCart WHERE CartId = ?;""",(ItemSelected,))
			conn.commit()
			cursor.execute("""SELECT * FROM MyCart ;""")
			availableitems = cursor.fetchall()
			PrintProductList(availableitems)
	except Exception as e:
		print(e)


def ViewAllBills():

	cursor.execute("""SELECT CustomerId FROM Customer""")
	users = cursor.fetchall()
	for i in users:
		userId =i[0]
		ViewBills(userId)
	

def admin(task_selected):
	if task_selected == 1 :
		AddCategory()
	elif task_selected == 2 :
		AddProduct()
	elif task_selected == 3 :
		ViewUserDetails()
	elif task_selected == 4 :
		ViewAllBills()
	else : print('Unkown request, please provide correct credentials')


def User(task_selected,id):
	if task_selected == 1 :
		ShowCategory()
	elif task_selected == 2 :
		ShowProduct()
	elif task_selected == 3 :
		AddProductToCart()
	elif task_selected == 4 :
		DeleteProductFromCart(id)
	elif task_selected == 5:
		ViewBills(id)
	else : print('Unkown request, please provide correct credentials') 


def CreateAccount():

	print('Please enter id and name')
	Id = input('Id:')
	Name = input('Name:')
	cursor.execute("""INSERT INTO Customer(CustomerId, CustomerName) VALUES(?,?)""",(Id,Name,))
	conn.commit ()
	print('Account created succesfully')
	cursor.execute("""SELECT * FROM Customer ORDER BY CustomerId DESC LIMIT 1;""")
	record = cursor.fetchall()
	return record[0][0]

def LogintoAccount():

	print('Please enter your Id')
	getId = input('CustomerId :')
	cursor.execute(""" SELECT * FROM Customer WHERE  CustomerId = ?""",(getId,))
	CustomerId = cursor.fetchall()
	if len(CustomerId) == 0 :
		print('User not present with given Id')
		print(' 1.Create Account \n 2.Exit')
		getinput = input('Selected option:')
		if getinput == 1:
			id = CreateAccount()
		else:
			Exit()
	else:
		id = CustomerId[0][0]
	return id
	

def checkStatus(Identity):
	if Identity == 1:
		print('Please select one of the options below :')
		print(' 1.Add Category \n 2.Add Product \n 3.View user details \n 4.View bills \n 5.Log Out')
		task_selected = input('Task selected :')
		return(task_selected)
	if Identity == 2:
		userId = LogintoAccount()
		if userId != None:
			print('Your user Id is :',userId)
		print('Please select one of the options below :')
		print(' 1.Show Category \n 2.Show Product \n 3.Add Product To Cart \n 4.Delete Product From Cart \n 5.View bills \n 6.Log Out')
		task_selected = input('Task selected :')
		if task_selected == 4 or 5 :
			return(task_selected,userId)
		else: return(task_selected)


print('Welcome to MyCart')
print('Please confirm your identity. \n You are \n 1. Admin \n 2. User')
Identity = input('Identity:')
getIdentity(Identity)
getStatus = checkStatus(Identity)
if Identity == 1:
	while  getStatus != 5 :
		admin(getStatus)
		getStatus = checkStatus(Identity)
elif Identity == 2:
	while getStatus != 6 :
		if len(getStatus) > 1:
			User(getStatus[0],getStatus[1])
		else: User(getStatus)
		getStatus = checkStatus(Identity)
else :
	print('Unkown request')

lastNote(Identity)