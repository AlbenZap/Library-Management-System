from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import pymysql
from PyQt5.uic import loadUiType
import datetime

ui, _ = loadUiType('library.ui')
login, _ = loadUiType('login.ui')


class Login(QWidget , login):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.Handle_Login)
        style = open('themes/darkgray.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Handle_Login(self):
        self.db = pymysql.connect(host='localhost', port=8080 , user='root', password='root', db='library')
        self.cur = self.db.cursor()

        username = self.lineEdit.text()
        password = self.lineEdit_2.text()

        sql = ''' SELECT * FROM users '''

        self.cur.execute(sql)
        data = self.cur.fetchall()
        for row in data:
            if username == row[1] and password == row[3]:
                print('User Matched')
                self.window2 = MainApp()
                self.close()
                self.window2.show()

            else:
                self.label.setText('Make Sure You Have Entered Your Username and Password Correctly')

class MainApp(QMainWindow , ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handle_UI_Changes()
        self.Handle_Buttons()
        self.Dark_Gray_Theme()

        self.Show_Category()
        self.Show_Author()
        self.Show_Publisher()

        self.Show_Category_ComboBox()
        self.Show_Author_ComboBox()
        self.Show_Publisher_ComboBox()

        self.Show_All_Clients()
        self.Show_All_Books()
        self.Show_All_Operations()

    def Handle_UI_Changes(self):
        self.Hiding_Themes()
        self.tabWidget.tabBar().setVisible(False)

    def Handle_Buttons(self):
        self.pushButton_5.clicked.connect(self.Show_Themes)
        self.pushButton_21.clicked.connect(self.Hiding_Themes)

        self.pushButton.clicked.connect(self.Open_Day_To_Day_Tab)
        self.pushButton_2.clicked.connect(self.Open_Books_Tab)
        self.pushButton_3.clicked.connect(self.Open_Clients_Tab)
        self.pushButton_26.clicked.connect(self.Open_Users_Tab)
        self.pushButton_4.clicked.connect(self.Open_Settings_Tab)

        self.pushButton_7.clicked.connect(self.Add_New_Book)
        self.pushButton_11.clicked.connect(self.Search_Books)
        self.pushButton_8.clicked.connect(self.Edit_Books)
        self.pushButton_12.clicked.connect(self.Delete_Books)

        self.pushButton_22.clicked.connect(self.Add_Category)
        self.pushButton_24.clicked.connect(self.Add_Author)
        self.pushButton_25.clicked.connect(self.Add_Publisher)

        self.pushButton_13.clicked.connect(self.Add_New_User)
        self.pushButton_14.clicked.connect(self.Login)
        self.pushButton_15.clicked.connect(self.Edit_User)

        self.pushButton_18.clicked.connect(self.Dark_Orange_Theme)
        self.pushButton_17.clicked.connect(self.Dark_Blue_Theme)
        self.pushButton_19.clicked.connect(self.Dark_Gray_Theme)
        self.pushButton_20.clicked.connect(self.QDark_Theme)

        self.pushButton_9.clicked.connect(self.Add_New_Client)
        self.pushButton_16.clicked.connect(self.Search_Client)
        self.pushButton_10.clicked.connect(self.Edit_Client)
        self.pushButton_23.clicked.connect(self.Delete_Client)

        self.pushButton_6.clicked.connect(self.Handle_Day_Operations)


    def Show_Themes(self):
        self.groupBox_3.show()

    def Hiding_Themes(self):
        self.groupBox_3.hide()

    ##########################################################
    ################### Opening Tabs #########################

    def Open_Day_To_Day_Tab(self):
        self.tabWidget.setCurrentIndex(0)

    def Open_Books_Tab(self):
        self.tabWidget.setCurrentIndex(1)

    def Open_Clients_Tab(self):
        self.tabWidget.setCurrentIndex(2)

    def Open_Users_Tab(self):
        self.tabWidget.setCurrentIndex(3)

    def Open_Settings_Tab(self):
        self.tabWidget.setCurrentIndex(4)


    ##########################################################
    ################## Day Operations ########################

    def Handle_Day_Operations(self):
        book_title = self.lineEdit.text()
        client_name = self.lineEdit_25.text()
        type = self.comboBox.currentText()
        days_number = self.comboBox_2.currentIndex() + 1
        today_date = datetime.date.today()
        to_date = today_date +  datetime.timedelta(days=days_number)

        print(today_date)
        print(to_date)

        self.db = pymysql.connect(host='localhost', port=8080, user='root', password='root', db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''
            INSERT INTO dayoperations(book_name , client , type , days , date , to_date)
            VALUES (%s , %s , %s , %s , %s , %s)
        ''' , (book_title , client_name , type , days_number , today_date , to_date))

        self.db.commit()
        self.statusBar().showMessage('New Operation Added')

        self.Show_All_Operations()


    def Show_All_Operations(self):
        self.db = pymysql.connect(host='localhost', port=8080, user='root', password='root', db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''
            SELECT book_name , client , type , date , to_date FROM dayoperations
        ''')

        data = self.cur.fetchall()
        print(data)

        self.tableWidget.setRowCount(0)
        self.tableWidget.insertRow(0)
        for row , form in enumerate(data):
            for column , item in enumerate(form):
                self.tableWidget.setItem(row , column , QTableWidgetItem(str(item)))
                column += 1

            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)

    ##########################################################
    ######################## Books ###########################

    def Show_All_Books(self):
        self.db = pymysql.connect(host='localhost', port=8080, user='root', password='root', db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''
            SELECT book_code,book_name,book_description,book_category,book_author,book_publisher,book_price FROM book
        ''')
        data = self.cur.fetchall()

        print(data)
        self.tableWidget_3.setRowCount(0)
        self.tableWidget_3.insertRow(0)

        for row, form in enumerate(data):
            for column, item in enumerate(form):
                self.tableWidget_3.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1

            row_position = self.tableWidget_3.rowCount()
            self.tableWidget_3.insertRow(row_position)

        self.db.close()



    def Add_New_Book(self):
        self.db = pymysql.connect(host='localhost', port=8080, user='root', password='root', db='library')
        self.cur = self.db.cursor()

        book_title = self.lineEdit_2.text()
        book_description = self.textEdit_2.toPlainText()
        book_code = self.lineEdit_3.text()
        book_category = self.comboBox_3.currentText()
        book_author = self.comboBox_4.currentText()
        book_publisher = self.comboBox_5.currentText()
        book_price = self.lineEdit_4.text()

        self.cur.execute('''
            INSERT INTO book(book_name, book_description, book_code, book_category, book_author, book_publisher, book_price)
            VALUES (%s  , %s , %s , %s , %s , %s , %s)
            ''' ,(book_title , book_description , book_code , book_category , book_author , book_publisher , book_price))

        self.db.commit()
        self.statusBar().showMessage('New Book Added')

        self.lineEdit_2.setText('')
        self.textEdit_2.setPlainText('')
        self.lineEdit_3.setText('')
        self.comboBox_3.setCurrentIndex(0)
        self.comboBox_4.setCurrentIndex(0)
        self.comboBox_5.setCurrentIndex(0)
        self.lineEdit_4.setText('')
        self.Show_All_Books()

    def Search_Books(self):
        self.db = pymysql.connect(host='localhost', port=8080, user='root', password='root', db='library')
        self.cur = self.db.cursor()

        book_title = self.lineEdit_14.text()

        sql = ''' SELECT * FROM book WHERE book_name = %s '''
        self.cur.execute(sql , [(book_title)])

        data = self.cur.fetchone()

        self.lineEdit_5.setText(data[1])
        self.textEdit.setPlainText(data[2])
        self.lineEdit_6.setText(data[3])
        self.comboBox_7.setCurrentText(data[4])
        self.comboBox_6.setCurrentText(data[5])
        self.comboBox_8.setCurrentText(data[6])
        self.lineEdit_7.setText(str(data[7]))



    def Edit_Books(self):
        self.db = pymysql.connect(host='localhost', port=8080, user='root', password='root', db='library')
        self.cur = self.db.cursor()

        book_title = self.lineEdit_5.text()
        book_description = self.textEdit.toPlainText()
        book_code = self.lineEdit_6.text()
        book_category = self.comboBox_7.currentText()
        book_author = self.comboBox_6.currentText()
        book_publisher = self.comboBox_8.currentText()
        book_price = self.lineEdit_7.text()

        search_book_title = self.lineEdit_14.text()

        self.cur.execute('''
            UPDATE book SET book_name=%s,book_description=%s,book_code=%s,book_category=%s,book_author=%s,book_publisher=%s,book_price=%s WHERE book_name=%s 
            ''',(book_title , book_description , book_code , book_category , book_author , book_publisher , book_price , search_book_title))

        self.db.commit()
        self.statusBar().showMessage('Book Updated')
        self.Show_All_Books()


    def Delete_Books(self):
        self.db = pymysql.connect(host='localhost', port=8080, user='root', password='root', db='library')
        self.cur = self.db.cursor()

        book_title = self.lineEdit_14.text()

        warning = QMessageBox.warning(self , 'Delete Book' , "Are you sure you want to delete this book?" , QMessageBox.Yes | QMessageBox.No)
        if warning == QMessageBox.Yes:
            sql = ''' DELETE FROM book WHERE book_name = %s '''
            self.cur.execute(sql , [(book_title)])
            self.db.commit()
            self.statusBar().showMessage('Book Deleted')

            self.Show_All_Books()

    ##########################################################
    ######################## Clients ###########################

    def Show_All_Clients(self):
        self.db = pymysql.connect(host='localhost', port=8080, user='root', password='root', db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''
            SELECT client_name , client_email , client_id FROM clients
        ''')
        data = self.cur.fetchall()

        print(data)
        self.tableWidget_6.setRowCount(0)
        self.tableWidget_6.insertRow(0)

        for row , form in enumerate(data):
            for column , item in enumerate(form):
                self.tableWidget_6.setItem(row , column , QTableWidgetItem(str(item)))
                column += 1

            row_position = self.tableWidget_6.rowCount()
            self.tableWidget_6.insertRow(row_position)

        self.db.close()

    def Add_New_Client(self):
        client_name = self.lineEdit_8.text()
        client_email = self.lineEdit_9.text()
        client_id = self.lineEdit_10.text()

        self.db = pymysql.connect(host='localhost', port=8080, user='root', password='root', db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''
            INSERT INTO clients(client_name , client_email , client_id)
            VALUES (%s , %s , %s)
        ''' , (client_name , client_email , client_id))

        self.db.commit()
        self.db.close()
        self.statusBar().showMessage('New Client Added')
        self.Show_All_Clients()

    def Search_Client(self):
        client_id = self.lineEdit_24.text()
        self.db = pymysql.connect(host='localhost', port=8080, user='root', password='root', db='library')
        self.cur = self.db.cursor()

        sql = ''' SELECT * FROM clients WHERE client_id = %s '''
        self.cur.execute(sql , [(client_id)])
        data = self.cur.fetchone()
        print(data)

        self.lineEdit_13.setText(data[1])
        self.lineEdit_12.setText(data[2])
        self.lineEdit_11.setText(data[3])

    def Edit_Client(self):
        client_original_id = self.lineEdit_24.text()
        client_name = self.lineEdit_13.text()
        client_email = self.lineEdit_12.text()
        client_id = self.lineEdit_11.text()

        self.db = pymysql.connect(host='localhost', port=8080, user='root', password='root', db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''
            UPDATE clients SET client_name = %s , client_email = %s , client_id = %s WHERE client_id = %s
        ''' , (client_name , client_email , client_id , client_original_id))
        self.db.commit()
        self.db.close()
        self.statusBar().showMessage('Client Data Updated')
        self.Show_All_Clients()

    def Delete_Client(self):
        client_original_id = self.lineEdit_24.text()

        warning_message = QMessageBox.warning(self , "Delete Client" , "Are you sure you want to delete this client?" , QMessageBox.Yes | QMessageBox.No)

        if warning_message == QMessageBox.Yes:
            self.db = pymysql.connect(host='localhost', port=8080, user='root', password='root', db='library')
            self.cur = self.db.cursor()

            sql = ''' DELETE FROM clients WHERE client_id = %s '''
            self.cur.execute(sql , [(client_original_id)])

            self.db.commit()
            self.db.close()
            self.statusBar().showMessage('Client Deleted')
            self.Show_All_Clients()

    ##########################################################
    ######################## Users ###########################

    def Add_New_User(self):
        self.db = pymysql.connect(host='localhost', port=8080, user='root', password='root', db='library')
        self.cur = self.db.cursor()

        username = self.lineEdit_15.text()
        email = self.lineEdit_16.text()
        password = self.lineEdit_18.text()
        password2 = self.lineEdit_17.text()

        if password == password2:
            self.cur.execute('''
            INSERT INTO users(user_name, user_email, user_password)
            VALUES (%s , %s , %s)
            ''' ,(username , email , password))

            self.db.commit()
            self.statusBar().showMessage('New User Added')

        else:
            self.label_45.setText('Please enter the same password as entered earlier')

    def Login(self):
        self.db = pymysql.connect(host='localhost', port=8080 , user='root', password='root', db='library')
        self.cur = self.db.cursor()

        username = self.lineEdit_20.text()
        password = self.lineEdit_19.text()

        sql = ''' SELECT * FROM users '''

        self.cur.execute(sql)
        data = self.cur.fetchall()
        for row in data:
            if username == row[1] and password == row[3]:
                print('User Matched')
                self.statusBar().showMessage('Valid Username and Password')
                self.groupBox_4.setEnabled(True)

                self.lineEdit_26.setText(row[1])
                self.lineEdit_21.setText(row[2])
                self.lineEdit_22.setText(row[3])


    def Edit_User(self):
        username = self.lineEdit_26.text()
        email = self.lineEdit_21.text()
        password = self.lineEdit_22.text()
        password2 = self.lineEdit_23.text()

        original_name = self.lineEdit_20.text()

        if password == password2:
            self.db = pymysql.connect(host='localhost', port=8080, user='root', password='root', db='library')
            self.cur = self.db.cursor()

            self.cur.execute('''
                UPDATE users SET user_name=%s,user_email=%s,user_password=%s WHERE user_name=%s
            ''',(username , email , password , original_name))

            self.db.commit()
            self.statusBar().showMessage('User Data Updated Succesfully')
        else:
            print('Make sure you have entered your password correctly')

    ##########################################################
    ##################### Settings ###########################

    def Add_Category(self):
        self.db = pymysql.connect(host='localhost', port=8080 , user='root', password='root', db='library')
        self.cur = self.db.cursor()

        category_name = self.lineEdit_27.text()

        self.cur.execute('''
                INSERT INTO category (category_name) VALUES(%s)''',(category_name,))
        self.db.commit()
        self.statusBar().showMessage('New Category Added')
        self.lineEdit_27.setText('')
        self.Show_Category()
        self.Show_Category_ComboBox()

    def Show_Category(self):
        self.db = pymysql.connect(host='localhost', port=8080, user='root', password='root', db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT category_name FROM category''')
        data = self.cur.fetchall()

        print(data)

        if data:
            self.tableWidget_2.setRowCount(0)
            self.tableWidget_2.insertRow(0)
            for row , form in enumerate(data):
                for column , item in enumerate(form):
                    self.tableWidget_2.setItem(row , column , QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_2.rowCount()
                self.tableWidget_2.insertRow(row_position)


    def Add_Author(self):
        self.db = pymysql.connect(host='localhost', port=8080, user='root', password='root', db='library')
        self.cur = self.db.cursor()

        author_name = self.lineEdit_29.text()

        self.cur.execute('''
                INSERT INTO authors (author_name) VALUES(%s)''',(author_name,))
        self.db.commit()
        self.lineEdit_29.setText('')
        self.statusBar().showMessage('New Author Added')
        self.Show_Author()
        self.Show_Author_ComboBox()

    def Show_Author(self):
        self.db = pymysql.connect(host='localhost', port=8080, user='root', password='root', db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT author_name FROM authors''')
        data = self.cur.fetchall()

        print(data)

        if data:
            self.tableWidget_4.setRowCount(0)
            self.tableWidget_4.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_4.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_4.rowCount()
                self.tableWidget_4.insertRow(row_position)


    def Add_Publisher(self):
        self.db = pymysql.connect(host='localhost', port=8080, user='root', password='root', db='library')
        self.cur = self.db.cursor()

        publisher_name = self.lineEdit_30.text()

        self.cur.execute('''
                INSERT INTO publisher (publisher_name) VALUES(%s)''',(publisher_name,))
        self.db.commit()
        self.lineEdit_30.setText('')
        self.statusBar().showMessage('New Publisher Added')
        self.Show_Publisher()
        self.Show_Publisher_ComboBox()

    def Show_Publisher(self):
        self.db = pymysql.connect(host='localhost', port=8080, user='root', password='root', db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT publisher_name FROM publisher''')
        data = self.cur.fetchall()

        print(data)

        if data:
            self.tableWidget_5.setRowCount(0)
            self.tableWidget_5.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_5.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_5.rowCount()
                self.tableWidget_5.insertRow(row_position)

    ##########################################################
    ############## Show_Settings_Data_In_UI ##################

    def Show_Category_ComboBox(self):
        self.db = pymysql.connect(host='localhost', port=8080, user='root', password='root', db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT category_name FROM category ''')
        data = self.cur.fetchall()

        self.comboBox_3.clear()
        for category in data:
            self.comboBox_3.addItem(category[0])
            self.comboBox_7.addItem(category[0])




    def Show_Author_ComboBox(self):
        self.db = pymysql.connect(host='localhost', port=8080, user='root', password='root', db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT author_name FROM authors ''')
        data = self.cur.fetchall()

        self.comboBox_4.clear()
        for author in data:
            self.comboBox_4.addItem(author[0])
            self.comboBox_6.addItem(author[0])

    def Show_Publisher_ComboBox(self):
        self.db = pymysql.connect(host='localhost', port=8080, user='root', password='root', db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT publisher_name FROM publisher ''')
        data = self.cur.fetchall()

        self.comboBox_5.clear()
        for publisher in data:
            self.comboBox_5.addItem(publisher[0])
            self.comboBox_8.addItem(publisher[0])

    ##########################################################
    ##################### UI Themes ##########################

    def Dark_Blue_Theme(self):
        style = open('themes/darkblue.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Dark_Gray_Theme(self):
        style = open('themes/darkgray.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Dark_Orange_Theme(self):
        style = open('themes/darkorange.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def QDark_Theme(self):
        style = open('themes/qdark.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

def main():
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
