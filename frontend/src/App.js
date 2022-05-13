import "bootstrap/dist/css/bootstrap.css";
import './App.css';
import { BrowserRouter } from "react-router-dom";
import RoutesList from "./RoutesList";
import NavBar from "./NavBar";
import UserContext from "./UserContext";
import { useEffect, useState } from "react";
import ShareBBApi from "./api";
// import jwt from "jwt-decode";
import jwt_decode from "jwt-decode";
import LoadingSpinner from "./shared/LoadingSpinner";

/** App with user auth methods for jobly application
 *
 * state: currentUser, token, isLoading
 * props: none
 */

function App() {
  const [currentUser, setCurrentUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [isLoading, setIsLoading] = useState(true);

  async function signup(formData) {
    const response = await ShareBBApi.signup(formData);
    ShareBBApi.token = response;
    setToken(response);
  }

  async function login(formData) {
    const response = await ShareBBApi.login(formData);
    ShareBBApi.token = response;
    setToken(response);
  }

  function logout() {
    setCurrentUser(null);
    setToken(null);
    ShareBBApi.token = null;
    localStorage.clear();
  }


  /** useEffect runs on initial render and on changes in token state
   *  - makes request to API for user details from token payload
   *  - updates currentUser and sets token in localStorage
   */
   useEffect(
    function getUser() {
      async function getNewUser() {
        const username = jwt_decode(token).sub;
        try{
          const response = await ShareBBApi.getUser(username);
          setCurrentUser({ ...response });
          localStorage.setItem("token", token);
          setIsLoading(false);
        } catch (err){
          localStorage.clear();
          setIsLoading(false)
        }

      }
      if (token) {
        ShareBBApi.token = token;
        getNewUser();
      } else {
        setIsLoading(false);
      }
    },
    [token]
  );

  if (isLoading) return <LoadingSpinner />;


  return (
    <UserContext.Provider value={{ currentUser }}>
      <div className="App">
        <BrowserRouter>
          <NavBar logout={logout} />
          <RoutesList
            signup={signup}
            login={login}
            logout={logout}
          />
        </BrowserRouter>
      </div>
    </UserContext.Provider>
  );
}

export default App;
