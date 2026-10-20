import numpy as np
import pandas as pd

print("📐 Запуск Квант-Модуля Оптимизации Портфеля и Расчета Коэффициента Шарпа...")

# 1. СИМУЛИРУЕМ ДАННЫЕ: генерируем ежедневные доходности для 3-х активов (BTC, ETH, SOL)
np.random.seed(42)
n_days = 252 # Количество торговых дней в году

# Генерируем случайные суточные доходности активов
btc_ret = np.random.normal(0.0008, 0.018, n_days) # Средний рост +0.08%, волатильность 1.8%
eth_ret = np.random.normal(0.0006, 0.022, n_days) # Средний рост +0.06%, волатильность 2.2%
sol_ret = np.random.normal(0.0012, 0.032, n_days) # Средний рост +0.12%, волатильность 3.2%

# Собираем данные в матрицу Pandas DataFrame
df_returns = pd.DataFrame({"BTC": btc_ret, "ETH": eth_ret, "SOL": sol_ret})

# 2. ЧИСТАЯ МАТЕМАТИКА: Считаем средние доходности и Ковариационную Матрицу
mean_returns = df_returns.mean()
covariance_matrix = df_returns.cov()

# Безрисковая процентная ставка (Risk-Free Rate, берем стабильные 4% годовых в долларах)
risk_free_rate = 0.04 / 252 # Переводим суточную ставку

# 3. АЛГОРИТМ РАСЧЕТА МЕТРИК ПОРТФЕЛЯ ВРУЧНУЮ
def evaluate_portfolio(weights, mean_returns, cov_matrix, rf_rate):
    """
    Расчет показателей портфеля через линейную алгебру:
    Доходность = Сумма(Вес * Средняя Доходность)
    Волатильность = Корень(Веса.T * Ковариация * Веса)
    Коэффициент Шарпа = (Доходность - Безрисковая) / Волатильность
    """
    # Ожидаемая доходность портфеля
    port_return = np.sum(mean_returns * weights) * 252 # Аннуализируем (к масштабу года)
    
    # Волатильность портфеля (риск с учетом взаимных корреляций монет!)
    port_variance = np.dot(weights.T, np.dot(cov_matrix * 252, weights))
    port_volatility = np.sqrt(port_variance)
    
    # Коэффициент Шарпа
    sharpe_ratio = (port_return - 0.04) / port_volatility
    return port_return, port_volatility, sharpe_ratio

# Генерируем эталонный сбалансированный портфель (33% BTC, 33% ETH, 34% SOL)
test_weights = np.array([0.33, 0.33, 0.34])

port_ret, port_vol, sharpe = evaluate_portfolio(test_weights, mean_returns, covariance_matrix, risk_free_rate)

print("\n" + "="*60)
print("📊 РЕЗУЛЬТАТЫ МАТЕМАТИЧЕСКОЙ ОПТИМИЗАЦИИ МАРКОВИЦА")
print("="*60)
print(f"💼 Распределение долей в портфеле: BTC={test_weights[0]*100:.1f}%, ETH={test_weights[1]*100:.1f}%, SOL={test_weights[2]*100:.1f}%")
print(f"📈 Ожидаемая годовая доходность портфеля: {port_ret * 100:.2f}%")
print(f"📉 Общая годовая волатильность (σ): {port_vol * 100:.2f}%")
print(f"🧬 Итоговый Коэффициент Шарпа (Sharpe Ratio): {sharpe:.4f}")
print("="*60)
if sharpe > 1.0:
    print("🎯 ВЕРДИКТ КВАНТА: Отличная эффективность стратегии! Риск полностью окупается доходностью.")
elif sharpe > 0.0:
    print("⏳ ВЕРДИКТ КВАНТА: Умеренная эффективность. Портфель зарабатывает больше безрисковой ставки облигаций.")
else:
    print("❌ ВЕРДИКТ КВАНТА: Стратегия неэффективна! Проще купить государственные облигации.")
print("="*60)
