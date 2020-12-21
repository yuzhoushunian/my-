import pymysql
import numpy
import pandas as pd

# 创建连接
conn = pymysql.connect(user='root', password='123456')
# 创建游标
cursor = conn.cursor()
# 创建数据库
create_db = "CREATE DATABASE IF NOT EXISTS RAILWAY_SYSTEM"
cursor.execute(create_db)
# 创建乘客表CUSTOMER(CustomerID,CustomerName,cPasswd,IDNumber,cPhone)
create_customers = """CREATE TABLE CUSTOMERS(
                    CustomerID INT PRIMARY KEY auto_increment,
                    CustomerName VARCHAR(20) NOT NULL,
                    cPasswd VARCHAR(20) NOT NULL,
                    IDNumber BIGINT NOT NULL,
                    cPhone BIGINT NOT NULL,
                    CHECK(IDNumber>99999999999999999 AND IDNumber<1000000000000000000),
                    CHECK(cPhone>9999999999 AND cPhone<100000000000)
                    )"""
cursor.execute(create_customers)
# 创建订单表ORDERS(OrderID,OrderTime,TotalPrice,TotalAmount,CustomerID)
create_orders = """CREATE TABLE ORDERS(
                OrderID INT PRIMARY KEY auto_increment,
                OrderTime DATETIME NOT NULL,
                TotalPrice INT NOT NULL,
                TotalAmount INT NOT NULL,
                CustomerID INT NOT NULL,
                FOREIGN KEY(CustomerID) REFERENCES CUSTOMERS(CustomerID)
                )"""
cursor.execute(create_orders)
# 创建订单详情表ORDER_DETAILS(OrderID,TicketID,TrainID)
create_details = """CREATE TABLE ORDER_DETAILS(
                    OrderID INT,
                    TicketID INT,
                    TrainID INT NOT NULL,
                    PRIMARY KEY(OrderID,TicketID),
                    FOREIGN KEY(OrderID) REFERENCES ORDERS(OrderID),
                    FOREIGN KEY(TicketID) REFERENCES TICKETS(TicketID),
                    FOREIGN KEY(TrainID) REFERENCES TRAIN(TrainID)
                    )"""
cursor.execute(create_details)
# 创建车票表TICKETS(TicketID,SeatID,PriceID,CustomerID)
create_tickets = """CREATE TABLE TICKETS(
                    TicketID INT PRIMARY KEY,
                    SeatID INT NOT NULL,
                    PriceID INT NOT NULL,
                    CustomerID INT NOT NULL,
                    FOREIGN KEY(SeatID) REFERENCES SEATS(SeatID),
                    FOREIGN KEY(PriceID) REFERENCES TICKET_PRICE(PriceID),
                    FOREIGN KEY(CustomerID) REFERENCES CUSTOMERS(CustomerID)
                    )"""
cursor.execute(create_tickets)
# 创建票价表TICKET_PRICE(PriceID,TrainID,StationID_From,StationID_To,Seat1_Price,Seat2_Price,Standing_Price,Sleeper1_Price,Sleeper2_Price)
create_price = """CREATE TABLE TICKET_PRICE(
                PriceID INT PRIMARY KEY,
                TrainID INT NOT NULL,
                StationID_From CHAR(4) NOT NULL,
                StationID_To CHAR(4) NOT NULL,
                Seat1_Price INT,
                Seat2_Price INT,
                Standing_Price INT,
                Sleeper1_Price INT,
                Sleeper2_Price INT,
                FOREIGN KEY(TicketID) REFERENCES TICKETS(TicketID),
                FOREIGN KEY(StationID_From) REFERENCES STATION(StationID),
                FOREIGN KEY(StationID_To) REFERENCES STATION(StationID),
                )"""
cursor.execute(create_price)
# 创建座位表SEATS(SeatID,PassID,SeatClass,Empty)
create_seat = """CREATE TABLE SEATS(
                SeatID INT PRIMARY KEY,
                PassID INT NOT NULL,
                SeatClass INT NOT NULL,
                Empty TINYINT,
                FOREIGN KEY(PassID) REFERENCES Pass(PassID)
                )"""
cursor.execute(create_seat)
# 创建车次表TRAIN(TrainID,ManagerID,Seat1_Num,Seat2_Num,Standing_Num,Sleeper1_Num,Sleeper2_Num)
create_train = """CREATE TABLE TRAIN(
                TrainID INT PRIMARY KEY,
                ManagerID INT NOT NULL,
                Seat1_NUM INT NOT NULL,
                Seat2_NUM INT NOT NULL,
                Standing_NUM INT NOT NULL,
                Sleeper1_NUM INT NOT NULL,
                Sleeper2_NUM INT NOT NULL,
                FOREIGN KEY(ManagerID) REFERENCES MANAGERS(ManagerID)
                )"""
cursor.execute(create_train)
# 创建途径表Pass(PassID,StationID,TrainID,ArriveTime,LeavingTime)
create_pass = """CREATE TABLE PASS(
                PassID INT PRIMARY KEY,
                StationID INT NOT NULL,
                TrainID INT NOT NULL,
                ArriveTime DATETIME NOT NULL,
                LeavingTime DATETIME NOT NULL,
                FOREIGN KEY(StationID) REFERENCES STATION(StationID),
                FOREIGN KEY(TrainID) REFERENCES TRAIN(TrainID)
                )"""
cursor.execute(create_pass)
# 创建站点表STATION(StationID,Station_Name)
create_station = """CREATE TABLE STATION(
                    StationID INT PRIMARY KEY,
                    Station_Name VARCHAR(20) NOT NULL
                    )"""
cursor.execute(create_station)
# 创建管理员表MANAGERS(ManagerID,ManagerName,IDNumber,mPasswd,mPhone)
create_managers = """CREATE TABLE MANAGERS(
                    ManagerID INT PRIMARY KEY auto_increment,
                    ManagerName VARCHAR(20) NOT NULL,
                    mPasswd VARCHAR(20) NOT NULL,
                    IDNumber BIGINT NOT NULL,
                    mPhone BIGINT NOT NULL,
                    CHECK(IDNumber>99999999999999999 AND IDNumber<1000000000000000000),
                    CHECK(mPhone>9999999999 AND mPhone<100000000000)
                    )"""
cursor.execute(create_managers)
# 关闭连接
conn.close()