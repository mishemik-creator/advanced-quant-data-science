import numpy as np
import pandas as pd

print("📐 Запуск Квант-Модуля Скрытых Марковских Режимов Рынка...")

# 1. ЧИСТАЯ МАТЕМАТИКА: Симулируем смену режимов рынка
np.random.seed(888)
n_days = 150

# Скрытые состояния: 0 - Низкая волатильность (1.0%), 1 - Высокая волатильность (4.5%)
hidden_states = np.zeros(n_days, dtype=int)
market_returns = np.zeros(n_days)

# Задаем матрицу переходов между режимами
# [из Накопления в Накопление, из Накопления в Шторм]
# [из Шторма в Накопление, из Шторма в Шторм]
transition_matrix = np.array([
    [0.90, 0.10],  # Накопление длится долго
    [0.25, 0.75]   # Шторм затухает быстрее
])

current_state = 0 # Стартуем в режиме накопления

for t in range(n_days):
    # Определяем скрытое состояние на основе вероятностей переходов
    current_state = np.random.choice([0, 1], p=transition_matrix[current_state])
    hidden_states[t] = current_state
    
    # Генерируем доходность в зависимости от скрытого состояния
    if current_state == 0:
        market_returns[t] = np.random.normal(0.0002, 0.01) # Спокойный день
    else:
        market_returns[t] = np.random.normal(-0.001, 0.045) # Штормовой день (дамп/памп)

# 2. АЛГОРИТМ ДЕТЕКЦИИ: Квант-фильтр волатильности (простейший аналог декодера Витерби)
df = pd.DataFrame({"Return": market_returns, "True_State": hidden_states})
df["Rolling_Volatility"] = df["Return"].rolling(window=5).std()
df = df.dropna()

# Математический порог разделения фаз: средняя волатильность ряда
threshold = df["Rolling_Volatility"].median()
df["Detected_State"] = (df["Rolling_Volatility"] > threshold).astype(int)

# Считаем точность нашего математического детектора скрытых фаз
accuracy = np.mean(df["True_State"] == df["Detected_State"])

print("\n" + "="*60)
print("🔮 РЕЗУЛЬТАТЫ ДЕКОДИРОВАНИЯ СКРЫТЫХ МАРКОВСКИХ РЕЖИМОВ")
print("="*60)
print(f"📊 Всего симулировано торговых суток: {n_days}")
print(f"😴 Дней в режиме накопления (State 0): {np.sum(hidden_states == 0)}")
print(f"🌪️ Дней в режиме шторма (State 1): {np.sum(hidden_states == 1)}")
print(f"\n🎯 Точность математической детекции фаз: {accuracy * 100:.2f}%")
print("="*60)
print("📝 Последние 5 дней матрицы режимов:")
print(df[["Return", "True_State", "Detected_State"]].tail(5))
print("="*60)
