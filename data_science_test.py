import numpy as np
import pandas as pd

# 1. Генерируем даты за последние 365 дней
dates = pd.date_range(end=pd.Timestamp.now(), periods=365)

# 2. Моделируем "случайное блуждание" (генерация тренда цены монеты SOL)
np.random.seed(100)
daily_returns = np.random.normal(loc=0.001, scale=0.03, size=365) # Матожидание +0.1%, волатильность 3%
price_series = 150 * np.exp(np.cumsum(daily_returns)) # Стартуем со стоимости $150

# 3. Упаковываем данные в матрицу Pandas DataFrame
df = pd.DataFrame(data={"Price": price_series, "Return": daily_returns}, index=dates)

# 4. МАТЕМАТИЧЕСКИЙ АНАЛИЗ В ОДНУ СТРОКУ:
# Рассчитываем 30-дневное скользящее среднее (сглаживаем ценовой шум)
df["MA_30"] = df["Price"].rolling(window=30).mean()

# 5. НАХОДИМ СТАТИСТИЧЕСКИЕ АНОМАЛИИ (Дни экстремальной волатильности)
# Считаем среднее и стандартное отклонение (сигма) доходностей
mean_ret = df["Return"].mean()
std_ret = df["Return"].std()

# Аномалия — это день, когда доходность отклонилась от средней более чем на 2 сигмы!
df["Anomaly"] = (df["Return"] > mean_ret + 2 * std_ret) | (df["Return"] < mean_ret - 2 * std_ret)
anomalies_count = df["Anomaly"].sum()

print("=== РЕЗУЛЬТАТЫ QUANT-АНАЛИЗА МАТРИЦЫ PANDAS ===")
print(f"📊 Всего проанализировано торговых дней: {len(df)}")
print(f"📈 Финальная смоделированная цена актива: ${df['Price'].iloc[-1]:.2f}")
print(f"📉 Обнаружено статистических аномалий (выбросов): {anomalies_count} дней")
print("\n📝 Первые 5 дней матрицы после расчета скользящей средней:")
print(df[["Price", "MA_30", "Anomaly"]].tail(5))
