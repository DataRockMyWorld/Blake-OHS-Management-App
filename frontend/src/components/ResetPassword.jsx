import React, { useState} from "react";
import { useNavigate, useParams } from "react-router-dom";
import axiosInstance from "../utils/axiosInstance";
import { toast } from "react-toastify";

const ResetPassword = () => {
    const navigate = useNavigate()
    const { uid, token } = useParams()
    const [passwords, setPasswords] = useState({
        new_password: '',
        confirm_password: '',
    })

    const { new_password, confirm_password } = passwords

    const handleChange = (e) => {
        setPasswords({ ...passwords, [e.target.name]: e.target.value })
    }

    const data = {
        'new_password': new_password,
        'confirm_password': confirm_password,
        'uidb64': uid,
        'token': token,
    }

    const handleSubmit = async (e) => {
        e.preventDefault()
        if (data) {
            const response = await axiosInstance.patch('v1/set-new-password/', data)
            const result = response.data
            if (response.status === 200) {
                navigate('/login')
                toast.success(result.message)
            }
            console.log(result)
        }
    }


    return (
        <div className="form-container">
            <div className="wrapper" style={{ width: '100%' }}>
                <h2>Reset your password</h2>
                <form action="" onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label htmlFor="password">New Password</label>
                        <input type="password"
                        name="new_password"
                        className="email-form"
                        value={new_password}
                        onChange={handleChange}
                        required />
                    </div>
                    <div className="form-group">
                        <label htmlFor="confirmPassword">Confirm Password</label>
                        <input type="password"
                        name="confirm_password"
                        className="email-form"
                        value={confirm_password}
                        onChange={handleChange}
                        required />
                    </div>
                    <button type="submit" className="vbtn">Reset Password</button>
                </form>
            </div>
        </div>
    )
    
    
}

export default ResetPassword
