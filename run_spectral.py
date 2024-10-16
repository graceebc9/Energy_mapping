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

def load_and_prepare_data(input_path, test_size):
    data = pd.read_csv(input_path)
# Map age bands to integers
    age_band_mapping = {
        'Pre 1919': 0,
        '1919-1944': 1,
        '1945-1959': 2,
        '1960-1979': 3,
        '1980-1989': 4,
        '1990-1999': 5,
        'Post 1999': 6
    }
    data['localfill_median_age'] = data['localfill_median_age'].map(age_band_mapping)

    cols = [
        'all_types_total_buildings', 
        'all_res_heated_vol_h_total',
        # 'HDD_winter',
        'max_vol_per_uprn',
        'all_types_uprn_count_total',
        'postcode_area',
        'postcode_density',
 'localfill_median_age',
  'localfill_range_age',
    ]

    target = ['total_gas']

    np.random.seed(0)
    df = data[cols + target].copy() 
    df.dropna(inplace=True)

    # Define features and the transformed target
    X = df.drop(['total_gas'], axis=1)
    y = df['total_gas']

    # Split the data into train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=float(test_size), random_state=0)
    return X_train, X_test, y_train, y_test, cols

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

def save_model(output_path, run_name, spectral_model, scaler, pca, labels, X_principal, silhouette_avg):
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
        f.write(f'Silhouette Score: {silhouette_avg}')
    
    # Save the principal components
    X_principal.to_csv(os.path.join(run_path, 'X_principal.csv'), index=False)
    
    # Save the visualization
    plt.figure(figsize=(10, 7))
    scatter = plt.scatter(X_principal['P1'], X_principal['P2'], c=labels, cmap='hsv')
    plt.title('Spectral Clustering Results')
    plt.colorbar(scatter, label='Cluster')
    plt.xlabel('P1')
    plt.ylabel('P2')
    plt.savefig(os.path.join(run_path, 'spectral_clustering_results.png'))
    plt.close()
    
def plot_variable_distributions(X_train, labels, cols, run_path):
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
            cluster_data = df[df['Cluster'] == cluster]
            plt.hist(cluster_data[col], bins=30, alpha=0.5, label=f'Cluster {cluster}')
        plt.title(f'Distribution of {col} by Cluster')
        plt.xlabel(col)
        plt.ylabel('Frequency')
        plt.legend()
        plt.savefig(os.path.join(plots_folder, f'{col}_distribution.png'))
        plt.close()

def main():
    input_path = os.environ.get('MLPATH')
    output_path = os.environ.get('OUTPUTPATH')
    test_size = os.environ.get('TESTSIZE')
    num_clusters = os.environ.get('NUM_CLUSTERS')
    dataset_name = os.path.basename(input_path).split('_')[0]
    print(dataset_name)
    run_name = f'{dataset_name}_spectral_clustering_{num_clusters}_trainsize_{test_size}'

    # Convert environment variables to appropriate types
    test_size = float(test_size)
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

    X_train, X_test, y_train, y_test, cols = load_and_prepare_data(input_path, test_size)
    print(X_train.shape)
    spectral_model_rbf, scaler, pca, labels_rbf, X_principal, silhouette_avg = train_spectral_model(X_train, num_clusters)
    print('starting save ')
    save_model(output_path, run_name, spectral_model_rbf, scaler, pca, labels_rbf, X_principal, silhouette_avg)
    
    print('starting visualization')
    plot_variable_distributions(X_train, labels_rbf, cols, run_path)

if __name__ == "__main__":
    main()

# Example usage:
# export MLPATH='/Volumes/T9/Data_downloads/new-data-outputs/ml_input/V3.2_region_geoms.csv'
# export OUTPUTPATH='/Volumes/T9/Data_downloads/new-data-outputs/ml_results'
# export TESTSIZE=0.99
# export NUM_CLUSTERS=10
# python run_spectral.py
