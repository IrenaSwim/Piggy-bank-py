from datetime import datetime, date, timedelta

class Goal:
    all_progress = {}
    
    def __init__(self, goal_name, sum, category, current_balance=0, status='в процессе'):
        self.goal_name = goal_name 
        self.sum = sum
        self.category = category 
        self._current_balance = current_balance 
        self.status = status
        self.left_to_collect = 0
        self.progress = 0
        self.deposit_history = []
        Goal.all_progress.setdefault(self.goal_name, self.progress)
          
    def __str__(self):
        return f'Ваша цель: {self.goal_name}\nНужно накопить {self.sum} руб\nВаш баланс: {self._current_balance}'
        
    def __repr__(self):
        return f'Goal {self.goal_name}, {self.sum}, {self.category}, {self._current_balance}, {self.status}'
    
    def deposit(self, amount):
        if amount < 0:
            raise ValueError('Нельзя внести отрицательную сумму')
           
        self._current_balance += amount
        
        if self._current_balance >= self.sum:
            self.progress = 100
            self.deposit_history.append({'сумма':amount, 'дата':date.today()})
            self.left_to_collect = 0
            Goal.all_progress[self.goal_name] = self.progress
            print(f'Поздравляем! Цель "{self.goal_name}" достигнута. Ваш баланс: {self._current_balance}')
        else:
            self.progress = self._current_balance * 100 // self.sum
            self.deposit_history.append({'сумма':amount, 'дата':date.today()})
            self.left_to_collect = self.sum - self._current_balance
            Goal.all_progress[self.goal_name] = self.progress
            if self.progress >= 50:
                return f'Половина суммы в копилке! Ваш баланс {self._current_balance}'
            else:
                return f'Ура! Вы стали ближе к своей цели на {amount} руб!\nВаш текущий баланс: {self._current_balance} руб'
              
        
    def withdrawal(self, amount):
        if amount > self._current_balance:
            raise ValueError('Не хватает средств для снятия суммы')    
        
        self._current_balance -= amount 
        self.progress = self._current_balance * 100 // self.sum
        self.left_to_collect = self.sum - self._current_balance
        Goal.all_progress[self.goal_name] = self.progress
        return f'Минус {amount} руб в копилке.\nВаш баланс: {self._current_balance} руб. Копим дальше!' 
        
    def get_progress(self):
        return f'Цель выполнена на {self.progress} %' 
        
    def info(self):
        return {'цель':self.goal_name, 'категория':self.category, 'сумма':self.sum, 'статус':self.status, 'накоплено': self.progress}   
        
    @classmethod
    def all_goals_progress(cls):
        for key, value in cls.all_progress.items():
            print(f'Цель {key} выполнена на {value} %')
            
class Notebook:
    def __init__(self):
        self.goals = {}
        self.user_input = ''
        self.deadline = None
        self.aver_deposit = 0
        self.aver_freq = None
        
    def goal_deadline(self, goal: Goal):
        self.user_input = input('Введите желаемую дату достижения цели в формате гггг/мм/дд без пробелов ')
        self.goals[goal].setdefault('копим до', datetime.strptime(self.user_input, '%Y/%m/%d'))
        return 'Дата успешно добавлена'
        
    def add_goal(self, goal: Goal, creation_date = date.today()):
        self.goals.setdefault(goal, goal.info())
        self.goals[goal].setdefault('дата создания', creation_date)
        print(f'Цель добавлена в блокнот {creation_date}')
        
    def del_goal(self, goal: Goal):
        self.user_input = input('Вы действительно хотите удалить эту цель? Введите "да" или "нет" ')
        if self.user_input == 'нет':
            return 'Ok,цель остается в блокноте'
        else:
            del self.goals[goal]
            return 'Цель удалена из блокнота'
        
    def left_to_deadline(self, goal: Goal):
        if 'копим до' in self.goals[goal]:
            self.deadline = self.goals[goal]['копим до'] - datetime.now()
            return f'Осталось {self.deadline.days} дней до установленной даты достижения цели'
        else:
            print('Дата достижения цели не установлена. Хотите установить? Введите "да" или "нет" ')
            self.user_input = input()
            if self.user_input == 'да':
                self.goal_deadline(goal)
            else:
                return 'Возможно позже.'    

    def suggested_achivement_date(self, goal: Goal):
        self.aver_deposit = sum(d['сумма'] for d in goal.deposit_history) // len(goal.deposit_history) #средняя сумма пополнений
        if goal.deposit_history[len(goal.deposit_history) - 1]['дата'] == self.goals[goal]['дата создания']:
            self.aver_freq = timedelta(days=1)
        else:
            self.aver_freq = (goal.deposit_history[len(goal.deposit_history) - 1]['дата'] - self.goals[goal]['дата создания']) // len(goal.deposit_history)#средняя частота пополнений (delta object)
        return f'Предполагаемая дата достижения цели: {goal.deposit_history[len(goal.deposit_history) - 1]['дата'] + (goal.left_to_collect // self.aver_deposit * self.aver_freq)}'


    def get_goals(self):
        for value in self.goals.values():
            for key, value in value.items():
                print(key, ':', value)
            print()

 # пояснения для формулы def suggested_achivement_date: делим сумму, которую осталось
 # накопить на среднюю сумму поподнения и получаем сколько таких средних сумм нам 
 # еще нужно внести. Умножаем это число на средний отрезок времени между пополнениями
 #(для вычисления среднего отрезка находим разность между датой создания цели и датой последнего
 # пополнения и делим на количество пополнений). Полученный отрезок времени прибавляем к 
 # дате последнего пополнения.               

notebook1 = Notebook() 

objs = []

categories = ['отдых', 'работа', 'здоровье', 'учеба', 'стиль', 'транспорт', 'дом', 'разное']

while True:
    name = input('Введите название цели ')
    print()
    sum_goal = int(input('Введите сумму для накопления '))
    print()
    print('Выберите и введите название категории для своей цели ')
    print()
    for ind, item in enumerate(categories, start=1):
        print(ind, item) 
        
    category = input()  
    object = Goal(name, sum_goal, category)
    objs.append(object)
    notebook1.add_goal(object)
    answer = input('Вы хотите добавить еще одну цель? Введите "да" или "нет" ')    
    if answer == 'нет':
        break
    
print(objs[0].deposit(1500))
print(notebook1.suggested_achivement_date(objs[0]))



    