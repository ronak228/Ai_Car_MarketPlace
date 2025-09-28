// Prediction Storage Utility
export const PredictionStorage = {
  // Save a new prediction
  savePrediction: (predictionData) => {
    try {
      const predictions = PredictionStorage.getAllPredictions();
      const newPrediction = {
        id: Date.now(), // Use timestamp as unique ID
        ...predictionData,
        timestamp: new Date().toISOString(),
        date: new Date().toLocaleDateString(),
        saved: false,
        accuracy: null, // Will be updated later if actual price is provided
        actualPrice: null
      };
      
      predictions.unshift(newPrediction); // Add to beginning
      
      // Keep only last 50 predictions to avoid localStorage bloat
      const limitedPredictions = predictions.slice(0, 50);
      
      localStorage.setItem('carPredictions', JSON.stringify(limitedPredictions));
      return newPrediction;
    } catch (error) {
      console.error('Error saving prediction:', error);
      return null;
    }
  },

  // Get all predictions
  getAllPredictions: () => {
    try {
      const predictions = localStorage.getItem('carPredictions');
      return predictions ? JSON.parse(predictions) : [];
    } catch (error) {
      console.error('Error loading predictions:', error);
      return [];
    }
  },

  // Get saved predictions only
  getSavedPredictions: () => {
    const predictions = PredictionStorage.getAllPredictions();
    return predictions.filter(p => p.saved);
  },

  // Update prediction (for saving/unsaving, adding actual price, etc.)
  updatePrediction: (predictionId, updates) => {
    try {
      const predictions = PredictionStorage.getAllPredictions();
      const updatedPredictions = predictions.map(p => 
        p.id === predictionId ? { ...p, ...updates } : p
      );
      
      localStorage.setItem('carPredictions', JSON.stringify(updatedPredictions));
      return true;
    } catch (error) {
      console.error('Error updating prediction:', error);
      return false;
    }
  },

  // Toggle save status
  toggleSave: (predictionId) => {
    const predictions = PredictionStorage.getAllPredictions();
    const prediction = predictions.find(p => p.id === predictionId);
    if (prediction) {
      return PredictionStorage.updatePrediction(predictionId, { 
        saved: !prediction.saved 
      });
    }
    return false;
  },

  // Add actual price and calculate accuracy
  addActualPrice: (predictionId, actualPrice) => {
    const predictions = PredictionStorage.getAllPredictions();
    const prediction = predictions.find(p => p.id === predictionId);
    if (prediction) {
      const accuracy = ((1 - Math.abs(prediction.predictedPrice - actualPrice) / prediction.predictedPrice) * 100).toFixed(1);
      return PredictionStorage.updatePrediction(predictionId, { 
        actualPrice,
        accuracy: `${accuracy}%`
      });
    }
    return false;
  },

  // Delete prediction
  deletePrediction: (predictionId) => {
    try {
      const predictions = PredictionStorage.getAllPredictions();
      const filteredPredictions = predictions.filter(p => p.id !== predictionId);
      localStorage.setItem('carPredictions', JSON.stringify(filteredPredictions));
      return true;
    } catch (error) {
      console.error('Error deleting prediction:', error);
      return false;
    }
  },

  // Clear all predictions
  clearAllPredictions: () => {
    try {
      localStorage.removeItem('carPredictions');
      return true;
    } catch (error) {
      console.error('Error clearing predictions:', error);
      return false;
    }
  },

  // Export predictions as CSV
  exportPredictions: () => {
    const predictions = PredictionStorage.getAllPredictions();
    const csvContent = [
      ['Car', 'Company', 'Model', 'Year', 'Predicted Price', 'Confidence', 'Date', 'Accuracy', 'Saved'],
      ...predictions.map(p => [
        `${p.company} ${p.model}`,
        p.company,
        p.model,
        p.year,
        p.predictedPrice,
        p.confidence + '%',
        p.date,
        p.accuracy || 'Pending',
        p.saved ? 'Yes' : 'No'
      ])
    ].map(row => row.join(',')).join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `car-predictions-${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
  },

  // Get prediction statistics
  getStats: () => {
    const predictions = PredictionStorage.getAllPredictions();
    const savedPredictions = predictions.filter(p => p.saved);
    const predictionsWithAccuracy = predictions.filter(p => p.accuracy);
    
    const avgConfidence = predictions.length > 0 
      ? Math.round(predictions.reduce((sum, p) => sum + p.confidence, 0) / predictions.length)
      : 0;
    
    const avgAccuracy = predictionsWithAccuracy.length > 0
      ? Math.round(predictionsWithAccuracy.reduce((sum, p) => sum + parseFloat(p.accuracy), 0) / predictionsWithAccuracy.length)
      : 0;

    // Find most predicted brand
    const brandCounts = {};
    predictions.forEach(p => {
      brandCounts[p.company] = (brandCounts[p.company] || 0) + 1;
    });
    const favoriteBrand = Object.keys(brandCounts).reduce((a, b) => 
      brandCounts[a] > brandCounts[b] ? a : b, 'Toyota'
    );

    return {
      totalPredictions: predictions.length,
      totalSaved: savedPredictions.length,
      averageConfidence: avgConfidence,
      averageAccuracy: avgAccuracy,
      favoriteBrand,
      accuracyRate: avgAccuracy
    };
  }
};

export default PredictionStorage;
