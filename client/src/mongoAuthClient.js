/**
 * MongoDB Authentication Client for AI Car Marketplace
 * Handles authentication with MongoDB backend
 */

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000';

class MongoAuthClient {
    constructor() {
        this.token = localStorage.getItem('mongo_auth_token');
        this.user = this.getStoredUser();
    }

    // Authentication methods
    async register(email, password, fullName = null) {
        try {
            const response = await fetch(`${API_BASE_URL}/api/auth/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email,
                    password,
                    full_name: fullName
                })
            });

            const data = await response.json();

            if (response.ok) {
                this.setAuthData(data.user);
                return { success: true, user: data.user };
            } else {
                return { success: false, error: data.error || 'Registration failed' };
            }
        } catch (error) {
            console.error('Registration error:', error);
            return { success: false, error: 'Network error' };
        }
    }

    async login(email, password) {
        try {
            const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (response.ok) {
                this.setAuthData(data.user);
                return { success: true, user: data.user };
            } else {
                return { success: false, error: data.error || 'Login failed' };
            }
        } catch (error) {
            console.error('Login error:', error);
            return { success: false, error: 'Network error' };
        }
    }

    async logout() {
        try {
            if (this.token) {
                await fetch(`${API_BASE_URL}/api/auth/logout`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${this.token}`,
                        'Content-Type': 'application/json',
                    }
                });
            }
        } catch (error) {
            console.error('Logout error:', error);
        } finally {
            this.clearAuthData();
        }
    }

    async verifyToken() {
        if (!this.token) {
            return false;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/api/auth/verify-token`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ token: this.token })
            });

            const data = await response.json();
            return data.valid === true;
        } catch (error) {
            console.error('Token verification error:', error);
            return false;
        }
    }

    async getProfile() {
        if (!this.token) {
            return null;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/api/auth/profile`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${this.token}`,
                    'Content-Type': 'application/json',
                }
            });

            if (response.ok) {
                const data = await response.json();
                return data.user;
            } else {
                return null;
            }
        } catch (error) {
            console.error('Get profile error:', error);
            return null;
        }
    }

    async changePassword(currentPassword, newPassword) {
        if (!this.token) {
            return { success: false, error: 'Not authenticated' };
        }

        try {
            const response = await fetch(`${API_BASE_URL}/api/auth/change-password`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    current_password: currentPassword,
                    new_password: newPassword
                })
            });

            const data = await response.json();

            if (response.ok) {
                return { success: true, message: data.message };
            } else {
                return { success: false, error: data.error || 'Password change failed' };
            }
        } catch (error) {
            console.error('Change password error:', error);
            return { success: false, error: 'Network error' };
        }
    }

    async getUserPredictions() {
        if (!this.token) {
            return { success: false, error: 'Not authenticated' };
        }

        try {
            const response = await fetch(`${API_BASE_URL}/api/auth/predictions`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${this.token}`,
                    'Content-Type': 'application/json',
                }
            });

            const data = await response.json();

            if (response.ok) {
                return { success: true, predictions: data.predictions };
            } else {
                return { success: false, error: data.error || 'Failed to get predictions' };
            }
        } catch (error) {
            console.error('Get predictions error:', error);
            return { success: false, error: 'Network error' };
        }
    }

    // OTP methods removed - using simple authentication

    // Utility methods
    setAuthData(userData) {
        this.token = userData.token;
        this.user = userData;
        localStorage.setItem('mongo_auth_token', userData.token);
        localStorage.setItem('mongo_auth_user', JSON.stringify(userData));
        localStorage.setItem('mongo_auth_timestamp', Date.now().toString());
    }

    clearAuthData() {
        this.token = null;
        this.user = null;
        localStorage.removeItem('mongo_auth_token');
        localStorage.removeItem('mongo_auth_user');
        localStorage.removeItem('mongo_auth_timestamp');
    }

    getStoredUser() {
        try {
            const storedUser = localStorage.getItem('mongo_auth_user');
            const timestamp = localStorage.getItem('mongo_auth_timestamp');
            
            if (storedUser && timestamp) {
                // Check if token is not expired (24 hours)
                const tokenAge = Date.now() - parseInt(timestamp);
                const maxAge = 24 * 60 * 60 * 1000; // 24 hours
                
                if (tokenAge < maxAge) {
                    return JSON.parse(storedUser);
                } else {
                    this.clearAuthData();
                }
            }
        } catch (error) {
            console.error('Error parsing stored user:', error);
            this.clearAuthData();
        }
        return null;
    }

    isAuthenticated() {
        return !!(this.token && this.user);
    }

    getCurrentUser() {
        return this.user;
    }

    getAuthToken() {
        return this.token;
    }

    // Prediction methods with authentication
    async predictCarPrice(carData) {
        if (!this.token) {
            return { success: false, error: 'Not authenticated' };
        }

        try {
            const response = await fetch(`${API_BASE_URL}/api/predict`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    ...carData,
                    user_id: this.user.id
                })
            });

            const data = await response.json();

            if (response.ok) {
                return { success: true, prediction: data };
            } else {
                return { success: false, error: data.error || 'Prediction failed' };
            }
        } catch (error) {
            console.error('Prediction error:', error);
            return { success: false, error: 'Network error' };
        }
    }
}

// Create singleton instance
const mongoAuthClient = new MongoAuthClient();

export default mongoAuthClient;
