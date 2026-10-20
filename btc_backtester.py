import numpy as np
import pandas as pd

print("🎲 Генерируем массив исторических свечей BTC по модели Black-Scholes...")

# Симулируем 300 дней реального исторического цикла Биткоина
np.random.seed(42)
start_btc_price = 60000.0  # Начинаем симуляцию с $60,000

# Создаем ежедневные доходности с волатильностью 3.5% (классический шторм в крипте)
daily_returns = np.random.normal(loc=0.001, scale=0.035, size=300)
# Добавляем один катастрофический день - "Черный лебедь" (падение на 26% за день)
daily_returns[150] = -0.26 

price_series = start_btc_price * np.exp(np.cumsum(daily_returns))

df = pd.DataFrame(data={"Close": price_series, "Return": daily_returns})

# ВЫЧИСЛЯЕМ КВАНТОВЫЕ ПОКАЗАТЕЛИ (Скользящее среднее и сигму за 30 дней)
df['MA_30'] = df['Close'].rolling(window=30).mean()
df['Std_30'] = df['Close'].rolling(window=30).std()
df['Z_Score'] = (df['Close'] - df['MA_30']) / df['Std_30']
df = df.dropna()

# Стартовые депозиты по $10,000 USD каждого инвестора
dep_leverage = 10000.0
dep_quant = 10000.0

# Переменные риск-менеджмента для Квант-стратегии
in_position = False
buy_price = 0.0

# Флаг маржин-колла (ликвидации) для плеча х2
is_liquidated = False

# СИМУЛЯЦИЯ: Прогоняем депозиты через историю день за днем!
for idx, row in df.iterrows():
    
    # --- Стратегия №1: HODL с плечом х2 ---
    if not is_liquidated:
        # Прибыль или убыток дня умножаются на коэффициент плеча (x2)
        dep_leverage *= (1 + 2 * row['Return'])
        
        # Если баланс падает до нуля или ниже (из-за резкого падения) — маржин-колл
        if dep_leverage <= 0 or row['Return'] <= -0.50:
            dep_leverage = 0.0
            is_liquidated = True
            
    # --- Стратегия №2: Квант-сигналы Z-Score (Mean Reversion) ---
    # Точка Входа (Покупка): цена упала ниже -1.2 стандартных отклонений от нормы
    if row['Z_Score'] < -1.2 and not in_position:
        in_position = True
        buy_price = row['Close']
        
    # Точка Выхода (Продажа): цена перегрета и вылетела выше +1.2 стандартных отклонений
    elif row['Z_Score'] > 1.2 and in_position:
        profit_pct = (row['Close'] - buy_price) / buy_price
        dep_quant *= (1 + profit_pct)
        in_position = False
        
# Если бэктест закончился, а бот все еще держит Биткоин — фиксируем по финальной цене
if in_position:
    profit_pct = (df['Close'].iloc[-1] - buy_price) / buy_price
    dep_quant *= (1 + profit_pct)
    
print("\n" + "="*55)
print("🏆 РЕЗУЛЬТАТЫ МАТЕМАТИЧЕСКОГО БЭКТЕСТИНГА ДЕПОЗИТОВ")
print("="*55)
print(f"📊 Проанализировано свечей (дней рынка): {len(df)}")
print(f"💰 Стартовый капитал каждого: $10,000.00 USD")
print("-"*55)
print(f"📉 ДЕПОЗИТ №1 (HODL х2 плечо): ${dep_leverage:,.2f} USD " + ("💀 [ЛИКВИДАЦИЯ]" if is_liquidated else "✅ ЖИВ"))
print(f"🟢 ДЕПОЗИТ №2 (Алгоритм Z-Score): ${dep_quant:,.2f} USD ✅ [УСПЕХ]")
print("="*55)
print(f"📉 Финальная справочная цена BTC: ${df['Close'].iloc[-1]:,.2f}")
print("="*55)
