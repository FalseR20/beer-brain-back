import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Home from "./components/Home.tsx";
import SignIn from "./components/SignIn.tsx";
import SignUp from "./components/SignUp.tsx";
import Event from "./components/event/Event.tsx";
import NotFound from "./components/NotFound.tsx";
import Guest from "./components/Guest.tsx";
import "./css/App.scss";
import Profile from "./components/Profile.tsx";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/guest" element={<Guest />} />
        <Route path="/sign_in" element={<SignIn />} />
        <Route path="/sign_up" element={<SignUp />} />
        <Route path="/events/:event_id" element={<Event />} />
        <Route path="/profile/me" element={<Profile />} />
        <Route path="/profile/:profile_id" element={<Profile />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  );
}

export default App;
