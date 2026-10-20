from datetime import datetime
import numpy as np
import pandas as pd
from scipy import stats
import ccxt

# Получаем текущее точное время сервера в Москве
current_time_str = datetime.now().strftime("%d.%m.%Y | %H:%M:%S")

print(f"📡 Подключаемся к глобальному биржевому шлюзу через CCXT ({current_time_str})...")

try:
    # Инициализируем биржу KuCoin для безопасного обхода Cloudflare блокировок
    exchange = ccxt.kucoin({'timeout': 10000, 'enableRateLimit': True})
    
    print("📈 Загружаем реальные исторические свечи BTC/USDT...")
    # Скачиваем 200 дневных баров Биткоина напрямую с биржи
    bars = exchange.fetch_ohlcv('BTC/USDT', timeframe='1d', limit=200)
    
    # Упаковываем данные в матрицу Pandas DataFrame
    df = pd.DataFrame(bars, columns=['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])
    
    # Форматируем временные метки в читаемые даты
    df['Date'] = pd.to_datetime(df['Timestamp'], unit='ms')
    df.set_index('Date', inplace=True)
    
    # 1. Расчет реальной Логарифмической доходности (Log Returns)
    df['Log_Return'] = np.log(df['Close'] / df['Close'].shift(1))
    df = df.dropna()
    
    # Извлекаем самые свежие метрики текущей секунды торгов
    current_price = df['Close'].iloc[-1]
    mean_return = df['Log_Return'].mean()
    daily_sigma = df['Log_Return'].std()
    annual_sigma = daily_sigma * np.sqrt(365)
    
    # 2. Оценка формы распределения (Асимметрия и Избыточный Эксцесс)
    market_skew = stats.skew(df['Log_Return'])
    market_kurtosis = stats.kurtosis(df['Log_Return'])
    
    # 3. Расчет рисков по методу Value at Risk (VaR 95% и VaR 99%)
    var_95 = stats.norm.ppf(0.05, loc=mean_return, scale=daily_sigma)
    var_99 = stats.norm.ppf(0.01, loc=mean_return, scale=daily_sigma)
    
    # =====================================================================
    # КВАНТОВЫЙ АЛГОРИТМ РАСЧЕТА СИГНАЛОВ (Mean Reversion Z-Score)
    # =====================================================================
    # Вычисляем 30-дневное скользящее среднее и скользящее стандартное отклонение
    df['MA_30'] = df['Close'].rolling(window=30).mean()
    df['Std_30'] = df['Close'].rolling(window=30).std()
    
    # Считаем Z-Score (на сколько сигм живая цена отлетела от скользящей нормы)
    last_row = df.iloc[-1]
    z_score = (last_row['Close'] - last_row['MA_30']) / last_row['Std_30']
    
    # Генерируем торговую директиву по правилам распределения Гаусса
    if z_score < -2.0:
        signal = "🚨 СИГНАЛ: СВЕРХВЫГОДНАЯ ПОКУПКА (Мат. просадка, цена ниже -2σ) 🟢"
    elif z_score > 2.0:
        signal = "🚨 СИГНАЛ: ФИКСАЦИЯ ПРИБЫЛИ / ПРОДАЖА (Перекупленность, цена выше +2σ) 🔴"
    else:
        signal = "⏳ СИГНАЛ: УДЕРЖАНИЕ ПОЗИЦИИ (Цена в пределах нормального распределения) ⚪"
        
    # Выводим фундаментальный аналитический отчет
    print("\n" + "="*55)
    print(f"📊 ЖИВОЙ КВАНТ-АНАЛИЗ БИТКОИНА ({current_time_str})")
    print("="*55)
    print(f"💵 Текущая ЖИВАЯ цена BTC на бирже: ${current_price:,.2f} USDT")
    print(f"📈 Дневное мат. ожидание доходности: {mean_return * 100:.4f}%")
    print(f"📉 Суточная волатильность (σ): {daily_sigma * 100:.2f}%")
    print(f"🌪️ Аннуализированная волатильность: {annual_sigma * 100:.2f}%")
    print(f"📐 Коэффициент Асимметрии (Skewness): {market_skew:.4f}")
    print(f"🧬 Избыточный Эксцесс (Kurtosis): {market_kurtosis:.4f}")
    print(f"🚨 Риск потерь Value at Risk (VaR 95%): {var_95 * 100:.2f}%")
    print(f"💀 Критический риск (VaR 99%): {var_99 * 100:.2f}%")
    print("="*55)
    print(f"📊 СИСТЕМА МАТЕМАТИЧЕСКИХ СИГНАЛОВ (Mean Reversion)")
    print("="*55)
    print(f"📈 30-дневная средняя норма (MA30): ${last_row['MA_30']:,.2f} USDT")
    print(f"📐 Текущий Z-Score математического отклонения: {z_score:.4f}")
    print(f"\n🎯 {signal}")
    print("="*55)

except Exception as e:
    print(f"🚨 Ошибка квант-шлюза: {e}")
