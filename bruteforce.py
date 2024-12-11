import pandas as pd
from itertools import combinations

file_path = "actions.csv"
actions_data = pd.read_csv(file_path)

actions_data['Coût par action (en euros)'] = actions_data['Coût par action (en euros)'].astype(float)
actions_data['Bénéfice (après 2 ans)'] = actions_data['Bénéfice (après 2 ans)'].str.rstrip('%').astype(float) / 100
actions_data['Profit total'] = actions_data['Coût par action (en euros)'] * (1 + actions_data['Bénéfice (après 2 ans)']) - actions_data['Coût par action (en euros)']

def brute_force_optimise(data, budget):    
    best_profit = 0
    best_combination = []
    
    actions = [action for action in data.to_dict('records') if action['Coût par action (en euros)'] <= budget]
    
    for r in range(1, len(actions) + 1):
        for combination in combinations(actions, r):
            total_cost = sum(action['Coût par action (en euros)'] for action in combination)
            if total_cost > budget:
                continue
                
            total_profit = sum(action['Profit total'] for action in combination)
            if total_profit > best_profit:
                best_profit = total_profit
                best_combination = combination
                
    return best_combination, best_profit

budget_limit = 500
best_combination, max_profit = brute_force_optimise(actions_data, budget_limit)

if best_combination:
    print("\nMeilleure combinaison trouvée :")
    total_cost = sum(action['Coût par action (en euros)'] for action in best_combination)
    print(f"Coût total investi : {total_cost:.2f}€")
    for action in best_combination:
        print(f"\nAction: {action['Actions #']}")
        print(f"  Coût: {action['Coût par action (en euros)']}€")
        print(f"  Bénéfice: {action['Bénéfice (après 2 ans)']*100:.1f}%")
        print(f"  Profit: {action['Profit total']:.2f}€")
    print(f"\nProfit total: {max_profit:.2f}€")
else:
    print("Aucune combinaison valide trouvée.")
