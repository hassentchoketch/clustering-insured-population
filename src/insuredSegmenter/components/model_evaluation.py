from pathlib import Path
import numpy as np
import pandas as pd
import joblib
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt 
from typing import Dict, Tuple
from insuredSegmenter.entity.config_entity import ModelEvaluationConfig
from insuredSegmenter.utils.common import save_json



class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def eval_metrics(self, X: np.ndarray, labels: np.ndarray) -> Tuple[float, float, float]:
        """
        Calculate clustering evaluation metrics
        
        Args:
            X: Feature matrix
            labels: Cluster labels assigned by the model
            
        Returns:
            Tuple of (silhouette_score, calinski_harabasz_score, davies_bouldin_score)
        """
        # Note: All these metrics require both the data points and their assigned clusters
        s_s = silhouette_score(X, labels)
        cal_s = calinski_harabasz_score(X, labels)
        dav_s = davies_bouldin_score(X, labels)
        return s_s, cal_s, dav_s
    # Dict[str, List[float]]
    def evaluate_cluster_stability(self, model, X: np.ndarray, n_splits: int = 5):
        """
        Evaluate cluster stability across multiple data subsets
        
        Args:
            model: Trained clustering model
            X: Feature matrix of transformed data
            n_splits: Number of random splits to evaluate
            
        Returns:
            Dictionary with lists of metrics across splits
        """
        results = {
            "silhouette_scores": [],
            "calinski_harabasz_scores": [],
            "davies_bouldin_scores": []
        }
        
        for i in range(n_splits):
            # Create a random subset (70% of data)
            _, X_subset = train_test_split(X, test_size=0.7, random_state=i)
            
            # Predict on this subset
            labels = model.predict(X_subset)
            
            # Calculate metrics
            s_s, cal_s, dav_s = self.eval_metrics(X_subset, labels)
            
            # Store results
            results["silhouette_scores"].append(s_s)
            results["calinski_harabasz_scores"].append(cal_s)
            results["davies_bouldin_scores"].append(dav_s)
        
        return results
    
    def visualize_clusters(self, X: np.ndarray, labels: np.ndarray, save_path: Path = None):
        """
        Visualize clusters using PCA for dimensionality reduction in 3D
        
        Args:
            X: Feature matrix
            labels: Cluster labels assigned by the model
            save_path: Path to save the visualization
        """
        # Use PCA to reduce to 3 dimensions for visualization
        pca = PCA(n_components=3)
        X_pca = pca.fit_transform(X)
        
        # Create a DataFrame for easy plotting
        df_plot = pd.DataFrame({
            'PCA1': X_pca[:, 0],
            'PCA2': X_pca[:, 1],
            'PCA3': X_pca[:, 2],
            'Cluster': labels
        })
        
        # Create 3D plot
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # Get unique clusters
        unique_clusters = np.unique(labels)
        
        # Create color map
        cmap = plt.cm.get_cmap('viridis', len(unique_clusters))
        
        # Plot each cluster
        for i, cluster in enumerate(unique_clusters):
            cluster_data = df_plot[df_plot['Cluster'] == cluster]
            ax.scatter(
                cluster_data['PCA1'], 
                cluster_data['PCA2'], 
                cluster_data['PCA3'],
                s=50,  # marker size
                c=[cmap(i)],  # color based on cluster
                label=f'Cluster {cluster}'
            )
        
        # Set labels and title
        ax.set_xlabel('PCA1')
        ax.set_ylabel('PCA2')
        ax.set_zlabel('PCA3')
        ax.set_title('3D Cluster Visualization using PCA')
        
        # Add legend
        ax.legend()
        
        # Add grid for better spatial perception
        ax.grid(True)
        
        # Set initial view angle for better perspective
        ax.view_init(elev=30, azim=45)
        
        if save_path:
            plt.savefig(save_path)
            plt.close()
        else:
            # If not saving, add some interactivity hint
            plt.figtext(0.5, 0.01, "Tip: Click and drag to rotate the 3D visualization", 
                    ha='center', fontsize=9, style='italic')
            plt.tight_layout()
            plt.show()

    def train_test_evaluation(self) -> Dict:
        """"
        Perform train/test evaluation of clustering using transformed data
        
        Args:
            model_path: Optional path to load model (uses self.config.model_path if None)
            transformed_data_path: Optional path to transformed data (uses self.config.transformed_data_path if None)
            
        Returns:
            Dictionary with evaluation metrics
        """
        # Load the trained model
        # if model_path is None:
        #     model_path = self.config.model_path
        model = joblib.load(self.config.model_path)
        
        # Load transformed data
        transformed_data = joblib.load(self.config.transformed_data_path)
        
        # Split into train and test sets
        X_train, X_test = train_test_split(transformed_data, test_size=0.3, random_state=42)
        
        # Get cluster assignments for both sets
        train_labels = model.predict(X_train)
        test_labels = model.predict(X_test)
        
        # Calculate metrics for both sets
        train_metrics = self.eval_metrics(X_train, train_labels)
        test_metrics = self.eval_metrics(X_test, test_labels)
        
        # Evaluate cluster stability
        stability_metrics = self.evaluate_cluster_stability(model, transformed_data)
        
        # Format results
        results = {
            "train_metrics": {
                "silhouette_score": train_metrics[0],
                "calinski_harabasz_score": train_metrics[1],
                "davies_bouldin_score": train_metrics[2]
            },
            "test_metrics": {
                "silhouette_score": test_metrics[0],
                "calinski_harabasz_score": test_metrics[1],
                "davies_bouldin_score": test_metrics[2]
            },
            "stability_metrics": {
                "silhouette_scores_mean": np.mean(stability_metrics["silhouette_scores"]),
                "silhouette_scores_std": np.std(stability_metrics["silhouette_scores"]),
                "calinski_harabasz_scores_mean": np.mean(stability_metrics["calinski_harabasz_scores"]),
                "calinski_harabasz_scores_std": np.std(stability_metrics["calinski_harabasz_scores"]),
                "davies_bouldin_scores_mean": np.mean(stability_metrics["davies_bouldin_scores"]),
                "davies_bouldin_scores_std": np.std(stability_metrics["davies_bouldin_scores"])
            },
            "interpretation": {
                "silhouette_score": "Values near 1 indicate well-defined clusters. Values near 0 indicate overlapping clusters.",
                "calinski_harabasz_score": "Higher values indicate better-defined clusters.",
                "davies_bouldin_score": "Lower values indicate better clustering.",
                "stability": "Lower standard deviation values indicate more stable clustering across different data subsets."
            }
        }
        
        return results

    def save_results(self):
        """
        Load the model, evaluate it on transformed data, and save metrics
        
        In clustering, we should always evaluate using the same transformed data
        that was used during model training. Otherwise, the clusters won't align
        properly with the evaluation data.
        """
        # Load the trained model
        model = joblib.load(self.config.model_path)
        
        # Load transformed data from pickle file
        # For clustering evaluation, we must use the same transformation as training
        transformed_data = joblib.load(self.config.transformed_data_path)
        
        # Use the train_test_evaluation method with transformed data
        results = self.train_test_evaluation()
        
        # Save metrics
        save_json(path=Path(self.config.metric_file_name), data=results)
        
        # # Optionally visualize the clusters using transformed data
        # Optionally visualize the clusters using transformed data
        if hasattr(self.config, 'visualisation_path'):
            # For visualization, use all transformed data
            all_labels = model.predict(transformed_data)
            
            # Create 3D visualizations
            plot_path_3d = Path(str(self.config.visualisation_path).replace('.png', '_3d.png'))
            self.visualize_clusters(transformed_data, all_labels, save_path=plot_path_3d)
        
        return results