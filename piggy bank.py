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
            return f'Поздравляем! Цель "{self.goal_name}" достигнута. Ваш баланс: {self._current_balance}'
        else:
            self.progress = self._current_balance * 100 // self.sum
            self.deposit_history.append({'сумма':amount, 'дата':date.today()})
            self.left_to_collect = self.sum - self._current_balance
            Goal.all_progress[self.goal_name] = self.progress
            if self.progress >= 50:
                return f'Половина суммы в копилке! Ваш баланс {self._current_balance}'
            else:
                return f'Ура! Вы стали ближе к своей цели "{self.goal_name}" на {amount} руб!\nВаш текущий баланс: {self._current_balance} руб'
                
    def withdrawal(self, amount):
        if amount > self._current_balance:
            raise ValueError('Не хватает средств для снятия суммы')    
        
        self._current_balance -= amount 
        self.progress = self._current_balance * 100 // self.sum
        self.left_to_collect = self.sum - self._current_balance
        Goal.all_progress[self.goal_name] = self.progress
        return f'Минус {amount} руб в копилке для цели "{self.goal_name}".\nВаш баланс: {self._current_balance} руб. Копим дальше!' 
        
    def get_progress(self):
        return f'Цель "{self.goal_name}" выполнена на {self.progress} %' 
        
    def info(self):
        return {'цель':self.goal_name, 'категория':self.category, 'сумма':self.sum, 'статус':self.status, 'накоплено': self.progress}   
        
    @classmethod
    def all_goals_progress(cls):
        for key, value in cls.all_progress.items():
            print(f'Цель "{key}" выполнена на {value} %')
          
class Notebook:
    def __init__(self):
        self.goals = {}
        self.user_input = ''
        self.deadline = None
        self.aver_deposit = 0
        self.aver_freq = None
        
    def goal_deadline(self, goal: Goal):
        self.user_input = input('Введите желаемую дату достижения цели в формате гггг/мм/дд без пробелов ')
        isValidDate = True
        try:
            datetime.strptime(self.user_input, '%Y/%m/%d')
        except ValueError:
            isValidDate = False    
        if (isValidDate):
            self.goals[goal].setdefault('копим до', datetime.strptime(self.user_input, '%Y/%m/%d'))
            print('Дата успешно добавлена')
        else:
            print('Введенная дата не соответствует формату')

    def add_goal(self, goal: Goal, creation_date = date.today()):
        self.goals.setdefault(goal, goal.info())
        self.goals[goal].setdefault('дата создания', creation_date)
        return f'Цель добавлена в блокнот {creation_date}'
        
    def del_goal(self, goal: Goal):
        self.user_input = input(f'Вы действительно хотите удалить цель "{self.goals[goal]['цель']}"? Введите "да" или "нет" ')
        if self.user_input == 'нет':
            return 'Ok,цель остается в блокноте'
        else:
            del self.goals[goal]
            return 'Цель удалена из блокнота'
        
    def left_to_deadline(self, goal: Goal):
        if 'копим до' in self.goals[goal]:
            self.deadline = self.goals[goal]['копим до'] - datetime.now()
            return f'Осталось {self.deadline.days} дней до установленной даты достижения цели "{self.goals[goal]['цель']}"'
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
        return f'Предполагаемая дата достижения цели "{self.goals[goal]['цель']}": {goal.deposit_history[len(goal.deposit_history) - 1]['дата'] + (goal.left_to_collect // self.aver_deposit * self.aver_freq)}'


    def get_goals(self):
        for value in self.goals.values():
            for key, value in value.items():
                print(key, ':', value)
            print()
 # пояснения для формулы def suggested_achivement_date: делим сумму, которую осталось
 # накопить на среднюю сумму пополнения и получаем сколько таких средних сумм нам 
 # еще нужно внести. Умножаем это число на средний отрезок времени между пополнениями
 #(для вычисления среднего отрезка находим разность между датой создания цели и датой последнего
 # пополнения и делим на количество пополнений). Полученный отрезок времени прибавляем к 
 # дате последнего пополнения.               

notebook1 = Notebook() 

objs = []

def create_goals(notebook, obj_list):
    categories = ['отдых', 'работа', 'здоровье', 'учеба', 'стиль', 'транспорт', 'дом', 'разное']

    while True:
        name = input('Введите название цели ')
        print()
        while True:
            sum_goal = input('Введите сумму для накопления ')
            if sum_goal.isdigit() == False:
                print('Cумма должна содержать только числовые значения. Попробуйте снова')
            else:
                break
        print()
        print('Выберите и введите название категории для своей цели ')
        print()
        for ind, item in enumerate(categories, start=1):
            print(ind, item)
        print()     
            
        category = input()  
        object = Goal(name, int(sum_goal), category)
        obj_list.append(object)
        notebook.add_goal(object)
        print()
        while True:
            answer = input('Вы хотите добавить еще одну цель? Введите "да" или "нет" ')
            if answer != 'нет' and answer != 'да':
                print('Вы ввели неверное слово. Введите "да" или "нет"')
            else:
                break       
    
        if answer == 'нет':
            break
#примеры вызова методов для 2х целей
create_goals(notebook1, objs)
print()   
notebook1.get_goals()
print()        
print(objs[0].deposit(1500))
print()
print(Goal.all_goals_progress())
print()
print(notebook1.suggested_achivement_date(objs[0]))
print()
notebook1.goal_deadline(objs[0])
print()
print(notebook1.left_to_deadline(objs[0]))
print()
print(objs[0].withdrawal(500))
print()
print(notebook1.del_goal(objs[1]))
print()
notebook1.get_goals()
print()
print(objs[0].get_progress())



    