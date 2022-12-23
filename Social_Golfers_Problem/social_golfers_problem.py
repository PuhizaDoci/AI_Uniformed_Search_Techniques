from ortools.sat.python import cp_model
from itertools import groupby
from itertools import product
from itertools import combinations
import math

# This is a convenience function to help iterate over groups
def groupby_keys(input_list, keylist):
    keyfunc = lambda x: tuple(x[k] for k in keylist)
    yield from groupby(sorted(input_list, key=keyfunc), key=keyfunc)
 
def number_of_weeks(n_players, players_per_group):
    return math.floor((n_players-1)/(players_per_group-1))

# define the problem (use smaller numbers of players for testing)
n_players = 16 
players_per_group = 2
n_days = number_of_weeks(n_players, players_per_group)
print(f'Number of days for {n_players} players and {players_per_group} players per group is: {n_days}')

# these will come in handy
n_groups = n_players // players_per_group
players = list(range(n_players))
days = list(range(n_days))
groups = list(range(n_groups))

model = cp_model.CpModel()
 
variables = []
player_vars = {}
for player, day, group in product(players, days, groups):
    v_name = f"{player}_{day}_{group}"
    the_var = model.NewBoolVar(v_name)
    variables.append({k:v for v, k in zip([v_name, player, day, group, the_var], ['Name','Player','Day','Group','CP_Var'])})
    player_vars[player, day, group] = the_var
    
    
# each player must be in a single group on each day
for idx, grp in groupby_keys(variables, ['Player', 'Day']):
    model.Add(sum(x['CP_Var'] for x in grp) == 1)
 
# exactly the right number of players per group
for idx, grp in groupby_keys(variables, ['Day', 'Group']):
    model.Add(sum(x['CP_Var'] for x in grp) == players_per_group)
    
# players can't see each other more than once ever
# This uses an auxiliary variable since we can't do sum(a * b) <= 1
for p1, p2 in combinations(players, r=2):
    players_together = []
    for day in days:
        for group in groups:
            together = model.NewBoolVar(f"M_{p1}_{p2}_{day}_{group}")
            players_together.append(together)
            p1g = player_vars[p1, day, group]
            p2g = player_vars[p2, day, group]
            model.Add(p1g + p2g - together <= 1)

# This section shows how to implement the implication version of the 
# multiplicative constraint
    model.Add(sum(players_together) <= 1)
    
solver = cp_model.CpSolver()
solver.Solve(model)

def parse_answer(variables):
    solution = {}
    for var in variables:
        player, day, group = var['Player'], var['Day'], var['Group']
        solution[player, day, group] = solver.Value(var['CP_Var'])
     
    days = sorted(set(x[1] for x in solution))
    groups = sorted(set(x[2] for x in solution))
    answers = {}
    for day in days:
        answers[day] = {}
        for group in groups:
            ans = [k[0] for k, v in solution.items() if k[1] == day and k[2] == group and v]
            answers[day][group] = sorted(ans)
    return answers
 
ans = parse_answer(variables)
print(ans)