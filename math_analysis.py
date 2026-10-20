import numpy as np
from scipy import stats

# Моделируем 1000 дней торгов: случайные процентные изменения цены монеты SOL
# (Используем генератор случайных чисел на основе нормального распределения)
np.random.seed(42)
historical_returns = np.random.normal(loc=0.05, scale=2.5, size=1000)

# 1. Считаем матстатистику (Выборочное среднее и Дисперсию)
mean_return = np.mean(historical_returns)
std_deviation = np.std(historical_returns)

# 2. Теория вероятностей: считаем вероятность того, что в следующий день 
# цена монеты SOL упадет более чем на 5% (критический риск ликвидации на Aave)
critical_drop = -5.0
probability_of_crash = stats.norm.cdf(critical_drop, loc=mean_return, scale=std_deviation)

print("=== РЕЗУЛЬТАТЫ МАТЕМАТИЧЕСКОГО МОДЕЛИРОВАНИЯ РИСКОВ ===")
print(f"📊 Математическое ожидание доходности: {mean_return:.4f}%")
print(f"📉 Среднеквадратичное отклонение (Волатильность): {std_deviation:.4f}%")
print(f"🚨 Вероятность критического падения рынка (< -5%): {probability_of_crash * 100:.2f}%")
