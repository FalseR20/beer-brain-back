import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import Home from './components/Home.tsx';
import SignIn from "./forms/SignIn.tsx";
import SignUp from "./forms/SignUp.tsx";
import CreateEvent from "./components/CreateEvent.tsx";
import Event from "./components/Event.tsx";

function App() {
    return (
        <Router>
            <Routes>
                <Route path='/' element={<Home/>}/>
                <Route path='/sign_in' element={<SignIn/>}/>
                <Route path='/sign_up' element={<SignUp/>}/>
                <Route path='/create_event' element={<CreateEvent/>}/>
                <Route path='/events/:event_id' element={<Event/>}/>
            </Routes>
        </Router>
    );
}

export default App;
