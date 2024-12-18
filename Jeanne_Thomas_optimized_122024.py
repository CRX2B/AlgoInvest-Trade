import pandas as pd
from time import time

def load_and_prepare_data(file_path: str):
    """Charge et prépare les données du fichier CSV."""
    df = pd.read_csv(file_path)
    
    # Filtrer les actions avec un prix de 0
    df = df[df['price'] > 0.00]
    
    # Calculer le profit en valeur absolue et trier par ratio
    df['profit_value'] = df['price'] * (df['profit'] / 100)
    df['ratio'] = df['profit_value'] / df['price']
    return df.sort_values('ratio', ascending=False)

def optimized_invest(data: pd.DataFrame, max_budget: float):
    """
    Algorithme d'investissement optimisé utilisant une approche par ratio.
    """
    selected_shares = []
    total_cost = 0
    total_profit = 0
    
    # Convertir en numpy pour plus de rapidité
    prices = data['price'].values
    profits = data['profit_value'].values
    names = data['name'].values
    
    for i in range(len(data)):
        if total_cost + prices[i] <= max_budget:
            selected_shares.append({
                'name': names[i],
                'price': round(prices[i], 3),
                'profit': round((profits[i] / prices[i]) * 100, 3),
                'profit_value': round(profits[i], 3)
            })
            total_cost += prices[i]
            total_profit += profits[i]
            
    return selected_shares, round(total_profit, 3), round(total_cost, 3)

def main():
    BUDGET = 500
    FILE_PATH = "dataset1.csv"
    
    start_time = time()
    data = load_and_prepare_data(FILE_PATH)
    best_combination, max_profit, total_cost = optimized_invest(data, BUDGET)
    execution_time = time() - start_time
    
    # Afficher les résultats
    print("\nMeilleure combinaison trouvée :")
    print(f"Coût total investi : {total_cost:.2f}€")
    
    for share in best_combination:
        print(f"\nAction: {share['name']}")
        print(f"  Coût: {share['price']}€")
        print(f"  Bénéfice: {share['profit']:.1f}%")
        print(f"  Profit: {share['profit_value']:.2f}€")
    
    print(f"\nProfit total: {max_profit:.2f}€")
    print(f"Utilisation du budget: {(total_cost/BUDGET)*100:.1f}%")
    print(f"Temps d'exécution: {execution_time:.3f} secondes")

if __name__ == "__main__":
    main()
