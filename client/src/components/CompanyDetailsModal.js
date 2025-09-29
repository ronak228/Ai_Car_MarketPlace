import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  AreaChart,
  Area
} from 'recharts';

const CompanyDetailsModal = ({ isOpen, onClose, company }) => {
  const [activeTab, setActiveTab] = useState('trends');

  if (!isOpen) return null;

  const modalVariants = {
    hidden: {
      opacity: 0,
      scale: 0.8,
      y: 50
    },
    visible: {
      opacity: 1,
      scale: 1,
      y: 0,
      transition: {
        duration: 0.3,
        ease: "easeOut"
      }
    },
    exit: {
      opacity: 0,
      scale: 0.8,
      y: 50,
      transition: {
        duration: 0.2,
        ease: "easeIn"
      }
    }
  };

  const overlayVariants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1 },
    exit: { opacity: 0 }
  };

  return (
    <AnimatePresence>
      <motion.div
        className="modal-overlay"
        variants={overlayVariants}
        initial="hidden"
        animate="visible"
        exit="exit"
        onClick={onClose}
        style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: 'rgba(0, 0, 0, 0.7)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1050,
          padding: '20px'
        }}
      >
        <motion.div
          className="modal-content"
          variants={modalVariants}
          initial="hidden"
          animate="visible"
          exit="exit"
          onClick={(e) => e.stopPropagation()}
          style={{
            backgroundColor: 'white',
            borderRadius: '20px',
            boxShadow: '0 25px 50px rgba(0, 0, 0, 0.25)',
            maxWidth: '95vw',
            maxHeight: '95vh',
            width: '800px',
            overflow: 'hidden',
            position: 'relative'
          }}
        >
          {/* Header */}
          <div className="modal-header" style={{
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white',
            padding: '20px 30px',
            borderBottom: '1px solid #e9ecef'
          }}>
            <div className="d-flex justify-content-between align-items-center">
              <div>
                <h3 className="mb-1" style={{ fontWeight: '700', fontSize: '1.8rem' }}>
                  {company} Market Analysis
                </h3>
                <p className="mb-0" style={{ opacity: 0.9, fontSize: '1rem' }}>
                  Comprehensive market insights and trends
                </p>
              </div>
              <button
                onClick={onClose}
                className="btn btn-light btn-sm"
                style={{
                  borderRadius: '50%',
                  width: '40px',
                  height: '40px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '1.2rem',
                  fontWeight: 'bold'
                }}
              >
                ×
              </button>
            </div>
          </div>

          {/* Content */}
          <div className="modal-body" style={{
            padding: '30px',
            textAlign: 'center'
          }}>
            <h5 className="mb-4">📊 {company} Market Data</h5>
            <p className="text-muted mb-4">
              Testing Recharts integration with a simple chart.
            </p>
            
            {/* Simple Test Chart */}
            <div style={{ height: '300px', marginBottom: '20px' }}>
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={[
                  { year: 2020, price: 1000000 },
                  { year: 2021, price: 1200000 },
                  { year: 2022, price: 1400000 },
                  { year: 2023, price: 1600000 }
                ]}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="year" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="price" stroke="#8884d8" strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
            </div>
            
            <div className="row g-3">
              <div className="col-md-4">
                <div className="card">
                  <div className="card-body">
                    <h6>📈 Price Trends</h6>
                    <p className="small text-muted">Historical price analysis</p>
                  </div>
                </div>
              </div>
              <div className="col-md-4">
                <div className="card">
                  <div className="card-body">
                    <h6>📊 Sales Data</h6>
                    <p className="small text-muted">Units sold per year</p>
                  </div>
                </div>
              </div>
              <div className="col-md-4">
                <div className="card">
                  <div className="card-body">
                    <h6>🥧 Market Share</h6>
                    <p className="small text-muted">Competitor comparison</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Footer */}
          <div className="modal-footer" style={{
            padding: '20px 30px',
            backgroundColor: '#f8f9fa',
            borderTop: '1px solid #e9ecef'
          }}>
            <div className="d-flex justify-content-between align-items-center">
              <div className="text-muted">
                <small>
                  💡 <strong>Note:</strong> This is a simplified version. 
                  Full charts will be implemented after fixing the error.
                </small>
              </div>
              <button 
                className="btn btn-primary btn-sm"
                onClick={onClose}
              >
                ✅ Close
              </button>
            </div>
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
};

export default CompanyDetailsModal;
