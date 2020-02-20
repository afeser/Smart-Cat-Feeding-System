import datetime
import pickle
import os

class Cat:
    '''
    Cat object for various purposes.

    DATABASE
    ------------
    - On exit or destruction, it saves the object to database.
    - If id already exists in database, it automatically loads, otherwise it
        creates an empty database
    '''
    def __init__(self, id):
        # Cat identity
        self._id      = id
        self._name    = None
        self._picture = None

        # Eat logs...
        self._eatTimes   = []
        self._eatAmounts = []
        # Usual amount that cat eats, specified by the user
        self._normalEatAmount = 0

        # Database
        self._databaseDir = 'database'
        if os.path.exists(self._databaseDir):
            os.makedirs(self._databaseDir)
        if os.path.exists(self._databaseDir + '/' + self._id):
            with open(self._databaseDir + '/' + self._id, 'r') as f:
                save = pickle.load(f)
                [self._id, \
                self._name, \
                self._picture, \
                self._eatTimes, \
                self._eatAmounts, \
                self._normalEatAmount] = save

    def __del__(self):
        save = [
            self._id,
            self._name,
            self._picture,
            self._eatTimes,
            self._eatAmounts,
            self._normalEatAmount
        ]
        with open(self._databaseDir + '/' + self._id, 'r') as f:
            pickle.dump(f, save)

    def getId(self):
        return self._id
    def getName(self):
        return self._name
    def getPicture(self):
        return self._picture
    def getLastEatTime(self):
        return self._eatTimes[-1]
    def getEatTimes(self):
        return self._eatTimes
    def getEatAmounts(self):
        return self._eatAmounts
    def getTotalFoodGiven(self):
        return sum(self._eatAmounts)
    def getEatAmount(self):
        return self._normalEatAmount
    def setEatAmount(self, normalEatAmount):
        self._normalEatAmount = normalEatAmount
    def setName(self, name):
        self._name = name
    def setPicture(self, picture):
        self._picture = picture
    def fed(self, foodAmount=None):
        '''
        Trigger if this cat is detected and fed through the system
        '''
        if foodAmount is None:
            logging.info('Cat is fed with normal amount + ' str(self._normalEatAmount))
            foodAmount = self._normalEatAmount

        self._eatTimes.append(datetime.datetime.now())
        self._eatAmounts.append(foodAmount)
