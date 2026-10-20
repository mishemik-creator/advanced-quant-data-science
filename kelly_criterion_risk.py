import numpy as np
import pandas as pd

print("📐 Запуск Квант-Модуля Динамического Управления Капиталом по Критерию Келли...")

def calculate_kelly_fraction(p_win, reward_to_risk):
    """
    Вычисляет оптимальный размер позиции по формуле Келли:
    f* = (p * b - q) / b
    """
    b = reward_to_risk
    q = 1.0 - p_win
    
    kelly_f = (p_win * b - q) / b
    return max(0.0, kelly_f) # Если математическое ожидание отрицательное, размер позиции 0

# Параметры сделки текущих суток (20.10.2026) на основе наших прошлых Quant-моделей
probability_of_win = 0.60  # Шанс успеха 60% (положительное мат. ожидание)
b_ratio = 2.0              # Отношение выигрыша к проигрышу 2:1 (TakeProfit = 10%, StopLoss = 5%)

# Считаем долю Келли
optimal_fraction = calculate_kelly_fraction(probability_of_win, b_ratio)

# 🏎️ СИМУЛЯЦИЯ: Прогоняем 50 сделок инвестора, использующего дробное плечо Келли (возьмем 50% от Келли для безопасности)
np.random.seed(42)
n_trades = 50
starting_capital = 10000.0
capital_history = [starting_capital]

# Симулируем исходы сделок (60% побед, 40% проигрышей)
trade_outcomes = np.random.choice([1, -1], size=n_trades, p=[probability_of_win, 1 - probability_of_win])

current_capital = starting_capital
safe_kelly_fraction = optimal_fraction * 0.5 # Дробный Келли (Fractional Kelly) — стандарт Уолл-стрит

for outcome in trade_outcomes:
    trade_size = current_capital * safe_kelly_fraction
    if outcome == 1:
        current_capital += trade_size * b_ratio # Выигрыш
    else:
        current_capital -= trade_size # Проигрыш
    capital_history.append(current_capital)

print("\n" + "="*60)
print("📊 РЕЗУЛЬТАТЫ СИМУЛЯЦИИ УПРАВЛЕНИЯ КАПИТАЛОМ ПО КЕЛЛИ")
print("="*60)
print(f"🎯 Оптимальный жесткий размер позиции (Full Kelly): {optimal_fraction * 100:.2f}% от депозита")
print(f"🛡️ Безопасный размер позиции (Half Kelly 50%): {safe_kelly_fraction * 100:.2f}% от депозита")
print(f"ℹ️ Смысл: Заходить в каждую сделку строго на этот процент от текущего капитала.")
print("-"*60)
print(f"💰 Стартовый капитал инвестора: ${starting_capital:,.2f} USD")
print(f"📈 Финальный капитал после 50 сделок: ${current_capital:,.2f} USD")
print(f"🧬 Чистая эффективность прироста системы: +{(current_capital - starting_capital)/starting_capital*100:.2f}%")
print("="*60)
