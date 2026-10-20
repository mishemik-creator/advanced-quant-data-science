import numpy as np
import pandas as pd

print("🎲 Запускаем симуляцию Монте-Карло на 10,000 независимых траекторий...")

# Базовые параметры текущих суток (19.10.2026)
S0 = 82937.80          # Текущая живая цена Биткоина
target_price = 90000.0 # Целевая цена для фиксации прибыли
T = 30                 # Горизонт прогнозирования (30 дней)
N_simulations = 10000  # Количество симулируемых сценариев будущего

# Годовые параметры переводим в суточные
mu = 0.05 / 365        # Ожидаемый суточный тренд (+5% годовых)
sigma = 0.3698 / np.sqrt(365) # Суточная волатильность (на основе твоего живого σ = 36.98%)

# Генерируем матрицу случайного шума Гаусса (30 дней x 10,000 сценариев)
np.random.seed(42)
Z = np.random.normal(0, 1, (T, N_simulations))

# Симулируем геометрическое броуновское движение для всех 10,000 путей одновременно!
# Используем векторизацию NumPy для мгновенного матричного расчета
daily_growth = np.exp((mu - 0.5 * sigma**2) + sigma * Z)
# Перемножаем цепочку дней, чтобы получить финальные цены через 30 дней
final_prices = S0 * np.prod(daily_growth, axis=0)

# Матстатистика результатов: считаем, сколько сценариев пробили цель в $90,000
successful_scenarios = np.sum(final_prices > target_price)
probability_of_success = successful_scenarios / N_simulations

# Находим средний ожидаемый курс и критический сценарий худших 5% результатов
expected_final_price = np.mean(final_prices)
worst_5_percent_price = np.percentile(final_prices, 5)

print("="*60)
print("🎲 РЕЗУЛЬТАТЫ QUANT МОДЕЛИРОВАНИЯ МОНТЕ-КАРЛО")
print("="*60)
print(f"📈 Средний ожидаемый курс через 30 дней: ${expected_final_price:,.2f} USDT")
print(f"🎯 Математическая вероятность пробития ${target_price:,.2f}: {probability_of_success * 100:.2f}%")
print(f"💀 Худший сценарий (95% доверительный уровень): ${worst_5_percent_price:,.2f} USDT")
print("="*60)
