import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, normalize
from sklearn.decomposition import PCA
from sklearn.cluster import SpectralClustering
from sklearn.model_selection import train_test_split
from sklearn.metrics import silhouette_score
import joblib
import matplotlib.pyplot as plt
import seaborn as sns 

cols = ['Medium height flats 5-6 storeys', 'Small low terraces',
       '3-4 storey and smaller flats', 'Tall terraces 3-4 storeys',
       'Large semi detached', 'Standard size detached',
       'Standard size semi detached',
       '2 storeys terraces with t rear extension',
       'Semi type house in multiples', 'Tall flats 6-15 storeys',
       'Large detached', 'Very tall point block flats', 'Very large detached',
       'Planned balanced mixed estates', 'Linked and step linked premises',
       'Domestic outbuilding', 'city_total_builds', 'entropy']


col_names = ['large_houses', 'standard', 'large_flats', 'med_flats', 'small_terraces', 'estates',  'perc_asian',
 'perc_black',
 'perc_mixed',
 'perc_white',
 'detached',
 'all_flats',
 'tall_terraces',
 'semis',
  'perc_economically_active_employed',
 'perc_economically_active_unemployed',
 'perc_economically_inactive',]


def load_and_prepare_data(input_path):
    data = pd.read_csv(input_path)
    print(data.head())
    data=data[data['TCITY15NM']!='London'].copy()
    print(len(data))

    X = data.drop(columns=['TCITY15NM', 'Unnamed: 0'] )
    data_cols = X.columns.tolist() 

    return X , data_cols

def train_spectral_model(X_train, num_clusters):
    # Standardize the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_train)

    # Normalizing the Data 
    X_normalized = normalize(X_scaled) 

    # Reducing the dimensions of the data 
    pca = PCA(n_components=2) 
    X_principal = pca.fit_transform(X_normalized) 
    X_principal = pd.DataFrame(X_principal) 
    X_principal.columns = ['P1', 'P2'] 

    # Building the clustering model 
    spectral_model_rbf = SpectralClustering(n_clusters=num_clusters, affinity='rbf') 

    # Training the model and Storing the predicted cluster labels 
    labels_rbf = spectral_model_rbf.fit_predict(X_principal)

    # Calculate the silhouette score
    silhouette_avg = silhouette_score(X_principal, labels_rbf)
    print(f'Silhouette Score: {silhouette_avg}')
    
    return spectral_model_rbf, scaler, pca, labels_rbf, X_principal, silhouette_avg

import pandas as pd
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score

def save_model(output_path, run_name, spectral_model, scaler, pca, labels, X_principal):
    # Calculate clustering metrics
    silhouette_avg = silhouette_score(X_principal, labels)
    davies_bouldin = davies_bouldin_score(X_principal, labels)
    calinski_harabasz = calinski_harabasz_score(X_principal, labels)
    
    # Create the run path if it does not exist
    run_path = os.path.join(output_path, run_name)
    os.makedirs(run_path, exist_ok=True)

    # Save the model
    model_file = os.path.join(run_path, 'spectral_model_rbf.pkl')
    joblib.dump(spectral_model, model_file)
    
    # Save the scaler and PCA
    scaler_file = os.path.join(run_path, 'scaler.pkl')
    joblib.dump(scaler, scaler_file)
    
    pca_file = os.path.join(run_path, 'pca.pkl')
    joblib.dump(pca, pca_file)
    
    # Save the labels
    labels_file = os.path.join(run_path, 'labels.csv')
    labels_df = pd.DataFrame(labels, columns=['Cluster'])
    labels_df.to_csv(labels_file, index=False)

    # Save the silhouette score
    silhouette_file = os.path.join(run_path, 'silhouette_score.txt')
    with open(silhouette_file, 'w') as f:
        f.write(f'Silhouette Score: {silhouette_avg}\n')
    
    # Save the Davies-Bouldin Index
    davies_bouldin_file = os.path.join(run_path, 'davies_bouldin_score.txt')
    with open(davies_bouldin_file, 'w') as f:
        f.write(f'Davies-Bouldin Index: {davies_bouldin}\n')
    
    # Save the Calinski-Harabasz Index
    calinski_harabasz_file = os.path.join(run_path, 'calinski_harabasz_score.txt')
    with open(calinski_harabasz_file, 'w') as f:
        f.write(f'Calinski-Harabasz Index: {calinski_harabasz}\n')
    


def plot_variable_distributions(X_train, labels, run_path, cols):
    """
    Plot the KDE distributions of variables for each cluster.
    
    Parameters:
    X_train (pd.DataFrame): The training data.
    labels (np.array): The cluster labels.
    run_path (str): The path to save the plots.
    cols (list): The columns to plot.
    """
    # Get the variables and labels
    df = pd.DataFrame(X_train, columns=cols)
    df['Cluster'] = labels
    
    # Create a subfolder for the plots
    plots_folder = os.path.join(run_path, 'variable_distributions')
    os.makedirs(plots_folder, exist_ok=True)
    
    # Plot distributions of the variables with respect to each cluster
    for col in cols:
        plt.figure(figsize=(10, 6))
        for cluster in np.unique(labels):
            cluster_data = df[df['Cluster'] == cluster][col].dropna()
            sns.kdeplot(cluster_data, fill=True, label=f'Cluster {cluster}')
        plt.title(f'Distribution of {col} by Cluster')
        plt.xlabel(col)
        plt.ylabel('Density')
        plt.legend()
        plt.savefig(os.path.join(plots_folder, f'{col}_distribution.png'))
        plt.close()




def plot_variable_distributions(X_train, labels, run_path, cols):
    """
    Plot the KDE distributions of variables for each cluster in a figure with three columns and multiple rows.
    
    Parameters:
    X_train (pd.DataFrame): The training data.
    labels (np.array): The cluster labels.
    run_path (str): The path to save the plots.
    cols (list): The columns to plot.
    """
    # Get the variables and labels
    df = pd.DataFrame(X_train, columns=cols)
    df['Cluster'] = labels
    
    # Create a subfolder for the plots
    plots_folder = os.path.join(run_path, 'variable_distributions')
    os.makedirs(plots_folder, exist_ok=True)
    
    # Determine the number of rows needed for 3 columns
    num_cols = 3
    num_rows = (len(cols) + num_cols - 1) // num_cols  # Ceiling division
    
    # Create the figure with the required number of subplots
    plt.figure(figsize=(20, 5 * num_rows))
    
    for i, col in enumerate(cols):
        plt.subplot(num_rows, num_cols, i + 1)
        for cluster in np.unique(labels):
            cluster_data = df[df['Cluster'] == cluster][col].dropna()
            sns.kdeplot(cluster_data, fill=True, label=f'Cluster {cluster}')
        plt.title(f'Distribution of {col} by Cluster')
        plt.xlabel(col)
        plt.ylabel('Density')
        plt.legend()
    
    plt.tight_layout()
    plt.savefig(os.path.join(plots_folder, 'all_distributions.png'))
    plt.close()

def main():
    input_path = os.environ.get('MLPATH')
    output_path = os.environ.get('OUTPUTPATH')
    num_clusters = os.environ.get('NUM_CLUSTERS')
    dataset_name = os.path.basename(input_path).split('_')[0]
    print(dataset_name)
    run_name = f'{dataset_name}_spectral_clustering_{num_clusters}'

    # Convert environment variables to appropriate types
    
    num_clusters = int(num_clusters)

    run_path = os.path.join(output_path, run_name)
    
    # Check if the folder and expected files exist
    if os.path.exists(run_path):
        expected_files = [
            'spectral_model_rbf.pkl',
            'scaler.pkl',
            'pca.pkl',
            'labels.csv',
            'silhouette_score.txt',
            'spectral_clustering_results.png',
            'X_principal.csv'
        ]
        if all(os.path.exists(os.path.join(run_path, f)) for f in expected_files):
            print(f"All expected output files already exist in {run_path}. Aborting the training run to avoid overwriting.")
            return

    X_train, data_cols = load_and_prepare_data(input_path)
    print(X_train.shape)
    print(X_train)
    spectral_model_rbf, scaler, pca, labels_rbf, X_principal, silhouette_avg = train_spectral_model(X_train, num_clusters)
    print('starting save ')
    save_model(output_path, run_name, spectral_model_rbf, scaler, pca, labels_rbf, X_principal)
    
    print('starting visualization')
    plot_variable_distributions(X_train, labels_rbf, run_path, data_cols)

if __name__ == "__main__":
    main()


# export MLPATH='/Users/gracecolverd/New_dataset/ml_scripts/v33_city_clust.csv'
# export OUTPUTPATH='/Volumes/T9/Data_downloads/new-data-outputs/ml_results/cityfinalv2'
# export NUM_CLUSTERS=5
# python run_spectral_city.py
