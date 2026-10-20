import numpy as np
import pandas as pd

print("📐 Запуск Рекурсивного Фильтра Калмана для Парного Арбитража...")

# Симулируем 100 шагов цен ETH, жестко привязанных к BTC, но с шумом матрицы
np.random.seed(42)
n_steps = 100
btc_prices = np.linspace(82000, 84000, n_steps) + np.random.normal(0, 100, n_steps)
# Истинное отношение ETH/BTC = 0.030, но рынок шумит
true_ratio = 0.030
eth_prices = btc_prices * true_ratio + np.random.normal(0, 10, n_steps)

# =====================================================================
# ЧИСТАЯ МАТЕМАТИКА: Реализуем одномерный Фильтр Калмана вручную
# =====================================================================
# Начальные параметры фильтра
x_est = 0.010   # Априорное начальное утверждение (думаем, что отношение 0.010)
p_error = 1.0   # Начальная дисперсия ошибки (очень высокая неуверенность)

# Параметры шума системы и измерений
Q = 1e-5        # Шум процесса (как быстро меняется истинное отношение)
R = 0.01        # Шум измерений (рыночный шум в стакане биржи)

est_history = []
kalman_gains = []

for t in range(n_steps):
    # Измерение текущего шага: отношение ETH к BTC на бирже прямо сейчас
    z_measurement = eth_prices[t] / btc_prices[t]
    
    # 1. ШАГ ПРОГНОЗА (Predict)
    x_pred = x_est
    p_pred = p_error + Q
    
    # 2. ШАГ КОРРЕКЦИИ (Update)
    kalman_gain = p_pred / (p_pred + R)  # Коэффициент Калмана (вес доверия измерению)
    x_est = x_pred + kalman_gain * (z_measurement - x_pred) # Итоговое скрытое состояние
    p_error = (1 - kalman_gain) * p_pred # Обновление ошибки
    
    est_history.append(x_est)
    kalman_gains.append(kalman_gain)

df_kalman = pd.DataFrame({
    "Market_Ratio": eth_prices / btc_prices,
    "Kalman_Estimate": est_history,
    "Kalman_Gain": kalman_gains
})

print("\n" + "="*60)
print("🛰️ РЕЗУЛЬТАТЫ ФИЛЬТРАЦИИ КАЛМАНА НА ТЕКУЩИЕ СУТКИ")
print("="*60)
print(f"📊 Всего обработано рыночных тиков: {n_steps}")
print(f"📐 Стартовая грубая оценка: 0.0100")
print(f"🎯 Итоговая точная оценка скрытого спреда: {df_kalman['Kalman_Estimate'].iloc[-1]:.4f}")
print(f"ℹ️ Реальное заложенное отношение: {true_ratio:.4f}")
print("-"*60)
print(f"📉 Финальный коэффициент Калмана (Gain): {df_kalman['Kalman_Gain'].iloc[-1]:.4f}")
print("="*60)
print("📝 Траектория схождения фильтра к истине (последние 5 шагов):")
print(df_kalman.tail(5))
print("="*60)
