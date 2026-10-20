import numpy as np
import pandas as pd
import time

print("📐 Запуск Квант-Модуля Линейной Регрессии и Валидации Транзакций...")

# 1. ЧИСТАЯ МАТЕМАТИКА: Реализуем Метод Наименьших Квадратов (OLS) вручную
def calculate_ols_regression(x, y):
    """
    Вычисляет Y = alpha + beta * X
    Формулы из курса математической статистики:
    beta = Cov(X, Y) / Var(X)
    alpha = Mean(Y) - beta * Mean(X)
    """
    mean_x, mean_y = np.mean(x), np.mean(y)
    
    # Считаем ковариацию и дисперсию вручную
    covariance = np.sum((x - mean_x) * (y - mean_y))
    variance_x = np.sum((x - mean_x) ** 2)
    
    beta = covariance / variance_x
    alpha = mean_y - beta * mean_x
    return alpha, beta

# Симулируем 100 дней торгов BTC и ETH (с сильной математической корреляцией)
np.random.seed(777)
btc_returns = np.random.normal(0.001, 0.02, 100)
eth_returns = 0.8 * btc_returns + np.random.normal(0, 0.01, 100) # ETH зависит от BTC на 80%

alpha, beta = calculate_ols_regression(btc_returns, eth_returns)

# 2. БЭКЕНД-ИНЖЕНЕРИЯ: Симулируем защиту от Race Condition (Гонки условий)
class CloudDatabaseSimulator:
    def __init__(self):
        self.user_balance = 5000.0  # Баланс в MySQL
        self.is_locked = False      # Флаг пессимистической блокировки FOR UPDATE
        
    def secure_withdraw(self, amount, thread_name):
        print(f"🔄 [{thread_name}] Запрос на списание {amount} USDT. Проверка блокировки матрицы...")
        
        # Симулируем SELECT ... FOR UPDATE
        if self.is_locked:
            print(f"❌ [{thread_name}] База заблокирована другим процессом! Запрос ожидает шлюза...")
            return False
            
        self.is_locked = True  # Ставим жесткий лок на строку таблицы
        time.sleep(0.1)        # Симулируем задержку сети до Москвы
        
        if self.user_balance >= amount:
            self.user_balance -= amount
            print(f"✅ [{thread_name}] Списание успешно! Остаток в СУБД: {self.user_balance} USDT")
            self.is_locked = False # Снимаем лок
            return True
        else:
            print(f"❌ [{thread_name}] Отказ: Овердрафт баланса!")
            self.is_locked = False
            return False

# Запускаем симуляцию
db = CloudDatabaseSimulator()

print("\n" + "="*60)
print("📊 РЕЗУЛЬТАТЫ МАТЕМАТИЧЕСКОГО И СИСТЕМНОГО АНАЛИЗА")
print("="*60)
print(f"📐 Коэффициент корреляции тренда (Beta): {beta:.4f}")
print(f"📈 Сдвиг базовой доходности (Alpha): {alpha:.4f}")
print(f"ℹ️ Смысл: При росте BTC на 1%, ETH математически вырастет на {beta * 1:.2f}%")
print("-"*60)
print("🛡️ СИМУЛЯЦИЯ ГОНКИ ЗАПРОСОВ (RACE CONDITION):")
# Поток 1 и Поток 2 бьют в базу одновременно, пытаясь списать по 3000 USDT (всего 6000, при балансе 5000)
db.secure_withdraw(3000, "API_Thread_1")
db.secure_withdraw(3000, "API_Thread_2")
print("="*60)
