import numpy as np
import pandas as pd

print("📐 Запуск Квант-Модуля Моделирования Хвостовых Рисков Портфеля через Копулы...")

# 1. СИМУЛИРУЕМ РЕАЛЬНЫЙ КРИЗИС: генерируем данные с экстремальной зависимостью в хвостах
np.random.seed(999)
n_scenarios = 10000 # 10,000 симуляций стресс-теста

# Генерируем базовый рыночный шок (общий скрытый фактор паники)
market_panic_factor = np.random.exponential(scale=1.0, size=n_scenarios)

# Доходности BTC и ETH зависят от этого фактора паники нелинейно
btc_stress_returns = np.random.normal(0.0005, 0.02, n_scenarios) - 0.03 * market_panic_factor
eth_stress_returns = np.random.normal(0.0003, 0.025, n_scenarios) - 0.04 * market_panic_factor

df_copula = pd.DataFrame({"BTC": btc_stress_returns, "ETH": eth_stress_returns})

# 2. ЧИСТАЯ МАТЕМАТИКА: Находим критические пороги VaR 95% для каждого актива
var_threshold_btc = np.percentile(df_copula["BTC"], 5)
var_threshold_eth = np.percentile(df_copula["ETH"], 5)

# 3. ВЫЧИСЛЯЕМ РЕАЛЬНУЮ ВЕРОЯТНОСТЬ ОДНОВРЕМЕННОГО КРАХА (Co-Crash)
co_crash_scenarios = np.sum((df_copula["BTC"] < var_threshold_btc) & (df_copula["ETH"] < var_threshold_eth))
actual_co_crash_prob = co_crash_scenarios / n_scenarios

# Если бы активы были независимы в хвостах, по теории вероятностей шанс одновременного падения
# в зону 5% худших исходов был бы равен: 5% * 5% = 0.25% (0.0025)
theoretical_independent_prob = 0.05 * 0.05

# Считаем классическую линейную корреляцию Пирсона для сравнения
pearson_corr = df_copula["BTC"].corr(df_copula["ETH"])

print("\n" + "="*60)
print("🚨 РЕЗУЛЬТАТЫ СТРЕСС-ТЕСТИРОВАНИЯ ХВОСТОВЫХ РИСКОВ (COPULA LOGIC)")
print("="*60)
print(f"📊 Всего смоделировано экстремальных сценариев: {n_scenarios}")
print(f"📈 Линейная корреляция Пирсона между BTC и ETH: {pearson_corr:.4f}")
print(f"📉 Критический порог VaR 95% для BTC: {var_threshold_btc * 100:.2f}% за сутки")
print(f"📉 Критический порог VaR 95% для ETH: {var_threshold_eth * 100:.2f}% за сутки")
print("-"*60)
print(f"🔮 Теоретический шанс ко-дефолта по Гауссу (без учета хвостов): {theoretical_independent_prob * 100:.2f}%")
print(f"💀 РЕАЛЬНАЯ МАТЕМАТИЧЕСКАЯ ВЕРОЯТНОСТЬ ОДНОВРЕМЕННОГО КРАХА: {actual_co_crash_prob * 100:.2f}%")
print(f"📐 Коэффициент хвостового усложнения (Превышение риска): {actual_co_crash_prob / theoretical_independent_prob:.2f}х")
print("="*60)
if actual_co_crash_prob > 0.03:
    print("❌ ВЕРДИКТ РИСК-ИНЖЕНЕРА: Обнаружена критическая хвостовая зависимость! Диверсификация не работает. Требуется хеджирование пулов!")
else:
    print("✅ ВЕРДИКТ РИСК-ИНЖЕНЕРА: Риск ко-дефолта в пределах нормы. Портфель диверсифицирован.")
print("="*60)
