import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def probability_getter(desired_state, ans):
    for_plot = dict()
    for el in ans:
        for_plot[el] = round(np.abs(np.dot(desired_state, ans[el])[0])**2, 3)
        # print(el, " : ", for_plot[el])
    return for_plot

def plot_trans(prob_dict):
    df = pd.DataFrame(list(prob_dict.items()), columns=['Time', 'Probability'])
    df['Probability'] = df['Probability'].apply(lambda x: x.flatten().tolist() if isinstance(x, np.array) else x)
    sns.lineplot(x='Time', y='Probability', data=df)
    plt.xlabel('Time')
    plt.ylabel('Probability')
    plt.title('Transition Probability over Time')
    plt.show()
    
def main():
    # [0, 10]
    initial_state = np.array([[1], [0], [0]])
    E0 = 1
    hamiltonian = np.array([[0, E0, 0], [E0, 0, E0], [0, E0, 0]])
    step_t = 0.01 
    ans = dict()
    for el in range (0, 1000):
        ans[float(el)/100] = initial_state + (step_t/complex(0, 1))*(np.dot(hamiltonian, initial_state))
        # print(ans[float(el)/100])
        initial_state = ans[float(el)/100]
    desired_state = np.array([0, 1, 0])
    prob_dict = probability_getter(desired_state, ans)    
    # plot_trans(prob_dict)   
    # print(prob_dict)

main ()