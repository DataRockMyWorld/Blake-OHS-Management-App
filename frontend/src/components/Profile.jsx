import React, {useEffect} from 'react'
import { useNavigate } from "react-router-dom";
import { toast } from 'react-toastify';
import axiosInstance from "../utils/axiosInstance";

const Profile = () => {
    const jwt_access = localStorage.getItem('access');
    const user = JSON.parse(localStorage.getItem('user'));
    const navigate = useNavigate();

    useEffect(() => {
        if (jwt_access === null || !user) {
            navigate('/login');
        } else {
            getSomeData();
        }
    }, [jwt_access, user]);

    const getSomeData = async () => {
        try {
            const res = await axiosInstance.get('v1/test-authentication/');
            if (res.status === 200) {
                console.log(res.data);
                toast.success("Authenicated & Data Fetched");
            }
        } catch (error) {
            console.error("Error fetching data:", error);
        }
    };

    const refresh = localStorage.getItem('refresh');
   

    const handleLogout = async () => {
        try {
            const res = await axiosInstance.post('v1/logout/', { "refresh": refresh });
            if (res.status === 200) {
                localStorage.removeItem('access');
                localStorage.removeItem('refresh');
                localStorage.removeItem('user');
                navigate('/login');
                toast.warn("Logout successful");
            }
        } catch (error) {
            console.error("Error during logout:", error);
            toast.error("Failed to log out");
        }
    };

    return (
        <div className='container'>
            <h2>hi {user.full_name || user.names}</h2>
            <p style={{ textAlign: 'center' }}>Welcome to your profile</p>
            <button onClick={handleLogout} className='logout-btn'>Logout</button>
        </div>
    );
};

export default Profile;
