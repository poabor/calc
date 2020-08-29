from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()

today = datetime.today()


class Table(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=today)

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


class Todo:
    rows = list()

    def __init__(self):
        self.today = datetime.today()
        self.mon = today.strftime('%b')
        self.day_of_week = today.strftime('%A')
        self.day_of_month = today.strftime('%d').lstrip('0')
        self.user_choice = 1
        self.week = 0

    @staticmethod
    def my_menu():
        print()
        print("1) Today's tasks")
        print("2) Week's tasks")
        print("3) All tasks")
        print("4) Missed tasks")
        print("5) Add task")
        print("6) Delete task")
        print("0) Exit")

    def user_action(self):
        while True:
            self.my_menu()
            self.user_choice = int(input())
            if self.user_choice == 0:
                print('\nBye!')
                break
            else:
                if self.user_choice in [1, 2, 3, 4]:
                    self.task_type(self.user_choice)
                elif self.user_choice == 5:
                    self.add()
                elif self.user_choice == 6:
                    self.delete_task(self)
                # else:
                #     pass

    def task_type(self, user_choice):
        self.rows = list()
        if user_choice == 1:  # Today's tasks
            print(f'\nToday {self.today.day} {self.mon}:')
            self.rows = session.query(Table).filter(Table.deadline == self.today.date()).all()
            self.period_task()
        elif user_choice == 2:  # Week's tasks
            for day_time in range(7):
                self.week = self.today.date() + timedelta(days=day_time)
                self.day_of_week = self.week.strftime('%A')
                self.day_of_month = self.week.strftime('%d').lstrip('0')
                self.mon = self.week.strftime('%b')
                self.rows = session.query(Table).filter(Table.deadline == self.week).order_by(Table.deadline).all()
                print(f'\n{self.day_of_week} {self.day_of_month} {self.mon}:')
                self.period_task()
        elif user_choice == 3:  # All tasks
            print('\nAll tasks:')
            self.rows = session.query(Table).order_by(Table.deadline).all()
            self.period_task()
        else:
            print('\nMissed tasks:')
            self.rows = session.query(Table).filter(Table.deadline < self.today.date()).order_by(Table.deadline).all()
            self.period_task()

    def period_task(self):
        if len(self.rows) == 0:
            print('Nothing to do!')
        else:
            for row_id, row in enumerate(self.rows, 1):
                if self.user_choice in [1, 2]:
                    print(f'{row_id}. {row.task}')
                else:
                    print(f"{row_id}. {row.task}. {row.deadline.strftime('%d').lstrip('0')} {row.deadline.strftime('%b')}")
        # print()

    @staticmethod
    def add():
        print('\nEnter task')
        new_task = input()
        print('Enter deadline')
        input_date = datetime.strptime(input(), '%Y-%m-%d')
        new_row = Table(task=new_task, deadline=input_date)
        session.add(new_row)
        session.commit()
        print('The task has been added!')

    @staticmethod
    def delete_task(self):
        print('Choose the number of the task you want to delete:')
        self.rows = session.query(Table).filter(Table.deadline <= self.today.date()).all()
        self.period_task()
        if len(self.rows) > 0:
            task_number = int(input())
            specific_row = self.rows[task_number - 1]  # in case rows is not empty
            session.delete(specific_row)
            session.commit()
            print('The task has been deleted!')


todo_list = Todo()
todo_list.user_action()
