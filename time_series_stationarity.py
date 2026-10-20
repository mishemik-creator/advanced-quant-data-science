import numpy as np
import pandas as pd

print("📐 Запуск Квант-Модуля Анализа Стационарности Временных Рядов...")

# 1. Генерируем нестационарный временной ряд (Цену) и стационарный ряд (Доходность)
np.random.seed(42)
n_days = 200
initial_price = 82000.0

# Случайный шум (белый шум) с матожиданием 0
white_noise_returns = np.random.normal(loc=0.0, scale=0.02, size=n_days)
# Геометрическое блуждание цены
price_series = initial_price * np.exp(np.cumsum(white_noise_returns))

# Упаковываем в Pandas DataFrame
df = pd.DataFrame(data={"Price": price_series})

# Считаем разности первого порядка (доходность)
df["Return"] = df["Price"].pct_change()
df = df.dropna()

# 2. ЧИСТАЯ МАТЕМАТИКА: Считаем автокорреляцию Lag-1 вручную
def calculate_lag1_autocorrelation(series):
    """
    Вычисляет корреляцию между рядом и его собственной копией, сдвинутой на 1 шаг назад.
    Показывает, зависит ли сегодняшнее значение от вчерашнего.
    """
    x = series.values
    x_t = x[:-1]  # Ряд без последнего элемента
    x_t_plus_1 = x[1:]  # Ряд без первого элемента (сдвинутый на 1 шаг)
    
    # Формула корреляции Пирсона вручную
    mean_t, mean_t1 = np.mean(x_t), np.mean(x_t_plus_1)
    num = np.sum((x_t - mean_t) * (x_t_plus_1 - mean_t1))
    den = np.sqrt(np.sum((x_t - mean_t)**2) * np.sum((x_t_plus_1 - mean_t1)**2))
    
    return num / den

# Расчет для цены и доходности
price_autocorr = calculate_lag1_autocorrelation(df["Price"])
return_autocorr = calculate_lag1_autocorrelation(df["Return"])

print("\n" + "="*60)
print("📊 СТАТИСТИЧЕСКИЙ АНАЛИЗ ЗАВИСИМОСТЕЙ ВРЕМЕННОГО РЯДА")
print("="*60)
print(f"📈 Автокорреляция Lag-1 для ряда ЦЕН: {price_autocorr:.4f}")
print(f"ℹ️ Смысл: Значение близко к 1.0? Ряд НЕСТАЦИОНАРЕН. Цена зависит от тренда.")
print("-"*60)
print(f"📉 Автокорреляция Lag-1 для ряда ДОХОДНОСТЕЙ: {return_autocorr:.4f}")
print(f"ℹ️ Смысл: Значение близко к 0? Ряд СТАЦИОНАРЕН. Рыночный шум не имеет памяти.")
print("="*60)
if abs(return_autocorr) < 0.1:
    print("🎯 ВЕРДИКТ КВАНТА: Ряд доходностей успешно очищен от тренда и готов к прогнозированию рисков VaR!")
else:
    print("⚠️ ВЕРДИКТ КВАНТА: В доходностях осталась скрытая память, требуется модель ARMA.")
print("="*60)
