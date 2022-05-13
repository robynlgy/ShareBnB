import { useContext } from "react";
import UserContext from "./UserContext";

/** user details
 * context: currentUser
 */
function User() {
  const { currentUser } = useContext(UserContext);
  return (
    <div className="bg-dark my-3 d-flex p-3 container">
      <div className="row">
        {<img className="user-detail-img" src={currentUser.imageUrl} alt="user-detail-img"/>}
      </div>
      <div className="text-start ms-5">
        <h4>{currentUser.username}</h4>
        <p>{`${currentUser.firstName} ${currentUser.lastName}`}</p>
        <p>{currentUser.email}</p>
        <button className="btn btn-outline-light mt-5">
          Messages (Coming Soon!)
        </button>
      </div>
    </div>
  );
}

export default User;
