import './NavBar.css'
import { NavLink } from "react-router-dom";
import { useContext } from "react";
import UserContext from "./UserContext";

/** Nav component with links to listings, user, signup or login pages
 * props: logout
 */
function NavBar({ logout }) {

  const { currentUser } = useContext(UserContext);
  let activeStyle = {
    color: "#3a86ff",
    fontWeight: "bold",
  };

  return (
    <nav className="navbar navbar-dark bg-dark shadow-lg">
      {currentUser ? (
        <div className="container">
          <NavLink className="navbar-brand d-inline" to="/" end>
            ShareBnB
          </NavLink>
          <div>
            <NavLink
              className="nav-link d-inline"
              style={({ isActive }) => (isActive ? activeStyle : undefined)}
              to="/listings"
            >
              Listings
            </NavLink>
            <NavLink
              className="nav-link d-inline"
              style={({ isActive }) => (isActive ? activeStyle : undefined)}
              to="/listing/user"
            >
              My Listings
            </NavLink>
            <NavLink
              className="nav-link d-inline"
              style={({ isActive }) => (isActive ? activeStyle : undefined)}
              to="/user"
            >
              {currentUser.username}
            </NavLink>
            <button
              className="NavBar-logout nav-link bg-dark border-0 d-inline"
              onClick={logout}
            >
              Logout
            </button>
          </div>
        </div>
      ) : (
        <div className="container">
          <NavLink className="navbar-brand d-inline" to="/" end>
            ShareBnB
          </NavLink>
          <div>
            <NavLink
              className="nav-link d-inline"
              style={({ isActive }) => (isActive ? activeStyle : undefined)}
              to="/listings"
            >
              Listings
            </NavLink>
            <NavLink
              className="nav-link d-inline"
              style={({ isActive }) => (isActive ? activeStyle : undefined)}
              to="/login"
            >
              Login
            </NavLink>
            <NavLink
              className="nav-link d-inline"
              style={({ isActive }) => (isActive ? activeStyle : undefined)}
              to="/signup"
            >
              Sign Up
            </NavLink>
          </div>
        </div>
      )}
    </nav>
  );
}

export default NavBar;
