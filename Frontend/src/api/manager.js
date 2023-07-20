import axios from "~/axios";

export function login(username, password) {
  return axios.post("/login", {
    username,
    password,
  });
}

export function getinfo() {
  return axios.post("/getinfo");
}

export function updatepassword(data) {
  return axios.post("/updatepassword", data);
}
