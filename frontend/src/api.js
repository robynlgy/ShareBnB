import axios from "axios";

const BASE_URL = process.env.REACT_APP_BASE_URL || "http://localhost:5000";

/** API Class.
 */

class ShareBBApi {
  // Remember, the backend needs to be authorized with a token
  // We're providing a token you can use to interact with the backend API
  // DON'T MODIFY THIS TOKEN
  static token = null;

  static async request(endpoint, data = {}, method = "get") {
    console.debug("API Call:", endpoint, data, method);

    const url = `${BASE_URL}/${endpoint}`;
    const headers = { Authorization: `Bearer ${ShareBBApi.token}` };
    const params = method === "get" ? data : {};

    try {
      return (await axios({ url, method, data, params, headers })).data;
    } catch (err) {
      console.error("API Error:", err.response);
      let message = err.response.data.error.message;
      throw Array.isArray(message) ? message : [message];
    }
  }

  // Individual API routes

  /** Get details on a listing by id. */

  static async getListing(id) {
    let res = await this.request(`listings/${id}`);
    return res
  }

  /** Get all listings. */

  static async getListings() {
    let res = await this.request(`listings`);
    return res;
  }

  /** Register User and return token*/

  static async signup(data) {
    let res = await this.request(`signup`, data, "post");
    return res.token;
  }

  /** Login User and return token*/

  static async login(data) {
    let res = await this.request(`login`, data, "post");
    return res.token;

  }

  /** Get User detail*/

  static async getUser(username) {
    let res = await this.request(`${username}`);
    return res.user;
  }

  static async listingImage(id, data) {
    console.log('inside listingImage<<<<<<<<')
    let res = await this.request(`listings/${id}/img`, data, "post");
    console.log("res from api", res)
    return res.user;
  }

}

export default ShareBBApi;
