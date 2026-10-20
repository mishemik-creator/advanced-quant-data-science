import numpy as np

print("📐 Запуск Квант-Модуля Анализа Хаоса по Методу Энтропии Шеннона...")

def calculate_shannon_entropy(probabilities):
    """
    Вычисляет информационную энтропию Шеннона в битах:
    H(X) = -Sum(P(x) * log2(P(x)))
    """
    probabilities = np.array(probabilities)
    # Фильтруем нулевые вероятности, так как log2(0) не определен (0 * log2(0) = 0 в теории информации)
    probabilities = probabilities[probabilities > 0]
    
    entropy = -np.sum(probabilities * np.log2(probabilities))
    return entropy

# Симулируем два рынка предсказаний (Prediction Markets) на текущие сутки (20.10.2026)
# Рынок А (Хаотичный): Шансы кандидатов распределены почти поровну (0.48, 0.47, 0.05)
market_A_probs = [0.48, 0.47, 0.05]

# Рынок Б (Стабильный): Есть явный фаворит с тотальной поддержкой (0.90, 0.08, 0.02)
market_B_probs = [0.90, 0.08, 0.02]

entropy_A = calculate_shannon_entropy(market_A_probs)
entropy_B = calculate_shannon_entropy(market_B_probs)

# Максимально возможная энтропия для 3-х исходов (чистый хаос, когда все равны 1/3)
max_entropy = -np.sum([1/3, 1/3, 1/3] * np.log2([1/3, 1/3, 1/3]))

print("\n" + "="*60)
print("🔮 АНАЛИЗ ХАОСА И НЕОПРЕДЕЛЕННОСТИ PREDICTION MARKETS")
print("="*60)
print(f"📊 РЫНОК А (Равные шансы / Жесткая борьба): {market_A_probs}")
print(f"📐 Индекс Энтропии Шеннона H(X): {entropy_A:.4f} бит")
print(f"🧬 Степень неопределенности системы: {entropy_A / max_entropy * 100:.2f}%")
print("-"*60)
print(f"📊 РЫНОК Б (Явный фаворит / Стабильность): {market_B_probs}")
print(f"📐 Индекс Энтропии Шеннона H(X): {entropy_B:.4f} бит")
print(f"🧬 Степень неопределенности системы: {entropy_B / max_entropy * 100:.2f}%")
print("="*60)
print("ℹ️ _Чем ниже энтропия, тем выше уверенность алгоритма маркет-мейкинга в исходе события._")
print("="*60)
