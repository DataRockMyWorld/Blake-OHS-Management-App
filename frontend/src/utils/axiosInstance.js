import axios from "axios";
import { jwtDecode } from "jwt-decode";  // Use named import, not destructuring
import dayjs from "dayjs";

const baseUrl = 'http://localhost:8000/api/';

let token = localStorage.getItem('access') ? JSON.parse(localStorage.getItem('access')) : null;
let refresh_token = localStorage.getItem('refresh') ? JSON.parse(localStorage.getItem('refresh')) : null;

const axiosInstance = axios.create({
    baseURL: baseUrl,
    headers: {
        'Content-Type': 'application/json',
        'Authorization': token ? `Bearer ${token}` : null
    }
});

axiosInstance.interceptors.request.use(async (req) => {
    // Check if access token is available and set the header
    if (token) {
        req.headers.Authorization = `Bearer ${token}`;
        
        // Decode the token and check expiration
        const user = jwtDecode(token);
        const isExpired = dayjs.unix(user.exp).diff(dayjs()) < 1;
        
        if (isExpired) {
            try {
                // Attempt to refresh the token
                const res = await axios.post(`${baseUrl}token/refresh/`, { "refresh": refresh_token });
                const response = res.data;

                if (res.status === 200) {
                    // Update local storage and set the new access token in the request header
                    localStorage.setItem('access', JSON.stringify(response.access));
                    req.headers.Authorization = `Bearer ${response.access}`;
                    token = response.access;
                    console.log('access: ',token)
                    // Update token variable
                } else {
                    // Token refresh failed, handle logout
                    await handleLogout();  // Handle logout if the refresh fails
                }
            } catch (error) {
                console.error('Error refreshing token:', error);
                await handleLogout();
            }
        }
    }
    
    // Always return the request object
    return req;
}, (error) => {
    return Promise.reject(error);
});

// Function to handle user logout
const handleLogout = async () => {
    try {
        const res = await axios.post(`${baseUrl}v1/logout/`, { "refresh": refresh_token });
        if (res.status === 200) {
            localStorage.removeItem('access');
            localStorage.removeItem('refresh');
            localStorage.removeItem('user');
        }
    } catch (error) {
        console.error('Error during logout:', error);
    }
};

console.log("axiosInstance: ")

export default axiosInstance;
