import React, { useState } from 'react';
import { Container, Row, Col, Card, Form, Button, Alert, Spinner } from 'react-bootstrap';

const CarPriceAI = ({ onLogin, isSignUp = false }) => {
    const [formData, setFormData] = useState({
        email: '',
        password: '',
        fullName: '',
        confirmPassword: ''
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    // OTP functionality removed

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
        setError('');
    };

    // OTP change handler removed

    const validateForm = () => {
        if (!formData.email || !formData.password) {
            setError('Email and password are required');
            return false;
        }

        if (isSignUp) {
            if (!formData.fullName) {
                setError('Full name is required');
                return false;
            }
            if (formData.password !== formData.confirmPassword) {
                setError('Passwords do not match');
                return false;
            }
            if (formData.password.length < 6) {
                setError('Password must be at least 6 characters');
                return false;
            }
        }

        return true;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        if (!validateForm()) {
            return;
        }

        setLoading(true);
        setError('');

        try {
            // Simulate authentication for CarPrice AI
            await new Promise(resolve => setTimeout(resolve, 1000));
            
            if (isSignUp) {
                setSuccess('Welcome to CarPrice AI! Registration successful.');
                // Clear form except email
                setFormData(prev => ({
                    email: prev.email,
                    password: '',
                    fullName: '',
                    confirmPassword: ''
                }));
            } else {
                setSuccess('Welcome back to CarPrice AI!');
                // Simulate user login
                const user = {
                    id: '1',
                    email: formData.email,
                    name: formData.fullName || 'CarPrice AI User',
                    isAuthenticated: true
                };
                onLogin(user);
            }
        } catch (error) {
            setError('An unexpected error occurred');
            console.error('Auth error:', error);
        } finally {
            setLoading(false);
        }
    };

    // OTP handlers removed

    return (
        <Container className="mt-5">
            <Row className="justify-content-center">
                <Col md={6} lg={5}>
                    <Card className="shadow">
                        <Card.Header className="text-center bg-primary text-white">
                            <h4><i className="fas fa-robot me-2"></i>{isSignUp ? 'CarPrice AI Sign Up' : 'CarPrice AI Sign In'}</h4>
                        </Card.Header>
                        <Card.Body>
                            {error && <Alert variant="danger">{error}</Alert>}
                            {success && <Alert variant="success">{success}</Alert>}

                            <Form onSubmit={handleSubmit}>
                                {isSignUp && (
                                    <Form.Group className="mb-3">
                                        <Form.Label>Full Name</Form.Label>
                                        <Form.Control
                                            type="text"
                                            name="fullName"
                                            value={formData.fullName}
                                            onChange={handleInputChange}
                                            placeholder="Enter your full name"
                                            required
                                        />
                                    </Form.Group>
                                )}

                                <Form.Group className="mb-3">
                                    <Form.Label>Email</Form.Label>
                                    <Form.Control
                                        type="email"
                                        name="email"
                                        value={formData.email}
                                        onChange={handleInputChange}
                                        placeholder="Enter your email"
                                        required
                                    />
                                </Form.Group>

                                <Form.Group className="mb-3">
                                    <Form.Label>Password</Form.Label>
                                    <Form.Control
                                        type="password"
                                        name="password"
                                        value={formData.password}
                                        onChange={handleInputChange}
                                        placeholder="Enter your password"
                                        required
                                    />
                                </Form.Group>

                                {isSignUp && (
                                    <Form.Group className="mb-3">
                                        <Form.Label>Confirm Password</Form.Label>
                                        <Form.Control
                                            type="password"
                                            name="confirmPassword"
                                            value={formData.confirmPassword}
                                            onChange={handleInputChange}
                                            placeholder="Confirm your password"
                                            required
                                        />
                                    </Form.Group>
                                )}

                                <div className="d-grid gap-2">
                                    <Button
                                        type="submit"
                                        variant="primary"
                                        disabled={loading}
                                    >
                                        {loading ? (
                                            <>
                                                <Spinner size="sm" className="me-2" />
                                                {isSignUp ? 'Signing Up...' : 'Signing In...'}
                                            </>
                                        ) : (
                                            isSignUp ? 'Sign Up' : 'Sign In'
                                        )}
                                    </Button>
                                </div>
                            </Form>

                            <div className="text-center mt-3">
                                <small className="text-muted">
                                    {isSignUp ? 'Already have an account?' : "Don't have an account?"}{' '}
                                    <a href={isSignUp ? '/mongo-signin' : '/mongo-signup'}>
                                        {isSignUp ? 'Sign In' : 'Sign Up'}
                                    </a>
                                </small>
                            </div>
                        </Card.Body>
                    </Card>
                </Col>
            </Row>
        </Container>
    );
};

export default CarPriceAI;
