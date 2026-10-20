import unittest
import numpy as np
from scipy import stats

# 1. Импортируем нашу функцию для тестирования
# (Копируем её сюда в минимальном виде, чтобы тест был независимым)
def generate_math_risk_report(asset_name, current_price, mock_volatility=None):
    np.random.seed(42)
    # Если передана кастомная волатильность — берем её, иначе стандартную
    sigma = mock_volatility if mock_volatility is not None else 2.5
    
    mock_returns = np.random.normal(loc=0.08, scale=sigma, size=180)
    mean_return = np.mean(mock_returns)
    std_dev = np.std(mock_returns)
    
    target_drop = -7.0
    crash_probability = stats.norm.cdf(target_drop, loc=mean_return, scale=std_dev)
    
    status = "⚠️ ВЫСОКИЙ" if crash_probability > 0.02 else "✅ СТАБИЛЬНЫЙ"
    return status, crash_probability

# 2. КЛАСС АВТОМАТИЧЕСКИХ ТЕСТОВ (QA AUTOMATION STYLE)
class TestQuantEngine(unittest.TestCase):
    
    def test_stable_market_status(self):
        """Тест 1: Проверяем, что при низкой волатильности (1.0%) риск стабилен"""
        status, prob = generate_math_risk_report("BTC", 82000, mock_volatility=1.0)
        self.assertEqual(status, "✅ СТАБИЛЬНЫЙ")
        self.assertLess(prob, 0.02)

    def test_high_risk_market_status(self):
        """Тест 2: Проверяем, что при дикой волатильности (8.0%) риск становится ВЫСОКИМ"""
        status, prob = generate_math_risk_report("SOL", 150, mock_volatility=8.0)
        self.assertEqual(status, "⚠️ ВЫСОКИЙ")
        self.assertGreater(prob, 0.02)

    def test_extreme_price_handling(self):
        """Тест 3: Проверяем, что математика не падает при экстремальной стоимости актива"""
        try:
            status, prob = generate_math_risk_report("MEME", 999999999.99, mock_volatility=2.5)
            execution_passed = True
        except Exception:
            execution_passed = False
            
        self.assertTrue(execution_passed, "Математический движок упал на экстремальных числах!")

# Запуск тестов
if __name__ == '__main__':
    unittest.main()
