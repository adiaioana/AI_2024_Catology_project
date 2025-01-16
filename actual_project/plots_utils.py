import matplotlib.pyplot as plt
import seaborn as sns

def make_histograms_for_each_attr(df,folder_path):
    px = 1 / plt.rcParams['figure.dpi']
    sns.set_theme(style="whitegrid")

    for i, attribute in enumerate(df.columns):
        plt.figure(figsize=(300*px, 500*px))
        sns.histplot(df[attribute], bins=3, kde=True)
        plt.title(f'Distribuția valorilor pentru {attribute}')
        plt.xlabel(attribute)
        plt.ylabel('Frecvență')
        plt.grid(axis='y')
        plt.savefig(f'./{folder_path}/histogram_{attribute}.png')
        plt.close()

        #plt.tight_layout()
    #plt.show()

def make_boxplots_for_each_attr(df,folder_path):
    px = 1 / plt.rcParams['figure.dpi']
    sns.set_theme(style="whitegrid")

    for i, attribute in enumerate(df.columns):
        plt.figure(figsize=(300*px, 500*px))
        sns.boxplot(df[attribute])
        plt.title(f'Distribuția valorilor pentru {attribute}')
        plt.xlabel(attribute)
        plt.ylabel('Frecvență')
        plt.grid(axis='y')
        plt.savefig(f'./{folder_path}/boxplot_{attribute}.png')
        plt.close()

        #plt.tight_layout()
    #plt.show()

def plotCorrelationMatrix(df, folder_path):
    correlation_matrix = df.corr();
    plt.clf()
    sns.set(font_scale=0.1)
    heatmap = sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, fmt='.1f',annot_kws={"size": 6},
                cbar_kws={"shrink": 0.5, 'label': 'Correlation Coefficient', }  # Customize color bar
                )

    cbar = heatmap.collections[0].colorbar  # Get the color bar from the heatmap
    cbar.ax.tick_params(labelsize=6)  # Set the font size for color bar tick labels
    cbar.ax.set_ylabel('Correlation Coefficient', fontsize=6)  # Set font size for the color bar label

    plt.xticks(rotation=90,fontsize=4)  # X-axis tick labels
    plt.yticks(rotation=0,fontsize=4)  # Y-axis tick labels

    #plt.figure(figsize=(8,6));
    plt.tight_layout()

    plt.savefig(f'./{folder_path}/correlation_heatmap.png', dpi=1000)