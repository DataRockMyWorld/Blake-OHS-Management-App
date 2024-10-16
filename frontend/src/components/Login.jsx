import React, { useEffect, useState } from 'react'
import { Link, useNavigate} from "react-router-dom";
import { toast } from 'react-toastify';
import axiosInstance from '../utils/axiosInstance';


const Login = () => {
    const navigate = useNavigate()
    const [logindata, setLogindata] = useState({
        email: "",
        password: ""
    })

    const [error, setError] = useState("")
    const [isLoading, setIsLoading] = useState(false)


    const handleOnchange = (e) => {
        setLogindata({ ...logindata, [e.target.name]: e.target.value })
    }


    const handleLoginWithGoogle = (response) => {
        console.log("id_token", response.credential)
    }


    useEffect(() => {
        /* global google */
        google.accounts.id.initialize({
            client_id: import.meta.env.VITE_GOOGLE_CLIENT_ID,
            callback: handleLoginWithGoogle
        });
        google.accounts.id.renderButton(
            document.getElementById("signInDiv"),
            { theme: "outline", size: "large", text: "continue_with", shape: "circle", width: "280" }
        );

    }, [])


    const handleSubmit = async (e) => {
        e.preventDefault()
        const {email, password}=logindata
        if (!email || !password) {
            setError("All fields are required")
        }else{
            setIsLoading(true)
            const res = await axiosInstance.post('login/', {email, password})
            const response = res.data
            console.log(response)
            const user = {
                'full_name': response.full_name,
                'email': response.email
            }
            if (res.status === 200) {
                localStorage.setItem('access', JSON.stringify(response.access_token))
                localStorage.setItem('refresh', JSON.stringify(response.refresh_token))
                localStorage.setItem('user', JSON.stringify(user))
                await navigate('/dashboard')
                toast.success('login successful')
            } else {
                toast.error('something went wrong')
            }
        }
    }

    return (
        <div>

            <div className='form-container'>
                <div style={{ width: "100%" }} className='wrapper'>
                    <h2>Login into your account</h2>
                    <form action="" onSubmit={handleSubmit}>
                        {isLoading && 
                        <p>Loading...</p>
                        }
                        <div className='form-group'>
                            <label htmlFor="">Email Address:</label>
                            <input type="email"
                                className='email-form'
                                value={logindata.email}
                                name="email"
                                onChange={handleOnchange} />

                        </div>

                        <div className='form-group'>
                            <label htmlFor="">Password:</label>
                            <input type="password"
                                className='email-form'
                                value={logindata.password}
                                name="password"
                                onChange={handleOnchange} />
                        </div>

                        <input type="submit" value="Login" className="submitButton" />
                        <p className='pass-link'><Link to={'/forget_password'}>forgot password</Link></p>
                    </form>
                    <h3 className='text-option'>Or</h3>
                    <div className='googleContainer'>
                        <div id="signInDiv" className='gsignIn'></div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Login
