import { Routes, Route, Navigate } from "react-router-dom";
import Homepage from "./Homepage";
import ListingList from "./ListingsList";
import ListingDetails from "./ListingDetails";
import UserDetails from "./UserDetails";
import UserListing from "./UserListing";
import LoginForm from "./LoginForm";
import SignupForm from "./SignupForm";
import { useContext } from "react";
import UserContext from "./UserContext";

/** List of possible endpoints in our app, along with associated components */
function RoutesList({ signup, login }) {
  const { currentUser } = useContext(UserContext);

  if (currentUser) {
    return (
      <Routes>
        <Route path="/" element={<Homepage />} />
        <Route path="/listings" element={<ListingList />} />
        <Route path="/listings/:id" element={<ListingDetails />} />
        <Route path="/listing/user" element={<UserListing />} />
        <Route path="/user" element={<UserDetails />} />
      </Routes>
    );
  } else {
    return (
      <Routes>
        <Route path="/" element={<Homepage />} />
        <Route path="/listings" element={<ListingList />} />
        <Route path="/listings/:id" element={<ListingDetails />} />
        <Route path="/login" element={<LoginForm login={login} />} />
        <Route path="/signup" element={<SignupForm signup={signup} />} />
        <Route path="/*" element={<Navigate to="/login" />} />
      </Routes>
    );
  }
}

export default RoutesList;
