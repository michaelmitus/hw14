import sqlite3 as lite
import sys
import pprint
import pickle

def first():
    # Вывести 10 клиентов (id, имя, номер телефона, компания),
    # которых обслужлуживают сотрудники старше 50 лет,
    # оплативших музыку в любом жанре кроме Rock,
    # выходные данные должны быть отсортированы по городу пользователя в алфавитном порядке и емейлу в обратном.
    try:
        con = None
        con = lite.connect('Chinook_Sqlite.sqlite')
        query_invoice = '''
              SELECT Distinct Customer.CustomerID, Customer.FirstName, Customer.LastName, Customer.Phone, Customer.Company
              FROM Customer 
              INNER JOIN Employee ON Customer.SupportRepId = Employee.EmployeeId
              INNER JOIN Invoice ON Customer.CustomerID = Invoice.CustomerID   
              INNER JOIN InvoiceLine ON InvoiceLine.InvoiceID = Invoice.InvoiceID    
              INNER JOIN Track ON InvoiceLine.TrackID = Track.TrackID  
              INNER JOIN Genre ON Track.GenreId = Genre.GenreId
              WHERE Genre.Name NOT LIKE 'Rock' AND Employee.BirthDate < "1969-05-19"
              ORDER BY Employee.City ASC, Employee.Email DESC
              LIMIT 10    
            '''
        curID = con.cursor()
        curID.execute(query_invoice)
        pprint.pprint(curID.fetchall())
    except Exception as e:
        print(e)
        sys.exit(1)
    finally:
        if con is not None:
            con.close()

def second():
    # Вывести список пользователей (полное имя, телефон) с указанием руководителя (полное имя, телефон), сохранить в pickle в формате словаря.
    try:
        con = None
        con = lite.connect('Chinook_Sqlite.sqlite')
        query_invoice = '''
              SELECT e.FirstName, e.LastName, e.Phone, m.FirstName, m.LastName, m.Phone  FROM Employee e
               LEFT JOIN Employee as m ON m.EmployeeID = e.ReportsTo
            '''
        curID = con.cursor()
        curID.execute(query_invoice)
        pickle_data = curID.fetchall()
        pprint.pprint(pickle_data)                     #Вывести список пользователей (полное имя, телефон) с указанием руководителя (полное имя, телефон)
        pickle_file = open('pickle.pickle','wb')
        pickle.dump(pickle_data, pickle_file)           # сохранить в pickle
        pickle_file.close()
    except Exception as e:
      print(e)
      sys.exit(1)
    finally:
      if con is not None:
        con.close()

def third():
    # Вывести отсортированный список клиентов (имя, телефон) оплативших самые дорогие музыкальные треки.
    try:
        con = None
        con = lite.connect('Chinook_Sqlite.sqlite')
        query_invoice = '''
              SELECT distinct Customer.FirstName, Customer.LastName, Customer.Phone
              FROM Customer 
              LEFT JOIN Invoice ON Customer.CustomerID = Invoice.CustomerID   
              LEFT JOIN InvoiceLine ON InvoiceLine.InvoiceID = Invoice.InvoiceID    
              LEFT JOIN Track ON InvoiceLine.TrackID = Track.TrackID    
              WHERE Track.UnitPrice = (SELECT max(Track.UnitPrice) FROM Track)
              ORDER BY Customer.FirstName
            '''
        curID = con.cursor()
        curID.execute(query_invoice)
        pprint.pprint(curID.fetchall())
    except Exception as e:
      print(e)
      sys.exit(1)
    finally:
      if con is not None:
        con.close()

#Вывести 10 клиентов (id, имя, номер телефона, компания), которых обслужлуживают сотрудники старше 50 лет, оплативших музыку в любом жанре кроме Rock, выходные данные должны быть отсортированы по городу пользователя в алфавитном порядке и емейлу в обратном.
first()                                # работает

#Вывести список пользователей (полное имя, телефон) с указанием руководителя (полное имя, телефон), сохранить в pickle в формате словаря.
#second()

#Вывести отсортированный список клиентов (имя, телефон) оплативших самые дорогие музыкальные треки.

#third()                                # работает
