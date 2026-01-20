"""
Meta-analysis methods.
"""

from typing import Dict, Any
import numpy as np
from scipy.spatial.distance import euclidean, cosine
from scipy import stats

from ..engine.context import AnalysisContext
from ..engine.results import AnalysisResult
from ..engine.registry import register_method
from ..utils.logging import get_logger

logger = get_logger(__name__)


def inter_segment_comparison(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Compare segments for repetitions/anomalies.
    """
    num_segments = params.get('num_segments', 10)
    
    measurements = {}
    
    for channel_name, audio_data in context.audio_data.items():
        
        segment_length = len(audio_data) // num_segments
        
        if segment_length < 1024:
            logger.warning(f"Segments too short for {channel_name}")
            continue
        
        segments = []
        for i in range(num_segments):
            start = i * segment_length
            end = start + segment_length
            segments.append(audio_data[start:end])
        
        features = []
        for seg in segments:
            spectrum = np.abs(np.fft.rfft(seg))
            energy = np.sum(seg ** 2)
            centroid = np.sum(np.arange(len(spectrum)) * spectrum) / (np.sum(spectrum) + 1e-10)
            features.append([energy, centroid, np.mean(spectrum), np.std(spectrum)])
        
        features = np.array(features)
        
        distances = []
        for i in range(len(features)):
            for j in range(i+1, len(features)):
                dist = euclidean(features[i], features[j])
                distances.append(dist)
        
        distances = np.array(distances)
        
        mean_distance = np.mean(distances)
        std_distance = np.std(distances)
        min_distance = np.min(distances)
        max_distance = np.max(distances)
        
        similarity_score = 1.0 / (1.0 + mean_distance)
        
        measurements[channel_name] = {
            'num_segments': num_segments,
            'mean_distance': float(mean_distance),
            'std_distance': float(std_distance),
            'min_distance': float(min_distance),
            'max_distance': float(max_distance),
            'similarity_score': float(similarity_score)
        }
    
    logger.info(f"Inter-segment comparison for {len(measurements)} channels")
    
    return AnalysisResult(
        method='inter_segment_comparison',
        measurements=measurements,
        metrics={'num_segments': num_segments}
    )


def segment_clustering(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Cluster segments by similarity.
    """
    num_segments = params.get('num_segments', 20)
    
    measurements = {}
    
    for channel_name, audio_data in context.audio_data.items():
        
        segment_length = len(audio_data) // num_segments
        
        if segment_length < 1024:
            logger.warning(f"Segments too short for {channel_name}")
            continue
        
        segments = []
        for i in range(num_segments):
            start = i * segment_length
            end = start + segment_length
            segments.append(audio_data[start:end])
        
        features = []
        for seg in segments:
            spectrum = np.abs(np.fft.rfft(seg))
            if len(spectrum) > 100:
                spectrum_reduced = spectrum[:100]
            else:
                spectrum_reduced = np.pad(spectrum, (0, 100 - len(spectrum)))
            
            features.append(spectrum_reduced / (np.sum(spectrum_reduced) + 1e-10))
        
        features = np.array(features)
        
        distance_matrix = np.zeros((num_segments, num_segments))
        for i in range(num_segments):
            for j in range(num_segments):
                if i != j:
                    distance_matrix[i, j] = cosine(features[i], features[j])
        
        avg_intra_distance = np.mean(distance_matrix[distance_matrix > 0])
        
        unique_threshold = 0.5
        unique_segments = 0
        for i in range(num_segments):
            if np.min(distance_matrix[i, distance_matrix[i] > 0]) > unique_threshold:
                unique_segments += 1
        
        measurements[channel_name] = {
            'num_segments': num_segments,
            'avg_intra_distance': float(avg_intra_distance),
            'unique_segments': unique_segments,
            'repetition_rate': float(1.0 - unique_segments / num_segments)
        }
    
    logger.info(f"Segment clustering for {len(measurements)} channels")
    
    return AnalysisResult(
        method='segment_clustering',
        measurements=measurements,
        metrics={'num_segments': num_segments}
    )


def stability_scores(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Temporal and spectral stability indicators.
    
    Args:
        context: Analysis context
        params: window_size, hop_length
        
    Returns:
        AnalysisResult with stability scores and visualization_data
    """
    window_size = params.get('window_size', 2048)
    hop_length = params.get('hop_length', 512)
    
    measurements = {}
    visualization_data = {}
    
    for channel_name, audio_data in context.audio_data.items():
        
        max_samples = 200000
        if len(audio_data) > max_samples:
            audio_subset = audio_data[:max_samples]
            logger.warning(f"Stability scores: using first {max_samples} samples")
        else:
            audio_subset = audio_data
        
        energies = []
        spectral_centroids = []
        
        for i in range(0, len(audio_subset) - window_size, hop_length):
            window = audio_subset[i:i + window_size]
            
            energy = np.sum(window ** 2)
            energies.append(energy)
            
            spectrum = np.abs(np.fft.rfft(window))
            freqs = np.arange(len(spectrum))
            centroid = np.sum(freqs * spectrum) / (np.sum(spectrum) + 1e-10)
            spectral_centroids.append(centroid)
        
        energies = np.array(energies)
        spectral_centroids = np.array(spectral_centroids)
        
        energy_stability = 1.0 / (1.0 + np.std(energies) / (np.mean(energies) + 1e-10))
        spectral_stability = 1.0 / (1.0 + np.std(spectral_centroids) / (np.mean(spectral_centroids) + 1e-10))
        
        overall_stability = (energy_stability + spectral_stability) / 2.0
        
        measurements[channel_name] = {
            'energy_stability': float(energy_stability),
            'spectral_stability': float(spectral_stability),
            'overall_stability': float(overall_stability),
            'num_windows': len(energies)
        }
        
        # AJOUT: visualization_data pour afficher stability evolution dans le temps
        # Calculer les temps correspondants aux fenêtres
        times = (np.arange(len(energies)) * hop_length) / context.sample_rate
        visualization_data[channel_name] = {
            'times': times,
            'energy': energies,
            'spectral_centroid': spectral_centroids,
            'energy_mean': np.mean(energies),
            'centroid_mean': np.mean(spectral_centroids)
        }
    
    logger.info(f"Stability scores for {len(context.audio_data)} channels")
    
    return AnalysisResult(
        method='stability_scores',
        measurements=measurements,
        metrics={'window_size': window_size, 'hop_length': hop_length},
        visualization_data=visualization_data
    )


def high_order_statistics(context: AnalysisContext, params: Dict[str, Any]) -> AnalysisResult:
    """
    Compute high-order statistics (skewness, kurtosis).
    
    High-order statistics reveal information about the shape of the
    amplitude distribution beyond mean and variance.
    
    Args:
        context: Analysis context
        params: num_bins (for histogram visualization)
        
    Returns:
        AnalysisResult with statistical moments and visualization_data
    """
    num_bins = params.get('num_bins', 50)
    
    measurements = {}
    visualization_data = {}
    
    for channel_name, audio_data in context.audio_data.items():
        
        # Limit for performance on histogram
        max_samples = 200000
        if len(audio_data) > max_samples:
            audio_subset = audio_data[:max_samples]
            logger.warning(f"High-order statistics: using first {max_samples} samples")
        else:
            audio_subset = audio_data
        
        # Basic statistics
        mean = np.mean(audio_subset)
        std = np.std(audio_subset)
        variance = np.var(audio_subset)
        
        # High-order moments
        skewness = stats.skew(audio_subset)
        kurtosis = stats.kurtosis(audio_subset)
        
        # Peak statistics
        peak_value = np.max(np.abs(audio_subset))
        crest_factor = peak_value / (np.sqrt(np.mean(audio_subset ** 2)) + 1e-10)
        
        # Histogram for distribution analysis
        hist, bin_edges = np.histogram(audio_subset, bins=num_bins, density=True)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        
        # Fit normal distribution for comparison
        normal_dist = stats.norm.pdf(bin_centers, mean, std)
        
        measurements[channel_name] = {
            'mean': float(mean),
            'std': float(std),
            'variance': float(variance),
            'skewness': float(skewness),
            'kurtosis': float(kurtosis),
            'peak_value': float(peak_value),
            'crest_factor': float(crest_factor),
            'samples_analyzed': len(audio_subset)
        }
        
        # Visualization data
        visualization_data[channel_name] = {
            'histogram': hist,
            'bin_centers': bin_centers,
            'normal_distribution': normal_dist,
            'mean': mean,
            'std': std,
            'skewness': skewness,
            'kurtosis': kurtosis
        }
    
    logger.info(f"High-order statistics for {len(context.audio_data)} channels")
    
    return AnalysisResult(
        method='high_order_statistics',
        measurements=measurements,
        metrics={'num_bins': num_bins},
        visualization_data=visualization_data
    )


register_method("inter_segment_comparison", "meta_analysis", inter_segment_comparison, "Inter-segment comparison")
register_method("segment_clustering", "meta_analysis", segment_clustering, "Segment clustering")
register_method("stability_scores", "meta_analysis", stability_scores, "Temporal/spectral stability")
register_method("high_order_statistics", "meta_analysis", high_order_statistics, "High-order statistical moments")