import os
import sys

def get_obj(log_file):
    '''
    Get the objective function values from the mcsqs.log file and save them to a new file.
    '''
    with open(log_file, 'r') as f:
        lines = f.readlines()

    obj_values = []
    for line in lines:
        if 'Objective_function=' in line:
            obj_values.append(float(line.split('=')[-1].strip()))
    
    with open('sqs_obj.dat', 'w') as f:
        for obj in obj_values:
            f.write(f'{obj}\n')

    return obj_values

def plot_obj(obj_values):
    '''
    Plot the objective function values.
    '''
    import matplotlib.pyplot as plt
    import seaborn as sns
    import matplotlib
    from matplotlib.ticker import FormatStrFormatter
    
    sns.set(font_scale=1.0, style='whitegrid')
    matplotlib.rcParams['xtick.direction'] = 'in'
    matplotlib.rcParams['ytick.direction'] = 'in'
    
    fig = plt.figure()
    ax = plt.subplot()
    
    ax.plot(obj_values, marker='o')
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Objective Value')
    ax.set_title('SQS Optimization Process')
    
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    plt.tight_layout()
    plt.savefig('sqs_obj.png', dpi=300, bbox_inches='tight')

if __name__ == '__main__':
    log_file = 'mcsqs.log'
    obj_values = get_obj(log_file)
    plot_obj(obj_values)
