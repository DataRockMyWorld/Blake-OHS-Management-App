import './App.css'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'
import SignUp from './components/SignUp'
import Login from './components/Login'
import Profile from './components/Profile'
import VerifyEmail from './components/VerifyEmail'
import ForgetPassword from './components/ForgetPassword'
import ResetPassword from './components/ResetPassword'


function App() {

  return (
    <>
      <Router>
        <ToastContainer />
        <Routes>
          <Route path="/" element={<SignUp />} />
          <Route path="/login" element={<Login />} />
          <Route path="/dashboard" element={<Profile />} />
          <Route path="/otp/verify" element={<VerifyEmail />} />
          <Route path="/forget_password" element={<ForgetPassword />} />
          <Route path="/password-reset-confirm/:uid/:token" element={<ResetPassword />} />
        </Routes>
      </Router>
    </>
  )
}

export default App
