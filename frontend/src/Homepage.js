import { Link } from "react-router-dom";
import { useContext } from "react";
import UserContext from "./UserContext";

/** Landing page component with simple banner */
function Homepage() {
    const { currentUser } = useContext(UserContext);

    return (
        <section className="HomePage">
            <h1 className="mb-5 display-1">ShareBnB</h1>

            <h2 className="my-4">Find your next listing!</h2>

            {currentUser
                ? <h2>Welcome Back, {currentUser.firstName}!</h2>
                :
                <div>
                    <Link className="btn btn-primary mx-2" to="/login">Login</Link>
                    <Link className="btn btn-primary mx-2" to="/signup">Sign Up</Link>
                </div>}
        </section>
    )
}

export default Homepage