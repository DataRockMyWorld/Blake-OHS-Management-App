import React, { useState, useEffect } from "react";
import axios from "axios";
import { toast } from "react-toastify";
import { useNavigate } from "react-router-dom";

const Signup = () => {
  const navigate=useNavigate()
  const [formdata, setFormdata]=useState({
      email:"",
      first_name:"",
      last_name:"",
      password:"",
      password2:"",
      department:"Operations"
  })
  const [error, setError]=useState('')

  const handleOnchange = (e)=>{
      setFormdata({...formdata, [e.target.name]:e.target.value})
  }

  
  const handleSigninWithGoogle = async (response)=>{
      const payload=response.credential
      const server_res= await axios.post("http://localhost:8000/api/auth/google/", {'access_token':payload})
      const user={
        email: server_res.data.email,
        names: server_res.data.full_name,
      }
      if (server_res.status === 200) {
        localStorage.setItem('user', JSON.stringify(user));
        localStorage.setItem('access', JSON.stringify(server_res.data.access_token));
        localStorage.setItem('refresh', JSON.stringify(server_res.data.refresh_token) );
        navigate("/dashboard")
        toast.success("Login Successful")
      }
  }

  useEffect(() => {
    /* global google */
    google.accounts.id.initialize({
      client_id:import.meta.env.VITE_GOOGLE_CLIENT_ID,
      callback: handleSigninWithGoogle
    });
    google.accounts.id.renderButton(
      document.getElementById("signInDiv"),
      {theme:"outline", size:"large", text:"continue_with", shape:"circle", width:"280"}
    );
      
  }, [])

  const {email, first_name, last_name, password, password2, department}=formdata
 
  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("Form Data:", formdata);

    try {
        const response = await axios.post('http://localhost:8000/api/v1/register/', formdata);
        if (response.status === 201) {
            navigate("/otp/verify");
            toast.success(response.data.message);
        }
    } catch (error) {
        if (error.response) {
            console.error("Error during registration:", error.response.data);
            toast.error("Registration failed: " + error.response.data.message);
        } else {
            console.error("Error during registration:", error.message);
        }
    }
};


  return (
    <div>
              <div className='form-container'>
            <div style={{width:"100%"}} className='wrapper'>
            <h2>create account</h2>
            <form action="" onSubmit={handleSubmit}>
                <div className='form-group'>
                 <label htmlFor="">Email Address:</label>
                 <input type="text"
                  className='email-form'  
                  name="email" 
                  value={email}  
                  onChange={handleOnchange} />
               </div>
               <div className='form-group'>
                 <label htmlFor="">First Name:</label>
                 <input type="text"
                  className='email-form'
                  name="first_name" 
                  value={first_name} 
                  onChange={handleOnchange}/>
               </div>
               <div className='form-group'>
                 <label htmlFor="">Last Name:</label>
                 <input type="text" 
                 className='email-form'  
                 name="last_name" 
                 value={last_name} 
                 onChange={handleOnchange}/>
               </div>
               <div className='form-group'>
                 <label htmlFor="">Password:</label>
                 <input type="text" 
                 className='email-form'  
                 name="password" 
                 value={password} 
                 onChange={handleOnchange}/>
               </div>
               <div className='form-group'>
                 <label htmlFor="">Confirm Password:</label>
                 <input type="text" 
                 className='p'  
                 name="password2" 
                 value={password2} 
                 onChange={handleOnchange}/>
               </div>
               <div className="form-group">
                <label htmlFor="">Department:</label>
                <select 
                name="department" 
                value={department}
                onChange={handleOnchange}
                className="email-form"
                >
                  <option value="HSSE">HSSE</option>
                  <option value="Operations">Operations</option>
                  <option value="Finance">Finance</option>
                  <option value="MD">MD</option>
                  <option value="Stores">Stores</option>
                </select>
               </div>
               <input type="submit" value="Submit" className="submitButton" />
                </form>
                 <h3 className='text-option'>Or</h3>
            <div className='googleContainer' id="signInDiv">

            </div>
           </div>
        </div>
    </div>
  );
};

export default Signup;
