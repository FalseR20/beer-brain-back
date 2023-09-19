import {BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import Home from './pages/Home.tsx';
import SignIn from "./pages/forms/SignIn.tsx";
import SignUp from "./pages/forms/SignUp.tsx";

function App() {
    return (
        <Router>
            <Routes>
                <Route path='/' element={<Home/>}/>
                <Route path='/sign_in' element={<SignIn/>}/>
                <Route path='/sign_up' element={<SignUp/>}/>
            </Routes>
        </Router>
    );
}

export default App;
