import sqlite3 as lite
import sys
import pprint
import pickle

def first():               # Рабочий вариант через вложенные запросы
    # Вывести 10 клиентов (id, имя, номер телефона, компания),
    # которых обслужлуживают сотрудники старше 50 лет,
    # оплативших музыку в любом жанре кроме Rock,
    # выходные данные должны быть отсортированы по городу пользователя в алфавитном порядке и емейлу в обратном.
    try:
        con = None
        con = lite.connect('Chinook_Sqlite.sqlite')
        query_invoice = '''
              SELECT Customer.CustomerID, Customer.FirstName, Customer.LastName, Customer.Phone, Customer.Company
              FROM Customer 
              INNER JOIN Employee ON Customer.SupportRepId = Employee.EmployeeId
              WHERE Employee.BirthDate < "1969-05-19" AND 
              EXISTS (SELECT Genre.Name FROM Genre
                  INNER JOIN Track ON Track.GenreId = Genre.GenreId
                  INNER JOIN InvoiceLine ON InvoiceLine.TrackID = Track.TrackID  
                  INNER JOIN Invoice ON InvoiceLine.InvoiceID = Invoice.InvoiceID    
                  INNER JOIN Customer ON Customer.CustomerID = Invoice.CustomerID   
                  WHERE Genre.Name NOT LIKE 'Rock') 
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

def first2():               # Нерабочий вариант
    # Вывести 10 клиентов (id, имя, номер телефона, компания),
    # которых обслужлуживают сотрудники старше 50 лет,
    # оплативших музыку в любом жанре кроме Rock,
    # выходные данные должны быть отсортированы по городу пользователя в алфавитном порядке и емейлу в обратном.
    try:
        con = None
        con = lite.connect('Chinook_Sqlite.sqlite')
        query_invoice = '''
              SELECT Customer.CustomerID, Customer.FirstName, Customer.LastName, Customer.Phone, Customer.Company
              FROM Customer 
              INNER JOIN Employee ON Customer.SupportRepId = Employee.EmployeeId
              INNER JOIN Invoice ON Customer.CustomerID = Invoice.CustomerID   
              INNER JOIN InvoiceLine ON InvoiceLine.InvoiceID = Invoice.InvoiceID    
              INNER JOIN Track ON InvoiceLine.TrackID = Track.TrackID  
              INNER JOIN Genre ON Track.GenreId = Genre.GenreId
              WHERE Genre.Name NOT LIKE 'Rock' AND Employee.BirthDate < "1969-05-19"
              ORDER BY Employee.City ASC, Employee.Email DESC
              -- LIMIT = 10    
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

def first_crutch():             # Без вложенных запросов, но через костыли
    # Вывести 10 клиентов (id, имя, номер телефона, компания),
    # которых обслужлуживают сотрудники старше 50 лет,
    # оплативших музыку в любом жанре кроме Rock,
    # выходные данные должны быть отсортированы по городу пользователя в алфавитном порядке и емейлу в обратном.
    try:
        con = None
        con = lite.connect('Chinook_Sqlite.sqlite')
        query_invoice = '''
              SELECT Customer.CustomerID, Customer.FirstName, Customer.LastName, Customer.Phone, Customer.Company  
              FROM Customer 
              LEFT JOIN Employee ON Customer.SupportRepId = Employee.EmployeeId
              LEFT JOIN Invoice ON Customer.CustomerID = Invoice.CustomerID   
              LEFT JOIN InvoiceLine ON InvoiceLine.InvoiceID = Invoice.InvoiceID    
              LEFT JOIN Track ON InvoiceLine.TrackID = Track.TrackID  
              LEFT JOIN Genre ON Track.GenreId = Genre.GenreId
              WHERE Genre.Name NOT LIKE 'Rock' AND Employee.BirthDate < "1969-05-19"
              ORDER BY Employee.City ASC, Employee.Email DESC
              -- LIMIT = 10    
            '''
        curID = con.cursor()
        curID.execute(query_invoice)
        list_of_all = curID.fetchall()
        good_list = []
        counter = 0
        for iterator in list_of_all:
            if iterator in good_list:
                pass
            else:
                good_list.append(iterator)
                counter += 1
            if counter >= 10:
                break
        pprint.pprint(good_list)

    except Exception as e:
        print(e)
        sys.exit(1)
    finally:
        if con is not None:
            con.close()

def second():                   # Рабочий вариант
    # Вывести список пользователей (полное имя, телефон) с указанием руководителя (полное имя, телефон), сохранить в pickle в формате словаря.
    try:
        con = None
        con = lite.connect('Chinook_Sqlite.sqlite')
        query_invoice = '''
              SELECT e.FirstName, e.LastName, e.Phone, m.FirstName, m.LastName, m.Phone  FROM Employee e, Employee m 
              WHERE m.EmployeeID = e.ReportsTo 
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

def third():                # Рабочий вариант через вложенные запросы
    # Вывести отсортированный список клиентов (имя, телефон) оплативших самые дорогие музыкальные треки.
    try:
        con = None
        con = lite.connect('Chinook_Sqlite.sqlite')
        query_invoice = '''
              SELECT Customer.FirstName, Customer.LastName, Customer.Phone
              FROM Customer
              WHERE EXISTS 
                (SELECT InvoiceLine.UnitPrice from InvoiceLine
                 INNER JOIN Invoice ON InvoiceLine.InvoiceID = Invoice.InvoiceID    
                 INNER JOIN Customer ON Customer.CustomerID = Invoice.CustomerID   
                 WHERE InvoiceLine.UnitPrice = (SELECT max(InvoiceLine.UnitPrice) FROM InvoiceLine)) 
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

def third2():               # Нерабочий вариант
    # Вывести отсортированный список клиентов (имя, телефон) оплативших самые дорогие музыкальные треки.
    try:
        con = None
        con = lite.connect('Chinook_Sqlite.sqlite')
        query_invoice = '''
              SELECT Customer.FirstName, Customer.LastName, Customer.Phone
              FROM Customer 
              LEFT JOIN Invoice ON Customer.CustomerID = Invoice.CustomerID   
              LEFT JOIN InvoiceLine ON InvoiceLine.InvoiceID = Invoice.InvoiceID    
              WHERE InvoiceLine.UnitPrice = (SELECT max(InvoiceLine.UnitPrice) FROM InvoiceLine)
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

def third_crutch():                 # Рабочий вариант без вложенных запросов но через костыль
    # Вывести отсортированный список клиентов (имя, телефон) оплативших самые дорогие музыкальные треки.
    try:
        con = None
        con = lite.connect('Chinook_Sqlite.sqlite')
        query_invoice = '''
              SELECT Customer.FirstName, Customer.LastName, Customer.Phone
              FROM Customer 
              LEFT JOIN Invoice ON Customer.CustomerID = Invoice.CustomerID   
              LEFT JOIN InvoiceLine ON InvoiceLine.InvoiceID = Invoice.InvoiceID    
              WHERE InvoiceLine.UnitPrice = (SELECT max(InvoiceLine.UnitPrice) FROM InvoiceLine)
              ORDER BY Customer.FirstName
            '''
        curID = con.cursor()
        curID.execute(query_invoice)
        list_of_all = curID.fetchall()
        good_list = []
        counter = 0
        for iterator in list_of_all:
            if iterator in good_list:
                pass
            else:
                good_list.append(iterator)
                counter += 1
            if counter >= 100:
                break
        pprint.pprint(good_list)
    except Exception as e:
      print(e)
      sys.exit(1)
    finally:
      if con is not None:
        con.close()

#Вывести 10 клиентов (id, имя, номер телефона, компания), которых обслужлуживают сотрудники старше 50 лет, оплативших музыку в любом жанре кроме Rock, выходные данные должны быть отсортированы по городу пользователя в алфавитном порядке и емейлу в обратном.
first()                                # работает
#first_crutch()                         # работает верно, но с костылём

#Вывести список пользователей (полное имя, телефон) с указанием руководителя (полное имя, телефон), сохранить в pickle в формате словаря.
second()

#Вывести отсортированный список клиентов (имя, телефон) оплативших самые дорогие музыкальные треки.
third()                                # работает
#third_crutch()                          # работает верно, но с костылём
